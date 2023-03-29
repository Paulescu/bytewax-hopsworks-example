from typing import List
from dataclasses import dataclass

@dataclass
class Ticker:
    product_id : str
    ts_unix : int
    price : float
    size : float

@dataclass
class FeatureGroupMetadata:
    name: str
    version: int
    description: str
    primary_key: List[str]
    event_time: str
    online_enabled: bool
