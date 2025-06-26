# OFFLINE AI STORY & JOKE GENERATOR (No API)
import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
import pygame
import random

# --- CONFIGURATION ---
MUSIC_FILE = "background.mp3"  # Place this file in the same directory

# --- Offline Data ---

story_data = {
    "Adventure": [
        {
            "text": "You find a mysterious map leading to a lost treasure. Do you follow it into the jungle?",
            "choices": ["Yes", "No"],
            "next": {
                "Yes": "You bravely enter the jungle and discover ancient ruins guarded by a sleeping tiger.",
                "No": "You ignore the map and return home, always wondering what could've been."
            }
        }
    ],
    "Horror": [
        {
            "text": "You hear whispers in an abandoned house. Do you investigate the attic or run outside?",
            "choices": ["Investigate", "Run"],
            "next": {
                "Investigate": "In the attic, you find an old diary that tells your future...",
                "Run": "You flee safely, but feel something is now following you in the shadows."
            }
        }
    ],
    "Fantasy": [
        {
            "text": "A wizard offers to teach you magic. Do you accept his offer or decline?",
            "choices": ["Accept", "Decline"],
            "next": {
                "Accept": "You become an apprentice and learn to cast fire from your fingertips.",
                "Decline": "You walk away, but the wizard places a mysterious charm on you..."
            }
        }
    ],
    "Sci-fi": [
        {
            "text": "You receive a message from aliens asking to meet. Do you go alone or inform the government?",
            "choices": ["Go Alone", "Inform Government"],
            "next": {
                "Go Alone": "They grant you interstellar knowledge but erase your memories before returning you.",
                "Inform Government": "The government intercepts the message and starts a secret space mission."
            }
        }
    ]
}

joke_data = {
    "Tech": [
        "Why do Java developers wear glasses? Because they can't C#!",
        "There are 10 types of people: those who understand binary and those who don’t."
    ],
    "Dad": [
        "I'm reading a book on anti-gravity. It's impossible to put down!",
        "Why don't eggs tell jokes? They'd crack each other up."
    ],
    "Dark": [
        "Why don’t graveyards ever get overcrowded? People are dying to get in.",
        "My boss told me to have a good day... so I went home."
    ],
    "Knock-knock": [
        "Knock knock.\nWho's there?\nTank.\nTank who?\nYou're welcome!",
        "Knock knock.\nWho's there?\nBoo.\nBoo who?\nDon’t cry, it’s just a joke!"
    ]
}

# --- Music ---
def play_music():
    try:
        pygame.mixer.init()
        pygame.mixer.music.load(MUSIC_FILE)
        pygame.mixer.music.play(-1)
    except:
        print("⚠️ Background music failed to load.")

# --- Typing Animation ---
def type_text(text_widget, text, delay=30):
    text_widget.config(state='normal')
    text_widget.delete("1.0", tk.END)
    for char in text:
        text_widget.insert(tk.END, char)
        text_widget.update()
        time.sleep(delay / 1000.0)
    text_widget.config(state='disabled')

# --- Story Logic ---
def start_story():
    genre = genre_var.get()
    if genre == "None":
        messagebox.showwarning("Missing Selection", "Please choose a story genre.")
        return

    story = story_data[genre][0]
    current_story.clear()
    current_story.update(story)

    type_text(story_box, story["text"])
    for widget in choice_frame.winfo_children():
        widget.destroy()
    for choice in story["choices"]:
        tk.Button(choice_frame, text=choice, command=lambda c=choice: continue_story(c)).pack(side="left", padx=5)

def continue_story(choice):
    story = current_story
    result = story["next"].get(choice, "The story ends here.")
    type_text(story_box, result)
    for widget in choice_frame.winfo_children():
        widget.destroy()

# --- Joke Logic ---
def generate_joke():
    category = joke_var.get()
    if category == "None":
        messagebox.showwarning("Missing Selection", "Please choose a joke category.")
        return
    joke = random.choice(joke_data[category])
    threading.Thread(target=lambda: type_text(joke_box, joke, delay=40)).start()

# --- GUI Setup ---
app = tk.Tk()
app.title("Offline AI Story & Joke Generator")
app.geometry("800x600")
app.config(bg="#f0f0f0")

current_story = {}


notebook = ttk.Notebook(app)
notebook.pack(pady=10, expand=True)

# --- Story Tab ---
story_tab = tk.Frame(notebook, bg="#ffffff")
notebook.add(story_tab, text="📖 Story Generator")

tk.Label(story_tab, text="Choose a story genre:", bg="#ffffff", font=("Arial", 12)).pack(pady=10)
genre_var = tk.StringVar(value="None")
ttk.Combobox(story_tab, textvariable=genre_var, values=list(story_data.keys()), state="readonly").pack()

tk.Button(story_tab, text="Start Story", command=start_story, bg="#4CAF50", fg="white", padx=10, pady=5).pack(pady=10)

story_box = tk.Text(story_tab, wrap="word", height=15, width=90, state="disabled", font=("Arial", 11))
story_box.pack(padx=10, pady=10)

choice_frame = tk.Frame(story_tab, bg="#ffffff")
choice_frame.pack(pady=5)

# --- Joke Tab ---
joke_tab = tk.Frame(notebook, bg="#ffffff")
notebook.add(joke_tab, text="🤣 Joke Generator")

tk.Label(joke_tab, text="Choose a joke category:", bg="#ffffff", font=("Arial", 12)).pack(pady=10)
joke_var = tk.StringVar(value="None")
ttk.Combobox(joke_tab, textvariable=joke_var, values=list(joke_data.keys()), state="readonly").pack()

tk.Button(joke_tab, text="Tell Me a Joke", command=generate_joke, bg="#2196F3", fg="white", padx=10, pady=5).pack(pady=10)

joke_box = tk.Text(joke_tab, wrap="word", height=10, width=90, state="disabled", font=("Arial", 11))
joke_box.pack(padx=10, pady=10)

# --- Start background music ---
threading.Thread(target=play_music, daemon=True).start()

app.mainloop()

