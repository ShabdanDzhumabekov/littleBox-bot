from aiogram import Router

from .start import router as start_router
from .help import router as help_router
from .ads import router as ads_router
from .my_ads import router as my_ads_router
from .routes import router as routes_router
from .routes_view import router as routes_view_router
from .ads_view import router as ads_view_router 
from .edit_ad import router as edit_ad_router
from .edit_route import router as edit_route_router
from .feedback import router as feedback_router
from .stats import router as stats_router
from .admin import router as admin_router
from .cancel import router as cancel_router
from .safety import router as safety_router
from .form_fallback import router as form_fallback_router


def setup_routers() -> Router:
    router = Router()
    router.include_router(cancel_router)
    router.include_router(start_router)
    router.include_router(help_router)
    router.include_router(safety_router)
    router.include_router(ads_router)
    router.include_router(routes_router)
    router.include_router(my_ads_router)
    router.include_router(routes_view_router)
    router.include_router(ads_view_router)
    router.include_router(edit_ad_router)
    router.include_router(edit_route_router)
    router.include_router(feedback_router)
    router.include_router(stats_router)
    router.include_router(admin_router)
    router.include_router(form_fallback_router)

    return router