from datetime import datetime
from random import choice
from utils.texttospeech import spell_integer, text_to_speech

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
    text_to_speech(choice(greetings))

def sayGoodbye():
    goodbyes = (
        'Goodbye',
        'Cheerio!',
        'Farewell',
        'See you later',
        'See you soon',
    )
    text_to_speech(choice(goodbyes)) 

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

def sayJoke():
    jokes = (
        "My quad-core processor allows me to make very fast, very accurate mistakes.",
        "The past, the present, and the future walk into a bar. It was tense.",
        "What does myself and a neutrino have in common? We're both constantly penetrating your mom.",
        "What do they do to dead chemists? Barium.",
        "The majority of people have an above average number of legs.",
        "How many programmers does it take to change a light bulb? None. It's a hardware problem.",
        "An SQL query walks into a bar, goes up to two tables and asks to join them.",
        "Time flies like an arrow. Fruit flies like a banana.",

    )
    text_to_speech(choice(jokes) + " Ha ha ha.")

def sayWeather():
    text_to_speech("It gon'rain, nigga")