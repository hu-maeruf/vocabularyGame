import os
from gtts import gTTS
import pyttsx3
import pygame

def speak_word(full_text, file_name_token, output_dir="assets/audio/words"):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    safe_filename = file_name_token.lower().strip().replace(" ", "_")
    file_path = os.path.join(output_dir, f"{safe_filename}.mp3")

    if not os.path.exists(file_path):
        try:
            tts = gTTS(text=full_text, lang='en', slow=True)
            tts.save(file_path)
        except Exception as e:
            print(f"[TTS] Offline fallback engaging: {e}")
            try:
                engine = pyttsx3.init()
                engine.setProperty('rate', 145)
                voices = engine.getProperty('voices')
                if len(voices) > 1:
                    engine.setProperty('voice', voices[1].id)
                else:
                    engine.setProperty('voice', voices[0].id)
                engine.say(full_text)
                engine.runAndWait()
            except Exception as local_err:
                print(f"[TTS] Critical fallback failure: {local_err}")
            return None

    try:
        return pygame.mixer.Sound(file_path)
    except Exception as e:
        print(f"Error loading sound object: {e}")
        return None