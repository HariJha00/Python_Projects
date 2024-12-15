import datetime
import os
import webbrowser
import openai
import speech_recognition as sr
from config import apikey

chat_history = ""  # To store conversation history


def chat(query):
    """Handles conversation with OpenAI's API."""
    global chat_history
    try:
        openai.api_key = apikey
        chat_history += f"User: {query}\nJarvis: "
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=chat_history,
            temperature=0.7,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        reply = response["choices"][0]["text"].strip()
        chat_history += reply + "\n"
        say(reply)
        return reply
    except Exception as e:
        say("Sorry, I encountered an error while processing your request.")
        print(f"Error in chat(): {e}")
        return "Error"


def ai(prompt):
    """Saves OpenAI-generated responses for prompts containing 'artificial intelligence'."""
    try:
        openai.api_key = apikey
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            temperature=0.7,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        text = f"OpenAI response for Prompt: {prompt}\n{'*' * 25}\n\n{response['choices'][0]['text']}"
        if not os.path.exists("Openai"):
            os.mkdir("Openai")
        filename = f"Openai/{prompt.replace(' ', '_')[:50]}.txt"
        with open(filename, "w") as f:
            f.write(text)
        say("Response saved successfully.")
    except Exception as e:
        say("Sorry, I couldn't process your request.")
        print(f"Error in ai(): {e}")


def say(text):
    """Converts text to speech."""
    try:
        os.system(f'say "{text}"')  # macOS-specific TTS command
    except Exception as e:
        print(f"Error in say(): {e}")


def take_command():
    """Captures voice input from the user."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            print("Recognizing...")
            query = recognizer.recognize_google(audio, language="en-in")
            print(f"User said: {query}")
            return query
        except sr.WaitTimeoutError:
            say("I didn't hear anything. Please try again.")
            return None
        except sr.UnknownValueError:
            say("Sorry, I couldn't understand you.")
            return None
        except Exception as e:
            print(f"Error in take_command(): {e}")
            return None


if __name__ == '__main__':
    print('Welcome to Jarvis AI')
    say("Welcome to Jarvis AI!")
    while True:
        query = take_command()
        if query:
            query = query.lower()

            # Open predefined websites
            sites = {
                "youtube": "https://www.youtube.com",
                "wikipedia": "https://www.wikipedia.com",
                "google": "https://www.google.com"
            }
            for site, url in sites.items():
                if f"open {site}" in query:
                    say(f"Opening {site}...")
                    webbrowser.open(url)
                    break

            # Play music
            if "play music" in query:
                music_path = os.path.expanduser("~/Downloads/sample-music.mp3")
                if os.path.exists(music_path):
                    os.system(f"open '{music_path}'")
                else:
                    say("Sorry, I couldn't find the music file.")

            # Announce the time
            elif "the time" in query:
                now = datetime.datetime.now()
                time_string = now.strftime("%H:%M")
                say(f"The time is {time_string}.")

            # Open applications
            elif "open facetime" in query:
                os.system("open /System/Applications/FaceTime.app")

            elif "open pass" in query:
                os.system("open /Applications/Passky.app")

            # AI-based responses
            elif "using artificial intelligence" in query:
                ai(prompt=query)

            # Reset chat history
            elif "reset chat" in query:
                chat_history = ""
                say("Chat history reset.")

            # Exit
            elif "quit" in query or "exit" in query:
                say("Goodbye!")
                break

            # Chat
            else:
                chat(query)
