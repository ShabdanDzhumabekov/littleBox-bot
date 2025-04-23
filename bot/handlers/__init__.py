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

def setup_routers() -> Router:
    router = Router()
    router.include_router(start_router)
    router.include_router(help_router)
    router.include_router(ads_router)
    router.include_router(routes_router)
    router.include_router(my_ads_router)
    router.include_router(routes_view_router)
    router.include_router(ads_view_router)
    router.include_router(edit_ad_router)
    router.include_router(edit_route_router)
    router.include_router(feedback_router)

    return router