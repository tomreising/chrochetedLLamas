import speech_recognition as sr
import ollama
from gtts import gTTS
import os
import pygame
import logging


logging.basicConfig(level=logging.INFO, format='%(message)s')

MP3_RESPONSE= str('response.mp3')
MP3_WAIT= str('wait_please.mp3')

def run_voicebot():
    """
    Function to run the voice activated chatbot. Commands must start with the phrase "chatbot"
    otherwise the command is ignored. If running in vs code stop the program in the terminal via ctrl+c command.
    """
    r = sr.Recognizer()
    if not os.path.exists(MP3_WAIT):
        wait_mp3 = gTTS(text="please wait while I look that up", lang='en', slow=False)
        wait_mp3.save(MP3_WAIT) 
        logging.info("File created!")
    else:
        logging.info("File already exists!")

    while True:
        try:
            text_out = None
            text = None
            with sr.Microphone() as source:
                logging.info("Waiting for voice input")
                audio = r.listen(source, timeout=3,phrase_time_limit=10)
                text = r.recognize_google(audio)
                text = text.lower()
                logging.info(f"captured recording -- {text} --")
            if "chatbot" in text:
                pygame.mixer.init()
                pygame.mixer.music.load(MP3_WAIT)
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy():
                    pass
                pygame.mixer.music.unload()
                text = text.replace("chatbot","")
                response = ollama.chat(model='llama3', messages=[
                    {
                        'role': 'user',
                        'content': f"{text}",
                    },
                    ])
                text_out = str(response['message']['content'])
            if text_out:
                myobj = gTTS(text=text_out, lang='en', slow=False)
                myobj.save(MP3_RESPONSE)
                pygame.mixer.init()
                pygame.mixer.music.load(MP3_RESPONSE)
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy():
                    pass
                pygame.mixer.music.unload()
                os.remove(MP3_RESPONSE)

        except Exception as e:
            logging.info(e)
            r = sr.Recognizer()
            continue

if __name__ == "__main__":
    run_voicebot()