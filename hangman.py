import tkinter as tk
from tkinter import messagebox, simpledialog
import random

# Word bank with categories
word_bank = {
    "Animals": ["elephant", "giraffe", "kangaroo", "penguin", "alligator"],
    "Movies": ["inception", "titanic", "gladiator", "avatar", "coco"],
    "Technology": ["python", "internet", "laptop", "keyboard", "robotics"]
}

# Game variables
chosen_word = ""
previous_word = ""  # To track the last word used
guessed_letters = set()
attempts_left = 6
hint_used = False
score = 0
leaderboard = {}  # Stores player names and their scores

# Function to reset the game
def reset_game():
    global chosen_word, guessed_letters, attempts_left, hint_used, previous_word
    category = category_var.get()
    if not category:
        messagebox.showwarning("Warning", "Please select a category!")
        return
    
    # Ensure the new word is different from the previous one
    while True:
        chosen_word = random.choice(word_bank[category])
        if chosen_word != previous_word:
            previous_word = chosen_word
            break

    guessed_letters.clear()
    attempts_left = 6
    hint_used = False
    update_game_display()

# Function to update the game display
def update_game_display():
    word_display = " ".join(
        [letter if letter in guessed_letters else "_" for letter in chosen_word]
    )
    word_label.config(text=word_display)
    attempts_label.config(text=f"Attempts left: {attempts_left}")
    guessed_label.config(
        text=f"Guessed letters: {', '.join(sorted(guessed_letters))}"
    )
    hangman_canvas.delete("all")
    draw_hangman(attempts_left)

# Function to process the guessed letter
def guess_letter():
    global attempts_left, score
    letter = letter_entry.get().lower()
    letter_entry.delete(0, tk.END)  # Clear entry field
    if len(letter) != 1 or not letter.isalpha():
        messagebox.showerror("Invalid Input", "Please enter a single letter.")
        return
    if letter in guessed_letters:
        messagebox.showinfo("Already Guessed", f"You've already guessed '{letter}'.")
        return

    guessed_letters.add(letter)
    if letter in chosen_word:
        score += 10  # Award points for correct guesses
        messagebox.showinfo("Correct!", f"Good job! The word contains '{letter}'.")
    else:
        attempts_left -= 1
        messagebox.showinfo("Incorrect!", f"Oops! The word does not contain '{letter}'.")

    if attempts_left == 0:
        hangman_canvas.create_text(
            100, 100, text="Game Over!", fill="red", font=("Helvetica", 24, "bold")
        )
        messagebox.showerror("Game Over", f"You've been hanged! The word was: {chosen_word}")
        add_to_leaderboard()
        reset_game()
    elif all(letter in guessed_letters for letter in chosen_word):
        score += 50  # Bonus points for guessing the word
        messagebox.showinfo("Congratulations", f"You guessed the word: {chosen_word}")
        add_to_leaderboard()
        reset_game()
    else:
        update_game_display()

# Function to use a hint
def use_hint():
    global hint_used, score
    if hint_used:
        messagebox.showinfo("Hint Used", "You have already used your hint.")
        return
    for letter in chosen_word:
        if letter not in guessed_letters:
            guessed_letters.add(letter)
            hint_used = True
            score -= 10  # Deduct points for using a hint
            update_game_display()
            messagebox.showinfo("Hint", f"The word contains the letter '{letter}'.")
            return

# Function to draw the hangman on the canvas
def draw_hangman(attempts_left):
    parts = [
        lambda: hangman_canvas.create_oval(80, 50, 120, 90, fill="black"),  # Head
        lambda: hangman_canvas.create_line(100, 90, 100, 150, fill="black", width=2),  # Body
        lambda: hangman_canvas.create_line(100, 110, 80, 130, fill="black", width=2),  # Left Arm
        lambda: hangman_canvas.create_line(100, 110, 120, 130, fill="black", width=2),  # Right Arm
        lambda: hangman_canvas.create_line(100, 150, 80, 180, fill="black", width=2),  # Left Leg
        lambda: hangman_canvas.create_line(100, 150, 120, 180, fill="black", width=2),  # Right Leg
    ]
    for i in range(6 - attempts_left):
        parts[i]()

# Function to add the player's score to the leaderboard
def add_to_leaderboard():
    global score
    player_name = simpledialog.askstring("Name", "Enter your name for the leaderboard:")
    if player_name:
        if player_name in leaderboard:
            leaderboard[player_name] += score
        else:
            leaderboard[player_name] = score
        score = 0  # Reset score after adding to leaderboard
        show_leaderboard()

# Function to display the leaderboard
def show_leaderboard():
    leaderboard_window = tk.Toplevel(root)
    leaderboard_window.title("Leaderboard")
    leaderboard_window.geometry("300x300")
    leaderboard_window.configure(bg="black")

    tk.Label(leaderboard_window, text="Leaderboard", font=("Helvetica", 16), bg="black", fg="white").pack(pady=10)

    sorted_leaderboard = sorted(leaderboard.items(), key=lambda x: x[1], reverse=True)
    for rank, (name, score) in enumerate(sorted_leaderboard, start=1):
        tk.Label(
            leaderboard_window,
            text=f"{rank}. {name}: {score} points",
            font=("Helvetica", 12),
            bg="black",
            fg="white"
        ).pack(pady=2)

# GUI setup
root = tk.Tk()
root.title("Hangman Game")
root.configure(bg="black")

# Frames for layout
top_frame = tk.Frame(root, bg="black")
top_frame.pack(pady=10)
middle_frame = tk.Frame(root, bg="black")
middle_frame.pack(pady=20)
bottom_frame = tk.Frame(root, bg="black")
bottom_frame.pack(pady=10)

# Category selection
category_var = tk.StringVar()
category_label = tk.Label(top_frame, text="Select a Category:", bg="black", fg="white", font=("Helvetica", 12))
category_label.pack()
category_menu = tk.OptionMenu(top_frame, category_var, *word_bank.keys())
category_menu.pack()

# Word display
word_label = tk.Label(middle_frame, text="", font=("Helvetica", 24), bg="black", fg="white")
word_label.pack(pady=10)

# Hangman canvas
hangman_canvas = tk.Canvas(middle_frame, width=200, height=200, bg="white")
hangman_canvas.pack()

# Attempts and guessed letters
attempts_label = tk.Label(middle_frame, text="Attempts left: 6", bg="black", fg="white", font=("Helvetica", 12))
attempts_label.pack(pady=5)
guessed_label = tk.Label(middle_frame, text="Guessed letters: ", bg="black", fg="white", font=("Helvetica", 12))
guessed_label.pack(pady=5)

# Guess input
letter_label = tk.Label(bottom_frame, text="Enter a letter:", bg="black", fg="white")
letter_label.grid(row=0, column=0, padx=5)
letter_entry = tk.Entry(bottom_frame)
letter_entry.grid(row=0, column=1, padx=5)
guess_button = tk.Button(bottom_frame, text="Guess", command=guess_letter)
guess_button.grid(row=0, column=2, padx=5)

# Hint and Reset buttons
hint_button = tk.Button(bottom_frame, text="Use Hint", command=use_hint)
hint_button.grid(row=1, column=0, columnspan=1, pady=10)
reset_button = tk.Button(bottom_frame, text="Start Game", command=reset_game)
reset_button.grid(row=1, column=1, pady=10)
leaderboard_button = tk.Button(bottom_frame, text="Leaderboard", command=show_leaderboard)
leaderboard_button.grid(row=1, column=2, pady=10)

# Start the GUI
reset_game()
root.mainloop()
