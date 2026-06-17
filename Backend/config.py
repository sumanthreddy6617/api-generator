# from pydantic_settings import BaseSettings
# class Settings(BaseSettings):
#     DATABASE_URL: str = "mysql+pymysql://root:password@localhost:3306/mockforge"
#     JWT_SECRET: str = "change-me"
#     JWT_ALG: str = "HS256"
#     JWT_EXPIRE_MIN: int = 1440
#     GEMINI_API_KEY: str = ""
#     ML_MODEL_PATH: str = "../ML/api_classifier.pkl"
#     class Config:
#         env_file = ".env"
# settings = Settings()

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str

    class Config:
        env_file = ".env"

settings = Settings()