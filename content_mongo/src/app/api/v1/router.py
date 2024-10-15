from fastapi import APIRouter
from app.api.v1.routers.film_rating import router as rating_router
from app.api.v1.routers.film_reviews import router as reviews_router
from app.api.v1.routers.film_bookmarks import router as bookmarks_router

router = APIRouter(prefix="/api/v1")

router.include_router(rating_router, prefix="/rating", tags=["Рейтинг фильмов"])
router.include_router(reviews_router, prefix="/reviews", tags=["Комментарий к фильму"])
router.include_router(bookmarks_router, prefix="/bookmarks", tags=["Закладки фильмов"])