class Config:
    SECRET_KEY = "supersecret"
    JWT_SECRET_KEY = "superjwtsecret"
    SQLALCHEMY_DATABASE_URI = "sqlite:///sdn_users.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    API_TITLE = "SDN API"
    API_VERSION = "1.0"
    OPENAPI_VERSION = "3.0.3"
    OPENAPI_SWAGGER_UI_PATH = "/docs"
    OPENAPI_SWAGGER_UI_URL = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
