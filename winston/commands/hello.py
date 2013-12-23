from commands import RegexCommand
from datetime import datetime
from random import choice
from utils.texttospeech import text_to_speech

class HelloCommand(RegexCommand):
    """
    Activates winston's interpreter
    """
    def __init__(self, name='command'):
        """
        Build the basic regex command
        """
        regex = "(say hello|(time to )?wake up|get back to work)"

        super(HelloCommand, self).__init__(regex, True)

    def on_event(self, event, sender):
        """
        Activates winston and returns a random, personalized greeting
        """
        if self.match(event['text']):
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
                'Good %s, sir. I missed your presence.' % period,
                'Greetings sir',
                'Greetings sir. Is there anything I can do for you?',
                'Hello sir',
                'Hello sir. I missed you.',
                'Hello sir. What can I do for you?',
            )
            text_to_speech(choice(greetings))