from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str
    API_KEY: str

    @property
    def JWT_SECRET_KEY(self):
        return self.SECRET_KEY

    @property
    def JWT_ALGORITHM(self):
        return self.ALGORITHM

    @property
    def EXTERNAL_API_KEY(self):
        return self.API_KEY

    class Config:
        env_file = '.env'


settings = Settings()
