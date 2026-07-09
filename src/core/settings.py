
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):

    # Application ==============================
    app_name: str = 'template-fastapi'
    frontend_url: str = 'portal.hmc.az'
    app_version: str = '1.0.0'
    debug: bool = True
    environment: str = 'production'

    # Database =================================
    database_engine: str = 'postgresql+psycopg'
    database_ip: str = 'localhost'
    database_port: str = '5432'
    database_name: str = 'auth_database'
    database_username: str = 'faroosha'
    database_password: str = '1419'

    # Security =================================
    encryption_key : str = ''
    secret_key: str = 'blablablasecretkeytest'
    algorithm : str = 'HS256'
    access_token_expire_minutes : int = 15
    refresh_token_expire_days : int = 30
    ip_check_enabled : bool = True
    max_attempt_per_ip : int = 10
    rate_limit_minutes : int = 5

    user_email_code_limit : int = 10
    user_bad_password_limit : int = 5

    email_code_timeout : int = 10

    session_email_code_limit : int = 10
    session_expire_minute : int = 15

    # Password policy ==========================
    password_min_length : int = 10
    password_require_uppercase : bool = True
    password_require_lowercase : bool = True
    password_require_digit : bool = True
    password_require_symbol : bool = True
    password_min_life_hours : int = 24
    password_max_life_days : int = 90

    # Mail server ==============================
    smtp_server: str = ''
    smtp_port: int = 587
    smtp_user:str = ''
    smtp_password: str = ''
    smtp_sender_email: str = ''
    smtp_sender_name: str = ''

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        case_sensitive=False,
        extra='ignore'
    )

    @property
    def max_attempts_per_ip(self) -> int:
        return self.max_attempt_per_ip

    @property
    def database_url(self) -> str:
        return (
            f'{self.database_engine}://'
            f'{self.database_username}:{self.database_password}@'
            f'{self.database_ip}:{self.database_port}/'
            f'{self.database_name}'
        )


# Singleton instance
settings = Settings()
