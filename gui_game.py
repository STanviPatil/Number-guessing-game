import tkinter as tk
from tkinter import messagebox
from tkinter.font import Font
import random

class NumberGuessingGameApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Number Guessing Game 🎯")
        self.geometry("500x600")
        self.configure(bg="#0D0907")
        self.resizable(False, False)

        self.gaming_font = Font(family="Arial Black", size=20, weight="bold")
        self.label_font = Font(family="Helvetica", size=14)
        self.button_font = Font(family="Helvetica", size=12, weight="bold")

        self.container = tk.Frame(self, bg="#0D0907")
        self.container.place(relx=0.5, rely=0.5, anchor="center")

        self.player_name = ""
        self.selected_difficulty = None
        self.number_to_guess = 0
        self.max_attempts = 0
        self.attempts_left = 0
        self.hint_used = False

        self.time_left = 0
        self.timer_id = None
        self.total_duration = 0

        self.show_name_input()

    def clear_container(self):
        for widget in self.container.winfo_children():
            widget.destroy()
        if self.timer_id:
            self.after_cancel(self.timer_id)
            self.timer_id = None

    def show_name_input(self):
        self.clear_container()

        header = tk.Label(self.container, text="🎮 Number Guessing Game", font=self.gaming_font, fg="white", bg="#0D0907")
        header.pack(pady=(0, 20))

        info_label = tk.Label(self.container, text="Let's test your brain with some numbers!", font=("Helvetica", 15, "italic"), fg="white", bg="#0D0907")
        info_label.pack(pady=(0, 20))

        tk.Label(self.container, text="Enter your name to begin:", font=self.label_font, fg="white", bg="#0D0907").pack()

        self.name_entry = tk.Entry(self.container, font=("Helvetica", 14), width=30, justify="center", bd=2, relief="groove")
        self.name_entry.pack(pady=15)

        start_btn = tk.Button(self.container, text="▶ Start Game", font=self.button_font, bg="#4A90E2", fg="white", activebackground="#357ABD", command=self.start_game)
        start_btn.pack(pady=10)

    def start_game(self):
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showwarning("Name Required", "Please enter your name to continue.")
            return
        self.player_name = name
        self.show_difficulty_selection()

    def show_difficulty_selection(self):
        self.clear_container()

        tk.Label(self.container, text=f"Welcome, {self.player_name}!", font=self.gaming_font, fg="white", bg="#0D0907").pack(pady=(0, 30))

        tk.Label(self.container, text="Choose your difficulty:", font=("Helvetica", 14, "bold"), fg="white", bg="#0D0907").pack(pady=(0, 15))

        self.diff_frame = tk.Frame(self.container, bg="#0D0907")
        self.diff_frame.pack()

        self.diff_buttons = {}

        self.diff_buttons['easy'] = tk.Button(self.diff_frame, text="🟢 Easy (1–20)", font=self.button_font, width=25, bg="#e0e0e0", command=lambda: self.select_difficulty('easy', 1, 20))
        self.diff_buttons['easy'].pack(pady=7)

        self.diff_buttons['medium'] = tk.Button(self.diff_frame, text="🟡 Medium (1–50)", font=self.button_font, width=25, bg="#e0e0e0", command=lambda: self.select_difficulty('medium', 1, 50))
        self.diff_buttons['medium'].pack(pady=7)

        self.diff_buttons['hard'] = tk.Button(self.diff_frame, text="🔴 Hard (1–100)", font=self.button_font, width=25, bg="#e0e0e0", command=lambda: self.select_difficulty('hard', 1, 100))
        self.diff_buttons['hard'].pack(pady=7)

        self.play_button = tk.Button(self.container, text="🎲 Let's Play!", font=self.button_font, bg="#4CAF50", fg="white", width=20, command=self.start_guessing_game)

    def select_difficulty(self, level, low, high):
        self.selected_difficulty = (level, low, high)

        for key, btn in self.diff_buttons.items():
            btn.configure(bg="#e0e0e0", fg="black")

        colors = {'easy': '#9EFF9E', 'medium': '#FFF799', 'hard': '#FFA1A1'}
        self.diff_buttons[level].configure(bg=colors[level], fg="black")

        if not self.play_button.winfo_ismapped():
            self.play_button.pack(pady=30)

    def start_guessing_game(self):
        level, low, high = self.selected_difficulty
        self.number_to_guess = random.randint(low, high)
        self.max_attempts = self.attempts_left = round((high - low + 1) ** 0.5)
        self.hint_used = False
        self.low = low
        self.high = high
        timer_values = {'easy': 45, 'medium': 65, 'hard': 95}
        self.time_left = timer_values[level]
        self.total_duration = self.time_left

        self.show_guessing_screen()
        self.update_timer()

    def show_guessing_screen(self):
        self.clear_container()

        self.prompt_label = tk.Label(self.container, text=f"Guess a number between {self.low} and {self.high}", font=("Helvetica", 18, "bold"), fg="white", bg="#0D0907")
        self.prompt_label.pack(pady=(0, 20))

        self.name_label = tk.Label(self.container, text=f"Player: {self.player_name}", font=("Helvetica", 16, "bold"), fg="skyblue", bg="#0D0907")
        self.name_label.pack()

        self.attempts_label = tk.Label(self.container, text=f"Attempts Left: {self.attempts_left}", font=("Helvetica", 14), fg="skyblue", bg="#0D0907")
        self.attempts_label.pack(pady=(5, 10))

        self.timer_label = tk.Label(self.container, text=f"Time Left: {self.time_left}s", font=("Helvetica", 14), fg="orange", bg="#0D0907")
        self.timer_label.pack(pady=(0, 15))

        self.guess_entry = tk.Entry(self.container, font=("Helvetica", 14), width=20, justify="center", bd=2, relief="groove")
        self.guess_entry.pack(pady=10)

        self.result_label = tk.Label(self.container, text="", font=("Helvetica", 13, "bold"), fg="white", bg="#0D0907")
        self.result_label.pack(pady=(10, 5))

        self.hint_label = tk.Label(self.container, text="", font=("Helvetica", 12, "italic"), fg="gold", bg="#0D0907")
        self.hint_label.pack()

        btn_frame = tk.Frame(self.container, bg="#0D0907")
        btn_frame.pack(pady=20)

        guess_btn = tk.Button(btn_frame, text="🎯 Submit Guess", font=self.button_font, bg="#4A90E2", fg="white", command=self.check_guess)
        guess_btn.pack(side="left", padx=10)

        hint_btn = tk.Button(btn_frame, text="💡 Hint", font=self.button_font, bg="#FFA500", fg="white", command=self.show_hint)
        hint_btn.pack(side="left", padx=10)

    def update_timer(self):
        if self.time_left > 0:
            self.timer_label.config(text=f"Time Left: {self.time_left}s")
            self.time_left -= 1
            self.timer_id = self.after(1000, self.update_timer)
        else:
            self.timer_label.config(text="Time's up!")
            self.result_label.config(text=f"⏰ Time's up! Number was {self.number_to_guess}.", fg="red")
            self.guess_entry.config(state="disabled")
            self.show_game_over_screen(win=False)

    def show_hint(self):
        if self.hint_used:
            self.hint_label.config(text="Hint already used!")
            return

        self.hint_used = True
        number = self.number_to_guess
        hints = []

        hints.append(f"The number is {'even' if number % 2 == 0 else 'odd'}.")
        if number % 3 == 0:
            hints.append("It's divisible by 3.")
        elif number % 5 == 0:
            hints.append("It's divisible by 5.")

        midpoint = (self.low + self.high) // 2
        if number <= midpoint:
            hints.append("It's in the lower half.")
        else:
            hints.append("It's in the upper half.")

        self.hint_label.config(text=random.choice(hints))

    def check_guess(self):
        guess = self.guess_entry.get().strip()
        if not guess.isdigit():
            self.result_label.config(text="Please enter a valid number.")
            return

        guess = int(guess)

        if self.attempts_left <= 0 or (self.timer_id is None and self.time_left <= 0):
            return

        self.attempts_left -= 1
        self.attempts_label.config(text=f"Attempts Left: {self.attempts_left}")

        if guess == self.number_to_guess:
            if self.timer_id:
                self.after_cancel(self.timer_id)
                self.timer_id = None
            self.show_game_over_screen(win=True)
        elif guess < self.number_to_guess:
            self.result_label.config(text="📉 Too low!", fg="white")
        else:
            self.result_label.config(text="📈 Too high!", fg="white")

        if self.attempts_left > 0 and guess != self.number_to_guess:
            self.guess_entry.delete(0, tk.END)

        if self.attempts_left == 0 and guess != self.number_to_guess:
            if self.timer_id:
                self.after_cancel(self.timer_id)
                self.timer_id = None
            self.show_game_over_screen(win=False)

    def show_game_over_screen(self, win):
        self.clear_container()

        result_text = "🎉 You Win!" if win else "😞 You Lose!"
        result_color = "#00FF00" if win else "#FF4C4C"
        attempts_used = self.max_attempts - self.attempts_left
        time_used = self.total_duration - self.time_left

        tk.Label(self.container, text=result_text, font=("Arial Black", 26, "bold"), fg=result_color, bg="#0D0907").pack(pady=(30, 10))

        tk.Label(self.container, text=f"The number was: {self.number_to_guess}", font=("Helvetica", 16, "bold"), fg="white", bg="#0D0907").pack(pady=10)

        tk.Label(self.container, text=f"Attempts Used: {attempts_used} / {self.max_attempts}", font=("Helvetica", 14), fg="skyblue", bg="#0D0907").pack(pady=5)

        tk.Label(self.container, text=f"Time Taken: {time_used} sec / {self.total_duration} sec", font=("Helvetica", 14), fg="orange", bg="#0D0907").pack(pady=5)

        btn_frame = tk.Frame(self.container, bg="#0D0907")
        btn_frame.pack(pady=30)

        play_again_btn = tk.Button(btn_frame, text="🔁 Play Again", font=self.button_font, bg="#4CAF50", fg="white", command=self.show_name_input)
        play_again_btn.pack(side="left", padx=10)

        exit_btn = tk.Button(btn_frame, text="❌ Exit", font=self.button_font, bg="#FF5C5C", fg="white", command=self.destroy)
        exit_btn.pack(side="left", padx=10)

if __name__ == "__main__":
    app = NumberGuessingGameApp()
    app.mainloop()