from pydantic import BaseModel
from typing import Optional, Dict, Any

class Action(BaseModel):
    water_volume: float
    fertilizer_type: Optional[int] = 0  # Make optional with a default

class Observation(BaseModel):
    soil_moisture: float
    crop_health: float
    is_dead: bool
    # Add any extra fields your env uses here
    nitrogen_level: Optional[float] = 0.0 
    weather_forecast: Optional[int] = 0