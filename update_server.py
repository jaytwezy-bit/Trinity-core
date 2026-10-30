import re

council_code = '''

class DebateRequest(BaseModel):
    topic: str

@app.post("/council/debate")
def trigger_council_debate(req: DebateRequest):
    discussion = [
        {
            "speaker": "Ashley",
            "role": "Brunette Persona / Operations & Systems",
            "argument": f"Regarding '{req.topic}': We should prioritize backend stability and lead-generation automation in Termux first."
        },
        {
            "speaker": "April",
            "role": "Blonde Persona / Growth & Strategy",
            "argument": f"I agree with Ashley, but we also need live audience loops and interactive stream capabilities running in parallel."
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
'''

with open("server.py", "r") as f:
    content = f.read()

if "/council/debate" not in content:
    with open("server.py", "a") as f:
        f.write(council_code)
    print("[SUCCESS] Council debate endpoint appended to server.py")
else:
    print("[INFO] Council debate endpoint already exists in server.py")
