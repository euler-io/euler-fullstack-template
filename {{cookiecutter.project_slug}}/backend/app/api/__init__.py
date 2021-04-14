from fastapi.routing import APIRouter

from .detail_config import router as detail_config_router
from .sample import router as sample_router
from .search_config import router as search_config_router

router = APIRouter()
router.include_router(sample_router)
router.include_router(search_config_router)
router.include_router(detail_config_router)