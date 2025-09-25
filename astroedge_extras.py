import datetime
import psutil
import matplotlib.pyplot as plt
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import random

#######################################################
# 🔹 System Health Monitor
#######################################################
class SystemHealth:
    def __init__(self):
        self.history = []

    def get_stats(self):
        cpu = psutil.cpu_percent()
        mem = psutil.virtual_memory().percent
        disk = psutil.disk_usage("/").percent
        stats = {
            "timestamp": datetime.datetime.now().isoformat(),
            "cpu": cpu,
            "memory": mem,
            "disk": disk
        }
        self.history.append(stats)
        return stats

    def plot_history(self):
        if not self.history:
            print("⚠️ No history to plot yet.")
            return
        times = [h["timestamp"][-8:] for h in self.history]
        cpu_vals = [h["cpu"] for h in self.history]
        mem_vals = [h["memory"] for h in self.history]
        disk_vals = [h["disk"] for h in self.history]

        plt.plot(times, cpu_vals, label="CPU %")
        plt.plot(times, mem_vals, label="Memory %")
        plt.plot(times, disk_vals, label="Disk %")
        plt.xticks(rotation=45)
        plt.legend()
        plt.tight_layout()
        plt.show()

#######################################################
# 🔹 Mission Report Generator
#######################################################
class MissionReport:
    def __init__(self, log_file=r"D:\astro_edge_ai\astro_edge_ai\logs\report\mission_report.pdf"):
        self.log_file = log_file
        self.styles = getSampleStyleSheet()

    def generate(self, metrics):
        doc = SimpleDocTemplate(self.log_file)
        story = []

        story.append(Paragraph("🚀 AstroEdge Mission Report", self.styles["Title"]))
        story.append(Spacer(1, 20))

        for entry in metrics:
            text = f"<b>Time:</b> {entry['timestamp']}<br/>" \
                   f"<b>Query:</b> {entry['query']}<br/>" \
                   f"<b>Response:</b> {entry['response']}<br/>" \
                   f"<b>Inference Time:</b> {entry['inference_time']}s<br/>" \
                   f"<b>Memory:</b> {entry['memory_MB']} MB"
            story.append(Paragraph(text, self.styles["Normal"]))
            story.append(Spacer(1, 15))

        doc.build(story)
        print(f"✅ Mission report saved as {self.log_file}")

#######################################################
# 🔹 Stress Relief (Fun Mode)
#######################################################
class StressRelief:
    def __init__(self):
        self.jokes = [
            "Why don’t astronauts get hungry after being blasted into space? Because they’ve just had a big launch!",
            "I asked the space engineer how they organize a party. They said: You planet!",
            "In space, you can’t cry... because there’s zero gravity for your tears!"
        ]
        self.quotes = [
            "Keep looking up! – Neil deGrasse Tyson",
            "That’s one small step for man, one giant leap for mankind. – Neil Armstrong",
            "The Earth is the cradle of humanity, but mankind cannot stay in the cradle forever. – Konstantin Tsiolkovsky"
        ]

    def random_joke(self):
        return random.choice(self.jokes)

    def random_quote(self):
        return random.choice(self.quotes)
