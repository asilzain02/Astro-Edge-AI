import tkinter as tk
from tkinter import scrolledtext, ttk, messagebox
from llama_cpp import Llama
import pyttsx3
import threading
import time
import datetime
import os

#######################################################
# 🔹 CORE AI ENGINE – TinyLlama with memory + modes
#######################################################
class CoreAI:
    def __init__(self, model_path):
        print("🚀 Loading TinyLlama model...")
        self.llm = Llama(model_path=model_path, n_ctx=2048, n_threads=6)
        print("✅ TinyLlama loaded successfully.")
        self.base_prompt = (
            "You are AstroEdge AI, an expert astronaut assistant. "
            "Always provide clear, step-by-step instructions for space operations. "
            "Use a calm, reassuring tone, and adapt style based on personality mode."
        )
        self.chat_history = []  
        self.mission_mode = "General Assistance"
        self.personality = "Neutral"

    def set_mode(self, mode):
        self.mission_mode = mode

    def set_personality(self, personality):
        self.personality = personality

    def ask(self, user_query: str) -> str:
        """Send astronaut query to TinyLlama with context + mode"""
        system_prompt = f"{self.base_prompt} Current mission mode: {self.mission_mode}. Personality: {self.personality}."
        messages = [{"role": "system", "content": system_prompt}] + self.chat_history
        messages.append({"role": "user", "content": user_query})

        response = self.llm.create_chat_completion(
            messages=messages,
            max_tokens=350,
            temperature=0.45
        )

        answer = response["choices"][0]["message"]["content"].strip()
        self.chat_history.append({"role": "user", "content": user_query})
        self.chat_history.append({"role": "assistant", "content": answer})
        return answer

    def reset_memory(self):
        """Clear chat history for a fresh start"""
        self.chat_history.clear()

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

    def toggle(self):
        self.voice_enabled = not self.voice_enabled
        return self.voice_enabled

