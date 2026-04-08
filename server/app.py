import sys
import os
import uvicorn
from fastapi import FastAPI

# Ensure the root directory is in the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app

def main():
    """Entry point for the Meta OpenEnv validator."""
    # Port 7860 is the standard for Hugging Face Spaces
    uvicorn.run(app, host="0.0.0.0", port=7860)

if __name__ == "__main__":
    main()