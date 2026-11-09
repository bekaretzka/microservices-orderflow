from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = (
        "postgresql+psycopg2://orders:orders@localhost:5432/orders"
    )
    catalog_service_url: str = "http://127.0.0.1:8001"
    payment_service_url: str = "http://127.0.0.1:8003"

    rabbitmq_url: str = "amqp://guest:guest@localhost:5672"

    payment_exchange_name: str = "payment.events"
    payment_succeeded_routing_key: str = "payment.succeeded"

    payment_queue_name: str = "payment.results"

settings = Settings()

class NotFoundError(Exception):
    pass