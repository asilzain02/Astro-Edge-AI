import tkinter as tk
from tkinter import scrolledtext, ttk, messagebox
from llama_cpp import Llama
import pyttsx3, threading, time, datetime, json, csv, os, random, psutil

#######################################################
# 🔹 YOLOv8 Vision Stub
#######################################################
class VisionModule:
    """Simulated YOLOv8 object detection for demo purposes."""
    def detect(self):
        objects = ["toolbox", "loose wire", "oxygen valve", "control panel"]
        detection = random.choice(objects)
        confidence = round(random.uniform(0.75, 0.99), 2)
        return {"object": detection, "confidence": confidence}

#######################################################
# 🔹 Core AI Engine – TinyLlama w/ metrics
#######################################################
class CoreAI:
    def __init__(self, model_path):
        print("🚀 Loading TinyLlama model...")
        self.llm = Llama(model_path=model_path, n_ctx=2048, n_threads=6)
        print("✅ TinyLlama loaded successfully.")
        self.base_prompt = "You are AstroEdge AI, a futuristic astronaut mission assistant."
        self.chat_history = []
        self.metrics_log = []
        self.peak_cpu = 0
        self.peak_ram = 0

    def ask(self, user_query: str) -> tuple:
        """Ask LLM and log performance metrics."""
        start = time.time()
        cpu_before = psutil.cpu_percent()

        messages = [{"role": "system", "content": self.base_prompt}] + self.chat_history
        messages.append({"role": "user", "content": user_query})

        # Query TinyLlama
        response = self.llm.create_chat_completion(messages=messages, max_tokens=350, temperature=0.4)
        answer = response["choices"][0]["message"]["content"].strip()

        elapsed = round(time.time() - start, 2)
        cpu = psutil.cpu_percent()
        mem = round(psutil.Process(os.getpid()).memory_info().rss / (1024 * 1024), 2)

        # Track peak CPU/RAM
        self.peak_cpu = max(self.peak_cpu, cpu)
        self.peak_ram = max(self.peak_ram, mem)

        # Log metrics
        self.metrics_log.append({
            "timestamp": datetime.datetime.now().isoformat(),
            "query": user_query,
            "response": answer,
            "inference_time_sec": elapsed,
            "cpu_usage_%": cpu,
            "ram_usage_MB": mem
        })

        # Maintain history for contextual replies
        self.chat_history.append({"role": "user", "content": user_query})
        self.chat_history.append({"role": "assistant", "content": answer})

        return answer, elapsed, cpu, mem

    def save_metrics(self, filename="astroedge_metrics.csv"):
        """Save full metrics log as CSV."""
        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["timestamp", "query", "response", "inference_time_sec", "cpu_usage_%", "ram_usage_MB"])
            writer.writeheader()
            writer.writerows(self.metrics_log)
        print(f"✅ Metrics saved to {filename}")

    def export_json_log(self, filename="astroedge_log.json"):
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(self.metrics_log, f, indent=4)
        print(f"✅ JSON log saved to {filename}")

#######################################################
# 🔹 Voice System
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

    def toggle(self):
        self.voice_enabled = not self.voice_enabled
        return self.voice_enabled

