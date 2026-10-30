import os
import json
import subprocess
from datetime import datetime
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()
LOG_FILE = "documentary_logs.json"
LEADS_FILE = "leads_log.json"

class ActingRequest(BaseModel):
    persona: str
    script: str
    project_type: str

class LogEventRequest(BaseModel):
    title: str
    description: str
    category: str

class DebateRequest(BaseModel):
    topic: str

def log_documentary_event(title, description, category):
    logs = []
    if os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE, "r") as f:
                logs = json.load(f)
        except json.JSONDecodeError:
            logs = []
            
    event = {
        "timestamp": datetime.now().isoformat(),
        "category": category,
        "title": title,
        "description": description
    }
    logs.append(event)
    with open(LOG_FILE, "w") as f:
        json.dump(logs, f, indent=2)
    return event

@app.get("/documentary/logs")
def get_logs():
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            return json.load(f)
    return []

@app.post("/documentary/log")
def create_log(req: LogEventRequest):
    event = log_documentary_event(req.title, req.description, req.category)
    return {"success": True, "logged_event": event}

@app.post("/actor/speak")
def actor_perform(req: ActingRequest):
    log_documentary_event(
        title=f"Actor Line Generated: {req.persona.capitalize()}",
        description=f"Project: {req.project_type} | Line: '{req.script}'",
        category="acting"
    )
    
    audio_filename = f"outputs/{req.persona}_{int(datetime.now().timestamp())}.wav"
    audio_status = "Generated text-only log"
    
    try:
        os.makedirs("outputs", exist_ok=True)
        subprocess.run(["espeak", "-v", "en+f2", req.script, "-w", audio_filename], check=True)
        audio_status = f"Audio synthesized to {audio_filename}"
    except Exception:
        pass

    return {
        "success": True,
        "persona": req.persona,
        "project_type": req.project_type,
        "script_queued": req.script,
        "audio_status": audio_status,
        "message": f"Line assigned to {req.persona.capitalize()}."
    }

@app.post("/daemon/scan-leads")
def trigger_lead_scan():
    lead = {
        "source": "Reddit/Subreddit Scanner",
        "query": "custom automation AI agent",
        "status": "Lead captured successfully",
        "timestamp": datetime.now().isoformat()
    }
    
    leads = []
    if os.path.exists(LEADS_FILE):
        try:
            with open(LEADS_FILE, "r") as f:
                leads = json.load(f)
        except json.JSONDecodeError:
            leads = []
            
    leads.append(lead)
    with open(LEADS_FILE, "w") as f:
        json.dump(leads, f, indent=2)
        
    log_documentary_event(
        title="Automated Lead Scanned",
        description="Background daemon captured a new digital lead.",
        category="daemon"
    )
    
    return {"success": True, "lead": lead}

@app.post("/council/debate")
def trigger_council_debate(req: DebateRequest):
    discussion = [
        {
            "speaker": "Ashley",
            "role": "Brunette Persona / Operations & Systems",
            "argument": f"Regarding '{req.topic}': We must ensure robust backend stability and automated background execution in Termux first."
        },
        {
            "speaker": "April",
            "role": "Blonde Persona / Growth & Strategy",
            "argument": f"That's true Ashley, but we also need to push live multi-persona interactions forward immediately to engage our audience."
        }
    ]
    
    log_documentary_event(
        title=f"Council Debate: {req.topic}",
        description="Ashley and April held a strategic debate.",
        category="debate"
    )
    
    return {
        "success": True,
        "topic": req.topic,
        "debate_transcript": discussion
    }

def query_local_ollama(prompt: str, persona_role: str):
    try:
        url = "http://localhost:11434/api/generate"
        payload = {
            "model": "qwen2.5:0.5b",
            "prompt": f"You are {persona_role}. Respond concisely (1-2 sentences) to this topic: {prompt}",
            "stream": False
        }
        req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers={'Content-Type': 'application/json'})
        with urllib.request.urlopen(req, timeout=3) as response:
            res = json.loads(response.read().decode())
            return res.get("response", "").strip()
    except Exception:
        return None

from fastapi import WebSocket, WebSocketDisconnect

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

@app.websocket("/ws/live-stream")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"Trinity Stream Event: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
