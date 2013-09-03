from datetime import datetime
from random import choice
from utils.texttospeech import text_to_speech
from commands import Command

class ActivateCommand(Command):
    """
    Activates winston's interpreter
    """
    def __init__(self, name='command'):
        actions = [
            'say hello',
            '(time to )?wake up',
            'get back to work',
        ]
        callback = self.activate
        super(ActivateCommand, self).__init__(actions=actions, callback=callback, name=name, always_active=True)

    def activate(self, command):
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
            'Good %s, sir' % period,
            'Good %s, sir. I am all ears.' % period,
            'Greetings sir',
            'Greetings sir. Is there anything I can do for you?',
            'Hello sir',
            'Hello sir. I missed you.',
            'I am all ears sir',
            'Hello sir. What can I do for you?',
        )
        text_to_speech(choice(greetings))
