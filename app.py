# app.py
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk # pip install pillow
import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from content.database import TOPICS
from utils.leaderboard import load_scores, save_score

class OpenLearnApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("OpenLearn - Offline Encyclopedia")
        self.geometry("800x600")
        
        # Container for all frames
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        
        # List of all page classes
        for F in (MainMenu, TopicViewer, QuizPage, Leaderboard):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("MainMenu")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()
        # Refresh data if needed when page is raised
        if hasattr(frame, "refresh"):
            frame.refresh()

class MainMenu(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#2c3e50")
        self.controller = controller
        
        tk.Label(self, text="Welcome to OpenLearn", font=("Arial", 24, "bold"), bg="#2c3e50", fg="white").pack(pady=50)
        
        # Dynamically create buttons for topics
        for topic_id in TOPICS:
            btn = tk.Button(self, text=TOPICS[topic_id]["title"], 
                            command=lambda t=topic_id: self.open_topic(t),
                            font=("Arial", 14), width=20, height=2)
            btn.pack(pady=10)

        tk.Button(self, text="Leaderboard", command=lambda: controller.show_frame("Leaderboard"), 
                  font=("Arial", 12), bg="#e67e22", fg="white").pack(side="bottom", pady=20, fill="x")
        
        tk.Button(self, text="Exit", command=self.controller.quit, 
                  font=("Arial", 10), bg="#c0392b", fg="white").pack(side="bottom", pady=5)

    def open_topic(self, topic_id):
        # Store current topic in controller to access it in next frame
        self.controller.current_topic_id = topic_id
        self.controller.show_frame("TopicViewer")

class TopicViewer(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        self.controller = controller
        self.page_index = 0
        
        # Header
        self.header = tk.Label(self, text="", font=("Arial", 18, "bold"), bg="white")
        self.header.pack(pady=10)
        
        # Content Area (Image + Text)
        self.content_area = tk.Frame(self, bg="white")
        self.content_area.pack(fill="both", expand=True, padx=20)
        
        self.img_label = tk.Label(self.content_area)
        self.img_label.pack(side="left", padx=10)
        
        self.text_box = tk.Label(self.content_area, text="", justify="left", wraplength=400, font=("Arial", 12), bg="white")
        self.text_box.pack(side="right", fill="both", expand=True)

        # Controls
        self.nav_frame = tk.Frame(self, bg="white")
        self.nav_frame.pack(side="bottom", fill="x", pady=20)
        
        tk.Button(self.nav_frame, text="< Prev", commandself.prev_page).pack(side="left", padx=20)
        tk.Button(self.nav_frame, text="Take Quiz >", command=self.start_quiz, bg="#27ae60", fg="white").pack(side="right", padx=20)
        tk.Button(self.nav_frame, text="Home", command=lambda: controller.show_frame("MainMenu")).pack(side="bottom")

    def refresh(self):
        self.topic_data = TOPICS[self.controller.current_topic_id]
        self.header.config(text=self.topic_data["title"])
        self.page_index = 0
        self.update_content()

    def update_content(self):
        pages = self.topic_data["content"]
        if self.page_index < 0: self.page_index = 0
        if self.page_index >= len(pages): self.page_index = len(pages) - 1
        
        page = pages[self.page_index]
        
        # Update Text
        full_text = f"{page['title']}\n\n{page['text']}"
        self.text_box.config(text=full_text)
        
        # Update Image
        try:
            img_path = os.path.join("assets", "images", page.get("image", ""))
            if os.path.exists(img_path):
                # Using PIL to resize image for tkinter
                img = Image.open(img_path)
                img = img.resize((250, 250), Image.Resampling.LANCZOS)
                self.photo = ImageTk.PhotoImage(img)
                self.img_label.config(image=self.photo)
            else:
                self.img_label.config(image="", text="[Image Placeholder]") 
        except Exception as e:
            print(f"Error loading image: {e}")
            self.img_label.config(image="", text="[Image Error]")

    def prev_page(self):
        self.page_index -= 1
        self.update_content()
        
    def next_page(self):
        self.page_index += 1
        self.update_content()

    def start_quiz(self):
        self.controller.show_frame("QuizPage")

class QuizPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#ecf0f1")
        self.controller = controller
        self.q_index = 0
        self.score = 0
        
        tk.Label(self, text="Quiz Time!", font=("Arial", 20), bg="#ecf0f1").pack(pady=20)
        
        self.question_label = tk.Label(self, text="", font=("Arial", 14), bg="#ecf0f1", wraplength=600)
        self.question_label.pack(pady=20)
        
        self.var = tk.StringVar()
        self.rb_frame = tk.Frame(self, bg="#ecf0f1")
        self.rb_frame.pack()
        
        tk.Button(self, text="Submit Answer", command=self.check_answer).pack(pady=20)
        tk.Button(self, text="Back to Topic", command=lambda: controller.show_frame("TopicViewer")).pack()

    def refresh(self):
        self.topic_data = TOPICS[self.controller.current_topic_id]
        self.questions = self.topic_data["quiz"]
        self.q_index = 0
        self.score = 0
        self.show_question()

    def show_question(self):
        if self.q_index >= len(self.questions):
            self.finish_quiz()
            return
            
        q = self.questions[self.q_index]
        self.question_label.config(text=f"Q{self.q_index+1}: {q['question']}")
        
        # Clear old radio buttons
        for widget in self.rb_frame.winfo_children():
            widget.destroy()
            
        self.var.set(None)
        for opt in q['options']:
            rb = tk.Radiobutton(self.rb_frame, text=opt, variable=self.var, value=opt, font=("Arial", 12), bg="#ecf0f1")
            rb.pack(anchor="w")

    def check_answer(self):
        q = self.questions[self.q_index]
        if self.var.get() == q['answer']:
            self.score += 1
        self.q_index += 1
        self.show_question()

    def finish_quiz(self):
        save_score(self.topic_data["title"], self.score, len(self.questions))
