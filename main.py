import os
import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import tensorflow as tf
from dotenv import load_dotenv
import google.generativeai as genai

# 1. SETUP & THEME COLORS
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

BG_MAIN = "#0F172A"      # Deep Navy/Black
BG_SIDEBAR = "#1E293B"   # Slate Blue/Grey
ACCENT_BLUE = "#38BDF8"  # Electric Sky Blue
TEXT_PRIMARY = "#F8FAFC"
ACCENT_GREEN = "#10B981"

MODEL_PATH = "weights.best.hdf5"
class_names = ['Blotch_Apple', 'Normal_Apple', 'Rot_Apple', 'Scab_Apple']

class AppleAI:
    def __init__(self):
        self.model = tf.keras.models.load_model(MODEL_PATH)

    def predict_frame(self, frame):
        img = cv2.resize(frame, (224, 224))
        img = img / 255.0
        img = np.expand_dims(img, axis=0)
        preds = self.model.predict(img, verbose=0)
        idx = np.argmax(preds[0])
        return class_names[idx], 100 * np.max(preds[0])

class AppleApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Apple Health AI Pro v2.0")
        self.root.geometry("1100x800")
        self.root.configure(bg=BG_MAIN)
        
        self.engine = AppleAI()
        self.cap = None 
        self.is_live = False
        
        self.setup_ui()
        
    def setup_ui(self):
        # --- LEFT SIDEBAR (Navigation) ---
        sidebar = tk.Frame(self.root, width=260, bg=BG_SIDEBAR, padx=20)
        sidebar.pack(side="left", fill="y")
        
        # App Title
        tk.Label(sidebar, text="APPLE AI", fg=ACCENT_BLUE, bg=BG_SIDEBAR, 
                 font=("Inter", 22, "bold")).pack(pady=(40, 5))
        tk.Label(sidebar, text="Health Monitoring System", fg="#94A3B8", bg=BG_SIDEBAR, 
                 font=("Inter", 9)).pack(pady=(0, 40))

        # Camera Button
        self.cam_btn = tk.Button(sidebar, text="🎥  Open Camera", command=self.toggle_live, 
                                 bg=ACCENT_BLUE, fg=BG_MAIN, font=("Inter", 11, "bold"),
                                 activebackground="#7DD3FC", relief="flat", height=2, cursor="hand2")
        self.cam_btn.pack(fill="x", pady=10)

        # Upload Button
        tk.Button(sidebar, text="📁  Upload File", command=self.upload_image, 
                  bg="#334155", fg=TEXT_PRIMARY, font=("Inter", 11),
                  activebackground="#475569", relief="flat", height=2, cursor="hand2").pack(fill="x", pady=10)

        # Status Indicator
        self.status_dot = tk.Label(sidebar, text="● System Ready", fg=ACCENT_GREEN, 
                                   bg=BG_SIDEBAR, font=("Inter", 10))
        self.status_dot.pack(side="bottom", pady=30)

        # --- MAIN CONTENT AREA ---
        content = tk.Frame(self.root, bg=BG_MAIN, padx=40, pady=20)
        content.pack(side="right", expand=True, fill="both")

        # Header
        self.res_label = tk.Label(content, text="Waiting for Input...", 
                                  fg=TEXT_PRIMARY, bg=BG_MAIN, font=("Inter", 24, "bold"))
        self.res_label.pack(anchor="w", pady=(0, 20))

        # Visualizer Frame (Camera/Image display)
        self.video_container = tk.Frame(content, bg="#1E293B", bd=0)
        self.video_container.pack(fill="x")
        
        self.video_label = tk.Label(self.video_container, bg="#1E293B")
        self.video_label.pack(pady=10)

        # Gemini Advice Area
        tk.Label(content, text="AI TREATMENT ADVICE", fg="#94A3B8", bg=BG_MAIN, 
                 font=("Inter", 10, "bold")).pack(anchor="w", pady=(30, 10))
        
        self.advice_box = tk.Text(content, height=8, bg="#1E293B", fg="#CBD5E1", 
                                  font=("Inter", 11), padx=20, pady=20, borderwidth=0)
        self.advice_box.pack(fill="x")

    def toggle_live(self):
        if not self.is_live:
            self.cap = cv2.VideoCapture(0)
            if not self.cap.isOpened():
                messagebox.showerror("Error", "Camera not found.")
                return
            self.is_live = True
            self.cam_btn.config(text="🛑  Stop Camera", bg="#EF4444", fg="white")
            self.status_dot.config(text="● Recording Live", fg="#F87171")
            self.update_live()
        else:
            self.is_live = False
            if self.cap: self.cap.release()
            self.cam_btn.config(text="🎥  Open Camera", bg=ACCENT_BLUE, fg=BG_MAIN)
            self.status_dot.config(text="● System Ready", fg=ACCENT_GREEN)

    def update_live(self):
        if self.is_live:
            ret, frame = self.cap.read()
            if ret:
                disease, conf = self.engine.predict_frame(frame)
                color = ACCENT_GREEN if disease == "Normal_Apple" else "#F87171"
                self.res_label.config(text=f"{disease.replace('_', ' ')}  ({conf:.1f}%)", fg=color)
                
                cv2_img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(cv2_img).resize((720, 450))
                tk_img = ImageTk.PhotoImage(image=img)
                self.video_label.imgtk = tk_img
                self.video_label.configure(image=tk_img)
            self.root.after(15, self.update_live)

    def upload_image(self):
        self.is_live = False
        path = filedialog.askopenfilename()
        if path:
            frame = cv2.imread(path)
            disease, conf = self.engine.predict_frame(frame)
            color = ACCENT_GREEN if disease == "Normal_Apple" else "#F87171"
            self.res_label.config(text=f"{disease.replace('_', ' ')}  ({conf:.1f}%)", fg=color)
            
            img = Image.open(path).resize((720, 450))
            tk_img = ImageTk.PhotoImage(img)
            self.video_label.imgtk = tk_img
            self.video_label.configure(image=tk_img)

if __name__ == "__main__":
    root = tk.Tk()
    # Change 'Inter' to 'Arial' if font is not installed
    app = AppleApp(root)
    root.mainloop()