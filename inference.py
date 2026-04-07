import os
import requests
import textwrap
from typing import List, Optional
from openai import OpenAI

# 1. MANDATORY ENVIRONMENT VARIABLES & DEFAULTS
API_BASE_URL = os.getenv("API_BASE_URL", "https://router.huggingface.co/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "Qwen/Qwen2.5-72B-Instruct")
HF_TOKEN = os.getenv("HF_TOKEN")
API_KEY = HF_TOKEN  # Using HF_TOKEN as the API Key

# Meta Benchmark Details
TASK_NAME = "survival"
BENCHMARK = "smart-irrigation"
SPACE_URL = "https://shreyamani-meta-ai-openenv-farm.hf.space"
MAX_STEPS = 5
MAX_TOTAL_REWARD = 5.0  # Used for score normalization (Sum of rewards / Max possible)

client = OpenAI(base_url=API_BASE_URL, api_key=API_KEY)

# 2. LOGGING UTILITIES (MATCHING SAMPLE EXACTLY)
def log_start(task: str, env: str, model: str) -> None:
    print(f"[START] task={task} env={env} model={model}", flush=True)

def log_step(step: int, action: str, reward: float, done: bool, error: Optional[str]) -> None:
    error_val = error if error else "null"
    done_val = str(done).lower()
    print(f"[STEP] step={step} action={action} reward={reward:.2f} done={done_val} error={error_val}", flush=True)

def log_end(success: bool, steps: int, score: float, rewards: List[float]) -> None:
    rewards_str = ",".join(f"{r:.2f}" for r in rewards)
    print(f"[END] success={str(success).lower()} steps={steps} score={score:.2f} rewards={rewards_str}", flush=True)

# 3. INFERENCE LOGIC
def run_inference():
    log_start(task=TASK_NAME, env=BENCHMARK, model=MODEL_NAME)
    
    rewards = []
    steps_taken = 0
    success = False
    
    try:
        # Reset the environment
        res = requests.post(f"{SPACE_URL}/reset").json()
        obs = res
        
        for step in range(1, MAX_STEPS + 1):
            # Prompt the LLM
            prompt = f"Current soil moisture is {obs['soil_moisture']}. Provide a water volume between 0.0 and 1.0. Output only the number."
            
            completion = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=10
            )
            
            try:
                action_text = completion.choices[0].message.content.strip()
                action_val = float(action_text)
            except:
                action_val = 0.5 # Default fallback
            
            # Perform Step
            response = requests.post(f"{SPACE_URL}/step", json={"water_volume": action_val, "fertilizer_type": 0}).json()
            
            reward = response["reward"]
            done = response["done"]
            obs = response["observation"]
            
            rewards.append(reward)
            steps_taken = step
            
            log_step(step=step, action=str(action_val), reward=reward, done=done, error=None)
            
            if done:
                break
                
        # Calculate Final Score (Normalized to 0.0 - 1.0)
        final_score = sum(rewards) / MAX_TOTAL_REWARD
        final_score = min(max(final_score, 0.0), 1.0)
        success = final_score > 0.5

    except Exception as e:
        print(f"[DEBUG] Error during inference: {e}")
    finally:
        log_end(success=success, steps=steps_taken, score=final_score, rewards=rewards)

if __name__ == "__main__":
    run_inference()