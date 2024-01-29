import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    host = os.getenv("DB_HOST", "chat-cleaner-host")
    port = 54321 if host == "localhost" else 5432
    password = os.getenv("DB_PASSWORD", "chat-cleaner-password")
    user = os.getenv("DB_USER", "chat-cleaner-user")
    db_name = os.getenv("DB_NAME", "chat-cleaner-test")
    postgres_uri = f"postgresql://{user}:{password}@{host}:{port}/{db_name}"

    db_uri: str = (
        "sqlite:///cleaning.db" if os.environ.get("TEST_RUN") else postgres_uri
    )

    # api_host = os.getenv("API_HOST", "0.0.0.0")
    # api_port = 8000 if api_host == "localhost" else 8000
    # api_uri: str = (
    #     f"http://{api_host}:{api_port}"
    #     if os.environ.get("TEST_RUN")
    #     else f"http://{api_host}:{api_port}"
    # )


def get_database_uri() -> str:
    return Settings.db_uri


# def get_api_uri() -> str:
#     return Settings.api_uri
