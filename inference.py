import os
import requests
from typing import List, Optional
from openai import OpenAI

# 5) Code Structure Checklist: Environment Variables & Defaults
API_BASE_URL = os.getenv("API_BASE_URL", "https://api-inference.huggingface.co/v1/")
MODEL_NAME = os.getenv("MODEL_NAME", "meta-llama/Llama-3-8B-Instruct")
HF_TOKEN = os.getenv("HF_TOKEN")

# Initialize OpenAI Client (Checklist #5)
client = OpenAI(base_url=API_BASE_URL, api_key=HF_TOKEN)

SPACE_URL = "https://shreyamani-meta-ai-openenv-farm.hf.space"
TASK_NAME = "survival"

def log_start(task: str, env: str, model: str):
    print(f"[START] task={task} env={env} model={model}", flush=True)

def log_step(step: int, action: str, reward: float, done: bool, error: Optional[str]):
    # Checklist #6: Lowercase booleans and 2 decimal rewards
    print(f"[STEP] step={step} action={action} reward={reward:.2f} done={str(done).lower()} error={error or 'null'}", flush=True)

def log_end(success: bool, steps: int, score: float, rewards: List[float]):
    # Checklist #6: Lowercase booleans
    rewards_str = ",".join(f"{r:.2f}" for r in rewards)
    print(f"[END] success={str(success).lower()} steps={steps} score={score:.2f} rewards={rewards_str}", flush=True)

def run_inference():
    log_start(TASK_NAME, "smart-irrigation", MODEL_NAME)
    rewards, steps_taken, success = [], 0, False
    final_score = 0.0

    try:
        # Reset Env
        res = requests.post(f"{SPACE_URL}/reset").json()
        obs = res.get("observation", res) # Handle different API structures

        for step in range(1, 6):
            # LLM Call via OpenAI Client
            prompt = f"Moisture is {obs.get('soil_moisture')}. Water volume (0.0-1.0)? Just the number."
            completion = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=10
            )
            action = completion.choices[0].message.content.strip()
            
            # Environment Step
            response = requests.post(f"{SPACE_URL}/step", json={"water_volume": float(action or 0.5)}).json()
            
            reward = response.get("reward", 0.0)
            done = response.get("done", False)
            obs = response.get("observation", {})
            
            rewards.append(reward)
            steps_taken = step
            log_step(step, action, reward, done, None)
            
            if done: break
        
        final_score = sum(rewards) / len(rewards) if rewards else 0.0
        success = final_score > 0.5

    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Checklist #6: Must always print [END]
        log_end(success, steps_taken, final_score, rewards)

if __name__ == "__main__":
    run_inference()