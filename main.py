from fastapi import FastAPI
from models import Action, Observation
from environment import SmartFarmEnv

app = FastAPI(title="Meta OpenEnv: Smart Irrigation")
env = SmartFarmEnv()

@app.post("/reset")
def reset():
    return env.reset()

@app.post("/step")
def step(action: Action):
    obs, reward, done, info = env.step(action)
    return {"observation": obs, "reward": reward, "done": done, "info": info}

@app.get("/state")
def state():
    return env.state()

@app.get("/tasks")
def list_tasks():
    return ["survival", "efficiency", "drought"]