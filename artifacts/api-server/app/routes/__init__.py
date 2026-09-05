from app.routes.health import health_bp
from app.routes.locations import locations_bp
from app.routes.categories import categories_bp
from app.routes.schemes import schemes_bp
from app.routes.analysis import analysis_bp
from app.routes.financial import financial_bp
from app.routes.ai import ai_bp
from app.routes.auth import auth_bp
from app.routes.admin import admin_bp

__all__ = [
    "health_bp",
    "locations_bp",
    "categories_bp",
    "schemes_bp",
    "analysis_bp",
    "financial_bp",
    "ai_bp",
    "auth_bp",
    "admin_bp",
]
