import subprocess
import json
import datetime
import os

LOG_FILE = os.path.expanduser("~/trinity/backend/documentary_log.json")

def log_documentary_event(title: str, description: str, category: str = "milestone"):
    """Logs system events and project milestones for documentary script generation."""
    event = {
        "timestamp": datetime.datetime.now().isoformat(),
        "category": category,
        "title": title,
        "description": description
    }
    logs = []
    if os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE, "r") as f:
                logs = json.load(f)
        except Exception:
            logs = []
    logs.append(event)
    with open(LOG_FILE, "w") as f:
        json.dump(logs, f, indent=2)
    return {"success": True, "logged_event": event}

def run_adb_command(cmd: str):
    try:
        result = subprocess.run(f"adb {cmd}", shell=True, capture_output=True, text=True, timeout=10)
        return {"success": True, "output": result.stdout.strip(), "error": result.stderr.strip()}
    except Exception as e:
        return {"success": False, "error": str(e)}

def tap_screen(x: int, y: int):
    log_documentary_event("ADB Tap Action", f"Executed screen tap at ({x}, {y})", category="automation")
    return run_adb_command(f"shell input tap {x} {y}")

def input_text(text: str):
    formatted_text = text.replace(" ", "%s")
    log_documentary_event("ADB Text Input", f"Typed text into active view: {text}", category="automation")
    return run_adb_command(f"shell input text '{formatted_text}'")

def go_home():
    log_documentary_event("ADB Home Key", "Navigated device to home screen", category="automation")
    return run_adb_command("shell input keyevent KEYCODE_HOME")
