import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests
from gtts import gTTS
import pygame
import os
import edge_tts
import asyncio

# pip install pocketsphinx
# pip install requests speechrecognition pyttsx3 gtts pygame pyaudio

recognizer = sr.Recognizer()
engine = pyttsx3.init()




async def generate_voice(text):
    communicate = edge_tts.Communicate(
        text,
        voice="en-IN-PrabhatNeural"   # Male Indian voice
    )
    await communicate.save("temp.mp3")


def speak(text):

    asyncio.run(generate_voice(text))

    pygame.mixer.init()

    pygame.mixer.music.load("temp.mp3")
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    pygame.mixer.music.unload()

    os.remove("temp.mp3")


# -----------------------------
# TinyLlama AI Function
# -----------------------------
def aiProcess(command):

    prompt = f"""
You are Gojo, a smart virtual assistant like Alexa.
Give very short and helpful responses.

User: {command}
Gojo:
"""

    try:
        response = requests.post(
            "http://127.0.0.1:11434/api/generate",
            json={
                "model": "tinyllama:latest",
                "prompt": prompt,
                "stream": False
            },
            timeout=60
        )

        response.raise_for_status()

        result = response.json()

        return result.get("response", "No response from model.")

    except requests.exceptions.RequestException as e:
        return f"Ollama Error: {e}"


# -----------------------------
# Command Processing
# -----------------------------
def processCommand(c):

    c = c.lower()

    if "open google" in c:
        webbrowser.open("https://google.com")
        return "Opening Google"

    elif "open youtube" in c:
          webbrowser.open("https://youtube.com")
          return "Opening YouTube"

    elif "open chatgpt" in c:
          webbrowser.open("https://chatgpt.com")
          return "Opening ChatGPT"

    elif "open linkedin" in c:
          webbrowser.open("https://linkedin.com")
          return "Opening LinkedIn"

    elif c.startswith("play"):

        try:
            song = c.split(" ")[1]
            link = musicLibrary.music[song]
            webbrowser.open(link)

        except:
            speak("Song not found")

    

        if r.status_code == 200:

            data = r.json()
            articles = data.get('articles', [])

            for article in articles[:5]:
                speak(article['title'])

    else:
        output = aiProcess(c)
        print(output)
        speak(output)
        return output

def process_text_command(command):
    try:
        return processCommand(command)
    except Exception as e:
        return str(e)

# -----------------------------
# Main Program
# -----------------------------
if __name__ == "__main__":

    speak("Satoru Gojo aapki baat sun raha hai, kripaya boliye.")

    while True:

        r = sr.Recognizer()

        print("Recognizing...")

        try:
            with sr.Microphone() as source:

                print("Listening for wake word...")
                audio = r.listen(source, timeout=2, phrase_time_limit=2)

            word = r.recognize_google(audio)

            if word.lower() == "gojo":

                speak("haan, boliye")

                with sr.Microphone() as source:

                    print("Gojo Active...")
                    audio = r.listen(source)

                    command = r.recognize_google(audio)

                    print("Command:", command)

                    processCommand(command)

        except Exception as e:
            print(f"Error: {e}")