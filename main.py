import speech_recognition as sr
import webbrowser
import pyttsx3
import music_library
from openai import OpenAI
import pyjokes
import feedparser
import datetime
import os
import pyautogui
import wikipedia

client = OpenAI(api_key="your_openai_api_key_here")

recognizer = sr.Recognizer()
engine = pyttsx3.init()

last_response = ""

def remember(text):
    global last_response
    last_response = text

def speak(text):
    remember(text)
    engine.say(text)
    engine.runAndWait()

def wishme():
    hour = datetime.datetime.now().hour
    speak("Welcome back.")
    if 4 <= hour < 12:
        speak("Good morning.")
    elif 12 <= hour < 16:
        speak("Good afternoon.")
    elif 16 <= hour < 24:
        speak("Good evening.")
    else:
        speak("Good night.")
    speak("Nova at your service.")

def tell_time():
    current_time = datetime.datetime.now().strftime("%I:%M %p")
    speak(f"The current time is {current_time}")

def tell_date():
    today = datetime.datetime.now()
    speak(f"Today's date is {today.day} {today.strftime('%B')} {today.year}")

def take_screenshot():
    path = os.path.expanduser("~/Pictures/nova_screenshot.png")
    img = pyautogui.screenshot()
    img.save(path)
    speak("Screenshot taken and saved.")

def search_wikipedia(query):
    try:
        speak("Searching Wikipedia.")
        result = wikipedia.summary(query, sentences=2)
        speak(result)
    except wikipedia.exceptions.DisambiguationError:
        speak("Please be more specific.")
    except:
        speak("I could not find anything.")

def speak_headlines():
    try:
        feed_url = "https://news.google.com/rss?hl=en-IN&gl=IN&ceid=IN:en"
        feed = feedparser.parse(feed_url)
        if not feed.entries:
            speak("No news available right now.")
            return
        speak("Here are the top headlines.")
        for entry in feed.entries[:5]:
            speak(entry.title)
    except:
        speak("Unable to fetch news.")

def processCommand(c):
    c = c.lower()

    if "time" in c:
        tell_time()

    elif "date" in c:
        tell_date()

    elif "screenshot" in c:
        take_screenshot()

    elif "repeat" in c or "say that again" in c:
        if last_response:
            speak(last_response)
        else:
            speak("I have nothing to repeat.")

    elif "wikipedia" in c:
        topic = c.replace("wikipedia", "").strip()
        search_wikipedia(topic)

    elif "open notepad" in c:
        os.startfile("notepad.exe")

    elif "open calculator" in c:
        os.startfile("calc.exe")

    elif "open command prompt" in c:
        os.system("start cmd")

    elif "open vscode" in c:
        os.startfile("code")

    elif "open google" in c:
        webbrowser.open("https://google.com")

    elif "open instagram" in c:
        webbrowser.open("https://instagram.com")

    elif "open youtube" in c:
        webbrowser.open("https://youtube.com")

    elif "open linkedin" in c:
        webbrowser.open("https://linkedin.com")

    elif "open pradhan linkedin" in c:
        webbrowser.open("https://www.linkedin.com/in/nikhilpradhan-08082403nikk/")

    elif c.startswith("play"):
        song = " ".join(c.split()[1:]).strip()
        link = music_library.music.get(song)
        if link:
            webbrowser.open(link)
            speak(f"Playing {song}")
        else:
            speak("Sorry, I couldn't find that song.")

    elif "headline" in c or "news" in c:
        speak_headlines()

    elif "tell me a joke" in c:
        speak(pyjokes.get_joke())

    elif "shutdown" in c:
        speak("Shutting down the system. Goodbye.")
        os.system("shutdown /s /f /t 1")

    elif "restart" in c:
        speak("Restarting the system.")
        os.system("shutdown /r /f /t 1")

    elif "exit" in c or "offline" in c or "stop" in c:
        speak("Going offline. Have a good day.")
        exit()

    else:
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a virtual assistant named Nova."},
                    {"role": "user", "content": c}
                ]
            )
            reply = response.choices[0].message['content']
            speak(reply)
        except:
            speak("Sorry, I couldn't understand that.")

if __name__ == "__main__":
    wishme()
    while True:
        try:
            with sr.Microphone() as source:
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=3)
                word = recognizer.recognize_google(audio)
                if word.lower() == "nova":
                    speak("Yes?")
                    with sr.Microphone() as source:
                        audio = recognizer.listen(source)
                        command = recognizer.recognize_google(audio)
                        processCommand(command)
        except:
            pass
