import uuid
from datetime import datetime
from uuid import UUID

from fastapi import HTTPException
from starlette.responses import Response
from starlette import status

from orders.app import app
from orders.api.schemes import (
    GetOrderSchema,
    CreateOrderSchema,
    GetOrderSchema
)

ORDERS = []


@app.get("/health")
async def health():
    return Response(status_code=status.HTTP_200_OK, content="OK")


@app.get("/orders", response_model=GetOrderSchema)
def get_orders():
    return {"orders": ORDERS}


@app.post("/orders",
          status_code=status.HTTP_201_CREATED,
          response_model=GetOrderSchema)
def create_order(order_details: CreateOrderSchema):
    order = order_details.dict()
    order['id'] = str(uuid.uuid4())
    order['created'] = datetime.now()
    order['status'] = 'created'
    ORDERS.append(order)
    return order


@app.put("/orders/{order_id}")
def update_order(order_id: UUID, order_detail: CreateOrderSchema):
    for order in ORDERS:
        if order["id"] == order_id:
            order.update(order_detail.dict())
            return order
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Order not found"
    )


@app.delete("/orders/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_order(order_id: UUID):
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.post("/orders{order_id}/cancel")
def cancel_order(order_id: UUID):
    for order in ORDERS:
        if order["id"] == order_id:
            order["status"] = 'cancelled'
            return order
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="not found")


@app.post("/orders/{order_id}/pay")
def pay_order(order_id: UUID, updated_order: dict):
    for order in ORDERS:
        if order["id"] == order_id:
            order["status"] = 'progress'
            return order
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="not found")


@app.get("/orders/{order_id}")
def get_order(order_id: UUID):
    for order in ORDERS:
        if order["id"] == order_id:
            return order
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Order not found"
    )

