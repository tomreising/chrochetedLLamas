import speech_recognition as sr
import ollama
from gtts import gTTS
import os
import time
import pygame

mp3_response= str('response.mp3')
mp3_wait= str('wait_please.mp3')
# myobj = gTTS(text="please wait while I look that up", lang='en', slow=False)
# myobj.save(mp3_wait)
r = sr.Recognizer()

while True:
    try:
        text_out = None
        text = None
        response_bool = False
        with sr.Microphone() as source:
            audio = r.listen(source, timeout=3,phrase_time_limit=10)
            text = r.recognize_google(audio)
            text = text.lower()
            print(text)
            if "chatbot" in text:
                pygame.mixer.init()
                pygame.mixer.music.load(mp3_wait)
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy(): pass
                # unload the loaded music file
                pygame.mixer.music.unload()
                text = text.replace("chatbot","")
                response = ollama.chat(model='llama3', messages=[
                    {
                        'role': 'user',
                        'content': f"{text}",
                    },
                    ])
                text_out = str(response['message']['content'])
                response_bool = True
        if text_out:
            myobj = gTTS(text=text_out, lang='en', slow=False)
            myobj.save(mp3_response)
            pygame.mixer.init()
            pygame.mixer.music.load(mp3_response)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy(): pass
        # unload the loaded music file
        if response_bool:
            pygame.mixer.music.unload()
            os.remove(mp3_response)

    except Exception as e:
        print(e)
        r = sr.Recognizer()
        continue