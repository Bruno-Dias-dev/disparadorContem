from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    anti_captcha_api_key: str
    sistema_login: str
    sistema_senha: str
    base_url: str
    openai_api_key: str
    username_digital_sac: str
    password_digital_sac: str
    base_url_digital_sac: str
    contato: str
    db_host: str
    db_name: str
    db_user: str
    db_password: str
    db_port: str
    secret_key: str
    API_URL: str
    
    class Config:
        extra = "allow"  # Permite campos extras
        env_file = ".env"
        
settings = Settings()
