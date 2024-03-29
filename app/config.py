# 定义token相关配置
from fastapi.security import OAuth2PasswordBearer

SECRET_KEY = "SECRET KEY"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 表示access token的过期时间为30分钟。

# OAuth2密码授权流程，获取access token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

DB_HOST = 'localhost'
DB_USERNAME = 'root'
DB_PASSWORD = '123456'
DB_DATABASE = 'datas'

DB_partition = r"D:\datas"
DB_time = 30
DB_buffer_size = 1000
