from datetime import timedelta

DATABASE_URL = 'sqlite:///database.db'


JWT_SECRET = '123'
JWT_EXPIRATION_TIME = timedelta(days=1)
HOST: str = "127.0.0.1"
PORT: int = 8000