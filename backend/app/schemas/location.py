from pydantic import BaseModel
from typing import Optional, List

class PincodeDetails(BaseModel):
    pincode: str
    office_name: str
    district: str
    state: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    circle: Optional[str] = None
    region: Optional[str] = None

class LocationQuery(BaseModel):
    query: str

class LocationResolveResponse(BaseModel):
    query: str
    resolved_name: str
    pincode: Optional[str] = None
    district: Optional[str] = None
    state: Optional[str] = None
    latitude: float
    longitude: float
    confidence: float = 1.0
