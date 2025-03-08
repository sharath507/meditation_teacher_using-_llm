import os
from typing import List, Optional
from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import httpx
from pydantic import BaseModel
import json
from prompt_templates import MEDITATION_SCRIPT_PROMPT

app = FastAPI(title="Guided Meditation Script Generator")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Set up templates and static files
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Configuration for LLM API
WEBUI_ENABLED = True  # Set to use open-webui API
WEBUI_BASE_URL = "https://chat.ivislabs.in/api"
API_KEY = "INSERT_YOUR_API_KEY"  # Replace with actual API key
DEFAULT_MODEL = "gemma2:2b"  # Update to an available model

OLLAMA_ENABLED = True  # Fallback to local Ollama API
OLLAMA_HOST = "localhost"
OLLAMA_PORT = "11434"
OLLAMA_API_URL = f"http://{OLLAMA_HOST}:{OLLAMA_PORT}/api"

class GenerationRequest(BaseModel):
    goal: str
    experience_level: str
    duration: int = 10
    voice_tone: Optional[str] = "calm"

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index12.html", {"request": request})

@app.post("/generate")
async def generate_script(
    goal: str = Form(...),
    experience_level: str = Form(...),
    duration: int = Form(10),
    voice_tone: str = Form("calm"),
    model: str = Form(DEFAULT_MODEL)
):
    try:
        prompt = MEDITATION_SCRIPT_PROMPT.format(
            goal=goal,
            experience_level=experience_level,
            duration=duration,
            voice_tone=voice_tone
        )

        if WEBUI_ENABLED:
            try:
                messages = [{"role": "user", "content": prompt}]
                request_payload = {"model": model, "messages": messages}
                async with httpx.AsyncClient() as client:
                    response = await client.post(
                        f"{WEBUI_BASE_URL}/chat/completions",
                        headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},
                        json=request_payload,
                        timeout=60.0
                    )
                    if response.status_code == 200:
                        result = response.json()
                        generated_text = result.get("choices", [{}])[0].get("message", {}).get("content", "")
                        return {"generated_script": generated_text}
            except Exception as e:
                print(f"API attempt failed: {str(e)}")

        if OLLAMA_ENABLED:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{OLLAMA_API_URL}/generate",
                    json={"model": model, "prompt": prompt, "stream": False},
                    timeout=60.0
                )
                if response.status_code == 200:
                    result = response.json()
                    generated_text = result.get("response", "")
                    return {"generated_script": generated_text}

        raise HTTPException(status_code=500, detail="Failed to generate script")
    except Exception as e:
        print(f"Error generating script: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error generating script: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host= "localhost", port=8001, reload=True)
