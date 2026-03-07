from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import delete, select, text
from sqlalchemy.ext.asyncio import AsyncSession

from database.connection import get_session, lifespan
from services.schemas import (
    IdSchema,
    OrderCreateSchema,
    ProductCreateSchema,
    ProductSchema,
    UserCreateSchema,
)
from services.tables import Order, Product, User

app = FastAPI(lifespan=lifespan)


# ==========
# debug
# ==========

_SEED_DATA = {
    "users": [{"id": i, "name": f"user_name_test_{i}"} for i in range(1, 11)],
    "products": [
        {"id": i, "name": f"product_name_test_{i}", "price": 10000 + i}
        for i in range(1, 11)
    ],
    "orders": [
        {"id": 1, "product_id": 4, "user_id": 1, "quantity": 15},
        {"id": 2, "product_id": 4, "user_id": 2, "quantity": 12},
        {"id": 3, "product_id": 4, "user_id": 3, "quantity": 18},
        {"id": 4, "product_id": 5, "user_id": 4, "quantity": 25},
        {"id": 5, "product_id": 5, "user_id": 5, "quantity": 22},
        {"id": 6, "product_id": 5, "user_id": 6, "quantity": 28},
        {"id": 7, "product_id": 6, "user_id": 7, "quantity": 35},
        {"id": 8, "product_id": 6, "user_id": 8, "quantity": 30},
        {"id": 9, "product_id": 6, "user_id": 9, "quantity": 40},
        {"id": 10, "product_id": 7, "user_id": 10, "quantity": 45},
        {"id": 11, "product_id": 7, "user_id": 1, "quantity": 50},
        {"id": 12, "product_id": 7, "user_id": 2, "quantity": 42},
        {"id": 13, "product_id": 8, "user_id": 3, "quantity": 55},
        {"id": 14, "product_id": 8, "user_id": 4, "quantity": 60},
        {"id": 15, "product_id": 8, "user_id": 5, "quantity": 58},
        {"id": 16, "product_id": 9, "user_id": 6, "quantity": 65},
        {"id": 17, "product_id": 9, "user_id": 7, "quantity": 70},
        {"id": 18, "product_id": 9, "user_id": 8, "quantity": 68},
        {"id": 19, "product_id": 10, "user_id": 9, "quantity": 75},
        {"id": 20, "product_id": 10, "user_id": 10, "quantity": 80},
        {"id": 21, "product_id": 10, "user_id": 1, "quantity": 85},
        {"id": 22, "product_id": 1, "user_id": 4, "quantity": 12},
        {"id": 23, "product_id": 1, "user_id": 5, "quantity": 14},
        {"id": 24, "product_id": 1, "user_id": 6, "quantity": 16},
        {"id": 25, "product_id": 2, "user_id": 7, "quantity": 24},
        {"id": 26, "product_id": 2, "user_id": 8, "quantity": 26},
        {"id": 27, "product_id": 2, "user_id": 9, "quantity": 29},
        {"id": 28, "product_id": 3, "user_id": 10, "quantity": 33},
        {"id": 29, "product_id": 3, "user_id": 1, "quantity": 31},
        {"id": 30, "product_id": 3, "user_id": 2, "quantity": 34},
    ],
}


@app.post("/debug/seed/", summary="Заполнить БД тестовыми данными", tags=["debug"])
async def seed_db(session: AsyncSession = Depends(get_session)):
    await session.execute(delete(Order))
    await session.execute(delete(Product))
    await session.execute(delete(User))

    for u in _SEED_DATA["users"]:
        session.add(User(**u))
    for p in _SEED_DATA["products"]:
        session.add(Product(**p))
    for o in _SEED_DATA["orders"]:
        session.add(Order(**o))

    await session.flush()

    await session.execute(
        text("SELECT setval('api_users_id_seq', (SELECT MAX(id) FROM api_users))")
    )
    await session.execute(
        text("SELECT setval('api_products_id_seq', (SELECT MAX(id) FROM api_products))")
    )
    await session.execute(
        text("SELECT setval('api_orders_id_seq', (SELECT MAX(id) FROM api_orders))")
    )

    await session.commit()
    return {"status": 200, "detail": "DB seeded"}


@app.delete("/debug/flush/", tags=["debug"], summary="Очистить все таблицы")
async def flush_db(session: AsyncSession = Depends(get_session)):
    await session.execute(delete(Order))
    await session.execute(delete(Product))
    await session.execute(delete(User))
    await session.commit()
    return {"status": 200, "detail": "DB flushed"}


# ==========
# products
# ==========


