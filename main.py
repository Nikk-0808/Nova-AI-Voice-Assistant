import speech_recognition as sr
import webbrowser
import pyttsx3
import music_library
from openai import OpenAI
import pyjokes
import feedparser


# OpenAI api key
client = OpenAI(api_key="your_openai_api_key_here")
  
recognizer = sr.Recognizer()
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

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

    except Exception as e:
        print("RSS error:", e)
        speak("Unable to fetch news.")

def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open instagram" in c.lower():
        webbrowser.open("https://instagram.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")
    elif "open pradhan linkedin" in c.lower():
        webbrowser.open("https://www.linkedin.com/in/nikhilpradhan-08082403nikk/")
    # ...existing code...
    elif c.lower().startswith("play"):
        try:
            song = " ".join(c.split()[1:]).strip().lower()
            link = music_library.music.get(song)
            if link:
                webbrowser.open(link)
                speak(f"Playing {song}")
            else:
                speak("Sorry, I couldn't find that song.")
        except IndexError:
            speak("Please say the song name after 'play'.")
    elif "headline" in c.lower() or "news" in c.lower():
        speak_headlines()

    elif "tell me a joke" in c.lower():   # New jokes feature
        joke = pyjokes.get_joke()
        speak(joke)
    else:
        # Let OpenAI handle unknown commands
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
        except Exception as e:
            print("OpenAI error:", e)
            speak("Sorry, I couldn't understand that.")

if __name__ == "__main__":
    speak("Initializing Nova....")
    while True:
        try:
            with sr.Microphone() as source:
                print("Listening for wake word...")
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=3)
                word = recognizer.recognize_google(audio)
                if word.lower() == "nova":
                    speak("Yes?")
                    with sr.Microphone() as source:
                        print("Nova Active...")
                        audio = recognizer.listen(source)
                        command = recognizer.recognize_google(audio)
                        print("Command received:", command)
                        processCommand(command)
        except Exception as e:
            print("Error:", e)
