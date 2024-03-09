from pydantic import BaseModel


class KLine(BaseModel):  # Customized to Binance KLine
    open: float
    high: float
    low: float
    close: float
    volume: float
    open_time: int
    close_time: int
    quote_volume: float
    count: int
    taker_buy_volume: float
    taker_buy_quote_volume: float
    ignore: int

