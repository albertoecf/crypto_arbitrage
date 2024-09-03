from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class UnifiedMarketData(BaseModel):
    exchange: str
    symbol: str
    price: float
    bid: Optional[float] = None
    ask: Optional[float] = None
    timestamp: datetime

    class Config:
        # Updated to json_schema_extra for Pydantic v2
        json_schema_extra = {
            "example": {
                "exchange": "binance",
                "symbol": "BTC/USDT",
                "price": 29000.5,
                "bid": 28950.1,
                "ask": 29010.3,
                "timestamp": "2024-08-29T12:30:00Z"
            }
        }
