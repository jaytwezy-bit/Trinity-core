import urllib.request
import json

with open("server.py", "r") as f:
    content = f.read()

llm_router_code = '''
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
'''

if "query_local_ollama" not in content:
    with open("server.py", "a") as f:
        f.write(llm_router_code)
    print("[SUCCESS] Ollama dynamic router added.")
else:
    print("[INFO] Ollama router already in server.py.")