#######################################################
# 🔹 GUI APP – AstroEdge Research Edition
#######################################################
class AstroEdgeApp:
    def __init__(self, model_path):
        self.ai = CoreAI(model_path)
        self.voice = VoiceSystem()
        self.vision = VisionModule()
        self.log_count = 0

        os.makedirs("logs", exist_ok=True)

        # 🖥 Window Setup
        self.root = tk.Tk()
        self.root.title("🚀 AstroEdge AI – Research Edition")
        self.root.geometry("1200x750")
        self.root.configure(bg="#0B0B15")

        # 🚀 Header
        header = tk.Label(self.root, text="🚀 ASTROEDGE RESEARCH EDITION",
                          font=("Orbitron", 24, "bold"), fg="cyan", bg="#141424", pady=15)
        header.grid(row=0, column=0, columnspan=3, sticky="ew")

        # 📊 Telemetry Dashboard
        self.telemetry = tk.Label(self.root, text="🛰 Mode: General | Logs: 0 | CPU: 0% | RAM: 0 MB | Peak CPU: 0% | Peak RAM: 0 MB",
                                  font=("Consolas", 10), fg="white", bg="#141424")
        self.telemetry.grid(row=1, column=0, columnspan=3, sticky="ew")

        # 📂 Mission Bar
        side_panel = tk.Frame(self.root, bg="#161622", width=240)
        side_panel.grid(row=2, column=0, rowspan=5, sticky="ns")
        tk.Label(side_panel, text="MISSION BAR", font=("Consolas", 12, "bold"), fg="white", bg="#161622").pack(pady=5)

        tk.Button(side_panel, text="🛠 Detect Objects", command=self.run_vision,
                  bg="orange", fg="black", font=("Consolas", 10, "bold")).pack(pady=5, fill="x")
        tk.Button(side_panel, text="🎙 Voice Input (stub)", command=self.voice_input_stub,
                  bg="purple", fg="white", font=("Consolas", 10, "bold")).pack(pady=5, fill="x")
        tk.Button(side_panel, text="💾 Export Research Logs", command=self.save_all_logs,
                  bg="gray", fg="white", font=("Consolas", 10, "bold")).pack(pady=5, fill="x")
        tk.Button(side_panel, text="🔄 Reset AI Memory", command=self.reset_ai,
                  bg="darkred", fg="white", font=("Consolas", 10, "bold")).pack(pady=5, fill="x")

        # 💬 Chat Window
        self.chat_display = scrolledtext.ScrolledText(self.root, bg="#1C1C28", fg="white",
                                                      font=("Consolas", 12), wrap="word", state=tk.DISABLED)
        self.chat_display.grid(row=2, column=1, columnspan=2, padx=10, pady=10, sticky="nsew")
        self._append_chat("🤖 AstroEdge: Research Edition online. Awaiting mission input.\n\n", "lightgreen")

        # Mode Selector
        selectors_frame = tk.Frame(self.root, bg="#0B0B15")
        selectors_frame.grid(row=3, column=1, columnspan=2, sticky="ew")
        tk.Label(selectors_frame, text="Mode:", fg="white", bg="#0B0B15", font=("Consolas", 11)).pack(side=tk.LEFT, padx=5)
        self.mode_var = tk.StringVar(value="General Assistance")
        mode_dropdown = ttk.Combobox(selectors_frame, textvariable=self.mode_var,
                                     values=["General Assistance", "Repairs", "Navigation", "Stress Management", "Mission Commander", "Mentor Mode"],
                                     font=("Consolas", 11), width=25)
        mode_dropdown.pack(side=tk.LEFT)
        mode_dropdown.bind("<<ComboboxSelected>>", self.change_mode)

        # Input Field + Buttons
        input_frame = tk.Frame(self.root, bg="#0B0B15")
        input_frame.grid(row=6, column=1, columnspan=2, pady=10, sticky="ew")

        self.entry = tk.Entry(input_frame, font=("Consolas", 12))
        self.entry.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.X, expand=True)
        self.entry.bind("<Return>", self.send_query)

        tk.Button(input_frame, text="Send", command=self.send_query, bg="green", fg="white",
                  font=("Consolas", 12, "bold")).pack(side=tk.LEFT, padx=5)
        tk.Button(input_frame, text="🗑 Clear", command=self.clear_chat, bg="red", fg="white",
                  font=("Consolas", 10, "bold")).pack(side=tk.LEFT, padx=5)

        self.voice_btn = tk.Button(input_frame, text="🔊 Voice: ON", command=self.toggle_voice, bg="blue", fg="white",
                                   font=("Consolas", 10, "bold"))
        self.voice_btn.pack(side=tk.LEFT, padx=5)

        # Layout Config
        self.root.grid_rowconfigure(2, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

        self.update_telemetry()

    #######################################################
    # 🌟 FUNCTIONS
    #######################################################
    def change_mode(self, event=None):
        new_mode = self.mode_var.get()
        self._append_chat(f"🛰 Mission mode changed to: {new_mode}\n\n", "yellow")

    def send_query(self, event=None):
        query = self.entry.get().strip()
        if not query:
            return
        self.entry.delete(0, tk.END)
        self._append_chat(f"👨‍🚀 Astronaut: {query}\n", "cyan")
        threading.Thread(target=self._get_ai_response, args=(query,), daemon=True).start()

    def _get_ai_response(self, query):
        answer, elapsed, cpu, mem = self.ai.ask(query)
        self.root.after(0, lambda: self._append_ai_answer(answer, elapsed, cpu, mem))

    def _append_chat(self, text, color):
        self.chat_display.configure(state=tk.NORMAL)
        self.chat_display.insert(tk.END, text)
        self.chat_display.tag_config(color, foreground=color)
        self.chat_display.tag_add(color, f"end-{len(text)}c", tk.END)
        self.chat_display.configure(state=tk.DISABLED)
        self.chat_display.see(tk.END)

    def _append_ai_answer(self, answer, elapsed, cpu, mem):
        self._append_chat(f"🤖 AstroEdge: {answer}\n⏱ {elapsed}s | 🖥 CPU {cpu}% | 🧠 {mem} MB\n\n", "lightgreen")
        self.voice.speak(answer)
        self.log_count += 1

    def clear_chat(self):
        self.chat_display.configure(state=tk.NORMAL)
        self.chat_display.delete(1.0, tk.END)
        self.chat_display.configure(state=tk.DISABLED)

    def toggle_voice(self):
        enabled = self.voice.toggle()
        self.voice_btn.config(text="🔊 Voice: ON" if enabled else "🔇 Voice: OFF")

    def run_vision(self):
        detection = self.vision.detect()
        log_path = "logs/yolo_detections.json"
        if not os.path.exists(log_path):
            json.dump([], open(log_path, "w"))
        detections = json.load(open(log_path))
        detections.append({"time": datetime.datetime.now().isoformat(), **detection})
        json.dump(detections, open(log_path, "w"), indent=4)
        self._append_chat(f"👁 YOLOv8 detected: {detection['object']} (conf {detection['confidence']})\n\n", "orange")

    def voice_input_stub(self):
        self._append_chat("🎙 Voice input stub triggered (future Whisper integration)\n\n", "magenta")

    def reset_ai(self):
        self.ai.chat_history.clear()
        self._append_chat("🧠 AI memory reset.\n\n", "red")

    def save_all_logs(self):
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        self.ai.save_metrics(f"logs/astroedge_metrics_{timestamp}.csv")
        self.ai.export_json_log(f"logs/astroedge_metrics_{timestamp}.json")
        messagebox.showinfo("Logs Saved", "✅ Metrics & logs saved for research use.")

    def update_telemetry(self):
        cpu = psutil.cpu_percent()
        mem = round(psutil.Process(os.getpid()).memory_info().rss / (1024 * 1024), 2)
        self.telemetry.config(
            text=f"🛰 Mode: {self.mode_var.get()} | Logs: {self.log_count} | CPU: {cpu}% | RAM: {mem} MB | Peak CPU: {self.ai.peak_cpu}% | Peak RAM: {self.ai.peak_ram} MB"
        )
        self.root.after(1000, self.update_telemetry)

    def run(self):
        self.root.mainloop()

class VoiceInput:
    def __init__(self):
        print("🎙 Loading Whisper model (tiny)…")
        self.model = whisper.load_model("tiny")

    def listen_and_transcribe(self, duration=5):
        """Records for X seconds & transcribes"""
        print("🎙 Listening...")
        audio = sd.rec(int(duration * 16000), samplerate=16000, channels=1, dtype='float32')
        sd.wait()
        print("✅ Recording complete. Transcribing...")
        result = self.model.transcribe(audio.flatten())
        return result["text"].strip()

#######################################################
# 🚀 RUN APP
#######################################################
if __name__ == "__main__":
    MODEL_PATH = r"C:\Hema\Contest\astro_edge_ai\tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf"
    app = AstroEdgeApp(MODEL_PATH)
    app.run()
