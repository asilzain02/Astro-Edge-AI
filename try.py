import tkinter as tk
from tkinter import scrolledtext, ttk, messagebox
from llama_cpp import Llama
import pyttsx3
import threading
import time
import datetime
import json
import csv
import os
import random
import psutil   # For memory usage monitoring

#######################################################
# 🔹 CORE AI ENGINE – with testing hooks
#######################################################
class CoreAI:
    def __init__(self, model_path):
        print("🚀 Loading TinyLlama model...")
        self.llm = Llama(model_path=model_path, n_ctx=2048, n_threads=6)
        print("✅ TinyLlama loaded successfully.")
        self.base_prompt = (
            "You are AstroEdge AI, an astronaut assistant. "
            "Provide step-by-step guidance for repairs, navigation, and stress management."
        )
        self.chat_history = []
        self.metrics_log = []   # store performance metrics

    def ask(self, user_query: str) -> str:
        """Query the model and log inference metrics"""
        start_time = time.time()

        messages = [{"role": "system", "content": self.base_prompt}] + self.chat_history
        messages.append({"role": "user", "content": user_query})

        response = self.llm.create_chat_completion(
            messages=messages,
            max_tokens=350,
            temperature=0.45
        )
        answer = response["choices"][0]["message"]["content"].strip()

        end_time = time.time()
        inference_time = round(end_time - start_time, 2)

        # Memory usage capture
        process = psutil.Process(os.getpid())
        mem_usage = round(process.memory_info().rss / (1024 * 1024), 2)  # MB

        # Log metrics
        self.metrics_log.append({
            "timestamp": datetime.datetime.now().isoformat(),
            "query": user_query,
            "response": answer,
            "inference_time": inference_time,
            "memory_usage_MB": mem_usage
        })

        # Maintain history for context
        self.chat_history.append({"role": "user", "content": user_query})
        self.chat_history.append({"role": "assistant", "content": answer})

        return answer

    def save_metrics(self, filename="astroedge_metrics.csv"):
        """Save logged metrics to CSV for research"""
        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["timestamp", "query", "response", "inference_time", "memory_usage_MB"])
            writer.writeheader()
            writer.writerows(self.metrics_log)
        print(f"✅ Metrics saved to {filename}")

#######################################################
# 🔹 MOCK SENSOR INPUTS
#######################################################
class MockSensors:
    """Simulates gyroscope readings and emotion detection"""
    def get_gyroscope(self):
        # Simulate pitch/yaw/roll values
        return {"pitch": round(random.uniform(-10, 10), 2),
                "yaw": round(random.uniform(-10, 10), 2),
                "roll": round(random.uniform(-10, 10), 2)}

    def detect_emotion(self):
        # Randomly simulate astronaut stress levels
        return random.choice(["calm", "stressed", "neutral"])

#######################################################
# 🔹 VOICE SYSTEM
#######################################################
class VoiceSystem:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 160)
        self.voice_enabled = True

    def speak(self, text):
        if self.voice_enabled:
            self.engine.say(text)
            self.engine.runAndWait()

#######################################################
# 🔹 GUI APP – Research UI
#######################################################
class AstroEdgeApp:
    def __init__(self, model_path):
        self.ai = CoreAI(model_path)
        self.voice = VoiceSystem()
        self.sensors = MockSensors()
        self.log_count = 0

        os.makedirs("logs", exist_ok=True)

        # GUI Setup
        self.root = tk.Tk()
        self.root.title("🚀 AstroEdge AI – Research Prototype")
        self.root.geometry("950x650")
        self.root.configure(bg="#0B0B15")

        header = tk.Label(self.root, text="🚀 ASTROEDGE AI – Research Prototype",
                          font=("Orbitron", 20, "bold"), fg="cyan", bg="#141424", pady=15)
        header.pack(fill="x")

        # Chat Display
        self.chat_display = scrolledtext.ScrolledText(self.root, bg="#1C1C28", fg="white",
                                                      font=("Consolas", 12), wrap="word", state=tk.DISABLED)
        self.chat_display.pack(padx=10, pady=10, fill="both", expand=True)
        self._append_chat("🤖 AstroEdge: Research Mode Activated.\n\n", "lightgreen")

        # Entry Box
        self.entry = tk.Entry(self.root, font=("Consolas", 12))
        self.entry.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.X, expand=True)
        self.entry.bind("<Return>", self.send_query)

        # Buttons
        tk.Button(self.root, text="Send", command=self.send_query, bg="green", fg="white").pack(side=tk.LEFT, padx=5)
        tk.Button(self.root, text="Save Metrics", command=self.save_metrics, bg="orange", fg="black").pack(side=tk.LEFT, padx=5)

    def send_query(self, event=None):
        query = self.entry.get().strip()
        if not query:
            return

        # Simulate sensor readings
        gyro_data = self.sensors.get_gyroscope()
        emotion = self.sensors.detect_emotion()

        # Show astronaut query
        self._append_chat(f"👨‍🚀 Astronaut: {query} (Sensors: {gyro_data}, Emotion: {emotion})\n", "cyan")
        self.entry.delete(0, tk.END)

        # Run inference in background
        threading.Thread(target=self._get_ai_response, args=(query,), daemon=True).start()

    def _get_ai_response(self, query):
        answer = self.ai.ask(query)
        self.root.after(0, lambda: self._append_ai_answer(answer))

    def _append_chat(self, text, color):
        self.chat_display.configure(state=tk.NORMAL)
        self.chat_display.insert(tk.END, text)
        self.chat_display.tag_config(color, foreground=color)
        self.chat_display.tag_add(color, f"end-{len(text)}c", tk.END)
        self.chat_display.configure(state=tk.DISABLED)
        self.chat_display.see(tk.END)

    def _append_ai_answer(self, answer):
        self._append_chat(f"🤖 AstroEdge: {answer}\n\n", "lightgreen")
        self.voice.speak(answer)
        self.log_count += 1

    def save_metrics(self):
        filename = f"logs/astroedge_metrics_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        self.ai.save_metrics(filename)
        messagebox.showinfo("Metrics Saved", f"✅ Metrics saved to {filename}")

    def run(self):
        self.root.mainloop()

#######################################################
# 🚀 RUN APP
#######################################################
if __name__ == "__main__":
    MODEL_PATH = r"C:\Hema\Contest\astro_edge_ai\tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf"
    app = AstroEdgeApp(MODEL_PATH)
    app.run()
