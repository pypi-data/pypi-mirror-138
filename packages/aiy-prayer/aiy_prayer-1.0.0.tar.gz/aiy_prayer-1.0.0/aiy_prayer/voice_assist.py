"""prayer_tool"""
import sys
from datetime import datetime, time
from json import JSONDecodeError
import tempfile
from gtts import gTTS
from googletrans import Translator
from prayer_tool.prayer_times import PrayerTimes
from .utils import playsound, set_volume
from aiy.board import Board

##get translator instance
translator = Translator()
temp_dir = tempfile.TemporaryDirectory()

def get_translation(text: str, source: str, dest: str):
    """Translates the output"""
    translated = translator.translate(text,src=source ,dest=dest)
    return translated

def play(text: str, dest: str):
    """Plays the sound"""
    dire = temp_dir.name+"/out.mp3"
    output = get_translation(text, "fr", dest)
	#Use the translated text to generate an mp3 file with it
    gTTS(output.text, lang=dest).save(dire)
	#Plays the mp3 file
    playsound(dire)

def compare_time(time1, time2):
    """Returns the difference in minutes between two time objects"""
    minutes1 = int(time1.hour*60) + int(time1.minute)
    minutes2 = int(time2.hour*60) + int(time2.minute)
    return minutes2 - minutes1

def speak(instance: PrayerTimes, language: str = "fr", current_time: time = datetime.now().time()) -> None:
    """Will generate a string and play it in the STT class"""
    today_salat = instance.get_date()
    next_salat = today_salat.next_prayer()
    text = ""
    if next_salat is not None:
        difference = compare_time(current_time, next_salat.time)
        result = ""
        minutes = difference
        rest_minutes = int(minutes % 60)
        hours = int(minutes/60)
        if minutes >= 60:
            result = str(hours)+ " heures et "+ str(rest_minutes)+" minutes"
        else:
            result = str(minutes) + " minutes"
        text = f"La prière de {next_salat.name} est dans {result}."
    else:
        text = "Toutes les prières sont déjà passées."
    play(text, language)

def play_error(message: str):
    """Function to play the error messages"""
    path = temp_dir.name+"/error.mp3"
    gTTS(message).save(path)
    playsound(path)

class Assistant:
    def __init__(self, city: str = "Brussels", language: str = "fr", volume: int = 60) -> None:
        self.city = city
        self.language = language
        self.volume = volume

    def do(self):
        set_volume(self.volume)
        try:
            instance = PrayerTimes(city = self.city)
            speak(instance=instance, language=self.language)
        except JSONDecodeError:
            play_error("The city you have given is incorrect.")
        except ValueError:
            play_error("The language you have given is incorrect.")

    def loop(self):
        try:
            while 1:
                with Board() as board:
                    board.button.wait_for_press()
                    self.do()
        except KeyboardInterrupt:
            sys.exit(0)
