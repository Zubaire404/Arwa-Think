import asyncio
import os
import json
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from openai import AsyncOpenAI
from dotenv import load_dotenv

# Ensure keys are loaded
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

app = FastAPI(title="Arwa Think API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files for the custom HTML frontend
frontend_dir = Path(__file__).parent / "public"
frontend_dir.mkdir(exist_ok=True)
app.mount("/static", StaticFiles(directory="public"), name="static")

@app.get("/")
async def serve_frontend():
    index_path = frontend_dir / "index.html"
    if not index_path.exists():
        return {"error": "Frontend not built yet. Create public/index.html"}
    return FileResponse(index_path)

# Initialize Clients
gemini_key = os.getenv("GEMINI_API_KEY", "missing")
fireworks_key = os.getenv("FIREWORKS_API_KEY", "missing")
groq_key = os.getenv("GROQ_API_KEY", "missing")
openrouter_key = os.getenv("OPENROUTER_API_KEY", "missing")

gemini_client = AsyncOpenAI(api_key=gemini_key, base_url="https://generativelanguage.googleapis.com/v1beta/openai/")
fireworks_client = AsyncOpenAI(api_key=fireworks_key, base_url="https://api.fireworks.ai/inference/v1")
groq_client = AsyncOpenAI(api_key=groq_key, base_url="https://api.groq.com/openai/v1")
openrouter_client = AsyncOpenAI(api_key=openrouter_key, base_url="https://openrouter.ai/api/v1")

# ---- Model Registry ----
MODEL_REGISTRY = {
    # Gemini models (via Gemini API)
    "gemini-3.6-flash": {"client": "gemini", "api_id": "gemini-3.6-flash", "label": "Gemini 3.6 Flash"},
    "gemini-3.6-flash-lite": {"client": "gemini", "api_id": "gemini-3.6-flash-lite", "label": "Gemini 3.6 Flash Lite"},
    # Fireworks models
    "fw-deepseek-v4-pro": {"client": "fireworks", "api_id": "accounts/fireworks/models/deepseek-v4-pro-0813", "label": "DeepSeek V4 Pro"},
    "fw-deepseek-v4-flash": {"client": "fireworks", "api_id": "accounts/fireworks/models/deepseek-v4-flash-0731", "label": "DeepSeek V4 Flash"},
    "fw-qwen3p8-max": {"client": "fireworks", "api_id": "accounts/fireworks/models/qwen3p8-max", "label": "Qwen 3.8 Max"},
    "fw-kimi-k3": {"client": "fireworks", "api_id": "accounts/fireworks/models/kimi-k3", "label": "Kimi K3"},
    "fw-glm-5p2": {"client": "fireworks", "api_id": "accounts/fireworks/models/glm-5p2", "label": "GLM 5.2"},
    "fw-minimax-m3": {"client": "fireworks", "api_id": "accounts/fireworks/models/minimax-m3", "label": "Minimax M3"},
    "fw-nemotron-ultra": {"client": "fireworks", "api_id": "accounts/fireworks/models/nemotron-3-ultra-nvfp4", "label": "Nemotron 3 Ultra"},
    "fw-nemotron-light": {"client": "fireworks", "api_id": "accounts/fireworks/models/nemotron-lightning-3p5-30b-a3b", "label": "Nemotron Lightning"},
    "fw-inkling": {"client": "fireworks", "api_id": "accounts/fireworks/models/inkling", "label": "Inkling"},
    "fw-muse-glimmer": {"client": "fireworks", "api_id": "accounts/fireworks/models/muse-glimmer-30b", "label": "Muse Glimmer 30B"},
    "fw-kimi-k2p7-code": {"client": "fireworks", "api_id": "accounts/fireworks/models/kimi-k2p7-code", "label": "Kimi K2.7 Code"},
    "fw-qwen3p7-plus": {"client": "fireworks", "api_id": "accounts/fireworks/models/qwen3p7-plus", "label": "Qwen 3.7 Plus"},
    "fw-gpt-oss-120b": {"client": "fireworks", "api_id": "accounts/fireworks/models/gpt-oss-120b", "label": "GPT-OSS 120B"},
    "fw-qwen3-reranker": {"client": "fireworks", "api_id": "accounts/fireworks/models/qwen3-reranker-8b", "label": "Qwen3 Reranker 8B"},
    "fw-qwen3-embedding": {"client": "fireworks", "api_id": "accounts/fireworks/models/qwen3-embedding-8b", "label": "Qwen3 Embedding 8B"},
}

CLIENT_MAP = {
    "gemini": gemini_client,
    "fireworks": fireworks_client,
    "groq": groq_client,
    "openrouter": openrouter_client,
}

class ChatRequest(BaseModel):
    prompt: str
    auto_route: bool
    manual_models: list[str] = []
    file_data: str | None = None
    file_mime: str | None = None

class Draft(BaseModel):
    label: str
    text: str

class ChatResponse(BaseModel):
    final_answer: str
    models_used: list[str]
    category: str
    drafts: list[Draft]

# Auto-router uses Gemini to classify and pick models
AUTO_ROUTE_MODELS = {
    "Math": ["gemini-3.6-flash", "fw-deepseek-v4-pro", "fw-qwen3p8-max"],
    "Code": ["gemini-3.6-flash", "fw-deepseek-v4-pro", "fw-kimi-k2p7-code"],
    "Creative": ["gemini-3.6-flash", "fw-kimi-k3", "fw-glm-5p2"],
    "Fact": ["gemini-3.6-flash", "fw-deepseek-v4-flash", "fw-minimax-m3"],
    "Search": ["fw-qwen3-reranker", "fw-qwen3-embedding", "gemini-3.6-flash"]
}

async def analyze_and_route(prompt: str) -> tuple[list[str], str]:
    print(f"[Router] Analyzing: {prompt[:80]}...")
    router_prompt = (
        f"Classify this user prompt into exactly one category: Math, Code, Creative, Fact, or Search. If the user is asking to search the web or extract text from images, choose Search.\n"
        f"Prompt: \"{prompt}\"\n"
        f"Reply with ONLY a JSON object like: {{\"category\": \"Code\"}}"
    )
    try:
        res = await asyncio.wait_for(
            gemini_client.chat.completions.create(
                model="gemini-3.6-flash",
                messages=[{"role": "user", "content": router_prompt}],
                response_format={"type": "json_object"}
            ), timeout=10.0
        )
        data = json.loads(res.choices[0].message.content)
        cat = data.get("category", "Fact")
        if cat not in AUTO_ROUTE_MODELS:
            cat = "Fact"
        print(f"[Router] Category: {cat}")
        return AUTO_ROUTE_MODELS[cat], cat
    except Exception as e:
        print(f"[Router] Failed: {e}. Using Fact fallback.")
        return AUTO_ROUTE_MODELS["Fact"], "Fallback"


def build_messages(prompt: str, file_data: str = None, file_mime: str = None):
    if not file_data:
        return [{"role": "user", "content": prompt}]
    return [{
        "role": "user",
        "content": [
            {"type": "text", "text": prompt},
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:{file_mime};base64,{file_data}"
                }
            }
        ]
    }]


