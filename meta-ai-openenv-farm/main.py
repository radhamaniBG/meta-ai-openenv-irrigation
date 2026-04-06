import uvicorn
from fastapi import FastAPI, HTTPException
from environment import SmartFarmEnv
from models import Action

app = FastAPI(title="Meta OpenEnv: Smart Irrigation")
env = SmartFarmEnv()

# --- TASK GRADERS ---
@app.get("/tasks")
def list_tasks():
    return [
        {"id": "survival", "difficulty": "easy", "description": "Keep plant alive for 10 days."},
        {"id": "efficiency", "difficulty": "medium", "description": "Keep moisture at 0.7 with minimal water."},
        {"id": "drought", "difficulty": "hard", "description": "Survive a heatwave (high evaporation)."}
    ]

@app.get("/grade/{task_id}")
def grade_task(task_id: str):
    """Returns a score between 0.0 and 1.0 based on agent performance."""
    if task_id == "survival":
        # Score 1.0 if the plant lived at least 15 days
        score = min(1.0, env.state.day / 15.0)
    elif task_id == "efficiency":
        # Score based on how close moisture is to 0.7 and water use is low
        moisture_penalty = abs(env.current_moisture - 0.7)
        water_penalty = min(0.5, env.state.total_water_used / 20.0)
        score = max(0.0, 1.0 - moisture_penalty - water_penalty)
    elif task_id == "drought":
        # Hard task: Survival during high evaporation
        score = 1.0 if (env.state.day >= 30 and env.current_moisture > 0.1) else 0.0
    else:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return {"task": task_id, "score": round(score, 2)}

# --- CORE API ---
@app.post("/reset")
async def reset():
    return env.reset()

@app.post("/step")
async def step(action: Action):
    observation, reward, done = env.step(action)
    return {"observation": observation, "reward": reward, "done": done}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7860)