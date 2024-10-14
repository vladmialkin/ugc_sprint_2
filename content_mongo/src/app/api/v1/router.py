from fastapi import APIRouter
from app.api.v1.routers.film_rating import router as rating_router

router = APIRouter(prefix="/api/v1")

router.include_router(rating_router, prefix="/rating", tags=["Рейтинг фильмов"])