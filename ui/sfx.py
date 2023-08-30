# play sounds

import pygame
import os
import time 
import random
import pygame._sdl2.audio as sdl2_audio

if __name__ == "__main__":
    from conf_app import SHINANO_LOVE
else:
    from conf_app import SHINANO_LOVE

def get_devices(capture_devices=False):
    init_by_me = not pygame.mixer.get_init()
    if init_by_me:
        pygame.mixer.init()
    devices = tuple(sdl2_audio.get_audio_device_names(capture_devices))
    if init_by_me:
        pygame.mixer.quit()
    return devices

def sound_mail(device=get_devices()[0]):
    pygame.mixer.init(frequency=48000, devicename=device, buffer=8192)
    sound_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),"res","mp3")
    soundlist = os.listdir(sound_path)
    soundlist = [x for x in soundlist if x.endswith(".mp3")]
    # print(soundlist)
    # init random
    random.seed(time.time())
    if random.random() < (0.5 if SHINANO_LOVE else 1):
        random.shuffle(soundlist)
        soundfile = os.path.join(sound_path,soundlist[0])
    else:
        soundfile = os.path.join(sound_path,"mail_shinano.mp3")
    playsound(soundfile)

def playsound(soundfile):
    print("play sound: ",soundfile)
    sound = pygame.mixer.Sound(soundfile)
    sound.set_volume(0.8)
    channel = sound.play(fade_ms=500)
    channel.set_volume(0.25,0.5)
    time.sleep(0.02)
    sound = pygame.mixer.Sound(soundfile)
    sound.set_volume(0.3)
    channel = sound.play(fade_ms=300)
    channel.set_volume(0.4,0.45)

def sound_guard():
    while pygame.mixer.get_busy():
        pygame.time.Clock().tick(100)

if __name__ == "__main__":
    sound_mail()
    sound_guard()
