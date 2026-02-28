from fastapi import FastAPI
from pydantic import BaseModel, ConfigDict, Field


class ProductNameSchema(BaseModel):
    name: str = Field(...)
    model_config = ConfigDict(extra="forbid")


class ProductIdSchema(BaseModel):
    id: int = Field(..., ge=1)
    model_config = ConfigDict(extra="forbid")


class ProductPriceShema(BaseModel):
    price: int = Field(...)
    model_config = ConfigDict(extra="forbid")


class ProductSchema(ProductIdSchema, ProductNameSchema, ProductPriceShema):
    pass


class OrderSchema(BaseModel):
    user_id: int = Field(..., ge=1)
    product_id: int = Field(..., ge=1)
    quantity: int = Field(..., ge=1)


db = [
    {"id": 1, "name": "product_name_test_1", "price": 10001},
    {"id": 2, "name": "product_name_test_2", "price": 10002},
    {"id": 3, "name": "product_name_test_3", "price": 10003},
]

app = FastAPI()


@app.get("/products/", summary="Получить все продукты", tags=["business", "debug"])
def get_products():
    return db


@app.get(
    "/products/name/{product_name}",
    summary="Получить продукт по имени",
    tags=["business"],
)
def get_product_by_name(product_name: str):
    for item in db:
        if item["name"] == product_name:
            return item
    return {"success": False, "status": 404}


@app.get(
    "/products/id/{product_id}", summary="Получить продукт по id", tags=["business"]
)
def get_product(product_id: int):
    for item in db:
        if item["id"] == product_id:
            return item
    return {"success": False, "status": 404}


@app.post("/products/", summary="Создать продукт; ожидает имя, цену", tags=["business"])
def create_product(product_name: ProductNameSchema, price: ProductPriceShema):
    try:
        db.append({"id": db[-1]["id"] + 1, "name": product_name, "price": price})
        return {"success": True}
    except Exception as e:
        return {"success": False, "error": dict(e)}