@app.get(
    "/products/limit/{limit}/offset/{offset}",
    summary="Получить все продукты",
    tags=["products"],
)
async def get_products(
    limit: int = 5,
    offset: int = 1,
    session: AsyncSession = Depends(get_session),
):
    if limit <= 0 or offset <= 0:
        raise HTTPException(status_code=400, detail="limit и offset должны быть > 0")
    result = await session.execute(
        select(Product).offset((offset - 1) * limit).limit(limit)
    )
    products = result.scalars().all()
    if not products:
        raise HTTPException(status_code=404, detail="Products not found")
    return products


@app.get(
    "/products/id/{product_id}", summary="Получить продукт по id", tags=["products"]
)
async def get_product(product_id: int, session: AsyncSession = Depends(get_session)):
    product = await session.get(Product, product_id)
    if product is None:
        raise HTTPException(status_code=404, detail=f"Product {product_id} not found")
    return product


@app.get(
    "/products/name/{product_name}",
    summary="Получить продукт по имени",
    tags=["products"],
)
async def get_product_by_name(
    product_name: str, session: AsyncSession = Depends(get_session)
):
    result = await session.execute(select(Product).where(Product.name == product_name))
    product = result.scalar_one_or_none()
    if product is None:
        raise HTTPException(
            status_code=404, detail=f"Product '{product_name}' not found"
        )
    return product


@app.post("/products/", summary="Создать продукт", status_code=201, tags=["products"])
async def create_product(
    product: ProductCreateSchema, session: AsyncSession = Depends(get_session)
):
    new_product = Product(name=product.name, price=product.price)
    session.add(new_product)
    await session.commit()
    await session.refresh(new_product)
    return new_product


@app.put("/products/", summary="Обновить продукт", tags=["products"])
async def update_product(
    product: ProductSchema, session: AsyncSession = Depends(get_session)
):
    existing = await session.get(Product, product.id)
    if existing is None:
        raise HTTPException(status_code=404, detail=f"Product {product.id} not found")
    existing.name = product.name
    existing.price = product.price
    await session.commit()
    await session.refresh(existing)
    return existing


@app.delete("/products/", summary="Удалить продукт", tags=["products"])
async def delete_product(
    product: IdSchema, session: AsyncSession = Depends(get_session)
):
    existing = await session.get(Product, product.id)
    if existing is None:
        raise HTTPException(status_code=404, detail=f"Product {product.id} not found")
    await session.delete(existing)
    await session.commit()
    return {"status": 200}


# ==========
# users
# ==========


@app.get(
    "/users/limit/{limit}/offset/{offset}",
    summary="Получить пользователей",
    tags=["users"],
)
async def get_users(
    limit: int = 5,
    offset: int = 1,
    session: AsyncSession = Depends(get_session),
):
    if limit <= 0 or offset <= 0:
        raise HTTPException(status_code=400, detail="limit и offset должны быть > 0")
    result = await session.execute(
        select(User).offset((offset - 1) * limit).limit(limit)
    )
    users = result.scalars().all()
    if not users:
        raise HTTPException(status_code=404, detail="Users not found")
    return users


@app.get("/users/id/{user_id}", summary="Получить пользователя по id", tags=["users"])
async def get_user_by_id(user_id: int, session: AsyncSession = Depends(get_session)):
    user = await session.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")
    return user


@app.get(
    "/users/name/{user_name}", summary="Получить пользователя по имени", tags=["users"]
)
async def get_user_by_name(
    user_name: str, session: AsyncSession = Depends(get_session)
):
    result = await session.execute(select(User).where(User.name == user_name))
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail=f"User '{user_name}' not found")
    return user


@app.post("/users/", summary="Создать пользователя", status_code=201, tags=["users"])
async def create_user(
    user: UserCreateSchema, session: AsyncSession = Depends(get_session)
):
    new_user = User(name=user.name)
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return new_user


# ==========
# orders
# ==========


@app.get(
    "/users/{user_id}/orders/", summary="Получить заказы пользователя", tags=["orders"]
)
async def get_user_orders(user_id: int, session: AsyncSession = Depends(get_session)):
    user = await session.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")
    result = await session.execute(select(Order).where(Order.user_id == user_id))
    orders = result.scalars().all()
    if not orders:
        raise HTTPException(status_code=404, detail=f"User {user_id} has no orders")
    return orders


@app.post("/orders/", summary="Создать заказ", status_code=201, tags=["orders"])
async def create_order(
    order: OrderCreateSchema, session: AsyncSession = Depends(get_session)
):
    user = await session.get(User, order.user_id)
    if user is None:
        raise HTTPException(status_code=404, detail=f"User {order.user_id} not found")
    product = await session.get(Product, order.product_id)
    if product is None:
        raise HTTPException(
            status_code=404, detail=f"Product {order.product_id} not found"
        )
    new_order = Order(
        user_id=order.user_id,
        product_id=order.product_id,
        quantity=order.quantity,
    )
    session.add(new_order)
    await session.commit()
    await session.refresh(new_order)
    return new_order
