from pydantic import BaseModel
from datetime import date
from typing import List

# Minimum data that is required
class SaleRecord(BaseModel):
    date: date
    product_id: str
    quantity: int
    price: float
    cost: float

# Used to show the user what data we have received
class SaleResponse(BaseModel):
    filename: str
    row_count: int
    columns: List[str]
    sample_data: List[dict]
