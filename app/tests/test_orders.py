import pytest
from app.models.order import Order
from sqlalchemy.future import select

@pytest.mark.asyncio
async def test_create_order_successfully(async_client, db_session):
    # 1. Arrange: Prepare a valid payload matching our Pydantic schema
    payload = {
        "customer_email": "test-buyer@company.com",
        "product_sku": "SKU-ASYNC-99",
        "quantity": 5,
        "total_price": 199.4
    }

    # 2. Send a async POST request to out api endpoint
    response = await async_client.post("/api/v1/orders/", json=payload)

    # 3. Assert: Verify the API returned the correct HTTP 201 Created and JSON payload
    assert response.status_code == 201
    json_data = response.json()
    assert json_data["customer_email"] == "test-buyer@company.com"
    assert json_data["status"] == "pending"
    assert "id" in json_data

    #4. Verify DB State: Query the isolated database to prove it actually persisted
    query = select(Order).where(Order.id == json_data["id"])
    result = await db_session.execute(query)
    persisted_order = result.scalars().first()

    assert persisted_order is not None 
    assert persisted_order.product_sku == "SKU-ASYNC-99"