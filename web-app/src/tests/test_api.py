import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient

from api.api import app

# Говорим pytest-asyncio использовать один event loop на всю сессию
pytestmark = pytest.mark.asyncio(loop_scope="session")


@pytest_asyncio.fixture(loop_scope="session", autouse=True)
async def prepare_db():
    """Перед всеми тестами — seed, после — flush"""
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        await client.post("/debug/seed/")
    yield
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        await client.delete("/debug/flush/")


@pytest_asyncio.fixture
async def client():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as c:
        yield c


# ==========
# products
# ==========


async def test_get_products(client):
    response = await client.get("/products/limit/5/offset/1")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 5
    assert data[0]["id"] == 1


async def test_get_product_by_id(client):
    response = await client.get("/products/id/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1


async def test_get_product_by_id_not_found(client):
    response = await client.get("/products/id/9999")
    assert response.status_code == 404


async def test_get_product_by_name(client):
    response = await client.get("/products/name/product_name_test_1")
    assert response.status_code == 200
    assert response.json()["name"] == "product_name_test_1"


async def test_get_product_by_name_not_found(client):
    response = await client.get("/products/name/nonexistent")
    assert response.status_code == 404


async def test_create_product(client):
    response = await client.post(
        "/products/", json={"name": "new_product", "price": 999}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "new_product"
    assert data["price"] == 999
    assert "id" in data


async def test_create_product_invalid(client):
    # price не может быть 0 (ge=1 в схеме)
    response = await client.post("/products/", json={"name": "bad", "price": 0})
    assert response.status_code == 422


async def test_update_product(client):
    response = await client.put(
        "/products/", json={"id": 1, "name": "updated", "price": 5000}
    )
    assert response.status_code == 200
    assert response.json()["name"] == "updated"


async def test_update_product_not_found(client):
    response = await client.put(
        "/products/", json={"id": 9999, "name": "x", "price": 1}
    )
    assert response.status_code == 404


async def test_delete_product(client):
    # Создаём продукт специально для удаления
    create = await client.post("/products/", json={"name": "to_delete", "price": 1})
    product_id = create.json()["id"]

    response = await client.request("DELETE", "/products/", json={"id": product_id})
    assert response.status_code == 200

    # Проверяем что удалён
    check = await client.get(f"/products/id/{product_id}")
    assert check.status_code == 404


async def test_delete_product_not_found(client):
    response = await client.request("DELETE", "/products/", json={"id": 9999})
    assert response.status_code == 404


async def test_get_products_invalid_params(client):
    response = await client.get("/products/limit/0/offset/1")
    assert response.status_code == 400


# ==========
# users
# ==========


async def test_get_users(client):
    response = await client.get("/users/limit/5/offset/1")
    assert response.status_code == 200
    assert len(response.json()) == 5


async def test_get_user_by_id(client):
    response = await client.get("/users/id/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1


async def test_get_user_by_id_not_found(client):
    response = await client.get("/users/id/9999")
    assert response.status_code == 404


async def test_get_user_by_name(client):
    response = await client.get("/users/name/user_name_test_1")
    assert response.status_code == 200
    assert response.json()["name"] == "user_name_test_1"


async def test_create_user(client):
    response = await client.post("/users/", json={"name": "new_user"})
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "new_user"
    assert "id" in data


async def test_create_user_invalid(client):
    # name обязателен
    response = await client.post("/users/", json={})
    assert response.status_code == 422


# ==========
# orders
# ==========


async def test_get_user_orders(client):
    response = await client.get("/users/1/orders/")
    assert response.status_code == 200
    data = response.json()
    assert all(order["user_id"] == 1 for order in data)


async def test_get_user_orders_user_not_found(client):
    response = await client.get("/users/9999/orders/")
    assert response.status_code == 404


async def test_create_order(client):
    response = await client.post(
        "/orders/",
        json={
            "user_id": 1,
            "product_id": 1,
            "quantity": 5,
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["user_id"] == 1
    assert data["product_id"] == 1
    assert data["quantity"] == 5


async def test_create_order_user_not_found(client):
    response = await client.post(
        "/orders/",
        json={
            "user_id": 9999,
            "product_id": 1,
            "quantity": 1,
        },
    )
    assert response.status_code == 404


async def test_create_order_product_not_found(client):
    response = await client.post(
        "/orders/",
        json={
            "user_id": 1,
            "product_id": 9999,
            "quantity": 1,
        },
    )
    assert response.status_code == 404


async def test_create_order_invalid_quantity(client):
    # quantity не может быть 0
    response = await client.post(
        "/orders/",
        json={
            "user_id": 1,
            "product_id": 1,
            "quantity": 0,
        },
    )
    assert response.status_code == 422


# ==========
# debug
# ==========


async def test_flush_and_seed(client):
    await client.delete("/debug/flush/")

    # После flush данных нет
    response = await client.get("/products/limit/5/offset/1")
    assert response.status_code == 404

    await client.post("/debug/seed/")

    # После seed данные снова есть
    response = await client.get("/products/limit/5/offset/1")
    assert response.status_code == 200
