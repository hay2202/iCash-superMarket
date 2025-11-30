from pydantic import BaseModel
from typing import List, Optional


class PurchaseIn(BaseModel):
    supermarket_id: str
    user_id: Optional[str] = None
    items_list: List[str]