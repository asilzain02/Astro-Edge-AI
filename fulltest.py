import os, time, csv, json, random, psutil, statistics
from datetime import datetime
import matplotlib.pyplot as plt
from fpdf import FPDF
from llama_cpp import Llama

#######################################################
# 🔹 YOLOv8 Vision Stub (Simulated for Research)
#######################################################
class VisionModule:
    def detect(self):
        objects = ["toolbox", "loose wire", "oxygen valve", "panel", "astronaut glove", "solar panel"]
        detection = random.choice(objects)
        confidence = round(random.uniform(0.75, 0.99), 2)
        return {"object": detection, "confidence": confidence}

#######################################################
# 🔹 Core AI Engine – TinyLLaMA with Safe Context Handling
#######################################################
class CoreAI:
    def __init__(self, model_path):
        print("🚀 Loading TinyLLaMA model for research...")
        self.llm = Llama(model_path=model_path, n_ctx=2048, n_threads=6)
        print("✅ TinyLLaMA loaded successfully.")
        self.base_prompt = "You are AstroEdge AI, a futuristic astronaut mission assistant."
        self.chat_history = []
        self.metrics_log = []
        self.peak_cpu = 0
        self.peak_ram = 0

    def ask(self, user_query: str, temperature=0.4):
        start = time.time()
        # ✅ Reset history if context gets too long
        if len(self.chat_history) > 50:
            self.chat_history = []

        messages = [{"role": "system", "content": self.base_prompt}] + self.chat_history
        messages.append({"role": "user", "content": user_query})

        response = self.llm.create_chat_completion(
            messages=messages,
            max_tokens=300,
            temperature=temperature
        )
        answer = response["choices"][0]["message"]["content"].strip()

        elapsed = round(time.time() - start, 2)
        cpu = psutil.cpu_percent()
        mem = round(psutil.Process(os.getpid()).memory_info().rss / (1024 * 1024), 2)

        self.peak_cpu = max(self.peak_cpu, cpu)
        self.peak_ram = max(self.peak_ram, mem)

        self.metrics_log.append({
            "timestamp": datetime.now().isoformat(),
            "query": user_query,
            "response": answer,
            "temperature": temperature,
            "inference_time_sec": elapsed,
            "cpu_usage_%": cpu,
            "ram_usage_MB": mem
        })

        self.chat_history.append({"role": "user", "content": user_query})
        self.chat_history.append({"role": "assistant", "content": answer})

        return answer, elapsed, cpu, mem

    def save_metrics_csv(self, filename):
        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["timestamp", "query", "response", "temperature", "inference_time_sec", "cpu_usage_%", "ram_usage_MB"])
            writer.writeheader()
            writer.writerows(self.metrics_log)
        print(f"✅ Metrics saved to {filename}")

#######################################################
# 🔹 Research Test Harness with Safety for Context
#######################################################
def run_full_research(ai: CoreAI):
    os.makedirs("logs", exist_ok=True)
    print("\n🚀 Starting EXTENSIVE Research Testing...")

    test_queries = [
        "How do I repair an oxygen leak?",
        "Give me a checklist for spacecraft re-entry.",
        "How to stabilize rotation in zero gravity?",
        "What is the emergency protocol for fire onboard?",
        "Explain how to realign the satellite dish.",
        "Summarize Apollo 13 mission in 3 bullet points.",
        "Write a motivational speech for astronauts facing an emergency.",
        "Generate a 5-step plan for solar panel repair.",
        "How to manage stress in long-term space missions?",
        "Explain orbital mechanics simply."
    ]

    # Add stress tests to measure performance
    for i in range(1, 51):
        test_queries.append(f"Stress test query #{i}: Describe step {i} of spacewalk safety.")

    for temp in [0.2, 0.4, 0.7]:
        for query in test_queries:
            try:
                answer, elapsed, cpu, mem = ai.ask(query, temperature=temp)
                print(f"🛰 {query[:30]}... | ⏱ {elapsed}s | 🖥 CPU {cpu}% | 🧠 {mem} MB | Temp: {temp}")
            except ValueError as e:
                print(f"⚠️ Skipping query due to context overflow: {query[:30]}...")
                ai.chat_history = []  # reset history if overflow

    csv_file = f"logs/astroedge_research_metrics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    ai.save_metrics_csv(csv_file)

    create_graphs(ai.metrics_log)
    export_pdf_report(ai.metrics_log, csv_file)
    print("\n✅ Research Testing Complete. CSV, Graphs, and PDF generated.")

#######################################################
# 🔹 Graph Generation for Paper
#######################################################
def create_graphs(metrics_log):
    times = [m["inference_time_sec"] for m in metrics_log]
    cpu = [m["cpu_usage_%"] for m in metrics_log]
    ram = [m["ram_usage_MB"] for m in metrics_log]

    plt.figure(figsize=(12, 8))

    plt.subplot(3, 1, 1)
    plt.plot(times, label="Inference Time (s)", color="blue")
    plt.legend()
    plt.grid(True)

    plt.subplot(3, 1, 2)
    plt.plot(cpu, label="CPU Usage (%)", color="red")
    plt.legend()
    plt.grid(True)

    plt.subplot(3, 1, 3)
    plt.plot(ram, label="RAM Usage (MB)", color="green")
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.savefig("logs/research_metrics_graphs.png")
    plt.close()
    print("📊 Saved research graphs as logs/research_metrics_graphs.png")

#######################################################
# 🔹 PDF REPORT GENERATION FOR PAPER
#######################################################
def export_pdf_report(metrics_log, csv_file):
    times = [m["inference_time_sec"] for m in metrics_log]
    cpu = [m["cpu_usage_%"] for m in metrics_log]
    ram = [m["ram_usage_MB"] for m in metrics_log]

    mean_time = statistics.mean(times)
    mean_cpu = statistics.mean(cpu)
    mean_ram = statistics.mean(ram)

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, "AstroEdge Research Report", ln=True, align="C")

    pdf.set_font("Arial", size=12)
    pdf.ln(10)
    pdf.multi_cell(0, 10, f"This report summarizes the performance testing of AstroEdge AI using TinyLLaMA model.\n\n"
                             f"Queries tested: {len(metrics_log)}\n"
                             f"Average Inference Time: {mean_time:.2f}s\n"
                             f"Average CPU Usage: {mean_cpu:.2f}%\n"
                             f"Average RAM Usage: {mean_ram:.2f}MB\n"
                             f"Peak CPU Usage: {max(cpu)}%\n"
                             f"Peak RAM Usage: {max(ram)}MB")

    pdf.ln(10)
    pdf.image("logs/research_metrics_graphs.png", x=10, w=180)

    pdf.ln(10)
    pdf.set_font("Arial", "I", 10)
    pdf.multi_cell(0, 10, f"Raw CSV Data: {csv_file}")

    pdf.output("logs/astroedge_research_report.pdf")
    print("📄 PDF research report created: logs/astroedge_research_report.pdf")

#######################################################
# 🚀 RUN FULL RESEARCH TESTING
#######################################################
if __name__ == "__main__":
    MODEL_PATH = r"C:\\Hema\\Contest\\astro_edge_ai\\tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf"
    ai = CoreAI(MODEL_PATH)
    run_full_research(ai)
