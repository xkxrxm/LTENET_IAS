from passlib.context import CryptContext
import pandas as pd

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def convert_excel_to_csv(input_path, output_path):
    df = pd.read_excel(input_path)
    # 将数据写入 CSV 文件
    df.to_csv(output_path, index=False)


def get_password_hash(password):
    return pwd_context.hash(password)


def password_verify(password: str, hashed_password: str):
    return pwd_context.verify(password, hashed_password)
