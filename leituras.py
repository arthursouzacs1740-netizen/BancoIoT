"""Módulo de rotas para leituras."""
from time import perf_counter
from flask import Blueprint, request
from pymongo.errors import PyMongoError
from werkzeug.exceptions import BadRequest

from db import mongo, LogEntry
from utils import validar_json, sanitize_data, make_response, get_client_ip

leituras_bp = Blueprint("leituras", __name__)


@leituras_bp.route("/leituras", methods=["POST"])
def receber_leituras():
    """Recebe e registra uma nova leitura enviada via POST."""
    try:
        start = perf_counter()
        data = request.get_json(force=True)
        if not data:
            return make_response(False, None, "JSON inválido", 400)

        required = ["presenca", "acesso", "uid_tag"]
        erro = validar_json(data, required)
        if erro:
            return make_response(False, None, erro, 400)

        data = sanitize_data(data)
        leitura_id = mongo.insert_leitura(data)

        resposta_ms = int((perf_counter() - start) * 1000)
        client_ip = get_client_ip(request)
        entry = LogEntry(
            endpoint="/leituras",
            method=request.method,
            leitura_id=leitura_id,
            client_ip=client_ip,
            payload={"uid_tag": data.get("uid_tag")},
            status=201,
            response_time_ms=resposta_ms,
        )
        mongo.registrar_log(entry)

        return make_response(True, {"id": leitura_id}, "Leitura registrada", 201)
    except BadRequest:
        return make_response(False, None, "JSON inválido", 400)
    except PyMongoError:
        mongo.logger.exception("Erro de banco ao processar /leituras")
        return make_response(False, None, "Erro no banco de dados", 500)


@leituras_bp.route("/leituras", methods=["GET"])
def listar_leituras():
    """Lista as leituras registradas no banco de dados."""
    try:
        leituras = mongo.list_leituras(limit=100)
        for leitura in leituras:
            leitura["presenca"] = bool(leitura.get("presenca", False))
            leitura["acesso"] = bool(leitura.get("acesso", False))
        total = len(leituras)
        return make_response(
            True,
            {"total": total, "dados": leituras},
            "OK",
            200,
        )
    except PyMongoError:
        mongo.logger.exception("Erro ao listar leituras")
        return make_response(False, None, "Erro no banco de dados", 500)
