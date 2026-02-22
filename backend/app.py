from fastapi import FastAPI
from src.main import app
import os

# This creates an alias for the main app so Hugging Face can find it
application = app

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)