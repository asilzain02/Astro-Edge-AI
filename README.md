🚀 AstroEdge AI – NextGen Mission Console

An AI-powered astronaut assistant built with TinyLlama (GGUF model), Tkinter GUI, Voice Interaction, YOLOv8 Vision Stub, and System Health Monitoring.
AstroEdge AI is designed as a mission control console to assist astronauts with navigation, repairs, stress management, and real-time decision support.

🌟 Features

🧠 Core AI (TinyLlama)

Runs offline using llama.cpp GGUF models.

Tracks inference time and memory usage.

Saves AI interaction metrics in CSV logs.

🎙 Voice Assistant

Speech-to-Text with SpeechRecognition.

Text-to-Speech with pyttsx3.

Toggleable voice feedback.

👁 YOLOv8 Vision Stub

Simulated object detection (toolbox, oxygen valve, etc.).

Returns random detections with confidence levels.

📊 System Health Monitor

Monitors CPU, RAM, and Disk usage using psutil.

Displays telemetry panel in real time.

📝 Mission Reports

Generates structured reports from AI logs.

Stores logs as .csv in /logs.

🧘 Stress Relief Mode

Random motivational quotes and jokes.

Supports voice playback for morale boost.

🔥 Hotword Detection (Offline)

Uses Vosk model for real-time hotword listening.

Automatically activates voice assistant when hotword detected.

🖥 Tkinter GUI Console

Chat interface with scrollable history.

Side mission bar with quick actions.

Multiple mission modes: General, Repairs, Navigation, Stress Management, Mission Commander, Mentor Mode.

🛠 Tech Stack

Python 3.10+

Tkinter (GUI)

llama-cpp-python (LLM inference)

SpeechRecognition (Voice input)

pyttsx3 (Voice output)

psutil (System stats)

Vosk (Hotword detection)

Custom Modules:

astroedge_extras.SystemHealth

astroedge_extras.MissionReport

astroedge_extras.StressRelief

hotword_listener.HotwordListener

📂 Project Structure

<img width="838" height="334" alt="image" src="https://github.com/user-attachments/assets/6e05f807-fde9-4575-8237-344f6deb94a7" />


⚡ Installation
1️⃣ Clone Repository
git clone https://github.com/asilzain02/Astro-Edge-AI.git

cd Astro-Edge-AI


2️⃣ Install Dependencies
pip install -r requirements.txt


requirements.txt

tk
llama-cpp-python
pyttsx3
SpeechRecognition
psutil
vosk

3️⃣ Download Models

TinyLlama GGUF Model: HuggingFace

Vosk English Model: Vosk Models

Place them inside /models/.

🚀 Run the App
python astroedge_main.py


The console will launch with:

Real-time telemetry

Chat + voice assistant

Object detection stub

Stress management features

📊 Example Screens

Main GUI: AI mission control panel

Telemetry Updates: CPU / RAM usage in real time

Voice Commands: Hotword → speech recognition → AI response

📌 Future Improvements

✅ Replace YOLOv8 stub with real detection.

✅ Integrate camera feed for astronaut environment scanning.

✅ Add persistent memory system (JSON / vector DB).

✅ Deploy lightweight version on Raspberry Pi / Jetson Nano.

👨‍🚀 Author

Developed by Asil Zain 🚀
Contributions welcome!
