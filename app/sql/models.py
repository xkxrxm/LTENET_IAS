from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base
# 从database（来自上面的database.py文件）导入Base。
#创建从它继承的类。
#这些类就是 SQLAlchemy 模型。

class User(Base):
    # 这个__tablename__属性是用来告诉 SQLAlchemy 要在数据库中为每个模型使用的数据库表的名称。
    __tablename__ = "users"

    # 现在创建所有模型（类）属性。
    # 这些属性中的每一个都代表其相应数据库表中的一列。
    # 我们使用Column来表示 SQLAlchemy 中的默认值。
    # 我们传递一个 SQLAlchemy “类型”，如Integer、String和Boolean，它定义了数据库中的类型，作为参数。
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    # 创建关系
    # 当访问 user 中的属性items时，如 中my_user.items，
    # 它将有一个ItemSQLAlchemy 模型列表（来自items表），这些模型具有指向users表中此记录的外键。
    items = relationship("Item", back_populates="owner")


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="items")