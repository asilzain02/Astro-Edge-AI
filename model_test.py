import sounddevice as sd
import queue
from vosk import Model, KaldiRecognizer
import json

# -----------------------
# Settings
# -----------------------
MODEL_PATH = r"D:\astro_edge_ai\astro_edge_ai\models\vosk-model-small-en-us-0.15"
HOTWORD = "hello"

# -----------------------
# Load Model
# -----------------------
print("[INFO] Loading Vosk model...")
model = Model(MODEL_PATH)
rec = KaldiRecognizer(model, 16000)
print("[INFO] Model loaded!")

# -----------------------
# Audio Queue
# -----------------------
q = queue.Queue()

def callback(indata, frames, time, status):
    if status:
        print(status)
    q.put(bytes(indata))

# -----------------------
# Start Listening
# -----------------------
print("[INFO] Listening... Say the hotword:", HOTWORD)
with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                       channels=1, callback=callback):
    while True:
        data = q.get()
        if rec.AcceptWaveform(data):
            result = json.loads(rec.Result())
            text = result.get("text", "").lower()
            if text:
                print("Heard:", text)
                if HOTWORD in text:
                    print("🔥 Hotword detected!")
