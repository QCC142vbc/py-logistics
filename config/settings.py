from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Database
    database_url: str = "postgresql+asyncpg://logistics:password@localhost:5432/logistics_db"
    database_host: str = "localhost"
    database_port: int = 5432
    database_name: str = "logistics_db"
    database_user: str = "logistics"
    database_password: str = "password"

    # Redis
    redis_url: str = "redis://localhost:6379/0"
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_db: int = 0

    # RabbitMQ
    rabbitmq_url: str = "amqp://guest:guest@localhost:5672/"
    rabbitmq_host: str = "localhost"
    rabbitmq_port: int = 5672
    rabbitmq_user: str = "guest"
    rabbitmq_password: str = "guest"

    # API
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_reload: bool = True
    secret_key: str = "your-secret-key-change-this-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # External APIs
    carrier_api_key: str = ""
    carrier_api_base_url: str = "https://api.carrier.com"
    payment_gateway_api_key: str = ""
    payment_gateway_secret: str = ""
    geocoding_api_key: str = ""

    # AWS S3
    aws_access_key_id: str = ""
    aws_secret_access_key: str = ""
    aws_region: str = "us-east-1"
    aws_s3_bucket: str = ""

    # Logging
    log_level: str = "INFO"
    log_format: str = "json"

    # Environment
    environment: str = "development"
    debug: bool = True

    # Feature Flags
    enable_simulation: bool = True
    enable_advanced_analytics: bool = True
    enable_ml_forecasting: bool = False
    enable_real_time_tracking: bool = True

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
