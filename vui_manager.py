import speech_recognition as sr
import pyttsx3
import threading
import queue

class VUIManager:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        self.result_queue = queue.Queue()
        self.is_listening = False

        self.engine.setProperty('rate', 140)

        try:
            self.microphone = sr.Microphone()
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
            print("[🎙️ VUI] Microphone initialized successfully.")
        except Exception as e:
            print(f"[🎙️ VUI] Mic Error (Check PyAudio/Permissions): {e}")
            self.microphone = None

    def speak_and_listen(self, text):
        if self.is_listening or not self.microphone:
            return

        self.is_listening = True

        def _thread():
            try:
                # 1. Speak First
                self.engine.say(text)
                self.engine.runAndWait()

                with self.microphone as source:
                    print("\n[🎙️ VUI] Listening... speak now!")
                    audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=4)

                print("[🎙️ VUI] Processing audio...")
                text_result = self.recognizer.recognize_google(audio)
                print(f"[🎙️ VUI] You said: '{text_result}'")

                self.result_queue.put(text_result.lower())

            except sr.WaitTimeoutError:
                print("[🎙️ VUI] Timed out waiting for speech.")
            except sr.UnknownValueError:
                print("[🎙️ VUI] Could not understand the audio.")
                self.result_queue.put("UNKNOWN_AUDIO")
            except Exception as e:
                print(f"[🎙️ VUI] Error: {e}")
            finally:
                self.is_listening = False

        threading.Thread(target=_thread, daemon=True).start()

    def get_recognized_text(self):
        if not self.result_queue.empty():
            return self.result_queue.get()
        return None

vui = VUIManager()