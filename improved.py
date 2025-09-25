import tkinter as tk
from tkinter import scrolledtext, ttk, messagebox
from llama_cpp import Llama
import pyttsx3, threading, time, datetime, json, csv, os, random, psutil
import speech_recognition as sr
import json
import queue
from astroedge_extras import SystemHealth, MissionReport, StressRelief
from hotword_listener import HotwordListener





#######################################################
# 🔹 YOLOv8 Vision Stub
#######################################################
class VisionModule:
    """Simulated YOLOv8 object detection for demo purposes."""
    def detect(self):
        objects = ["toolbox", "loose wire", "oxygen valve", "panel"]
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
        self.base_prompt = "You are AstroEdge AI, an astronaut assistant."
        self.chat_history = []
        self.metrics_log = []

    def ask(self, user_query: str) -> str:
        start = time.time()

        messages = [{"role": "system", "content": self.base_prompt}] + self.chat_history
        messages.append({"role": "user", "content": user_query})
        pass
        response = self.llm.create_chat_completion(
            messages=messages,
            max_tokens=350,
            temperature=0.45
        )
        answer = response["choices"][0]["message"]["content"].strip()

        elapsed = round(time.time() - start, 2)
        mem = round(psutil.Process(os.getpid()).memory_info().rss / (1024 * 1024), 2)

        self.metrics_log.append({
            "timestamp": datetime.datetime.now().isoformat(),
            "query": user_query,
            "response": answer,
            "inference_time": elapsed,
            "memory_MB": mem
        })

        self.chat_history.append({"role": "user", "content": user_query})
        self.chat_history.append({"role": "assistant", "content": answer})
        return answer, elapsed, mem

    def save_metrics(self, filename="astroedge_metrics.csv"):
        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["timestamp", "query", "response", "inference_time", "memory_MB"])
            writer.writeheader()
            writer.writerows(self.metrics_log)
        print(f"✅ Metrics saved to {filename}")

#######################################################
# 🔹 Voice System
#######################################################
class VoiceSystem:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 160)
        self.voice_enabled = True
        self.queue = queue.Queue()
        threading.Thread(target=self._run, daemon=True).start()

    def speak(self, text):
        if self.voice_enabled:
            self.queue.put(text)
            self.engine.say(text)
            self.engine.runAndWait()

    def toggle(self):
        self.voice_enabled = not self.voice_enabled
        return self.voice_enabled
    
    def _run(self):
        while True:
            text = self.queue.get()
            if text:
                self.engine.say(text)
                self.engine.runAndWait()
            self.queue.task_done()



class VoiceInput:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()

    def listen(self):
        with self.microphone as source:
            try:
                print("🎙 Adjusting for background noise...")
                self.recognizer.adjust_for_ambient_noise(source, duration=1)

                print("🎙 Listening... Speak now")
                audio = self.recognizer.listen(source, timeout=10, phrase_time_limit=10)

                print("🎙 Processing speech...")
                text = self.recognizer.recognize_google(audio)
                return text

            except sr.WaitTimeoutError:
                return "⚠️ No speech detected (timeout)."
            except sr.UnknownValueError:
                return "❌ Could not understand audio."
            except sr.RequestError as e:
                return f"❌ Speech recognition service unavailable: {e}"


"""class MemoryManager:
    def __init__(self, filename="astro_memory.json"):
        self.filename = filename
        self.memory = self.load_memory()

    def load_memory(self):
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_memory(self):
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(self.memory, f, indent=2, ensure_ascii=False)

    def add_message(self, role, content):
        self.memory.append({"role": role, "content": content})
        self.save_memory()

    def get_recent(self, limit=10):
        return self.memory[-limit:]  # get last N messages """

