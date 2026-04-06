import random
from models import Observation, State, Action

class SmartFarmEnv:  # <--- Make sure this name is EXACTLY SmartFarmEnv
    def __init__(self):
        self.max_steps = 30
        self.reset()

    def reset(self) -> Observation:
        self.state = State(day=0, total_water_used=0.0, history=[])
        self.current_moisture = 0.5
        self.current_nitrogen = 0.6
        return self._get_observation()

    def step(self, action: Action) -> tuple[Observation, float, bool]:
        # Simple physics: evaporation
        self.current_moisture += (action.water_volume - 0.1) 
        self.current_moisture = max(0.0, min(1.0, self.current_moisture))
        
        self.state.day += 1
        self.state.total_water_used += action.water_volume
        
        # Reward: 1.0 if moisture is near 0.7, else lower
        reward = max(0.0, 1.0 - abs(self.current_moisture - 0.7))
        done = self.state.day >= self.max_steps
        
        return self._get_observation(), reward, done

    def _get_observation(self) -> Observation:
        return Observation(
            soil_moisture=round(self.current_moisture, 2),
            nitrogen_level=0.5,
            weather_forecast=0.0,
            crop_health=1.0 if self.current_moisture > 0.2 else 0.0
        )