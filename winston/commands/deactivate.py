from random import choice
from utils.texttospeech import text_to_speech
from commands import Command

class DeactivateCommand(Command):
    """
    Deactivates winston's interpreter
    """
    def __init__(self, name='command'):
        actions = [
            'say goodbye',
            'go to sleep',
            'deactivate yourself',
            'stop listening',
        ]
        callback = self.deactivate
        super(DeactivateCommand, self).__init__(actions=actions, callback=callback, name=name, always_active=True)

    def deactivate(self):
        """
        Deactivates winston
        """
        self.interpreter.active = False
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