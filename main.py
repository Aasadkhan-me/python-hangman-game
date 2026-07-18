"""
ADVANCED INTERACTIVE HANGMAN GAME

Architecture (matches the diagram):
1. get_word_from_api()       -> tries to fetch a random word from the internet
2. get_local_word()          -> backup word list (used if API fails)
3. choose_word()             -> picks difficulty, then gets a word of the right length
4. suggest_middle_letter()   -> NEW: suggests an unguessed letter near the middle of the word
5. display_tracker()         -> shows the current game state to the player (now includes the hint)
6. play_game()               -> the main while-loop that runs everything
"""

import requests
import random

# -------------------------------------------------------------------
# 1. LOCAL BACKUP WORD LISTS (grouped by difficulty)
#    This guarantees the game ALWAYS works, even with no internet.

LOCAL_WORDS = {
    "easy":   ["apple", "chair", "grape", "house", "plant"],
    "medium": ["python", "hangman", "keyboard", "monitor"],
    "hard":   ["difficulty", "programming", "algorithm", "university"],
}

# Difficulty -> (min_length, max_length, lives)
DIFFICULTY_SETTINGS = {
    "easy":   (4, 5, 5),
    "medium": (6, 7, 8),
    "hard":   (8, 10, 11),
}


# 2. TRY TO FETCH A WORD FROM A PUBLIC API

def get_word_from_api(min_len, max_len):

    try:
        # This API returns a list of random words, e.g. ["banana"]
        response = requests.get(
            "https://random-word-api.herokuapp.com/word?number=10",
            timeout=3  # don't let the game hang forever waiting on the internet
        )
        response.raise_for_status()  # raises an error if the request failed
        words = response.json()

        # Filter for a word that matches our difficulty's length range
        candidates = [w.lower() for w in words if min_len <= len(w) <= max_len and w.isalpha()]

        if candidates:
            return random.choice(candidates)
        return None  # no word in the batch matched, fall back to local list

    except (requests.RequestException, ValueError):
        # RequestException covers no internet / timeout / bad status
        # ValueError covers bad JSON
        return None


# 3. CHOOSE THE WORD (API first, local list as fallback)

def choose_word(difficulty):
    min_len, max_len, _ = DIFFICULTY_SETTINGS[difficulty]

    word = get_word_from_api(min_len, max_len)
    if word:
        print("(Word fetched from online API)")
        return word

    print("(API unavailable — using local word list instead)")
    return random.choice(LOCAL_WORDS[difficulty])

# 4. HINT SUGGESTION — suggest a middle character of the word

def suggest_middle_letter(secret_word, guessed_letters):
   
    middle_index = len(secret_word) // 2
    max_distance = len(secret_word)  # how far we're willing to search outward

    for distance in range(max_distance):
        for index in (middle_index - distance, middle_index + distance):
            if 0 <= index < len(secret_word):
                letter = secret_word[index]
                if letter not in guessed_letters:
                    return letter

    return None  # every letter has already been guessed


# 5. DISPLAY TRACKER — shows current progress to the player

def display_tracker(secret_word, guessed_letters, lives, show_hint=False):
    # Build the "_ _ p _ e" style display
    display = " ".join(
        letter if letter in guessed_letters else "_"
        for letter in secret_word
    )
    print("\nWord:    ", display)
    print("Guessed: ", ", ".join(sorted(guessed_letters)) if guessed_letters else "(none yet)")
    print("Lives:   ", "❤️ " * lives, f"({lives} left)")

    # Only print the hint when explicitly asked to (see play_game's hint_used flag)
    if show_hint:
        hint = suggest_middle_letter(secret_word, guessed_letters)
        if hint:
            print(f"Hint:     try the letter '{hint}' (from the middle of the word)")


# 6. MAIN GAME LOOP

def play_game():
    print("=== WELCOME TO HANGMAN ===")
    print("Choose a difficulty: easy / medium / hard")
    difficulty = input("> ").strip().lower()

    while difficulty not in DIFFICULTY_SETTINGS:
        print("Please type exactly: easy, medium, or hard")
        difficulty = input("> ").strip().lower()

    _, _, lives = DIFFICULTY_SETTINGS[difficulty]
    secret_word = choose_word(difficulty)
    guessed_letters = set()
    hint_used = False  # tracks whether we've already shown the one-time hint

    # This is the core while-loop: keep playing until you win or run out of lives
    while lives > 0:
        # Show the hint only once, on the very first turn — not on every loop
        display_tracker(secret_word, guessed_letters, lives, show_hint=not hint_used)
        hint_used = True

        # Check for WIN condition
        if all(letter in guessed_letters for letter in secret_word):
            print(f"\n🎉 You won! The word was '{secret_word}'.")
            return

        guess = input("\nGuess a letter: ").strip().lower()

        # --- Input validation ---
        if len(guess) != 1 or not guess.isalpha():
            print("Please enter a single letter.")
            continue

        if guess in guessed_letters:
            print("You already guessed that letter!")
            continue

        # --- String matching: is the guess in the word? ---
        guessed_letters.add(guess)
        if guess in secret_word:
            print(f"Good guess! '{guess}' is in the word.")
        else:
            lives -= 1
            print(f"Sorry, '{guess}' is not in the word.")

    # If the loop ends because lives == 0, it's a loss
    print(f"\n💀 Game over! The word was '{secret_word}'.")


# ENTRY POINT

if __name__ == "__main__":
    play_game()
