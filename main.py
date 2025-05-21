import random
import math
import json
import os

STATS_FILE = "game_stats.json"

# Initialize stats
stats = {
    "total_games": 0,
    "wins": 0,
    "losses": 0
}

def load_stats():
    if os.path.exists(STATS_FILE):
        with open(STATS_FILE, "r") as f:
            try:
                loaded_stats = json.load(f)
                stats.update(loaded_stats)
            except json.JSONDecodeError:
                print("⚠️ Stats file corrupted, starting fresh.")
    else:
        print("📁 No stats file found, starting fresh.")

def save_stats():
    with open(STATS_FILE, "w") as f:
        json.dump(stats, f)

def get_input(prompt):
    while True:
        user_input = input(prompt).strip().lower()
        if user_input == "hint":
            return "hint"
        try:
            return int(user_input)
        except ValueError:
            print("Invalid input! Enter a number or type 'hint'.")

def select_difficulty():
    print("\nSelect Difficulty Level:")
    print("1. Easy (1–20)")
    print("2. Medium (1–50)")
    print("3. Hard (1–100)")
    
    while True:
        choice = input("Enter 1, 2, or 3: ").strip()
        if choice == "1":
            return 1, 20
        elif choice == "2":
            return 1, 50
        elif choice == "3":
            return 1, 100
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

def give_hint(number, lower, upper):
    hints = []
    hints.append(f"The number is {'even' if number % 2 == 0 else 'odd'}.")
    if number % 3 == 0:
        hints.append("The number is divisible by 3.")
    elif number % 5 == 0:
        hints.append("The number is divisible by 5.")
    midpoint = (lower + upper) // 2
    if number <= midpoint:
        hints.append("The number is in the lower half of the range.")
    else:
        hints.append("The number is in the upper half of the range.")
    return random.choice(hints)

def play_game():
    stats["total_games"] += 1

    lower, upper = select_difficulty()
    number_to_guess = random.randint(lower, upper)
    total_chances = math.ceil(math.log(upper - lower + 1, 2))

    print(f"\n🧠 Guess the number between {lower} and {upper}")
    print(f"📌 You have {total_chances} chances to guess it!")
    print("💡 Type 'hint' once during the game to get a helpful hint.\n")

    attempts = 0
    guessed_correctly = False
    hint_used = False
    guess_history = []

    while attempts < total_chances:
        user_input = get_input(f"Attempt {attempts + 1} - Your guess (or 'hint'): ")

        if user_input == "hint":
            if not hint_used:
                print(f"\n🧩 Hint: {give_hint(number_to_guess, lower, upper)}\n")
                hint_used = True
            else:
                print("❗ You already used your hint.\n")
            continue

        guess = user_input
        guess_history.append(guess)
        attempts += 1

        if guess == number_to_guess:
            print(f"\n🎉 Congratulations! You guessed it in {attempts} tries.")
            guessed_correctly = True
            stats["wins"] += 1
            break
        elif guess < number_to_guess:
            print("📉 Too low!")
        else:
            print("📈 Too high!")

    if not guessed_correctly:
        print(f"\n❌ You've used all your chances! The number was {number_to_guess}.")
        print("💡 Better Luck Next Time!")
        stats["losses"] += 1

    print("\n📝 Your guesses:", ', '.join(str(g) for g in guess_history))

def main():
    print("🎮 Welcome to the Number Guessing Game!")
    load_stats()
    print(f"📊 Your saved stats - Played: {stats['total_games']}, Wins: {stats['wins']}, Losses: {stats['losses']}\n")
    while True:
        play_game()
        print(f"\n📊 Game Stats: Played: {stats['total_games']} | Wins: {stats['wins']} | Losses: {stats['losses']}")
        save_stats()
        replay = input("\n🔁 Do you want to play again? (yes/no): ").strip().lower()
        if replay not in ("yes", "y"):
            print("\n👋 Thanks for playing! Goodbye!")
            break

if __name__ == "__main__":
    main()