#######################################################
# 🔹 GUI APP – NextGen
#######################################################
class AstroEdgeApp:
    def __init__(self, model_path):
        self.ai = CoreAI(model_path)
        self.voice = VoiceSystem()
        self.vision = VisionModule()
        self.voice_input = VoiceInput()
        self.log_count = 0
        self.llm = Llama(model_path=MODEL_PATH)  # Load the GGUF model
       # self.memory = MemoryManager()
        self.engine = pyttsx3.init()
        self.health = SystemHealth()
        self.reporter = MissionReport()
        self.relief = StressRelief()
        # 🔹 Start Hotword Detection
       # self.hotword = HotwordListener(hotword="hello",callback=self.hotword_callback)
       # self.hotword.start()
       # 🔹 Start offline hotword listener
        self.hotword_listener = HotwordListener(
            hotword="hello",
            callback=self.hotword_callback,
            model_path=r"D:\astro_edge_ai\astro_edge_ai\models\vosk-model-small-en-us-0.15"
        )
        self.hotword_listener.start() 



        




        os.makedirs("logs", exist_ok=True)

        # 🖥 Window
        self.root = tk.Tk()
        self.root.title("🚀 AstroEdge AI – NextGen Mission Console")
        self.root.geometry("1150x720")
        self.root.configure(bg="#0A0A14")

        # 🚀 HEADER
        header = tk.Label(self.root, text="🚀 ASTROEDGE NEXTGEN MISSION CONTROL",
                          font=("Orbitron", 24, "bold"), fg="cyan", bg="#111122", pady=15)
        header.grid(row=0, column=0, columnspan=3, sticky="ew")

        # 📊 TELEMETRY PANEL
        self.telemetry = tk.Label(self.root, text="🛰 Mode: General | Logs: 0 | CPU: 0% | RAM: 0 MB",
                                  font=("Consolas", 10), fg="white", bg="#111122")
        self.telemetry.grid(row=1, column=0, columnspan=3, sticky="ew")

        # 📂 LEFT MISSION BAR
        side_panel = tk.Frame(self.root, bg="#161622", width=220)
        side_panel.grid(row=2, column=0, rowspan=4, sticky="ns")
        tk.Label(side_panel, text="MISSION BAR", font=("Consolas", 12, "bold"), fg="white", bg="#161622").pack(pady=5)
        tk.Button(side_panel, text="🎙 Voice Input", command=self.voice_input_command,
          bg="purple", fg="white", font=("Consolas", 10, "bold")).pack(pady=5, fill="x")


        tk.Button(side_panel, text="🛠 Detect Objects", command=self.run_vision,
                  bg="orange", fg="black", font=("Consolas", 10, "bold")).pack(pady=5, fill="x")
        tk.Button(side_panel, text="🎙 Voice Input", command=self.voice_input_command,
          bg="purple", fg="white", font=("Consolas", 10, "bold")).pack(pady=5, fill="x")
        tk.Button(side_panel, text="🔄 Reset AI", command=self.reset_ai,
                  bg="darkred", fg="white", font=("Consolas", 10, "bold")).pack(pady=5, fill="x")
        tk.Button(side_panel, text="💾 Save All Logs", command=self.save_all_logs,
                  bg="gray", fg="white", font=("Consolas", 10, "bold")).pack(pady=5, fill="x")
        tk.Button(side_panel, text="📊 System Health", command=self.show_health,
          bg="teal", fg="white", font=("Consolas", 10, "bold")).pack(pady=5, fill="x")

        tk.Button(side_panel, text="📄 Mission Report", command=self.save_report,
                bg="navy", fg="white", font=("Consolas", 10, "bold")).pack(pady=5, fill="x")

        tk.Button(side_panel, text="😂 Stress Relief", command=self.stress_relief,
                bg="darkgreen", fg="white", font=("Consolas", 10, "bold")).pack(pady=5, fill="x")


        # 💬 CHAT DISPLAY
        self.chat_display = scrolledtext.ScrolledText(self.root, bg="#1C1C28", fg="white",
                                                      font=("Consolas", 12), wrap="word", state=tk.DISABLED)
        self.chat_display.grid(row=2, column=1, columnspan=2, padx=10, pady=10, sticky="nsew")
        self._append_chat("🤖 AstroEdge: NextGen system ready. Awaiting mission input.\n\n", "lightgreen")

        # MODE SELECTOR
        selectors_frame = tk.Frame(self.root, bg="#0A0A14")
        selectors_frame.grid(row=3, column=1, columnspan=2, sticky="ew")
        tk.Label(selectors_frame, text="Mode:", fg="white", bg="#0A0A14", font=("Consolas", 11)).pack(side=tk.LEFT, padx=5)
        self.mode_var = tk.StringVar(value="General Assistance")
        mode_dropdown = ttk.Combobox(selectors_frame, textvariable=self.mode_var,
                                     values=["General Assistance", "Repairs", "Navigation", "Stress Management", "Mission Commander", "Mentor Mode"],
                                     font=("Consolas", 11), width=20)
        mode_dropdown.pack(side=tk.LEFT)
        mode_dropdown.bind("<<ComboboxSelected>>", self.change_mode)

        # INPUT FIELD
        input_frame = tk.Frame(self.root, bg="#0A0A14")
        input_frame.grid(row=5, column=1, columnspan=2, pady=10, sticky="ew")

        self.entry = tk.Entry(input_frame, font=("Consolas", 12))
        self.entry.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.X, expand=True)
        self.entry.bind("<Return>", self.send_query)

        # BUTTONS
        tk.Button(input_frame, text="Send", command=self.send_query, bg="green", fg="white",
                  font=("Consolas", 12, "bold")).pack(side=tk.LEFT, padx=5)
        tk.Button(input_frame, text="🗑 Clear", command=self.clear_chat, bg="red", fg="white",
                  font=("Consolas", 10, "bold")).pack(side=tk.LEFT, padx=5)

        self.voice_btn = tk.Button(input_frame, text="🔊 Voice: ON", command=self.toggle_voice, bg="blue", fg="white",
                                   font=("Consolas", 10, "bold"))
        self.voice_btn.pack(side=tk.LEFT, padx=5)

        # LAYOUT
        self.root.grid_rowconfigure(2, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

        # Telemetry updater
        self.update_telemetry()

    #######################################################
    # 🌟 FUNCTIONS
    #######################################################
    def change_mode(self, event=None):
        new_mode = self.mode_var.get()
        self._append_chat(f"🛰 Mission mode changed to: {new_mode}\n\n", "yellow")

    #def send_query(self, event=None):
     #   query = self.entry.get().strip()
      #  if not query:
       #     return
        #self.entry.delete(0, tk.END)
        #self._append_chat(f"👨‍🚀 Astronaut: {query}\n", "cyan")
        #threading.Thread(target=self._get_ai_response, args=(query,), daemon=True).start()

    """def send_query(self, event=None):
        query = self.entry.get().strip()
        if not query:
            return

        # show user input
        self._append_chat(f"👨‍🚀 You: {query}\n\n", "blue")
        self.entry.delete(0, tk.END)

        # store user query in memory
        self.memory.add_message("user", query)

        def _generate_response():
            try:
                self._append_chat("🤖 Thinking...\n\n", "green")

                # include memory context (last 10 messages)
                context = self.memory.get_recent(limit=10)
                messages = context + [{"role": "user", "content": query}]

                result = self.llm.create_chat_completion(
                    messages=messages,
                    max_tokens=256,
                    temperature=0.7
                )
                response = result["choices"][0]["message"]["content"].strip()

                # show assistant response
                self._append_chat(f"🤖 AstroEdge: {response}\n\n", "green")

                # store assistant reply in memory
                self.memory.add_message("assistant", response)

                # speak it
                self._speak(response)

            except Exception as e:
                self._append_chat(f"⚠️ Error during LLM call: {e}\n\n", "red")

        threading.Thread(target=_generate_response, daemon=True).start() """
    
    def send_query(self, event=None):
        query = self.entry.get().strip()
        if not query:
            return

        self._append_chat(f"👨‍🚀 Astronaut: {query}\n", "cyan")
        self.entry.delete(0, tk.END)

        def _run():
            # Show Thinking...
            self._append_chat("🤖 Thinking...\n", "gray")

            try:
                print("🟡 Sending query to LLM:", query)  # DEBUG
                result = self.llm(
                    query,
                    max_tokens=256,
                    temperature=0.7,
                    stop=["</s>"]
                )
                print("🟢 Raw LLM result:", result)       # DEBUG

                response = result["choices"][0]["text"].strip()
                if not response:
                    response = "⚠️ No response received."
            except Exception as e:
                print("🔴 Error during LLM call:", e)
                response = f"❌ Error: {e}"

            # Replace Thinking... with final response
            self.chat_area.config(state=tk.NORMAL)
            self.chat_area.delete("end-2l", "end-1l")
            self.chat_area.insert(tk.END, f"🤖 Assistant: {response}\n", "green")
            self.chat_area.config(state=tk.DISABLED)
            self.chat_area.yview(tk.END)

            self._speak(response)
        threading.Thread(target=self._get_ai_response, args=(query,), daemon=True).start()

    def _speak(self, text):
        #"""Speak response in background so multiple replies work."""
        def run_tts():
            try:
                self.engine.say(text)
                self.engine.runAndWait()
            except Exception as e:
                self._append_chat(f"⚠️ Speech error: {e}\n\n", "red")

        threading.Thread(target=run_tts, daemon=True).start()





    #def _get_ai_response(self, query):
     #   answer, elapsed, mem = self.ai.ask(query)
      #  self.root.after(0, lambda: self._append_ai_answer(answer, elapsed, mem))

    def _get_ai_response(self, query):
        # Show Thinking...
        self._append_chat("🤖 Thinking...\n", "gray")

        try:
            # Call CoreAI to generate response
            answer, elapsed, mem = self.ai.ask(query)

        except Exception as e:
            answer = f"❌ Error: {e}"
            elapsed = mem = 0

        # Replace "Thinking..." with the final answer
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.delete("end-2l", "end-1l")  # remove last line (Thinking...)
        self.chat_display.insert(tk.END, f"🤖 AstroEdge: {answer}\n⏱ {elapsed}s | 🧠 {mem} MB\n\n", "lightgreen")
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)

        # Play voice after displaying text
        self.voice.speak(answer)

        # Update log count
        self.log_count += 1


    def _append_chat(self, text, color):
        self.chat_display.configure(state=tk.NORMAL)
        self.chat_display.insert(tk.END, text)
        self.chat_display.tag_config(color, foreground=color)
        self.chat_display.tag_add(color, f"end-{len(text)}c", tk.END)
        self.chat_display.configure(state=tk.DISABLED)
        self.chat_display.see(tk.END)

    def _append_ai_answer(self, answer, elapsed, mem):
        self._append_chat(f"🤖 AstroEdge: {answer}\n⏱ {elapsed}s | 🧠 {mem} MB\n\n", "lightgreen")
        #self.voice.speak(answer)
        def delayed_speak():
            time.sleep(10)  # 4000ms delay
            # Speak reply afterwards
            self.voice.speak(answer)   # 👈 stays here
            self.log_count += 1

        #self.log_count += 1

        # 2️⃣ Then play audio in a separate thread (so GUI doesn’t freeze)
        threading.Thread(target=self.voice.speak, args=(answer,), daemon=True).start()
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
        self._append_chat(f"👁 YOLOv8 detected: {detection['object']} (conf {detection['confidence']})\n\n", "orange")

    def voice_input_command(self):
        def _listen_and_send():
            # Show "listening..." in chat
            self._append_chat("🎙 Listening... please speak\n\n", "magenta")

            query = self.voice_input.listen()

            # Remove the "listening..." text and show result
            if query.startswith("❌") or query.startswith("⚠️"):
                self._append_chat(query + "\n\n", "red")
            else:
                self._append_chat(f"👨‍🚀 Astronaut (via voice): {query}\n", "cyan")
                self.entry.delete(0, tk.END)
                self.entry.insert(0, query)
                self.send_query()  # send to AI

        threading.Thread(target=_listen_and_send, daemon=True).start()


    def reset_ai(self):
        self.ai.chat_history.clear()
        self._append_chat("🧠 AI memory reset.\n\n", "red")

    def save_all_logs(self):
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        self.ai.save_metrics(f"logs/astroedge_metrics_{timestamp}.csv")
        messagebox.showinfo("Logs Saved", "✅ Metrics and logs saved.")

    def update_telemetry(self):
        cpu = psutil.cpu_percent()
        mem = round(psutil.Process(os.getpid()).memory_info().rss / (1024 * 1024), 2)
        self.telemetry.config(text=f"🛰 Mode: {self.mode_var.get()} | Logs: {self.log_count} | CPU: {cpu}% | RAM: {mem} MB")
        self.root.after(1000, self.update_telemetry)

    def run(self):
        self.root.mainloop()

    def show_health(self):
        stats = self.health.get_stats()
        self._append_chat(f"📊 Health → CPU: {stats['cpu']}% | RAM: {stats['memory']}% | Disk: {stats['disk']}%\n\n", "yellow")

    def save_report(self):
        self.reporter.generate(self.ai.metrics_log)
        messagebox.showinfo("Mission Report", "✅ Report generated successfully.")

    def stress_relief(self):
        # Pick random joke or quote
        msg = random.choice([self.relief.random_joke(), self.relief.random_quote()])
        
        # 🔹 Show text immediately
        self._append_chat(f"🧘 {msg}\n\n", "magenta")
        
        # 🔹 Speak in background AFTER text is shown
        threading.Thread(target=self.voice.speak, args=(msg,), daemon=True).start()


    def hotword_callback(self):
        """Triggered when hotword is detected."""
        self._append_chat("🎙 Hotword detected! Listening...\n\n", "blue")
        self.voice_input_command()   # start voice input automatically

    





    

#######################################################
# 🚀 RUN APP
#######################################################
if __name__ == "__main__":
    MODEL_PATH = r"D:\astro_edge_ai\astro_edge_ai\tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf"
    app = AstroEdgeApp(MODEL_PATH)
    app.run()