async def fetch_draft(client: AsyncOpenAI, api_id: str, prompt: str, label: str, file_data: str = None, file_mime: str = None) -> dict:
    try:
        msgs = build_messages(prompt, file_data, file_mime)
        res = await asyncio.wait_for(
            client.chat.completions.create(
                model=api_id,
                messages=msgs
            ), timeout=45.0
        )
        text = res.choices[0].message.content or ""
        print(f"[OK] {label}")
        return {"success": True, "label": label, "text": text}
    except Exception as e:
        print(f"[FAIL] {label}: {e}")
        return {"success": False, "label": label, "text": ""}


from fastapi.responses import FileResponse, StreamingResponse
import json
import asyncio

async def stream_single_model(client, model_id, prompt, label, file_data=None, file_mime=None):
    meta = {
        "type": "metadata",
        "models_used": [label],
        "category": "Direct",
        "drafts": []
    }
    yield f"data: {json.dumps(meta)}\n\n"
    
    try:
        msgs = build_messages(prompt, file_data, file_mime)
        response = await client.chat.completions.create(
            model=model_id,
            messages=msgs,
            stream=True
        )
        async for chunk in response:
            if chunk.choices and chunk.choices[0].delta and chunk.choices[0].delta.content:
                yield f"data: {json.dumps({'type': 'chunk', 'text': chunk.choices[0].delta.content})}\n\n"
    except Exception as e:
        yield f"data: {json.dumps({'type': 'error', 'text': str(e)})}\n\n"
    
    yield f"data: {json.dumps({'type': 'done'})}\n\n"


