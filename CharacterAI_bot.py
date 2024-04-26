from charaiPY.AsyncPyCAI2 import PyAsyncCAI2
import asyncio 
import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
import os
import re
import pygame

owner_id = 'Paste here' # TOKEN 
char = "Paste here" # CHAR ID
chat_id = "Paste here" # CHAT ID

voice = 'en-US-ChristopherNeural'
voice2 = 'en-US-AnaNeural'
voice3 ='en-US-JennyNeural'
voice4 = 'en-IN-NeerjaExpressiveNeural'
voice5 = 'gu-IN-DhwaniNeural'

aut_set ={
    "author_id": "Paste here", # CREATOR 
    "is_human": True, # PLEASE DON'T WRITE TO 
    "name": "Paste here" # YOUR CAI 
}
client = PyAsyncCAI2(owner_id) # IMPORT OWNER 

def get_voice_input():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        # Adjust noise reduction settings based on environment
        recognizer.adjust_for_ambient_noise(source, duration=0.5)  # Adjust duration as needed
        print("Listening...")
        try:
            audio = recognizer.listen(source, phrase_time_limit=5)  # Set a timeout limit
            print("Recognizing...")
            text = recognizer.recognize_google(audio, language='en-IN')
            print(f"You Said: {text}\n")
            return text
        except sr.WaitTimeoutError:
            print("Error: No speech detected within the timeout limit.")
            return None
        except sr.UnknownValueError:
            print("Error: Could not understand audio.")
            return None
        except Exception as e:
            print(f"Error: {e}")
            return None

def remove_text_in_asterisks(text):
    pattern = r'\*([^*]+)\*'
    return re.sub(pattern, '', text)

def translate_to_hindi(dat):
    translator = Translator()
    translation = translator.translate(f'{dat}', dest='hi')
    return translation.text

def text_to_speech(dat):
    dat = remove_text_in_asterisks(dat)
    dat = dat.replace('\n', ' ').replace('\r', '')
    
    if not dat.strip():
        print("Error: Processed text is empty. No audio will be generated.")
        return
    dat = dat.replace('"', r'\"')
    command = f'edge-tts --rate=+15% --voice "{voice3}" --text "{dat}" --write-media "data.mp3"'
    try:
        os.system(command)
        pygame.init()
        pygame.mixer.init()
        if os.path.exists("data.mp3") and os.path.getsize("data.mp3") > 0:
            pygame.mixer.music.load("data.mp3")
            pygame.mixer.music.play()

            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
        else:
            print("Error: The generated audio file is empty or does not exist.")

    except pygame.error as e:
        print(f"pygame.error: {e}")
    except Exception as e:
        print(f"Error in text_to_speech: {e}")
    finally:
        pygame.mixer.music.stop()
        pygame.mixer.quit()
        os.remove("data.mp3")
        return

async def main():
    while True:
        message = input("Enter message: ")
        if message:
            try:
                async with client.connect(owner_id) as chat2:
                    r = await chat2.send_message(char, chat_id, message, aut_set, Return_name=False)
                    #print(r)
                text_to_speech(dat=f"{r}")
            except Exception as e:
                print(f"Error in sending message or processing response: {e}")


asyncio.run(main())
