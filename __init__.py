"""Route package for Banco-IoT API.

This package exposes the blueprints for `leituras` and `logs`.
"""

from .leituras import leituras_bp  # noqa: F401
from .logs import logs_bp  # noqa: F401