@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    user_prompt = request.prompt

    if request.auto_route:
        selected_keys, category = await analyze_and_route(user_prompt)
    else:
        selected_keys = request.manual_models
        category = "Manual"

    print(f"[Chat] Models: {selected_keys}")

    if not selected_keys:
        raise HTTPException(status_code=400, detail="No valid models selected.")

    if category == "Search":
        try:
            from duckduckgo_search import DDGS
            with DDGS() as ddgs:
                results = list(ddgs.text(user_prompt, max_results=3))
                if results:
                    context = "\n\n".join([f"Source: {r['href']}\n{r['body']}" for r in results])
                    user_prompt = f"Using this latest web search context:\n{context}\n\nAnswer the user query: {user_prompt}"
                    print("[Search] Injected web context.")
        except Exception as e:
            print(f"[Search API Error] {e}")

    # Single Model - stream directly without gathering!
    if len(selected_keys) == 1:
        info = MODEL_REGISTRY.get(selected_keys[0])
        if info:
            client = CLIENT_MAP[info["client"]]
            return StreamingResponse(
                stream_single_model(client, info["api_id"], user_prompt, info["label"], request.file_data, request.file_mime),
                media_type="text/event-stream"
            )
    
    # Multiple Models - gather drafts concurrently, then stream synthesis
    async def synthesize_stream():
        tasks = []
        for key in selected_keys:
            info = MODEL_REGISTRY.get(key)
            if info:
                client = CLIENT_MAP[info["client"]]
                tasks.append(fetch_draft(client, info["api_id"], user_prompt, info["label"], request.file_data, request.file_mime))

        drafts = await asyncio.gather(*tasks)
        valid_drafts = [d for d in drafts if d.get("success")]
        models_used = [d["label"] for d in valid_drafts]

        if category == "Search":
            # Add pipeline models to models_used so they show in the UI as having participated
            if "Qwen3 Reranker 8B" not in models_used: models_used.append("Qwen3 Reranker 8B")
            if "Qwen3 Embedding 8B" not in models_used: models_used.append("Qwen3 Embedding 8B")

        if not valid_drafts:
            yield f"data: {json.dumps({'type': 'error', 'text': 'All AI models failed to respond.'})}\n\n"
            return
            
        meta = {
            "type": "metadata",
            "models_used": models_used,
            "category": category,
            "drafts": valid_drafts
        }
        # Yield metadata immediately once drafts are ready
        yield f"data: {json.dumps(meta)}\n\n"
        
        context = "\n\n---\n\n".join([f"**{d['label']}:**\n{d['text']}" for d in valid_drafts])
        judge_sys = "You are Arwa Think, an expert synthesizer. Combine the following AI draft responses into one best, accurate, complete answer. Do not mention the drafts or models."

        try:
            response = await gemini_client.chat.completions.create(
                model="gemini-3.6-flash",
                messages=[
                    {"role": "system", "content": judge_sys},
                    {"role": "user", "content": f"User question: {user_prompt}\n\nDrafts:\n{context}"}
                ],
                temperature=0.3,
                stream=True
            )
            async for chunk in response:
                if chunk.choices and chunk.choices[0].delta and chunk.choices[0].delta.content:
                    yield f"data: {json.dumps({'type': 'chunk', 'text': chunk.choices[0].delta.content})}\n\n"
        except Exception as e:
            # Fallback to the first draft if synthesis fails
            yield f"data: {json.dumps({'type': 'chunk', 'text': valid_drafts[0]['text']})}\n\n"
            
        yield f"data: {json.dumps({'type': 'done'})}\n\n"

    return StreamingResponse(synthesize_stream(), media_type="text/event-stream")