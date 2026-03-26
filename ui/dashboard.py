import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

class MainDashboard(tk.Tk):
    def __init__(self, classifier, expert):
        super().__init__()
        self.classifier = classifier
        self.expert = expert
        
        self.title("AppleHealth AI: Professional Edition")
        self.geometry("1200x800")
        self._build_sidebar()
        self._build_main_view()

    def _build_sidebar(self):
        side_bar = tk.Frame(self, bg="#1e1e2d", width=250)
        side_bar.pack(side="left", fill="y")
        
        tk.Label(side_bar, text="DASHBOARD", fg="white", bg="#1e1e2d", font=("Arial", 12, "bold")).pack(pady=20)
        
        # Modern Styled Buttons
        style = ttk.Style()
        style.configure("Menu.TButton", font=("Arial", 10))
        
        ttk.Button(side_bar, text="Image Upload", style="Menu.TButton").pack(fill="x", padx=10, pady=5)
        ttk.Button(side_bar, text="Live Vision", style="Menu.TButton").pack(fill="x", padx=10, pady=5)

    def _build_main_view(self):
        self.main_content = tk.Frame(self, bg="#f8f9fc")
        self.main_content.pack(side="right", fill="both", expand=True)
        
        # Display Area
        self.canvas = tk.Label(self.main_content, bg="#eaecf4", width=80, height=20)
        self.canvas.pack(pady=30)
        
        # Results Section
        self.status_box = tk.Label(self.main_content, text="Ready for Analysis", font=("Arial", 16), bg="#f8f9fc")
        self.status_box.pack()
        
        self.advice_area = tk.Text(self.main_content, height=10, width=80, font=("Arial", 10), state="disabled")
        self.advice_area.pack(pady=20)

    def update_advice(self, disease):
        plan = self.expert.get_treatment_plan(disease)
        self.advice_area.config(state="normal")
        self.advice_area.delete('1.0', tk.END)
        self.advice_area.insert(tk.END, f"EXPERT ANALYSIS: {disease}\n\n{plan}")
        self.advice_area.config(state="disabled")