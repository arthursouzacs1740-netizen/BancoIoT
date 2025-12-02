"""API para receber leituras do ESP32 e registrar no MongoDB Atlas.

Este módulo expõe rotas REST para inserir leituras e listar logs/leituras.
"""

from flask import Flask

from db import mongo



def create_app(init_db: bool = True) -> Flask:
    """Cria e configura a aplicação Flask com blueprints e DB.

    Retorna a instância do `Flask` pronta para uso (server/production).
    """
    # imports kept at module scope to satisfy static checkers and avoid cycles
    from routes import leituras_bp, logs_bp
    from utils import make_response

    app = Flask(__name__)
    app.register_blueprint(leituras_bp)
    app.register_blueprint(logs_bp)

    @app.errorhandler(Exception)
    def erro_global(exc):
        mongo.logger.exception("Erro global no servidor: %s", exc)
        return make_response(False, None, "Erro interno do servidor", 500)

    # initialize DB explicitly when requested
    if init_db:
        mongo.init_db()
    return app


# The `create_app` factory exists for import in WSGI and tests.
