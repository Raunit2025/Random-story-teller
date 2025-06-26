# Required modules
import tkinter as tk
from tkinter import ttk, messagebox
import random
import pygame
import threading
import time
from openai import OpenAI

# --- CONFIGURATION ---
client = OpenAI(api_key="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")  # Replace with your secure API key
MUSIC_FILE = "background.mp3"  # Ensure this file exists in the same folder

# --- AI Generators ---

def generate_ai_story(genre, choice=None):
    prompt = f"Write a {genre.lower()} story with interactive choices. " \
             f"Include a point where the user must choose between two options. " \
             f"{'Continue from the choice: ' + choice if choice else ''}"
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You're a creative story generator."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.9,
            max_tokens=500
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ Error generating story:\n{e}"

def generate_ai_joke(category):
    prompt = f"Tell me a funny {category.lower()} joke."
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You're a funny AI joke generator."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.9,
            max_tokens=60
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ Error generating joke:\n{e}"

# --- Music ---
def play_music():
    try:
        pygame.mixer.init()
        pygame.mixer.music.load(MUSIC_FILE)
        pygame.mixer.music.play(-1)
    except:
        print("⚠️ Could not load background music.")

# --- Typing Animation ---
def type_text(text_widget, text, delay=30):
    text_widget.config(state='normal')
    text_widget.delete("1.0", tk.END)
    for char in text:
        text_widget.insert(tk.END, char)
        text_widget.update()
        time.sleep(delay / 1000.0)
    text_widget.config(state='disabled')

# --- Story Tab Logic ---
def start_story():
    genre = genre_var.get()
    if genre == "None":
        messagebox.showwarning("Missing Selection", "Please choose a story genre.")
        return
    story_box.config(state='normal')
    story_box.delete("1.0", tk.END)
    story_box.config(state='disabled')
    threading.Thread(target=lambda: type_text(story_box, generate_ai_story(genre))).start()

# --- Joke Tab Logic ---
def generate_joke():
    category = joke_var.get()
    if category == "None":
        messagebox.showwarning("Missing Selection", "Please choose a joke category.")
        return
    joke_box.config(state='normal')
    joke_box.delete("1.0", tk.END)
    joke_box.config(state='disabled')
    threading.Thread(target=lambda: type_text(joke_box, generate_ai_joke(category), delay=40)).start()

# --- GUI Setup ---
app = tk.Tk()
app.title("AI Story & Joke Generator")
app.geometry("800x600")
app.config(bg="#f0f0f0")

notebook = ttk.Notebook(app)
notebook.pack(pady=10, expand=True)

# --- Story Tab ---
story_tab = tk.Frame(notebook, bg="#ffffff")
notebook.add(story_tab, text="📖 Story Generator")

tk.Label(story_tab, text="Choose a story genre:", bg="#ffffff", font=("Arial", 12)).pack(pady=10)
genre_var = tk.StringVar(value="None")
ttk.Combobox(story_tab, textvariable=genre_var, values=["Adventure", "Horror", "Fantasy", "Sci-fi"], state="readonly").pack()

tk.Button(story_tab, text="Start Story", command=start_story, bg="#4CAF50", fg="white", padx=10, pady=5).pack(pady=10)

story_box = tk.Text(story_tab, wrap="word", height=20, width=90, state="disabled", font=("Arial", 11))
story_box.pack(padx=10, pady=10)

# --- Joke Tab ---
joke_tab = tk.Frame(notebook, bg="#ffffff")
notebook.add(joke_tab, text="🤣 Joke Generator")

tk.Label(joke_tab, text="Choose a joke category:", bg="#ffffff", font=("Arial", 12)).pack(pady=10)
joke_var = tk.StringVar(value="None")
ttk.Combobox(joke_tab, textvariable=joke_var, values=["Tech", "Dad", "Dark", "Knock-knock"], state="readonly").pack()

tk.Button(joke_tab, text="Tell Me a Joke", command=generate_joke, bg="#2196F3", fg="white", padx=10, pady=5).pack(pady=10)

joke_box = tk.Text(joke_tab, wrap="word", height=10, width=90, state="disabled", font=("Arial", 11))
joke_box.pack(padx=10, pady=10)

# --- Start background music ---
threading.Thread(target=play_music, daemon=True).start()

app.mainloop()
