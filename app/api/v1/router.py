from fastapi import APIRouter
from app.api.v1.endpoints import items, user, auth, recommendations

router = APIRouter()

router.include_router(items.router, prefix="/items", tags=["items"])
router.include_router(user.router, prefix="/users", tags=["users"])
router.include_router(auth.router, prefix="/auth", tags=["auth"])
router.include_router(recommendations.router, prefix="/recommendations", tags=["recommendations"])

