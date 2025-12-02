"""WSGI entrypoint used by Gunicorn or other WSGI servers.

This file exposes `app` object for WSGI and creates the DB connection.
"""
from banco_iot import create_app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
