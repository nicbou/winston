from datetime import datetime
from random import choice
from utils.texttospeech import spell_integer, text_to_speech
from json import load
from urllib2 import urlopen
from commands import Command

class SayCommand(Command):
    """
    Simple Q/A commands: say hello, say the time, tell us goodbye etc.
    """
    def __init__(self, name='command'):
        actions = [
            'say',
            'tell me',
            'tell us',
        ]
        subjects = [
            'the date',
            'the time',
            'the weather',
            'the temperature',
        ]
        callback = self.say
        super(SayCommand, self).__init__(actions=actions, subjects=subjects, callback=callback, name=name)

    def say(self, what):
        if what == "the time":
            sayTime()
        elif what == "the date":
            sayDate()
        elif what == "the weather" or what == "the temperature":
            sayWeather()
        elif what == "my account balance":
            sayBalance()
        else:
            print("Unexpected subject {0} for command {1}".format(self.name, what))

def sayTime():
    time = datetime.now().time()
    hours = time.hour
    minutes = time.minute

    intro = (
        'The time is',
        'It is',
        'It currently is',
        'The current time is',
    )
    readable_time = "{0} {1} {2}".format(choice(intro), spell_integer(hours), spell_integer(minutes))
    text_to_speech(readable_time)

def sayDate():
    intro = (
        'The date is',
        'Today is',
    )
    date = datetime.now().strftime("%B %d")
    readable_date = "{0} {1}".format(choice(intro), date)
    text_to_speech(readable_date)

def sayWeather():
    city = 'montreal'
    try:
        data = urlopen('http://openweathermap.org/data/2.1/find/name?q={0}&units=metric'.format(city), timeout=5)
    except:
        text_to_speech("I am afraid I cannot get the weather, sorry.")

    cities = load(data)

    if cities['count'] == 0:
        text_to_speech("I am afraid I cannot get the weather, sorry.")
    else:
        city = cities['list'][0]
        current_temp = spell_integer(int(city['main']['temp']))
        max_temp = spell_integer(int(city['main']['temp_max']))
        current_weather = city['weather'][0]['description']

        output = "{weather} with a temperature of {temp} and a maximum of {maxtemp}.".format(
            weather = current_weather,
            temp = current_temp,
            maxtemp = max_temp,
        )

        text_to_speech(output)