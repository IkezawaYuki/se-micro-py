from datetime import datetime
from enum import Enum
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, conint, conlist, validator, field_validator


class Size(Enum):
    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "big"


class StatusEnum(Enum):
    created = "created"
    paid = "paid"
    progress = "progress"
    cancelled = "cancelled"
    dispatched = "dispatched"
    delivered = "delivered"


class OrderItemSchema(BaseModel):
    product: str
    size: Size
    quantity: Optional[conint(ge=1, strict=True)] = 1

    @field_validator('quantity')
    def validate_quantity(cls, v):
        assert v is not None, 'quantity must not be None'
        return v


class CreateOrderSchema(BaseModel):
    order: conlist(OrderItemSchema, min_length=1)


class GetOrderSchema(CreateOrderSchema):
    id: UUID
    created: datetime
    status: StatusEnum


class GetOrdersSchemas(BaseModel):
    orders: List[GetOrderSchema]



