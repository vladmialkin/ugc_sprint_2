from app.settings.base import Settings


class ApiSettings(Settings):
    TITLE: str = "mongo-api"
    OPENAPI_URL: str = "/api/openapi.json"
    DOCS_URL: str = "/api/docs"
    REDOC_URL: str = "/api/redoc"
    SECRET_KEY: str


settings = ApiSettings()
