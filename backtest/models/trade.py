from pydantic import BaseModel, Field
from uuid import UUID, uuid4


class Trade(BaseModel):
    timestamp: int
    execution_id: UUID = Field(default_factory=uuid4)
    base: str
    quote: str
    side: str
    filled: float  # base amount
    price: float
    order_id: UUID
