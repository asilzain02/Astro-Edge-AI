"""import threading
import speech_recognition as sr
import time

class HotwordListener:
    def __init__(self, hotword="hello", callback=None):
        self.hotword = hotword.lower()
        self.callback = callback
        self.running = False
        self.recognizer = sr.Recognizer()
        self.mic = sr.Microphone()

    def _listen(self):
        with self.mic as source:
            self.recognizer.adjust_for_ambient_noise(source)
            while self.running:
                try:
                    audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=5)
                    query = self.recognizer.recognize_google(audio).lower()
                    print(f"[Hotword Debug] Heard: {query}")
                    if self.hotword in query:
                        if self.callback:
                            self.callback()  # Trigger main app function
                except sr.WaitTimeoutError:
                    continue
                except Exception as e:
                    print(f"[Hotword Error] {e}")
                time.sleep(0.1)

    def start(self):
        if not self.running:
            self.running = True
            threading.Thread(target=self._listen, daemon=True).start()
            print("[Hotword] Listener started...")

    def stop(self):
        self.running = False
        print("[Hotword] Listener stopped.")"""


import threading
import queue
import json
import sounddevice as sd
from vosk import Model, KaldiRecognizer

class HotwordListener:
    def __init__(self, model_path, hotword="hello", callback=None):
        self.hotword = hotword.lower()
        self.callback = callback
        self.running = False
        self.q = queue.Queue()

        print(f"[Hotword] Loading Vosk model from: {model_path}")
        self.model = Model(model_path)
        self.rec = KaldiRecognizer(self.model, 16000)
        print("[Hotword] Model loaded successfully.")

    def _audio_callback(self, indata, frames, time, status):
        if status:
            print(f"[Hotword Audio Error] {status}")
        # Put raw audio data in queue
        self.q.put(bytes(indata))
        print(f"[DEBUG] Got audio chunk ({len(indata)} frames)")

    def _listen(self):
        print(f"[Hotword] Listening for '{self.hotword}' ...")
        try:
            with sd.RawInputStream(
                samplerate=16000,
                blocksize=8000,
                dtype="int16",
                channels=1,
                callback=self._audio_callback,
            ):
                while self.running:
                    data = self.q.get()
                    if self.rec.AcceptWaveform(data):
                        result = json.loads(self.rec.Result())
                        text = result.get("text", "").lower()
                        if text:
                            print(f"[Listening] {text}")
                            if self.hotword in text:
                                print("🔥 Hotword detected!")
                                if self.callback:
                                    self.callback()
                    else:
                        partial = json.loads(self.rec.PartialResult())
                        if partial.get("partial"):
                            print(f"[Partial] {partial['partial']}")
        except Exception as e:
            print(f"[Hotword Critical Error] {e}")

    def start(self):
        if not self.running:
            self.running = True
            threading.Thread(target=self._listen, daemon=True).start()
            print("[Hotword] Listener started (background thread).")

    def stop(self):
        self.running = False
        print("[Hotword] Listener stopped.")

    def _listen(self):
        print("[Hotword DEBUG] _listen() thread started")  # ADD THIS
        try:
            with sd.RawInputStream(
                samplerate=16000,
                blocksize=8000,
                dtype="int16",
                channels=1,
                callback=self._audio_callback,
            ):
                print("[Hotword DEBUG] Microphone stream opened")  # ADD THIS
                while self.running:
                    data = self.q.get()
                    print(f"[Hotword DEBUG] Pulled {len(data)} bytes from queue")  # ADD THIS
                    if self.rec.AcceptWaveform(data):
                        result = json.loads(self.rec.Result())
                        text = result.get("text", "").lower()
                        if text:
                            print(f"[Listening] {text}")
                            if self.hotword in text:
                                print("🔥 Hotword detected!")
                                if self.callback:
                                    self.callback()
                    else:
                        partial = json.loads(self.rec.PartialResult())
                        if partial.get("partial"):
                            print(f"[Partial] {partial['partial']}")
        except Exception as e:
            print(f"[Hotword Critical Error] {e}")


