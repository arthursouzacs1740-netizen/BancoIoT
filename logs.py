"""Módulo de rotas para logs da API."""
from flask import Blueprint
from pymongo.errors import PyMongoError

from db import mongo
from utils import make_response

logs_bp = Blueprint("logs_api", __name__)


@logs_bp.route("/logs_api", methods=["GET"])
def listar_logs():
    """Lista os logs registrados no banco de dados."""
    try:
        logs = mongo.list_logs(limit=100)
        total = len(logs)
        return make_response(True, {"total": total, "dados": logs}, "OK", 200)
    except PyMongoError:
        mongo.logger.exception("Erro ao listar logs")
        return make_response(False, None, "Erro no banco de dados", 500)