#######################################################
# 🔹 GUI APP – FUTURISTIC EDITION
#######################################################
class AstroEdgeApp:
    def __init__(self, model_path):
        self.ai = CoreAI(model_path)
        self.voice = VoiceSystem()
        self.log_count = 0

        # Ensure log folder exists
        os.makedirs("logs", exist_ok=True)

        # 🖥 Main Window
        self.root = tk.Tk()
        self.root.title("🚀 AstroEdge AI – Astronaut Assistant")
        self.root.geometry("1080x700")
        self.root.configure(bg="#0A0A14")

        # 🚀 HEADER
        header = tk.Label(self.root, text="🚀 ASTROEDGE AI MISSION COMMAND",
                          font=("Orbitron", 24, "bold"), fg="cyan", bg="#111122", pady=15)
        header.grid(row=0, column=0, columnspan=3, sticky="ew")

        # 📊 MISSION STATUS HUD
        self.dashboard = tk.Label(self.root, text="🛰 Mode: General Assistance | Logs: 0 | Last Reply: — | Personality: Neutral",
                                  font=("Consolas", 10), fg="white", bg="#111122", pady=5)
        self.dashboard.grid(row=1, column=0, columnspan=3, sticky="ew")

        # 📂 LEFT MISSION PANEL
        mission_panel = tk.Frame(self.root, bg="#161622", width=200)
        mission_panel.grid(row=2, column=0, rowspan=4, sticky="ns")
        tk.Label(mission_panel, text="MISSION PANEL", font=("Consolas", 12, "bold"), fg="white", bg="#161622").pack(pady=5)

        # Quick actions in mission panel
        tk.Button(mission_panel, text="🛠 Emergency Repair", command=lambda: self.send_quick("Emergency repair protocol"),
                  bg="orange", fg="black", font=("Consolas", 10, "bold")).pack(pady=5, fill="x")
        tk.Button(mission_panel, text="🛰 Navigation", command=lambda: self.send_quick("Navigation assistance"),
                  bg="purple", fg="white", font=("Consolas", 10, "bold")).pack(pady=5, fill="x")
        tk.Button(mission_panel, text="🧘 Stress Relief", command=lambda: self.send_quick("Stress relief exercise"),
                  bg="teal", fg="white", font=("Consolas", 10, "bold")).pack(pady=5, fill="x")
        tk.Button(mission_panel, text="🔄 Reset Memory", command=self.reset_ai,
                  bg="darkred", fg="white", font=("Consolas", 10, "bold")).pack(pady=5, fill="x")
        tk.Button(mission_panel, text="💾 Export Log", command=self.save_log,
                  bg="gray", fg="white", font=("Consolas", 10, "bold")).pack(pady=5, fill="x")
        tk.Button(mission_panel, text="🛑 Emergency Shutdown", command=self.shutdown,
                  bg="red", fg="white", font=("Consolas", 10, "bold")).pack(pady=5, fill="x")

        # 💬 CHAT DISPLAY
        self.chat_display = scrolledtext.ScrolledText(self.root, bg="#1C1C28", fg="white",
                                                      font=("Consolas", 12), wrap="word", state=tk.DISABLED)
        self.chat_display.grid(row=2, column=1, columnspan=2, padx=10, pady=10, sticky="nsew")
        self._append_chat("🤖 AstroEdge: System online. Ready for your questions, astronaut.\n\n", "lightgreen")

        # MODE + PERSONALITY SELECTORS
        selectors_frame = tk.Frame(self.root, bg="#0A0A14")
        selectors_frame.grid(row=3, column=1, columnspan=2, sticky="ew", pady=5)

        tk.Label(selectors_frame, text="Mission Mode:", fg="white", bg="#0A0A14", font=("Consolas", 11)).pack(side=tk.LEFT, padx=5)
        self.mode_var = tk.StringVar(value="General Assistance")
        mode_dropdown = ttk.Combobox(selectors_frame, textvariable=self.mode_var,
                                     values=["General Assistance", "Repairs", "Navigation", "Stress Management"],
                                     font=("Consolas", 11), width=20)
        mode_dropdown.pack(side=tk.LEFT)
        mode_dropdown.bind("<<ComboboxSelected>>", self.change_mode)

        tk.Label(selectors_frame, text="Personality:", fg="white", bg="#0A0A14", font=("Consolas", 11)).pack(side=tk.LEFT, padx=10)
        self.personality_var = tk.StringVar(value="Neutral")
        personality_dropdown = ttk.Combobox(selectors_frame, textvariable=self.personality_var,
                                            values=["Neutral", "Humorous", "Strict NASA Protocol", "Friendly"],
                                            font=("Consolas", 11), width=20)
        personality_dropdown.pack(side=tk.LEFT)
        personality_dropdown.bind("<<ComboboxSelected>>", self.change_personality)

        # INPUT FRAME
        input_frame = tk.Frame(self.root, bg="#0A0A14")
        input_frame.grid(row=5, column=1, columnspan=2, pady=10, sticky="ew")

        self.entry = tk.Entry(input_frame, font=("Consolas", 12))
        self.entry.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.X, expand=True)
        self.entry.bind("<Return>", self.send_query)

        # BUTTONS
        tk.Button(input_frame, text="Send", command=self.send_query, bg="green", fg="white",
                  font=("Consolas", 12, "bold")).pack(side=tk.LEFT, padx=5)
        self.voice_btn = tk.Button(input_frame, text="🔊 Voice: ON", command=self.toggle_voice, bg="blue", fg="white",
                                   font=("Consolas", 10, "bold"))
        self.voice_btn.pack(side=tk.LEFT, padx=5)
        tk.Button(input_frame, text="🗑 Clear Chat", command=self.clear_chat, bg="red", fg="white",
                  font=("Consolas", 10, "bold")).pack(side=tk.LEFT, padx=5)

        # TYPING INDICATOR
        self.typing_label = tk.Label(self.root, text="", bg="#0A0A14", fg="yellow", font=("Consolas", 11))
        self.typing_label.grid(row=6, column=1, columnspan=2)

        # Layout scaling
        self.root.grid_rowconfigure(2, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

    #######################################################
    # 🌟 FUNCTIONS
    #######################################################
    def change_mode(self, event=None):
        new_mode = self.mode_var.get()
        self.ai.set_mode(new_mode)
        self._append_chat(f"🛰 Mission mode changed to: {new_mode}\n\n", "yellow")
        self._update_dashboard()

    def change_personality(self, event=None):
        new_personality = self.personality_var.get()
        self.ai.set_personality(new_personality)
        self._append_chat(f"🎭 Personality changed to: {new_personality}\n\n", "orange")
        self._update_dashboard()

    def toggle_voice(self):
        enabled = self.voice.toggle()
        self.voice_btn.config(text="🔊 Voice: ON" if enabled else "🔇 Voice: OFF")

    def send_query(self, event=None):
        query = self.entry.get().strip()
        if not query:
            return
        self.entry.delete(0, tk.END)
        self._append_chat(f"👨‍🚀 Astronaut: {query}\n", "cyan")
        self._start_typing_animation()
        threading.Thread(target=self._get_ai_response, args=(query,), daemon=True).start()

    def send_quick(self, command):
        self._append_chat(f"👨‍🚀 Astronaut (Quick): {command}\n", "cyan")
        self._start_typing_animation()
        threading.Thread(target=self._get_ai_response, args=(command,), daemon=True).start()

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
        self.typing_label.config(text="")
        self.voice.speak(answer)
        self.log_count += 1
        self._update_dashboard()

    def _start_typing_animation(self):
        def animate():
            dots = ""
            while True:
                dots += "."
                if len(dots) > 3:
                    dots = ""
                self.typing_label.config(text=f"🤖 AstroEdge is thinking{dots}")
                time.sleep(0.4)
        threading.Thread(target=animate, daemon=True).start()

    def reset_ai(self):
        self.ai.reset_memory()
        self._append_chat("🧠 AI memory has been reset. Fresh start!\n\n", "red")

    def clear_chat(self):
        if messagebox.askyesno("Clear Chat", "Are you sure you want to clear the chat?"):
            self.chat_display.configure(state=tk.NORMAL)
            self.chat_display.delete(1.0, tk.END)
            self.chat_display.configure(state=tk.DISABLED)

    def save_log(self):
        filename = f"logs/mission_log_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(filename, "w", encoding="utf-8") as f:
            for msg in self.ai.chat_history:
                f.write(f"{msg['role'].capitalize()}: {msg['content']}\n\n")
        messagebox.showinfo("Log Saved", f"Mission log saved as {filename}")

    def shutdown(self):
        if messagebox.askyesno("Emergency Shutdown", "Shut down AstroEdge AI now?"):
            self.root.destroy()

    def _update_dashboard(self):
        last_time = datetime.datetime.now().strftime('%H:%M:%S')
        self.dashboard.config(text=f"🛰 Mode: {self.ai.mission_mode} | Logs: {self.log_count} | Last Reply: {last_time} | Personality: {self.ai.personality}")

    def run(self):
        self.root.mainloop()

#######################################################
# 🚀 RUN APP
#######################################################
if __name__ == "__main__":
    MODEL_PATH = r"C:\Hema\Contest\astro_edge_ai\tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf"
    app = AstroEdgeApp(MODEL_PATH)
    app.run()
