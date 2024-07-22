import os


env = os.environ


class Settings:
    POSTGRES_DB: str = env.get('POSTGRES_DB')
    POSTGRES_USER: str = env.get('POSTGRES_USER')
    POSTGRES_PASSWORD: str = env.get('POSTGRES_PASSWORD')
    POSTGRES_HOST: str = env.get('POSTGRES_HOST')
    POSTGRES_PORT: str = env.get('POSTGRES_PORT')
