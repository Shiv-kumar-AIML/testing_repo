#!/usr/bin/env python3
"""Voice assistance utilities for the chatbot."""

import os
import speech_recognition as sr
import pyttsx3
from langchain_core.tools import tool


class VoiceAssistant:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        # Configure voice settings
        voices = self.engine.getProperty('voices')
        
        print("shiv")
        print("shiv")
        if voices:
            self.engine.setProperty('voice', voices[0].id)  # Use first available voice
        self.engine.setProperty('rate', 180)  # Speed of speech

    def listen(self) -> str:
        """Listen for voice input and convert to text."""
        with sr.Microphone() as source:
            print("Listening... (speak now)")
            self.recognizer.adjust_for_ambient_noise(source)
            try:
                audio = self.recognizer.listen(source, timeout=5)
                text = self.recognizer.recognize_google(audio)
                print(f"You said: {text}")
                return text
            except sr.WaitTimeoutError:
                return ""
            except sr.UnknownValueError:
                print("Could not understand audio")
                return ""
            except sr.RequestError as e:
                print(f"Speech recognition error: {e}")
                return ""

    def speak(self, text: str) -> None:
        """Convert text to speech and play it."""
        self.engine.say(text)
        self.engine.runAndWait()

    def random_fun_fact(self) -> str:
        """Speak a random fun fact."""
        import random
        fun_facts = [
            "Did you know that honey never spoils?",
            "Octopuses have three hearts.",
            "A group of flamingos is called a flamboyance.",
            "Bananas are berries, but strawberries aren't.",
            "The shortest war in history lasted only 38-45 minutes."
        ]
        fact = random.choice(fun_facts)
        self.speak(fact)
        return f"Spoke random fact: {fact}"


# Global instance
voice = VoiceAssistant()


@tool
def voice_input_tool() -> str:
    """Get voice input from the user.

    Returns:
        Transcribed text from speech.
    """
    return voice.listen()


@tool
def voice_output_tool(text: str) -> str:
    """Speak the given text aloud.

    Args:
        text: The text to speak.

    Returns:
        Confirmation message.
    """
    voice.speak(text)
    return f"Spoken: {text}"


@tool
def random_fun_fact_tool() -> str:
    """Speak a random fun fact aloud.

    Returns:
        Confirmation message.
    """
    return voice.random_fun_fact()
