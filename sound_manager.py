import os
import pygame
import components.tts_helper as tts

if not pygame.mixer.get_init():
    pygame.mixer.init()

def start_background_music():
    music_path = "assets/audio/music/background.mp3"
    if os.path.exists(music_path):
        try:
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.set_volume(0.2)
            pygame.mixer.music.play(-1)
        except Exception as e:
            print(f"Error loading background music: {e}")
    else:
        print(f"Background music file missing at: {music_path}")

def play_word_audio():
    full_sentence = "What is this?"
    tts_sound = tts.speak_word(full_sentence, "question_prompt")
    if tts_sound:
        try:
            voice_channel = pygame.mixer.Channel(7)
            voice_channel.stop()
            tts_sound.set_volume(0.5)
            voice_channel.play(tts_sound)
        except Exception as e:
            print(f"Audio playback error: {e}")

def play_success_sound():
    sound_path = "assets/audio/effects/correct.mp3"
    if os.path.exists(sound_path):
        try:
            success_sound = pygame.mixer.Sound(sound_path)
            fx_channel = pygame.mixer.Channel(6)
            fx_channel.stop()
            success_sound.set_volume(0.5)
            fx_channel.play(success_sound)
        except Exception as e:
            print(f"Error playing success sound: {e}")

def play_victory_sound():
    sound_path = "assets/audio/effects/victory.mp3"
    if os.path.exists(sound_path):
        try:
            pygame.mixer.music.fadeout(1000)
            victory_sound = pygame.mixer.Sound(sound_path)
            victory_channel = pygame.mixer.Channel(5)
            victory_channel.stop()
            victory_sound.set_volume(0.7)
            victory_channel.play(victory_sound)
        except Exception as e:
            print(f"Error playing victory sound: {e}")