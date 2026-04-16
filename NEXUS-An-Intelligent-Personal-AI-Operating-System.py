import cmd
import os
import time
import math
from turtle import listen
import zipfile
import threading
import tkinter as tk
from tkinter import ttk, filedialog, simpledialog, messagebox
from datetime import datetime
import webbrowser
import tkinter as tk
import math
from reportlab.lib.pagesizes import A4
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime
import mysql.connector
from datetime import datetime 
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.platypus import HRFlowable
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
import subprocess
import sys
from queue import Queue
import threading
try:
    import pyttsx3
except:
    pyttsx3 = None


from queue import Queue

# Optional libs
try:
    import psutil
except:
    psutil = None

try:
    import requests
except:
    requests = None

try:
    import feedparser
except:
    feedparser = None

try:
    import pyautogui
except:
    pyautogui = None

try:
    import pyttsx3
except:
    pyttsx3 = None

try:
    import speech_recognition as sr
except:
    sr = None


CITY_WEATHER = "Solapur"
SUMMARY_FILE = "NEXUS_ACTIVITY_SUMMARY.txt"


# ==========================================================
# ✅ TOAST NOTIFICATION SYSTEM
# ==========================================================
class Toast:
    def __init__(self, root):
        self.root = root
        self.active = []

    def show(self, title, msg, kind="info", duration=2600):
        colors = {
            "success": "#22c55e",
            "warning": "#facc15",
            "error": "#ef4444",
            "info": "#38bdf8"
        }

        color = colors.get(kind, "#38bdf8")

        win = tk.Toplevel(self.root)
        win.overrideredirect(True)
        win.attributes("-topmost", True)
        win.configure(bg="#0b1220")

        sw = win.winfo_screenwidth()
        w, h = 520, 110
        x = (sw // 2) - (w // 2)
        y = 18 + len(self.active) * (h + 10)
        win.geometry(f"{w}x{h}+{x}+{y}")

        outer = tk.Frame(win, bg="#0b1220")
        outer.pack(fill="both", expand=True)
        tk.Frame(outer, bg=color, width=10).pack(side="left", fill="y")

        body = tk.Frame(outer, bg="#0b1220")
        body.pack(side="left", fill="both", expand=True, padx=12, pady=10)

        tk.Label(body, text=title, fg="white", bg="#0b1220",
                 font=("Segoe UI", 12, "bold")).pack(anchor="w")

        tk.Label(body, text=msg, fg="#cbd5e1", bg="#0b1220",
                 font=("Segoe UI", 10), wraplength=410,
                 justify="left").pack(anchor="w")

        self.active.append(win)

        # 🔥 This now works because close() exists
        win.after(duration, lambda: self.close(win))

    # ✅ ADD THIS METHOD
    def close(self, win):
        if win in self.active:
            self.active.remove(win)
        win.destroy()

# ==========================================================
# ✅ FINAL NEXUS LOGO (Perfect Wave Alignment Version)
# ==========================================================

class NexusHomeLogo(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#f2f2f2")

        self.canvas = tk.Canvas(self, bg="#f2f2f2", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        # Wave settings
        self.wave_length = 430
        self.amplitude = 70
        self.lines = 22
        self.speed = 0.02
        self.phase = 0

        self.wave_items = []
        for _ in range(self.lines):
            line = self.canvas.create_line(
                0, 0, 0, 0,
                fill="#2f65a7",
                width=3,
                capstyle=tk.ROUND
            )
            self.wave_items.append(line)

        # TITLE
        self.title = self.canvas.create_text(
            0, 0,
            text="NEXUS",
            fill="black",
            font=("Segoe UI", 54, "bold")
        )



        # SUBTITLE
        self.subtitle = self.canvas.create_text(
            0, 0,
            text="AI PERSONAL OPERATING SYSTEM",
            fill="#444",
            font=("Segoe UI", 20, "bold")
        )

        # TAGLINE
        self.tagline = self.canvas.create_text(
            0, 0,
            text="Think it. Say it. NEXUS does it.",
            fill="#2f65a7",
            font=("Segoe UI", 16, "bold")
        )

        self.bind("<Configure>", self._on_resize)
        self.animate()

    def _on_resize(self, event=None):
        self.update_layout()

    def update_layout(self):
        w = self.winfo_width()
        h = self.winfo_height()

        self.center_x = w // 2
        self.center_y = h // 2 - 40

        # Position text
        self.canvas.coords(self.title, self.center_x, self.center_y + 140)
        self.canvas.coords(self.subtitle, self.center_x, self.center_y + 190)
        self.canvas.coords(self.tagline, self.center_x, self.center_y + 230)

    def animate(self):
        w = self.winfo_width()
        h = self.winfo_height()

        center_x = w // 2
        center_y = h // 2 - 180

        for i, line in enumerate(self.wave_items):
            points = []
            offset = (i - self.lines / 2) * 4

            for x in range(-self.wave_length, self.wave_length, 10):
                y = (
                    math.sin((x / 70) + self.phase + i * 0.18)
                    * self.amplitude
                    * math.exp(-abs(x) / 320)
                )
                points.extend([center_x + x, center_y + y + offset])

            self.canvas.coords(line, *points)

        self.phase += self.speed
        self.after(30, self.animate)



# ==========================================================
# ✅ SECURITY DASHBOARD
# ==========================================================
class SecurityDashboard(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#061824")

        self.cpu_var = tk.StringVar(value="0%")
        self.ram_var = tk.StringVar(value="0%")
        self.disk_var = tk.StringVar(value="0%")
        self.batt_var = tk.StringVar(value="N/A")

        header = tk.Frame(self, bg="#04121b", height=70)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(header, text="🛡️ SECURITY MONITORING DASHBOARD",
                 fg="white", bg="#04121b",
                 font=("Segoe UI", 16, "bold")).pack(side="left", padx=25)

        self.status_lbl = tk.Label(header, text="Status: OFF",
                                   fg="#ef4444", bg="#04121b",
                                   font=("Segoe UI", 12, "bold"))
        self.status_lbl.pack(side="right", padx=25)

        cards = tk.Frame(self, bg="#061824")
        cards.pack(fill="x", padx=25, pady=25)

        self.card(cards, "CPU", self.cpu_var, "#38bdf8")
        self.card(cards, "RAM", self.ram_var, "#a78bfa")
        self.card(cards, "DISK", self.disk_var, "#fb7185")
        self.card(cards, "BATTERY", self.batt_var, "#facc15")

        self.activity = tk.Listbox(self, bg="#0b1220", fg="white",
                                   font=("Consolas", 11),
                                   bd=0, highlightthickness=0)
        self.activity.pack(fill="both", expand=True, padx=25, pady=10)

        self.stop_btn = ttk.Button(self, text="⛔ Stop Monitoring")
        self.stop_btn.pack(pady=18)

    def card(self, parent, title, var, color):
        c = tk.Frame(parent, bg="#04121b", width=230, height=92)
        c.pack(side="left", padx=10)
        c.pack_propagate(False)
        tk.Label(c, text=title, fg=color, bg="#04121b",
                 font=("Segoe UI", 11, "bold")).pack(anchor="w", padx=12, pady=(10, 0))
        tk.Label(c, textvariable=var, fg="white", bg="#04121b",
                 font=("Segoe UI", 20, "bold")).pack(anchor="w", padx=12)

    def set_status(self, on=True):
        if on:
            self.status_lbl.config(text="Status: ON", fg="#22c55e")
        else:
            self.status_lbl.config(text="Status: OFF", fg="#ef4444")

    def update_stats(self, cpu, ram, disk, batt):
        self.cpu_var.set(f"{cpu:.1f}%")
        self.ram_var.set(f"{ram:.1f}%")
        self.disk_var.set(f"{disk:.1f}%")
        self.batt_var.set(batt)

    def add_activity(self, msg):
        self.activity.insert(tk.END, msg)
        self.activity.yview_moveto(1)


# ==========================================================
# ✅ STUDY MODE PAGE
# ==========================================================
class StudyModePage(tk.Frame):
    def __init__(self, parent, exit_callback):
        super().__init__(parent, bg="#020617")
        tk.Label(self, text="📚 STUDY MODE ACTIVE",
                 fg="#facc15", bg="#020617",
                 font=("Segoe UI", 34, "bold")).pack(pady=80)

        ttk.Button(self, text="✅ Stop Study Mode (Exit)", command=exit_callback).pack(pady=40)
        tk.Label(self, text="Tip: Press ESC anytime to exit Study Mode",
                 fg="#94a3b8", bg="#020617", font=("Segoe UI", 12)).pack(pady=10)


# ==========================================================
# ✅ NEWS PAGE
# ==========================================================
class NewsPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#071427")
        tk.Label(self, text="📰 NEXUS LATEST NEWS",
                 fg="white", bg="#071427",
                 font=("Segoe UI", 26, "bold")).pack(pady=18)

        box = tk.Frame(self, bg="#071427")
        box.pack(fill="both", expand=True, padx=35, pady=10)

        self.canvas = tk.Canvas(box, bg="#0b1220", highlightthickness=0)
        self.scroll = ttk.Scrollbar(box, orient="vertical", command=self.canvas.yview)
        self.scroll.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        self.canvas.configure(yscrollcommand=self.scroll.set)
        self.inner = tk.Frame(self.canvas, bg="#0b1220")
        self.canvas.create_window((0, 0), window=self.inner, anchor="nw")
        self.inner.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

    def clear(self):
        for w in self.inner.winfo_children():
            w.destroy()

    def add_card(self, title, source, link, published):
        card = tk.Frame(self.inner, bg="#111827", padx=15, pady=12)
        card.pack(fill="x", padx=15, pady=10)
        tk.Label(card, text=title, fg="white", bg="#111827",
                 font=("Segoe UI", 12, "bold"),
                 wraplength=950, justify="left").pack(anchor="w")
        tk.Label(card, text=f"{source}  •  {published}",
                 fg="#94a3b8", bg="#111827", font=("Segoe UI", 10)).pack(anchor="w", pady=5)
        ttk.Button(card, text="Read Full News", command=lambda: webbrowser.open(link)).pack(anchor="w")



# ==========================================================
# ✅ MAIN NEXUS FULL SYSTEM
# ==========================================================
class NexusFinalSystem:
    def __init__(self):
        self.study_mode = False
        self.monitoring = False
       

        # Voice engine
        self.engine = None
        self.speech_queue = Queue()
        if pyttsx3:
            self.engine = pyttsx3.init()
            self.engine.setProperty("rate", 170)
            threading.Thread(target=self._speech_worker, daemon=True).start()

        # UI
        self.root = tk.Tk()
        self.root.title("NEXUS - FINAL ALL WORKING")
        self.root.state("zoomed")

        self.toast = Toast(self.root)
        self.root.nexus_instance = self

        # Wrap tkinter messagebox functions to speak their messages via Nexus
        try:
            import tkinter.messagebox as _tk_messagebox

            self._orig_messagebox_showinfo = _tk_messagebox.showinfo
            self._orig_messagebox_showwarning = _tk_messagebox.showwarning
            self._orig_messagebox_showerror = _tk_messagebox.showerror

            def _speak_and_showinfo(title, msg, *a, **k):
                try:
                    self.say_and_log(f"{title}. {msg}")
                except:
                    pass
                return self._orig_messagebox_showinfo(title, msg, *a, **k)

            def _speak_and_showwarning(title, msg, *a, **k):
                try:
                    self.say_and_log(f"{title}. {msg}")
                except:
                    pass
                return self._orig_messagebox_showwarning(title, msg, *a, **k)

            def _speak_and_showerror(title, msg, *a, **k):
                try:
                    self.say_and_log(f"{title}. {msg}")
                except:
                    pass
                return self._orig_messagebox_showerror(title, msg, *a, **k)

            _tk_messagebox.showinfo = _speak_and_showinfo
            _tk_messagebox.showwarning = _speak_and_showwarning
            _tk_messagebox.showerror = _speak_and_showerror
        except Exception:
            pass

        self.container = tk.Frame(self.root)
        self.container.pack(fill="both", expand=True)

        self.home = NexusHomeLogo(self.container)
        self.security = SecurityDashboard(self.container)
        self.study = StudyModePage(self.container, self.stop_study_mode)
        self.news = NewsPage(self.container)

        for p in [self.home, self.security, self.study, self.news]:
            p.place(relx=0, rely=0, relwidth=1, relheight=1)

        self.security.stop_btn.config(command=self.stop_monitoring)

        # ✅ Activity Summary Panel
        self.summary_box = tk.Text(
            self.root, bg="#0b1220", fg="white",
            font=("Consolas", 10),
            height=8, bd=0, highlightthickness=0
        )
        self.summary_box.pack(fill="x", side="bottom")

        # Command bar
        bar = tk.Frame(self.root, bg="#04131b")
        bar.pack(fill="x", side="bottom")

        tk.Label(bar, text="Command:", fg="#38bdf8", bg="#04131b",
                 font=("Segoe UI", 11, "bold")).pack(side="left", padx=10)

        self.entry = ttk.Entry(bar, font=("Segoe UI", 12))
        self.entry.pack(side="left", fill="x", expand=True, padx=10, pady=8)
        self.entry.bind("<Return>", lambda e: self.run_command(self.entry.get()))

        ttk.Button(bar, text="Run", command=lambda: self.run_command(self.entry.get())).pack(side="left", padx=5)
        ttk.Button(bar, text="Home", command=lambda: self.show("home")).pack(side="left", padx=5)
        ttk.Button(bar, text="News", command=self.latest_news).pack(side="left", padx=5)
        
        # ESC unlock from study mode
        self.root.bind("<Escape>", lambda e: self.stop_study_mode() if self.study_mode else None)

        self.show("home")
        self.toast.show("NEXUS ✅ Online", "All features loaded", "success")
        self.say_and_log("Hello! I am Nexus. What can I help you with?")
        self.root.after(2000, self.update_monitor)

# ================= DATABASE CONNECTION =================
        import mysql.connector

        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root123",  # <-- change this
            database="nexus_ai"
        )

        self.cursor = self.conn.cursor()
# =======================================================
        self.start_voice_listener()

    def save_summary(self, msg):
        try:
            with open(SUMMARY_FILE, "a", encoding="utf-8") as f:
                f.write(msg + "\n")
        except:
            pass

    def log(self, msg):
        line = f"{datetime.now().strftime('%H:%M:%S')} | {msg}"
        self.summary_box.insert(tk.END, line + "\n")
        self.summary_box.see(tk.END)
        self.save_summary(line)

    def _speech_worker(self):
        while True:
            txt = self.speech_queue.get()
            try:
                self.engine.say(txt)
                self.engine.runAndWait()
            except:
                pass
            self.speech_queue.task_done()

    def speak(self, text):
        if self.engine:
            self.speech_queue.put(text)

    def say_and_log(self, text):
        self.log("NEXUS: " + text)
        self.speak(text)

    def show(self, page):
        if page == "home":
            self.home.tkraise()
        elif page == "security":
            self.security.tkraise()
        elif page == "study":
            self.study.tkraise()
        elif page == "news":
            self.news.tkraise()

    def start_voice_listener(self):        
# =====================================================
# WRITE AND OPEN (REQUIRED FOR APP GENERATOR)
# =====================================================
        def write_and_open(self, filename, code, name):

            filename = filename.replace(".py", ".pyw")

            with open(filename, "w", encoding="utf-8") as f:
                f.write(code)

            try:
                self.toast.show("App Created", name)
            except:
                pass

            try:
                self.say_and_log(f"{name} created successfully")
            except:
                pass

        # If study mode is active, don't auto-launch the created app
            if getattr(self, "study_mode", False):
                try:
                    self.toast.show("Launch Blocked", "Study mode active — app not launched", "warning")
                except:
                    pass
                return

            subprocess.Popen(
                [sys.executable.replace("python.exe", "pythonw.exe"), filename]
            )

# ================= Monitoring =================
    def start_monitoring(self):
        if not psutil:
            self.toast.show("Missing psutil", "pip install psutil", "error")
            self.say_and_log("Please install psutil.")
            return
        
        # ✅ START BACKEND TRACKING HERE
        self.start_feature("Security Monitoring")

        self.monitoring = True
        self.security.set_status(True)
        self.show("security")
        self.toast.show("Monitoring ✅", "Enabled", "success")
        self.say_and_log("Security monitoring started.")

    def stop_monitoring(self):
        self.monitoring = False
        self.security.set_status(False)
        self.toast.show("Monitoring OFF", "Stopped", "warning")
        self.say_and_log("Monitoring stopped.")
        self.show("home")

    # ✅ STOP BACKEND TRACKING HERE
        self.stop_feature()

    def update_monitor(self):
        if self.monitoring and psutil:
            cpu = psutil.cpu_percent()
            ram = psutil.virtual_memory().percent
            disk = psutil.disk_usage("C:\\").percent
            batt = "N/A"
            try:
                b = psutil.sensors_battery()
                if b:
                    batt = f"{int(b.percent)}%"
            except:
                pass
            self.security.update_stats(cpu, ram, disk, batt)
            self.security.add_activity(
                f"{datetime.now().strftime('%H:%M:%S')} CPU:{cpu:.0f}% RAM:{ram:.0f}% DISK:{disk:.0f}%"
            )
        self.root.after(2000, self.update_monitor)
        
# ================= Study Mode =================
    def _restrict_browser_to_chatgpt(self):
        """Close common browser processes, then open ChatGPT in the default browser.
        This uses platform task-kill commands; it's intentionally simple and best-effort.
        """
        procs = ["chrome.exe", "msedge.exe", "firefox.exe", "opera.exe", "brave.exe"]
        for p in procs:
            try:
                if os.name == "nt":
                    # Windows: force-kill known browser processes (silently)
                    os.system(f"taskkill /f /im {p} >nul 2>&1")
                else:
                    # Unix-like: attempt pkill
                    os.system(f"pkill -f {p} 2>/dev/null || true")
            except:
                pass

        # Re-open ChatGPT after closing other browsers
        try:
            webbrowser.open("https://chat.openai.com/")
        except:
            pass

    def start_study_mode(self):

        # ✅ START BACKEND TRACKING HERE
        self.start_feature("Study Mode")

        self.study_mode = True
        # Restrict browsing: close other browser processes and open ChatGPT
        try:
            self._restrict_browser_to_chatgpt()
        except:
            pass
        self.show("study")
        self.toast.show("Study Mode ✅", "Activated — Only ChatGPT allowed", "warning")
        self.say_and_log("Study mode enabled and browsers restricted to ChatGPT.")

    def stop_study_mode(self):
        # Safely disable study mode and return to home
        if self.study_mode:
            self.study_mode = False
        self.toast.show("Study Mode OFF ✅", "Deactivated", "success")
        self.say_and_log("Study mode disabled.")
        try:
            self.show("home")
        except:
            pass

        # ✅ STOP BACKEND TRACKING HERE
        self.stop_feature()

# ================= Open apps (smart prompt) =================
    def open_app(self, cmd):

        if self.study_mode:
            self.toast.show("Blocked 🚫", "Study mode active", "warning")
            self.say_and_log("Apps blocked in study mode.")
            return

        cmd = cmd.lower()

    # ✅ START TRACKING
        self.start_feature("Open App", extra_info=cmd)

        try:
 
            if "youtube" in cmd:
                q = simpledialog.askstring("YouTube Search", "What should I search on YouTube?")
                if q:
                    webbrowser.open(f"https://www.youtube.com/results?search_query={q}")
                    self.toast.show("YouTube ✅", f"Searching: {q}", "success")
                    self.say_and_log(f"Searching YouTube: {q}")
                return

            if "google" in cmd:
                q = simpledialog.askstring("Google Search", "What should I search on Google?")
                if q:
                    webbrowser.open(f"https://www.google.com/search?q={q}")
                    self.toast.show("Google ✅", f"Searching: {q}", "success")
                    self.say_and_log(f"Searching Google: {q}")
                return

            apps = {
                "whatsapp": "https://web.whatsapp.com",
                "spotify": "https://open.spotify.com",
                "chrome": "start chrome"
            }

            for k in apps:
                if k in cmd:
                    self.toast.show("Opening ✅", k, "info")
                    self.say_and_log(f"Opening {k}")
                    if apps[k].startswith("http"):
                        webbrowser.open(apps[k])
                    else:
                        os.system(apps[k])
                    return

            self.toast.show("Not Found", "App not configured", "error")
            self.say_and_log("Application not found.")

        finally:
        # ✅ ALWAYS EXECUTES
            self.stop_feature()

# ================= Play Song =================
    def play_song(self, q):
        if self.study_mode:
            self.toast.show("Blocked 🚫", "Study mode active", "warning")
            self.say_and_log("Music blocked in study mode.")
            return
        if not q.strip():
            return
        
        # ✅ START BACKEND TRACKING
        self.start_feature("Play Song", extra_info=q)

        webbrowser.open(f"https://www.youtube.com/results?search_query={q}")
        self.toast.show("Playing ✅", q, "success")
        self.say_and_log(f"Playing {q}")
        self.toast.show("play song success", "play song success", "success")
        self.say_and_log("song played successfully.")

        # ✅ STOP BACKEND TRACKING
        self.stop_feature()

# ================= Weather =================
    def weather(self):

        if self.study_mode:
            self.toast.show("Blocked 🚫", "Study mode active - weather blocked", "warning")
            self.say_and_log("Weather request blocked in study mode.")
            return

        if not requests:
            self.toast.show("Weather Error", "pip install requests", "error")
            self.say_and_log("Requests missing.")
            return

    # ✅ START BACKEND TRACKING
        self.start_feature("Weather", extra_info=CITY_WEATHER)

        try:
            data = requests.get(
                f"https://wttr.in/{CITY_WEATHER}?format=j1",
                timeout=6
            ).json()

            temp = data["current_condition"][0]["temp_C"]
            desc = data["current_condition"][0]["weatherDesc"][0]["value"]

            self.toast.show(
                f"{CITY_WEATHER} Weather ✅",
                f"{temp}°C | {desc}",
                "info",
                duration=4500
            )

            self.say_and_log(
                f"{CITY_WEATHER} weather is {temp} degrees {desc}"
            )

        except Exception as e:
            self.toast.show("Weather Error", "Unable to fetch weather", "error")
            self.say_and_log(f"Weather error: {e}")

        finally:
        # ✅ ALWAYS EXECUTES
            self.stop_feature()

# ================= News =================
    def latest_news(self):

        if self.study_mode:
            self.toast.show("Blocked 🚫", "Study mode active - news blocked", "warning")
            self.say_and_log("News load blocked in study mode.")
            return

        if not feedparser:
            self.toast.show("News Error", "pip install feedparser", "error")
            self.say_and_log("Feedparser missing.")
            return

    # ✅ START BACKEND TRACKING
        self.start_feature("Latest News")

        try:
            self.news.clear()
            self.show("news")
            self.toast.show("News ✅", "Loading latest headlines...", "info")
            self.say_and_log("Loading latest news.")

            feeds = {
                "Politics": "https://news.google.com/rss/search?q=politics+India&hl=en-IN&gl=IN&ceid=IN:en",
                "Bollywood": "https://news.google.com/rss/search?q=bollywood&hl=en-IN&gl=IN&ceid=IN:en",
                "Farmer": "https://news.google.com/rss/search?q=farmers+India&hl=en-IN&gl=IN&ceid=IN:en",
                "Lifestyle": "https://news.google.com/rss/search?q=lifestyle+India&hl=en-IN&gl=IN&ceid=IN:en",
            }

            for cat, url in feeds.items():
                parsed = feedparser.parse(url)
                self.news.add_card(f"===== {cat} =====", "", "", "")

                for entry in parsed.entries[:5]:
                    src = entry.get("source", {}).get("title", "Google News")
                    pub = entry.get("published", "")
                    self.news.add_card(entry.title, src, entry.link, pub)

            self.toast.show("News Updated ✅", "Latest news loaded", "success")
            self.say_and_log("News updated successfully.")

        except Exception as e:
            self.toast.show("News Error ❌", "Unable to fetch news", "error")
            self.say_and_log(f"News error: {e}")

        finally:
        # ✅ ALWAYS EXECUTES
            self.stop_feature()

   
# ================= Find file/folder =================
    def get_drives(self):
        drives = []
        for letter in "CDEFGHIJKLMNOPQRSTUVWXYZ":
            d = f"{letter}:\\"
            if os.path.exists(d):
                drives.append(d)
        return drives

    def safe_open(self, path):
        try:
            os.startfile(path)
            return True
        except:
            return False

    def find_file(self, keyword):
        keyword = keyword.strip().lower()
        if not keyword:
         return

       # ✅ START BACKEND
        self.start_feature("Find File", extra_info=keyword)

        self.toast.show("Searching...", f"File: {keyword}", "info")
        self.say_and_log(f"Searching file: {keyword}")

        start = time.time()
        for base in self.get_drives():
            for root_dir, _, files in os.walk(base):
                if time.time() - start > 18:
                    break
                for f in files:
                    if keyword in f.lower():
                        path = os.path.join(root_dir, f)
                        if self.safe_open(path):
                            self.toast.show("File Opened ✅", f, "success")
                            self.say_and_log("File opened successfully.")
                            return
        self.toast.show("Not Found ❌", "File not found", "error")
        self.say_and_log("File not found.")

    def find_folder(self, keyword):
        keyword = keyword.strip().lower()
        self.toast.show("Searching...", f"Folder: {keyword}", "info")
        self.say_and_log(f"Searching folder: {keyword}")

        start = time.time()
        for base in self.get_drives():
            for root_dir, dirs, _ in os.walk(base):
                if time.time() - start > 18:
                    break
                for d in dirs:
                    if keyword in d.lower():
                        path = os.path.join(root_dir, d)
                        if self.safe_open(path):
                            self.toast.show("Folder Opened ✅", d, "success")
                            self.say_and_log("Folder opened successfully.")
                            return
        self.toast.show("Not Found ❌", "Folder not found", "error")
        self.say_and_log("Folder not found.")

        # ✅ STOP BACKEND (Failure)
        self.stop_feature()

# ================= Backup ZIP =================
    def backup(self):
        folder = filedialog.askdirectory(title="Select Folder to Backup")
        if not folder:
            return
        
        # ✅ START BACKEND TRACKING
        self.start_feature("Backup", extra_info=folder)

        backup_dir = os.path.join(os.getcwd(), "NEXUS_Backups")
        os.makedirs(backup_dir, exist_ok=True)

        zip_name = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
        zip_path = os.path.join(backup_dir, zip_name)

        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
            for root_dir, _, files in os.walk(folder):
                for f in files:
                    full = os.path.join(root_dir, f)
                    arc = os.path.relpath(full, folder)
                    z.write(full, arc)

        self.toast.show("Backup ✅", zip_name, "success")
        self.say_and_log("Backup completed successfully.")

        # ✅ STOP BACKEND TRACKING
        self.stop_feature()

# ================= Screenshot =================
    def screenshot(self):

        if self.study_mode:
            self.toast.show("Blocked 🚫", "Study mode active - screenshot blocked", "warning")
            self.say_and_log("Screenshot blocked in study mode.")
            return

        if not pyautogui:
            self.toast.show("Screenshot Error", "pip install pyautogui pillow", "error")
            self.say_and_log("Please install pyautogui and pillow.")
            return

        folder = os.path.join(os.getcwd(), "NEXUS_Screenshots")
        os.makedirs(folder, exist_ok=True)

        name = f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        path = os.path.join(folder, name)

    # ✅ START BACKEND TRACKING
        self.start_feature("Screenshot", extra_info=name)

        try:
            pyautogui.screenshot(path)

            self.toast.show("Screenshot ✅", name, "success")
            self.say_and_log("Screenshot saved successfully.")

        except Exception as e:
            self.toast.show("Screenshot Error ❌", "Failed to capture", "error")
            self.say_and_log(f"Screenshot failed: {e}")

    # ✅ STOP BACKEND TRACKING
        self.stop_feature()
   
# ================= Restart / Shutdown =================
    def restart_pc(self):

    # ✅ START BACKEND TRACKING
        self.start_feature("Restart PC")

        self.toast.show("Restart ⚠️", "PC restarting in 5 seconds", "warning")
        self.say_and_log("System restarting.")

    # ✅ STOP BACKEND BEFORE SHUTDOWN
        self.stop_feature()

        os.system("shutdown /r /t 5")


    def shutdown_pc(self):

    # ✅ START BACKEND TRACKING
        self.start_feature("Shutdown PC")

        self.toast.show("Shutdown ⚠️", "PC shutting down in 5 seconds", "warning")
        self.say_and_log("System shutting down.")

    # ✅ STOP BACKEND BEFORE SHUTDOWN
        self.stop_feature()

        os.system("shutdown /s /t 5")

# =====================================================
# Pdf Generation 
# =====================================================
    def save_pdf_story(self, folder, filename, title, content_paragraphs):

        os.makedirs(folder, exist_ok=True)
        filepath = f"{folder}/{filename}.pdf"

    # ✅ START BACKEND TRACKING
        self.start_feature("Generate PDF", extra_info=filename)

        try:
            doc = SimpleDocTemplate(
                filepath,
                pagesize=A4,
                rightMargin=40,
                leftMargin=40,
                topMargin=60,
                bottomMargin=40
            )

            story = []

            styles = getSampleStyleSheet()

            story.append(
                Paragraph(f"<b><font size=18>{title}</font></b>", styles['Title'])
            )
            story.append(Spacer(1, 12))

            for para in content_paragraphs:
                story.append(Paragraph(para, styles['Normal']))
                story.append(Spacer(1, 12))

            doc.build(story)

            self.toast.show("PDF Generated ✅", filename, "success")
            self.say_and_log(f"{filename} generated successfully.")

        except Exception as e:
            self.toast.show("PDF Error ❌", "Failed to generate PDF", "error")
            self.say_and_log(f"PDF generation failed: {e}")

    # ✅ STOP BACKEND TRACKING
        self.stop_feature()

# =====================================================
# Medical_Report
# =====================================================
    def create_medical_report(self):

        name = simpledialog.askstring("Medical Report", "Patient Name:")
        age = simpledialog.askstring("Medical Report", "Patient Age:")
        problem = simpledialog.askstring("Medical Report", "Medical Problem:")

        if not name or not age or not problem:
            return

        date = datetime.now().strftime("%d %B %Y")

        content = [

            f"<b>Patient Information</b><br/>Name: {name}<br/>Age: {age} Years<br/>Date: {date}",
            f"<b>History of Present Illness</b><br/>Patient reports {problem}. Symptoms started recently and are mild to moderate.",
            "<b>Past Medical History</b><br/>• No known chronic illnesses<br/>• No previous surgeries<br/>• No allergies reported",
            "<b>Vital Signs</b><br/>• Temperature: Normal<br/>• Pulse: Normal<br/>• Blood Pressure: Normal<br/>• Respiratory Rate: Normal",
            "<b>Clinical Examination</b><br/>General condition: Fair<br/>Patient is conscious, alert, and oriented.<br/>No signs of distress observed.",
            "<b>Diagnosis</b><br/>Suspected viral infection (to be confirmed by physician if required).",
            "<b>Treatment & Advice</b><br/>• Adequate rest<br/>• Hydration (plenty of fluids)<br/>• Paracetamol if required<br/>• Steam inhalation<br/>• Avoid strenuous activity for 3–5 days",
            "<b>Follow-up</b><br/>Consult a doctor if symptoms persist more than 3 days or worsen.",
            "<b>Additional Notes</b><br/>• Patient advised to monitor temperature daily.<br/>• Keep a symptom diary if necessary.<br/>• Maintain proper hygiene.",
            "<b>Physician Signature:</b> ____________________"
        ]

        folder = "NEXUS_Reports/Medical"

    # cleaner filename (remove spaces)
        safe_name = name.replace(" ", "_")

        filename = f"Medical_Report_{safe_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

    # Backend logging happens inside save_pdf_story()
        self.save_pdf_story(
            folder,
            filename,
            "MEDICAL REPORT",
            content
        )

# =====================================================
# Resume Builder
# =====================================================
    def generate_resume(self, name, email, phone, education, skills):
        if not name:
            return

    # ✅ START BACKEND TRACKING
        self.start_feature("Generate Resume", extra_info=name)

        folder = os.path.join("NEXUS_Reports", "Resume")
        os.makedirs(folder, exist_ok=True)
        filename = os.path.join(folder, f"{name.replace(' ', '_')}_Resume.pdf")

        doc = SimpleDocTemplate(filename, pagesize=A4,
                                rightMargin=40, leftMargin=40,
                                topMargin=40, bottomMargin=40)

        styles = getSampleStyleSheet()
        name_style = ParagraphStyle('NameStyle', parent=styles['Heading1'], fontSize=26, leading=28)
        title_style = ParagraphStyle('TitleStyle', parent=styles['Heading2'], fontSize=12, textColor=colors.darkblue)
        heading = ParagraphStyle('Heading', parent=styles['Heading3'], fontSize=12, textColor=colors.black, spaceBefore=8)
        normal = ParagraphStyle('Normal', parent=styles['Normal'], fontSize=11, leading=14)
        bullet = ParagraphStyle('Bullet', parent=styles['Normal'], leftIndent=12, bulletIndent=6, bulletFontSize=10)

        elements = []

        # Header: Name + Contact
        elements.append(Paragraph(name, name_style))
        contact_line = f"{email}  |  {phone}"
        elements.append(Paragraph(contact_line, normal))
        elements.append(Spacer(1, 8))
        elements.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#444444')))
        elements.append(Spacer(1, 12))

        # Professional Summary
        prof = "Professional Summary"
        summary_text = f"Experienced professional skilled in {skills}. Demonstrated ability to deliver results, learn quickly, and collaborate across teams. Seeking opportunities to contribute technical and analytical skills."
        elements.append(Paragraph(prof, heading))
        elements.append(Paragraph(summary_text, normal))
        elements.append(Spacer(1, 10))

        # Skills
        elements.append(Paragraph("Skills", heading))
        skill_list = [s.strip() for s in (skills or "").split(",") if s.strip()]
        if skill_list:
            for s in skill_list:
                elements.append(Paragraph(f"• {s}", bullet))
        else:
            elements.append(Paragraph("• Not provided", bullet))
        elements.append(Spacer(1, 8))

        # Education
        elements.append(Paragraph("Education", heading))
        elements.append(Paragraph(education or "Education details not provided", normal))
        elements.append(Spacer(1, 8))

        # Experience placeholder (user can edit later)
        elements.append(Paragraph("Experience", heading))
        elements.append(Paragraph("Add recent positions, company names, dates and key achievements.", normal))
        elements.append(Spacer(1, 8))

        # Footer note
        elements.append(Spacer(1, 16))
        elements.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor('#dddddd')))
        elements.append(Paragraph("This resume was generated by NEXUS.", ParagraphStyle('Foot', parent=styles['Normal'], fontSize=9, textColor=colors.grey, alignment=1)))

        try:
            doc.build(elements)
            self.toast.show("Resume Created", f"Resume for {name} created successfully", "success")
            self.say_and_log("Resume created successfully")
        except Exception as e:
            self.toast.show("Resume Error", "Failed to create resume", "error")
            self.say_and_log(f"Resume generation failed: {e}")

    # ✅ STOP BACKEND TRACKING
            self.stop_feature()

# ================= Research =================
    def research_topic(self, topic):
        if not topic.strip():
            topic = simpledialog.askstring("Research Topic", "Enter topic:")
            if not topic:
                return
            
    # ✅ START BACKEND TRACKING
        self.start_feature("Research Topic", extra_info=topic)


        url = f"https://www.google.com/search?q={topic.replace(' ', '+')}"
        webbrowser.open(url)

        self.toast.show("Research 🔍", f"Searching: {topic}", "info")
        self.say_and_log(f"Researching {topic}")

    # ✅ STOP BACKEND TRACKING
        self.stop_feature()

# =====================================================
# APP GENERATOR (UNIFIED, NON-BLOCKING WINDOW)
# =====================================================

    def create_app_generator(self, initial_cmd=""):
        """Open a small generator window with several app templates.
        Writes the chosen template to a .py file and launches it unless study mode is active.
        """
        apps = {

"calculator": '''
import tkinter as tk
from tkinter import messagebox

root = tk.Tk()
root.title("Calculator")
root.geometry("350x450")

entry = tk.Entry(root,font=("Arial",20))
entry.pack(fill="both",pady=10)

def press(val):
    entry.insert(tk.END,val)

def clear():
    entry.delete(0,tk.END)

def calculate():
    try:
        result = eval(entry.get())
        entry.delete(0,tk.END)
        entry.insert(0,result)
    except:
        messagebox.showerror("Error","Invalid Expression")

buttons=['7','8','9','/','4','5','6','*','1','2','3','-','0','.','+']

frame=tk.Frame(root)
frame.pack()

row=0
col=0
for b in buttons:
    tk.Button(frame,text=b,width=5,height=2,
              command=lambda x=b: press(x)).grid(row=row,column=col,padx=5,pady=5)
    col+=1
    if col>3:
        col=0
        row+=1

tk.Button(root,text="=",command=calculate).pack(fill="x")
tk.Button(root,text="Clear",command=clear).pack(fill="x")

root.mainloop()
''',

"quiz": '''
import tkinter as tk
from tkinter import messagebox

root = tk.Tk()
root.title("Quiz")
root.geometry("600x400")

questions = [
("5+3?","8"),
("Capital of India?","Delhi"),
("2*6?","12"),
("Square root of 16?","4"),
("5*5?","25"),
("Sun rises in?","East"),
("Python is?","Language"),
("10/2?","5"),
("HTML full form?","HyperText Markup Language"),
("Largest planet?","Jupiter")
]

score=0
q_no=0

label=tk.Label(root,font=("Arial",14))
label.pack(pady=20)

entry=tk.Entry(root)
entry.pack()

def next_q():
    global q_no,score
    ans=entry.get()

    if q_no>0:
        if ans.lower()==questions[q_no-1][1].lower():
            score+=1

    entry.delete(0,tk.END)

    if q_no<len(questions):
        label.config(text=questions[q_no][0])
        q_no+=1
    else:
        messagebox.showinfo("Result",f"Score: {score}/10")
        root.destroy()

tk.Button(root,text="Next",command=next_q).pack(pady=10)
next_q()
root.mainloop()
''',

"notes": '''
import tkinter as tk
from tkinter import filedialog

root=tk.Tk()
root.title("Notes")
root.geometry("600x500")

text=tk.Text(root,font=("Arial",14))
text.pack(fill="both",expand=True)

def save():
    file=filedialog.asksaveasfilename(defaultextension=".txt")
    if file:
        with open(file,"w") as f:
            f.write(text.get("1.0",tk.END))

tk.Button(root,text="Save",command=save).pack()
root.mainloop()
''',

"stopwatch": '''
import tkinter as tk
import time

root=tk.Tk()
root.title("Stopwatch")
root.geometry("300x200")

running=False
start_time=0

label=tk.Label(root,font=("Arial",30))
label.pack(pady=20)

def start():
    global running,start_time
    running=True
    start_time=time.time()
    update()

def stop():
    global running
    running=False

def update():
    if running:
        elapsed=int(time.time()-start_time)
        label.config(text=str(elapsed)+" sec")
        root.after(1000,update)

tk.Button(root,text="Start",command=start).pack()
tk.Button(root,text="Stop",command=stop).pack()
root.mainloop()
''',

"library": '''
import tkinter as tk

root=tk.Tk()
root.title("Library Management")
root.geometry("500x450")

entry=tk.Entry(root)
entry.pack(pady=10)

listbox=tk.Listbox(root,width=50)
listbox.pack(pady=10)

def add():
    listbox.insert(tk.END,entry.get())
    entry.delete(0,tk.END)

def delete():
    selected=listbox.curselection()
    if selected:
        listbox.delete(selected)

tk.Button(root,text="Add Book",command=add).pack()
tk.Button(root,text="Delete Book",command=delete).pack()
root.mainloop()
''',

"todo": '''
import tkinter as tk

root=tk.Tk()
root.title("To-Do List")
root.geometry("400x400")

entry=tk.Entry(root)
entry.pack()

listbox=tk.Listbox(root,width=40)
listbox.pack()

def add():
    listbox.insert(tk.END,entry.get())
    entry.delete(0,tk.END)

tk.Button(root,text="Add Task",command=add).pack()
root.mainloop()
''',

"converter": '''
import tkinter as tk
from tkinter import messagebox

root=tk.Tk()
root.title("Unit Converter")
root.geometry("300x200")

entry=tk.Entry(root)
entry.pack()

label=tk.Label(root)
label.pack()

def convert():
    try:
        value=float(entry.get())
        label.config(text=str(value*100)+" cm")
    except:
        messagebox.showerror("Error","Enter number")

tk.Button(root,text="Meter to CM",command=convert).pack()
root.mainloop()
''',

"clock": '''
import tkinter as tk
import time

root=tk.Tk()
root.title("Clock")
root.geometry("300x150")

label=tk.Label(root,font=("Arial",30))
label.pack()

def update():
    label.config(text=time.strftime("%H:%M:%S"))
    root.after(1000,update)

update()
root.mainloop()
''',

"password": '''
import tkinter as tk
import random,string

root=tk.Tk()
root.title("Password Generator")
root.geometry("300x200")

label=tk.Label(root,font=("Arial",14))
label.pack(pady=20)

def generate():
    chars=string.ascii_letters+string.digits
    password="".join(random.choice(chars) for _ in range(8))
    label.config(text=password)

tk.Button(root,text="Generate",command=generate).pack()
root.mainloop()
''',

"student": '''
import tkinter as tk

root=tk.Tk()
root.title("Student Record")
root.geometry("400x300")

name=tk.Entry(root)
name.pack()
marks=tk.Entry(root)
marks.pack()

listbox=tk.Listbox(root)
listbox.pack()

def add():
    listbox.insert(tk.END,name.get()+" - "+marks.get())
    name.delete(0,tk.END)
    marks.delete(0,tk.END)

tk.Button(root,text="Add Record",command=add).pack()
root.mainloop()
'''
        }

        def generate_app(command):
            command = command.lower()
            for app in apps:
                if app in command:

                    # ✅ START BACKEND TRACKING
                    self.start_feature("App Generator", extra_info=app)

                    filename = app + ".py"

                try:

                    with open(filename, "w", encoding="utf-8") as f:
                        f.write(apps[app])
                    if getattr(self, "study_mode", False):
                        try:
                            self.toast.show("Launch Blocked", "Study mode active — app not launched", "warning")
                        except:
                            pass
                        self.say_and_log("App generation blocked in study mode.")

                        # ✅ STOP BACKEND
                        self.stop_feature()

                        return
                    subprocess.Popen([sys.executable, filename])

                    self.toast.show("App Created ✅", app, "success")
                    self.say_and_log(f"{app} app generated successfully.")

                except Exception as e:
                    self.toast.show("App Error ❌", "Failed to create app", "error")
                    self.say_and_log(f"App generation failed: {e}")

                # ✅ STOP BACKEND TRACKING
                    self.stop_feature()

                    return
            messagebox.showerror("Error", "App not found")

        win = tk.Toplevel(self.root)
        win.title("Text Command App Generator")
        win.geometry("450x200")

        tk.Label(win, text="Type Command (Example: create calculator)",
                 font=("Arial", 12)).pack(pady=10)

        entry = tk.Entry(win, width=40)
        entry.pack()
        if initial_cmd:
            entry.insert(0, initial_cmd)

        tk.Button(win, text="Generate",
                  command=lambda: generate_app(entry.get())
                  ).pack(pady=15)

# =====================================================
# COMMAND ROUTER
# =====================================================
    def run_command(self, cmd):
        cmd = cmd.lower().strip()
        try:
            self.entry.delete(0, tk.END)
        except:
            pass

        # If study mode is active, block most external actions.
        allowed_while_study = ["stop study mode", "how exactly you help me"]
        if getattr(self, "study_mode", False) and not any(a in cmd for a in allowed_while_study):
            self.toast.show("Blocked 🚫", "Study mode active — action blocked", "warning")
            self.say_and_log("Action blocked while study mode is active.")
            return

        # ===== Log user command =====
        try:
            self.summary_box.insert(tk.END, f"\n>> You said: {cmd}\n")
        except:
            pass

        # ===== HELP LIST =====
        if "how exactly you help me" in cmd:
            response = """
I can help you with:

• Open Applications
• Find Files and Folders
• Backup Data
• Study Mode
• Screenshot
• Weather Updates
• Latest News
• Security Monitoring
• Shutdown / Restart System
"""
            try:
                self.summary_box.insert(tk.END, response)
            except:
                pass
            self.say_and_log("Here is the list of features I provide")

        # ===== SHUTDOWN / RESTART =====
        elif "shutdown" in cmd:
            self.say_and_log("Shutting down system")
            os.system("shutdown /s /t 1")

        elif "restart" in cmd:
            self.say_and_log("Restarting system")
            os.system("shutdown /r /t 1")

        # ===== CREATE APPLICATIONS =====
        # Handle specific document creators first so they are not caught by the generic create handler.
        elif "create medical report" in cmd:
            self.say_and_log("Creating medical report")
            self.root.after(800, self.create_medical_report)
        elif "create resume" in cmd:
            name = simpledialog.askstring("Resume", "Enter your full name:")
            email = simpledialog.askstring("Resume", "Enter your email:")
            phone = simpledialog.askstring("Resume", "Enter your phone number:")
            education = simpledialog.askstring("Resume", "Enter your education background:")
            skills = simpledialog.askstring("Resume", "Enter your skills (comma separated):")
            self.generate_resume(name, email, phone, education, skills)
        elif "create" in cmd:
            # Open unified generator window and prefill the requested app name
            app_name = cmd.replace("create", "").strip()
            self.say_and_log(f"Opening app generator for: {app_name}")
            self.root.after(800, lambda name=app_name: self.create_app_generator(name))

        # ===== WEB / ONLINE =====
        elif "weather" in cmd:
            self.say_and_log("Opening weather information")
            self.root.after(800, lambda: webbrowser.open("https://www.google.com/search?q=weather"))

        elif "youtube" in cmd:
            self.say_and_log("Opening YouTube")
            self.toast.show("YouTube", "Opening YouTube", "info")
            self.root.after(800, lambda: webbrowser.open("https://youtube.com"))

        elif "news" in cmd:
            self.say_and_log("Opening latest news")
            self.root.after(800, lambda: webbrowser.open("https://news.google.com"))

        elif "open chrome" in cmd:
            self.say_and_log("Opening Chrome")
            self.toast.show("Opening Chrome ✅", "Launching browser", "info")
            self.root.after(800, lambda: os.system("start chrome"))

        # ===== MEDIA =====
        elif "play song" in cmd:
            song = cmd.replace("play song", "").strip()
            if not song:
                song = simpledialog.askstring("Play Song", "Enter song name:")
            if song:
                self.say_and_log(f"Playing {song}")
                self.root.after(800, lambda: self.play_song(song))

        # Document creation handled earlier in the 'CREATE APPLICATIONS' section.

        # ===== RESEARCH =====
        elif "research" in cmd:
            topic = cmd.replace("research", "").strip()
            self.say_and_log(f"Researching {topic}")
            self.root.after(800, lambda: self.research_topic(topic))

        # ===== SECURITY MONITORING =====
        elif "start security monitoring" in cmd or "start monitoring" in cmd:
            self.say_and_log("Starting security monitoring")
            self.root.after(800, self.start_monitoring)

        elif "stop security monitoring" in cmd or "stop monitoring" in cmd:
            self.say_and_log("Stopping security monitoring")
            self.root.after(800, self.stop_monitoring)

        # ===== STUDY MODE =====
        elif "start study mode" in cmd:
            self.say_and_log("Activating study mode")
            self.root.after(800, self.start_study_mode)

        elif "stop study mode" in cmd:
            self.say_and_log("Deactivating study mode")
            self.root.after(800, self.stop_study_mode)

        # ===== FILE / APP HANDLING =====
        elif "open app" in cmd:
            self.say_and_log("Opening application")
            self.root.after(800, lambda: self.open_app(cmd))

        elif "find folder" in cmd:
            folder = simpledialog.askstring("Find Folder", "Enter folder path or name:")
            if folder:
                self.say_and_log(f"Opening folder: {folder}")
                # If the user provided a full/valid path, open it directly.
                # Otherwise, call the search routine which looks for matching folder names on drives.
                if os.path.exists(folder):
                    self.root.after(800, lambda p=folder: os.startfile(p))
                else:
                    self.root.after(800, lambda f=folder: self.find_folder(f))

        elif "screenshot" in cmd:
            self.say_and_log("Taking a screenshot")
            self.root.after(800, self.screenshot)

        # ===== BACKUP =====
        elif "backup" in cmd:
            self.say_and_log("Opening backup dialog. Select a folder to backup.")
            self.root.after(800, self.backup)

        # ===== UNKNOWN COMMAND =====
        else:
            self.say_and_log("Command not recognized")
            self.toast.show("Unknown Command", "Command not recognized")
            try:
                self.summary_box.insert(tk.END, ">> Command not recognized.\n")
            except:
                pass

    # ================= VOICE LISTENER =================
    def start_voice_listener(self):

        if not sr:
            print("SpeechRecognition not installed")
            return

        def listen():

            recognizer = sr.Recognizer()
            mic = sr.Microphone()

            while True:
                try:
                    with mic as source:
                        print("Listening...")
                        recognizer.adjust_for_ambient_noise(source)
                        audio = recognizer.listen(source)

                    cmd = recognizer.recognize_google(audio).lower()

                    print("You said:", cmd)

                # 🔥 send command to Nexus system
                    self.root.after(0, lambda: self.run_command(cmd))

                except Exception as e:
                    print("Voice error:", e)

        threading.Thread(target=listen, daemon=True).start()

    
    def run(self):
        try:
            self.root.mainloop()
        except Exception:
            pass

    
    def start_feature(self, feature_name, extra_info=""):
        from datetime import datetime
        print("START FEATURE CALLED:", feature_name)  # 👈 ADD THIS
        self.current_feature = {
            "name": feature_name,
            "start_time": datetime.now(),
            "extra_info": extra_info
        }
    
    def stop_feature(self):
        if hasattr(self, "current_feature"):
            end_time = datetime.now()
            start_time = self.current_feature["start_time"]
            duration = int((end_time - start_time).total_seconds() / 60)

            try:
                self.cursor.execute("""
                    INSERT INTO nexus_activity
                    (feature_name, action_type, start_time, end_time, duration_minutes, extra_info)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (
                    self.current_feature["name"],
                    "completed",
                    start_time,
                    end_time,
                    duration,
                    self.current_feature["extra_info"] 
                ))
                self.conn.commit()
            except Exception as e:
                print("DB Error:", e)    
    


if __name__ == "__main__":
    NexusFinalSystem().run()