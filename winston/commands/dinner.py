from random import choice
from utils.texttospeech import text_to_speech
from commands import Command

class DinnerCommand(Command):
    """
    Simple Q/A commands: say hello, say the time, tell us goodbye etc.
    """
    def __init__(self, name='command'):
        actions = 'what should i eat (for (dinner|supper)|tonight)',
        callback = self.say
        super(DinnerCommand, self).__init__(actions=actions, subjects=None, callback=callback, name=name)

    def say(self, command):
        sayMealIdea()

def get_dinner_idea():
    """
    Gets dinner ideas. Meant to be replaced with an API
    of some sort.
    """
    choices = (
        'hot chicken sandwiches',
        'hamburgers',
        'hot dogs',
        'chicken pitas',
        'chicken',
        'salmon fillets',
        'spaghetti',
        'macaroni',
        'mac and cheese',
        'shrimp pasta',
        'fajitas',
        'nachos',
        'won ton soup',
        'grilled cheese sandwiches',
        'corn dogs',
        'stew',
        'shepherd\'s pie',
        'pizza',
        'ramen soup',
        'take out food'
    )
    return choice(choices)

def sayMealIdea():
    sentences = (
        'Would you enjoy some {0}?',
        'What about {0}',
        'I suggest {0}',
        '{0} for dinner seems like a good idea',
        'I would go for {0}',
    )
    suggestion = choice(sentences).format(get_dinner_idea())
    text_to_speech(suggestion)