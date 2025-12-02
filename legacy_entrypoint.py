"""Legacy wrapper for backward compatibility.

This file intentionally provides a very small wrapper for the new
`banco_iot.py` application. Prefer `banco_iot.py` as the main entrypoint.
"""

# pylint: disable=invalid-name
from banco_iot import create_app
from db import mongo


def main() -> None:
    """Run the Flask app using the shared Mongo instance."""
    app = create_app()
    mongo.init_db()
    app.run(host="0.0.0.0", port=5000, debug=False)


if __name__ == "__main__":
    main()
