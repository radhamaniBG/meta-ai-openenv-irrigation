from pydantic import BaseModel
from typing import List

class Action(BaseModel):
    water_volume: float  # Range: 0.0 to 1.0 liters
    fertilizer_type: int = 0 # 0: None, 1: Nitrogen

class Observation(BaseModel):
    soil_moisture: float
    nitrogen_level: float
    weather_forecast: float
    crop_health: float

class State(BaseModel):
    day: int
    total_water_used: float
    history: List[float]