from pydantic import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str = "LEAD_GEN_2024"  # Change this!
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
     CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/0"
    EMONSQUEEZY_API_KEY: str
    LEMONSQUEEZY_STORE_ID: str
    LEMONSQUEEZY_VARIANT_IDS: Dict[str, str] = {
        "basic": "your_basic_plan_variant_id",
        "pro": "your_pro_plan_variant_id",
        "enterprise": "your_enterprise_plan_variant_id"
    }
    FRONTEND_URL: str


    class Config:
        env_file = ".env"

settings = Settings()