import os
import subprocess

def generate_actor_speech(persona: str, script: str):
    """
    Generates speech output for the active persona.
    Saves audio to the outputs directory.
    """
    os.makedirs("outputs", exist_ok=True)
    filename = f"outputs/{persona}_{int(os.path.exists('outputs'))}.wav"
    
    # Placeholder for local espeak / festival / kokoro TTS integration in Termux
    print(f"[TTS ENGINE] Generating audio for {persona.capitalize()}: '{script}'")
    
    # If espeak is installed in Termux, this will synthesize live audio
    try:
        subprocess.run(["espeak", "-v", "en+f2", script, "-w", filename], check=True)
        print(f"[TTS ENGINE] Audio saved to {filename}")
        return filename
    except Exception as e:
        print(f"[TTS ENGINE] Note: espeak skipped or unavailable ({e}). Logging text-only response.")
        return None

if __name__ == "__main__":
    generate_actor_speech("ashley", "Trinity backend automation is fully online.")
