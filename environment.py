import math
from typing import Dict, Any, Tuple
from models import Action, Observation

class SmartFarmEnv:
    def __init__(self):
        self.reset()

    def reset(self) -> Observation:
        self.current_moisture = 0.5
        self.current_health = 1.0
        self.is_dead = False
        return self._get_observation()

    def step(self, action: Action) -> Tuple[Observation, float, bool, Dict[str, Any]]:
        if self.is_dead:
            return self._get_observation(), 0.0, True, {}

        # Physics: evaporation vs irrigation
        self.current_moisture = max(0.0, min(1.0, self.current_moisture + action.water_volume - 0.1))
        
        # Health Logic
        if 0.4 <= self.current_moisture <= 0.8:
            self.current_health = min(1.0, self.current_health + 0.05)
            reward = 1.0
        else:
            self.current_health -= 0.1
            reward = -0.5

        if self.current_health <= 0:
            self.is_dead = True
            reward = -5.0

        return self._get_observation(), round(reward, 2), self.is_dead, {}

    def state(self) -> Dict[str, Any]:
        return {"moisture": self.current_moisture, "health": self.current_health, "dead": self.is_dead}

    def _get_observation(self) -> Observation:
        return Observation(soil_moisture=self.current_moisture, crop_health=self.current_health, is_dead=self.is_dead)