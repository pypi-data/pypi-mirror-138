import os
from pygame import mixer 
import tempfile
import pkg_resources
from aiy.leds import (Leds, Pattern, PrivacyLed, RgbLeds, Color)
temp_dir = tempfile.TemporaryDirectory()

def get_temp_dir() -> str:
	"""Returns the path to the created temporary directory"""
	return temp_dir.name + '/'

def playsound(dir: str) -> None:
    mixer.init()
    mixer.music.load(dir)
    mixer.music.play()
    while mixer.music.get_busy() == True:
        continue

def set_volume(percent: int) -> None:
    os.system(f"amixer set Master {percent}%")

def boot_sound():
    path = pkg_resources.resource_filename(__name__, "/data/startup.mp3")
    set_volume(40)
    playsound(path)
    set_volume(60)

def led_button(event, color):
    with Leds() as leds:
        leds.update(Leds.rgb_on(color))
        event.wait()

def led_button_stop():
    with Leds() as leds:
        leds.update(Leds.rgb_off())
