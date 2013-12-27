from commands import RegexCommand
from random import choice
from utils.texttospeech import text_to_speech

class DinnerCommand(RegexCommand):
    """
    Returns dinner ideas
    """
    def __init__(self):
        """
        Build the basic regex command
        """
        regex = "what (should|do|can) (i|we) eat (for (dinner|supper)|tonight)"

        super(DinnerCommand, self).__init__(regex, False)

    def on_event(self, event, sender):
        """
        Suggests a dinner idea
        """
        if self.match(event['text']):
            sentences = (
                'Would you enjoy some {0}?',
                'What about {0}',
                'I suggest {0}',
                '{0} for dinner seems like a good idea',
                'I would go for {0}',
            )
            suggestion = choice(sentences).format(self.get_dinner_idea())
            text_to_speech(suggestion)

    def get_dinner_idea(self):
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
            'take out food',
            'sushi',
            'thai chicken',
        )
        return choice(choices)