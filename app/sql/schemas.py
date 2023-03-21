from typing import Union

from pydantic import BaseModel

#  SQLAlchemy模型和 Pydantic模型之间的混淆，
# 我们将有models.py（SQLAlchemy 模型的文件）和schemas.py（ Pydantic 模型的文件）。

# 创建一个ItemBase和UserBasePydantic模型（或者我们说“schema”）以及在创建或读取数据时具有共同的属性。
class ItemBase(BaseModel):
    title: str
    description: Union[str, None] = None

# ItemCreate为 创建一个UserCreate继承自它们的所有属性（因此它们将具有相同的属性），
# 以及创建所需的任何其他数据（属性）。
class ItemCreate(ItemBase):
    pass

# 创建用于读取/返回的Pydantic模型/模式?
# 现在创建当从 API 返回数据时、将在读取数据时使用的Pydantic模型（schemas）。

# 在创建一个项目之前，我们不知道分配给它的 ID 是什么，
# 但是在读取它时（从 API 返回时）我们已经知道它的 ID。
class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str

#当读取用户时，我们现在可以声明items，将包含属于该用户的项目。
class User(UserBase):
    id: int
    is_active: bool
    items: list[Item] = []
    # 设置属性orm_mode = True。
    # Pydanticorm_mode将告诉 Pydantic模型读取数据，
    # 即它不是一个dict，而是一个 ORM 模型（或任何其他具有属性的任意对象）。
    # 有了这个，Pydantic模型与 ORM 兼容，您只需在路径操作response_model的参数中声明它即可。
    # 将能够返回一个数据库模型，它将从中读取数据。
    class Config:
        orm_mode = True