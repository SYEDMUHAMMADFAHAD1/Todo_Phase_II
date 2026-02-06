@echo off
cd /d "C:\hackthone2_clone\Todo_App"
set PYTHONPATH=%cd%\backend;%PYTHONPATH%
python -c "import sys; sys.path.insert(0, 'C:/hackthone2_clone/Todo_App/backend'); import uvicorn; from backend.src.main import app; uvicorn.run(app, host='0.0.0.0', port=8000)"