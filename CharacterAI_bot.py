import os
from characterai import aiocai  # Importing necessary libraries
import asyncio
import re
from gtts import gTTS
import pygame


def speak(message):
    # Function to convert text to speech and play the audio
    tts = gTTS(message, lang='hi')  # Creating gTTS object for Hindi text-to-speech conversion
    tts.save("data.mp3")  # Saving the generated audio file

    try:
        pygame.init()  # Initializing Pygame
        pygame.mixer.init()  # Initializing Pygame mixer

        # Checking if the audio file exists and is not empty
        if os.path.exists("data.mp3") and os.path.getsize("data.mp3") > 0:
            pygame.mixer.music.load("data.mp3")  # Loading the audio file
            pygame.mixer.music.play()  # Playing the audio

            # Waiting for the audio playback to finish
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
        else:
            print("Error: The generated audio file is empty or does not exist.")

    except pygame.error:
        pass
    except Exception:
        pass
    finally:
        # Stopping Pygame mixer and removing the generated audio file
        pygame.mixer.music.stop()
        pygame.mixer.quit()
        os.remove("data.mp3")
        return


async def main():
    # Async function to interact with Character AI and handle the chat
    char = 'your_character_ai_api_key'  # Character AI API key

    # Initializing the Character AI client
    client = aiocai.Client('your_character_ai_api_secret')

    me = await client.get_me()  # Getting user details

    async with await client.connect() as chat:
        # Starting a new chat session
        new, answer = await chat.new_chat(
            char, me.id
        )

        while True:
            text = input('YOU: ')  # Taking user input

            # Sending user message to Character AI for processing
            message = await chat.send_message(
                char, new.chat_id, text
            )

            # Processing the response from Character AI
            reply = message.text.replace('~', '').replace('—', '')
            reply = re.sub(r'\*.*?\*', '', reply)
            reply = " ".join(line for line in reply.splitlines() if line.strip())
            print(f'{message.name}: {reply}')  # Printing the bot's response
            speak(reply)  # Converting bot's response to speech


asyncio.run(main())  # Running the main function asynchronously
