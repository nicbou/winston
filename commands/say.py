from os import system
from datetime import datetime
from random import choice

def say(what):
    """
    Dispatch the say command
    """
    if what == "hello":
        sayHello()
    elif what == "the time":
        sayTime()
    elif what == "goodbye":
        sayGoodbye()
    elif what == "the date":
        sayDate()
    elif what == "a joke":
        sayJoke()
    elif what == "the weather":
        sayWeather()

def sayHello():
    """
    Returns a random, personalized greeting
    """
    current_hour = datetime.now().time().hour
    period = 'day'
    if current_hour > 4 and current_hour < 12:
        period = 'morning'
    elif current_hour > 12 and current_hour < 17:
        period = 'afternoon'
    elif current_hour > 16 and current_hour < 5:
        period = 'night'

    greetings = (
        'Good %s' % period,
        'Good %s' % period,
        'Greetings',
        'Hello there',
        'Hello',
        'Hello, sir',
        'Hi',
        'Hi there',
        'Howdy',
    )
    textToSpeech(choice(greetings))

def sayGoodbye():
    goodbyes = (
        'Goodbye',
        'Cheerio!',
        'Farewell',
        'See you later',
        'See you soon',
    )
    textToSpeech(choice(goodbyes)) 

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
    readable_time = "{0} {1} {2}".format(choice(intro), hours, minutes)
    textToSpeech(readable_time)

def sayDate():
    intro = (
        'The date is',
        'Today is',
    )
    date = datetime.now().strftime("%B %d")
    readable_date = "{0} {1}".format(choice(intro), date)
    textToSpeech(readable_date)

def sayJoke():
    textToSpeech("Too soon")

def sayWeather():
    textToSpeech("It gon'rain, nigga")

def textToSpeech(text):
    """
    Sends a command for TTS processing
    """
    # This is linux-specific. Use the say command on OS X
    system('echo "%s" | festival --tts' % text)