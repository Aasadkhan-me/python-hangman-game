# python-hangman-game
Advanced Python Hangman game with difficulty levels, random word API, hint system, score tracking, and local backup words.

# 🎮 Advanced Interactive Hangman

A terminal-based Hangman game in Python featuring difficulty levels, online word fetching with offline fallback, and a smart hint system.

## Features

- **Difficulty levels** — easy, medium, hard — each with its own word length range and lives
- **Online word fetching** — pulls a random word from a public API, filtered by difficulty
- **Offline fallback** — automatically uses a local word list if the API is unreachable
- **Hint system** — suggests an unguessed letter near the middle of the word (shown once)
- **Live tracker** — displays revealed letters, guessed letters, and remaining lives (❤️) each turn
- **Input validation** — handles invalid or repeated guesses gracefully

## Requirements

- Python 3.7+
- `requests` library

```bash
pip install requests
```

## Usage

```bash
python hangman.py
```

Choose a difficulty, then guess one letter at a time until you reveal the word or run out of lives.

### Example

```
=== WELCOME TO HANGMAN ===
Choose a difficulty: easy / medium / hard
> medium

Word:     _ _ _ _ _ _
Lives:    ❤️ ❤️ ❤️ ❤️ ❤️ ❤️  (6 left)
Hint:     try the letter 'y' (from the middle of the word)

Guess a letter: p
Good guess! 'p' is in the word.
```

## Difficulty Settings

| Difficulty | Word Length | Lives |
|-----------|-------------|-------|
| Easy      | 3–4 letters | 5     |
| Medium    | 6–7 letters | 6     |
| Hard      | 8–9 letters | 5     |

## How It Works

```
get_word_from_api()     → fetches a random word from the internet
choose_word()            → picks a word matching the chosen difficulty
suggest_middle_letter()  → suggests a letter near the middle of the word
display_tracker()        → shows word progress, guesses, and lives
play_game()               → main game loop
```
