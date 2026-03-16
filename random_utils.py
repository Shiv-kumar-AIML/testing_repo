#!/usr/bin/env python3
"""Random utility functions."""

import random


def get_random_number(min_val: int = 1, max_val: int = 100) -> int:
    """Generate a random integer between min_val and max_val.

    Args:
        min_val: Minimum value (inclusive).
        max_val: Maximum value (inclusive).

    Returns:
        A random integer.
    """
    return random.randint(min_val, max_val)


def get_random_joke() -> str:
    """Return a random joke.

    Returns:
        A string containing a random joke.
    """
    jokes = [
        "Why don't scientists trust atoms? Because they make up everything!",
        "What do you call fake spaghetti? An impasta!",
        "Why did the scarecrow win an award? Because he was outstanding in his field!",
        "What do you get when you cross a snowman and a vampire? Frostbite!",
        "Why don't eggs tell jokes? They'd crack each other up!"
    ]
    return random.choice(jokes)


def random_color() -> str:
    """Return a random color name.

    Returns:
        A random color string.
    """
    colors = ["red", "blue", "green", "yellow", "purple", "orange", "pink", "black", "white"]
    return random.choice(colors)
