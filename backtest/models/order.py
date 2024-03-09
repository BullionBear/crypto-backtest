from pydantic import BaseModel, Field
from uuid import UUID, uuid4


class Order(BaseModel):
    base: str
    quote: str
    side: str
    amount: float  # base amount
    order_id: UUID = Field(default_factory=uuid4)

    class Config:
        arbitrary_types_allowed = True


class LimitOrder(Order):
    price: float


class MarketOrder(Order):
    pass


class StopLimitOrder(Order):
    stop_price: float
    limit_price: float
