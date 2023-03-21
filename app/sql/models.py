from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base
# ��database�����������database.py�ļ�������Base��
#���������̳е��ࡣ
#��Щ����� SQLAlchemy ģ�͡�

class User(Base):
    # ���__tablename__�������������� SQLAlchemy Ҫ�����ݿ���Ϊÿ��ģ��ʹ�õ����ݿ������ơ�
    __tablename__ = "users"

    # ���ڴ�������ģ�ͣ��ࣩ���ԡ�
    # ��Щ�����е�ÿһ������������Ӧ���ݿ���е�һ�С�
    # ����ʹ��Column����ʾ SQLAlchemy �е�Ĭ��ֵ��
    # ���Ǵ���һ�� SQLAlchemy �����͡�����Integer��String��Boolean�������������ݿ��е����ͣ���Ϊ������
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    # ������ϵ
    # ������ user �е�����itemsʱ���� ��my_user.items��
    # ������һ��ItemSQLAlchemy ģ���б�����items������Щģ�;���ָ��users���д˼�¼�������
    items = relationship("Item", back_populates="owner")


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="items")