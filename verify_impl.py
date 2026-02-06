import asyncio
import uuid
import httpx
import uvicorn
from multiprocessing import Process
import time
import os

from backend.src.core.config import settings

BASE_URL = "http://127.0.0.1:8000" + settings.API_V1_STR
USER_ID = "test_user_123"

async def verify_api():
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        print(f"Checking health...")
        # Check health at /health (root level usually, or api level?)
        # main.py: @app.get("/health") -> http://127.0.0.1:8000/health
        health_resp = await client.get("http://127.0.0.1:8000/health")
        print(f"Health: {health_resp.status_code} {health_resp.json()}")
        assert health_resp.status_code == 200

        print(f"Creating Task...")
        task_data = {"title": "Integration Task", "description": "Test Desc"}
        resp = await client.post(f"/{USER_ID}/tasks", json=task_data)
        print(f"Create: {resp.status_code} {resp.json()}")
        assert resp.status_code == 201
        task = resp.json()
        assert task["title"] == "Integration Task"
        assert task["owner_id"] == USER_ID
        task_id = task["id"]

        print(f"Listing Tasks...")
        resp = await client.get(f"/{USER_ID}/tasks")
        print(f"List: {resp.status_code} Found: {len(resp.json())}")
        assert resp.status_code == 200
        assert len(resp.json()) >= 1

        print(f"Get Task...")
        resp = await client.get(f"/{USER_ID}/tasks/{task_id}")
        assert resp.status_code == 200
        assert resp.json()["id"] == task_id

        print(f"Update Task...")
        update_data = {"title": "Updated Task", "is_completed": True}
        resp = await client.put(f"/{USER_ID}/tasks/{task_id}", json=update_data)
        print(f"Update: {resp.status_code}")
        assert resp.status_code == 200
        assert resp.json()["title"] == "Updated Task"
        assert resp.json()["is_completed"] is True

        print(f"Mark Complete...")
        resp = await client.patch(f"/{USER_ID}/tasks/{task_id}/complete")
        assert resp.status_code == 200
        assert resp.json()["is_completed"] is True

        print(f"Delete Task...")
        resp = await client.delete(f"/{USER_ID}/tasks/{task_id}")
        print(f"Delete: {resp.status_code}")
        assert resp.status_code == 204

        print(f"Get Deleted Task...")
        resp = await client.get(f"/{USER_ID}/tasks/{task_id}")
        assert resp.status_code == 404

        print("Verification Successful!")

def run_server():
    uvicorn.run("backend.src.main:app", host="127.0.0.1", port=8000, log_level="warning")

if __name__ == "__main__":
    # Start server in a separate process
    server_process = Process(target=run_server)
    server_process.start()

    # Wait for server to start
    time.sleep(5)

    try:
        asyncio.run(verify_api())
    finally:
        server_process.terminate()
        server_process.join()
