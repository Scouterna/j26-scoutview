from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "ScoutView"
    scoutnet_base: str = "https://scoutnet.se/api"
    scoutnet_activity_id: int = 0
    scoutnet_participants_key: str = ""
    scoutnet_questions_key: str = ""
    scoutnet_checkin_key: str = ""
    scoutview_debug_email: str | None = None
    scoutview_roles: dict[str, set[str]] | None = {}
    keycloak_url: str = ""
    keycloak_realm: str = ""
    keycloak_client_id: str = ""

    model_config = SettingsConfigDict(env_file=".env")


# settings = Settings()


@lru_cache()
def get_settings():
    return Settings()
