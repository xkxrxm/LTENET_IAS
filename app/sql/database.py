from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# �����ӡ���һ�� SQLite ���ݿ⣨�� SQLite ���ݿ��һ���ļ���
# ���ļ���λ���ļ��е�ͬһĿ¼��sql_app.db
# �����Ϊʲô���һ������./sql_app.db.
SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

# ����һ�� SQLAlchemy�ġ����桱��
# "check_same_thread": False ������SQLite�����������ݿⲻ��Ҫ����
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# ÿ��ʵ��SessionLocal������һ�����ݿ�Ự��
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# �������ǽ�ʹ��declarative_base()����һ���ࡣ
# �Ժ�(models�ļ�)���ǽ��������̳У�������ÿ�����ݿ�ģ�ͻ��ࣨORM ģ�ͣ�
Base = declarative_base()