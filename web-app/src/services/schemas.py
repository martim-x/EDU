from pydantic import BaseModel, ConfigDict, Field


class BaseModelForbid(BaseModel):
    model_config = ConfigDict(extra="forbid")


class IdSchema(BaseModelForbid):
    id: int = Field(..., ge=1)


# --- User ---
class UserCreateSchema(BaseModelForbid):
    name: str = Field(..., max_length=50)


class UserSchema(UserCreateSchema, IdSchema): ...


# --- Product ---
class ProductCreateSchema(BaseModelForbid):
    name: str = Field(..., max_length=50)
    price: int = Field(..., ge=1)


class ProductSchema(IdSchema, ProductCreateSchema): ...


# --- Order ---
class OrderCreateSchema(BaseModelForbid):
    user_id: int = Field(..., ge=1)
    product_id: int = Field(..., ge=1)
    quantity: int = Field(..., ge=1)


class OrderSchema(IdSchema, OrderCreateSchema): ...
