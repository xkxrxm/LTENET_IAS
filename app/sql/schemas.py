from typing import Union

from pydantic import BaseModel

#  SQLAlchemyģ�ͺ� Pydanticģ��֮��Ļ�����
# ���ǽ���models.py��SQLAlchemy ģ�͵��ļ�����schemas.py�� Pydantic ģ�͵��ļ�����

# ����һ��ItemBase��UserBasePydanticģ�ͣ���������˵��schema�����Լ��ڴ������ȡ����ʱ���й�ͬ�����ԡ�
class ItemBase(BaseModel):
    title: str
    description: Union[str, None] = None

# ItemCreateΪ ����һ��UserCreate�̳������ǵ��������ԣ�������ǽ�������ͬ�����ԣ���
# �Լ�����������κ��������ݣ����ԣ���
class ItemCreate(ItemBase):
    pass

# �������ڶ�ȡ/���ص�Pydanticģ��/ģʽ?
# ���ڴ������� API ��������ʱ�����ڶ�ȡ����ʱʹ�õ�Pydanticģ�ͣ�schemas����

# �ڴ���һ����Ŀ֮ǰ�����ǲ�֪����������� ID ��ʲô��
# �����ڶ�ȡ��ʱ���� API ����ʱ�������Ѿ�֪������ ID��
class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str

#����ȡ�û�ʱ���������ڿ�������items�����������ڸ��û�����Ŀ��
class User(UserBase):
    id: int
    is_active: bool
    items: list[Item] = []
    # ��������orm_mode = True��
    # Pydanticorm_mode������ Pydanticģ�Ͷ�ȡ���ݣ�
    # ��������һ��dict������һ�� ORM ģ�ͣ����κ������������Ե�������󣩡�
    # ���������Pydanticģ���� ORM ���ݣ���ֻ����·������response_model�Ĳ��������������ɡ�
    # ���ܹ�����һ�����ݿ�ģ�ͣ��������ж�ȡ���ݡ�
    class Config:
        orm_mode = True