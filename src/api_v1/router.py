from fastapi import APIRouter

from api_v1.endpoints.items import router as items_router
from core.settings import settings

router: APIRouter = APIRouter(
    prefix=settings.api.v1.prefix,
)
router.include_router(router=items_router)
