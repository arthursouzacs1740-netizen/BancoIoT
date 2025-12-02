"""Helpers utilitários para validação, sanitização e respostas JSON.

Contém funções de validação de UIDs e formatação de respostas padronizadas
para a API.
"""

import re
from datetime import datetime
from typing import Optional, Any

from flask import jsonify

UID_REGEX = re.compile(r"^[A-Fa-f0-9 ]{8,}$")


def validar_json(data: dict, required: list[str]) -> Optional[str]:
    """Valida se `data` contém os campos obrigatórios e se `uid_tag` é
    válido.

    Retorna uma mensagem de erro ou None quando válido.
    """
    for campo in required:
        if campo not in data:
            return f"Campo obrigatório ausente: {campo}"
    # UID validation
    uid = str(data.get("uid_tag", "")).strip()
    if not UID_REGEX.match(uid):
        return "UID inválido"
    return None


def sanitize_data(data: dict) -> dict:
    """Sanitiza e normaliza os campos do payload recebido.

    Converte `presenca` para bool, `acesso` para bool e garante `uid_tag`
    como string; adiciona timestamp caso não exista.
    """
    # Convert presenca
    try:
        data["presenca"] = bool(int(str(data.get("presenca", "0"))))
    except (ValueError, TypeError):
        data["presenca"] = False

    # Convert acesso
    data["acesso"] = str(data.get("acesso", "False")).lower() == "true"

    # Sanitize uid
    data["uid_tag"] = str(data.get("uid_tag", "")).strip()

    # timestamp
    data.setdefault("timestamp", datetime.now().isoformat())
    return data


def make_response(
    success: bool,
    data: Any = None,
    message: str = "",
    status_code: int = 200,
) -> tuple:
    """Cria uma resposta JSON padronizada com `success`, `data` e `message`.

    Retorna uma tupla `(jsonify(body), status_code)` para ser retornada
    diretamente pelo Flask.
    """
    body = {
        "success": bool(success),
        "data": data or {},
        "message": message,
    }
    return jsonify(body), status_code


def get_client_ip(flask_request) -> Optional[str]:
    """Retorna o IP do cliente a partir do request.

    Se a app estiver por trás de um proxy, respeita o cabeçalho
    `X-Forwarded-For`.
    """
    # Respect X-Forwarded-For if behind a proxy
    forwarded = flask_request.headers.get("X-Forwarded-For")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return flask_request.remote_addr
