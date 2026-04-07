from pydantic import BaseModel
from typing import Optional

class Action(BaseModel):
    water_volume: float
    fertilizer_type: int

class Observation(BaseModel):
    soil_moisture: float
    crop_health: float
    is_dead: bool
    nitrogen_level: float = 0.0
    weather_forecast: int = 0