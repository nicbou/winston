from datetime import datetime
from random import choice
from utils.texttospeech import text_to_speech
from commands import Command

class ActivateCommand(Command):
    """
    Enables/disables winston
    """
    def __init__(self, name='command'):
        actions = [
            'say',
        ]
        subjects = [
            'goodbye',
            'hello',
        ]
        callback = self.say
        super(ActivateCommand, self).__init__(actions=actions, subjects=subjects, callback=callback, name=name, always_active=True)

    def say(self, what):
        if what == "hello":
            self.sayHello()
        elif what == "goodbye":
            self.sayGoodbye()
        else:
            print("Unexpected subject {0} for command {1}".format(self.name, what))

    def sayHello(self):
        """
        Activates winston and returns a random, personalized greeting
        """
        self.interpreter.active = True
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

    def sayGoodbye(self):
        """
        Deactivates winston
        """
        self.interpreter.active = False
        goodbyes = (
            'Goodbye',
            'Cheerio!',
            'Farewell',
            'See you later',
            'See you soon',
        )
        text_to_speech(choice(goodbyes))