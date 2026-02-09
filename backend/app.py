from fastapi import FastAPI
from src.main import app

# This creates an alias for the main app so Hugging Face can find it
application = app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)