from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# “连接”到一个 SQLite 数据库（用 SQLite 数据库打开一个文件）
# 该文件将位于文件中的同一目录中sql_app.db
# 这就是为什么最后一部分是./sql_app.db.
SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

# 创建一个 SQLAlchemy的“引擎”。
# "check_same_thread": False 仅用于SQLite，在其他数据库不需要它。
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# 每个实例SessionLocal都会是一个数据库会话。
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 现在我们将使用declarative_base()返回一个类。
# 稍后(models文件)我们将用这个类继承，来创建每个数据库模型或类（ORM 模型）
Base = declarative_base()