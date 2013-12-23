from commands import RegexCommand
from random import choice
from utils.texttospeech import text_to_speech

class GoodbyeCommand(RegexCommand):
    """
    Activates winston's interpreter
    """
    def __init__(self, name='command'):
        """
        Build the basic regex command
        """
        actions = [
            'say goodbye',
            'go to sleep',
            'deactivate yourself',
            'stop listening',
        ]
        regex = "({0})".format("|".join(actions))

        super(GoodbyeCommand, self).__init__(regex, True)

    def on_event(self, event, sender):
        """
        Deactivates winston and returns a random, personalized farewell
        """
        if self.match(event['text']):
            goodbyes = (
                'I will remain silent sir.',
                'Farewell sir',
                'I will see you later sir.',
                'See you soon sir.',
                'You will be missed, sir.',
                'Have a nice day sir',
                'I am going to sleep sir',
                'Deactivating myself sir',
            )
            text_to_speech(choice(goodbyes))