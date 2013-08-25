from utils.texttospeech import text_to_speech
from commands import Command
import re

one_to_ten = ('one','two','three','four','five','six','seven','eight','nine','ten',)
eleven_to_nineteen = ('eleven','twelve','thirteen','fourteen','fifteen','sixteen','seventeen','eighteen','nineteen',)
twenty_to_ninety = ('twenty','thirty','forty','fifty','sixty','seventy','eighty','ninety',)

class AbsoluteAlarmCommand(Command):
    """
    Sets an alarm at an absolute time (8, 10, etc)
    """
    def __init__(self, name='command'):

        self.actions = '(set (an alarm|a reminder)|(ring|wake) (me|us) up)( tomorrow)? at'
        self.subjects = '(six|seven|eight|nine|ten|eleven)( fifteen| thirty| forty five)?( tomorrow)?'

        super(AbsoluteAlarmCommand, self).__init__(actions=self.actions, subjects=self.subjects, callback=self.set_alarm, name=name)

    def set_alarm(self, when):
        # Remove the clutter
        when.replace('tomorrow', '')

        #Parse the number

        text_to_speech("Setting an alarm in " + when )


class RelativeAlarmCommand(Command):
    """
    Sets an alarm at a relative time (in 8 minutes, in 20 hours)
    """
    def __init__(self, name='command'):
        self.actions = '(set (an alarm|a reminder)|(ring|wake) (me|us) up) in'
        self.subjects = "((%s)|(%s)|(%s)( (%s))?) minutes( from now)?" % (
            '|'.join(one_to_ten),
            '|'.join(eleven_to_nineteen),
            '|'.join(twenty_to_ninety),
            '|'.join(one_to_ten),
        )
        print(self.subjects)


        super(RelativeAlarmCommand, self).__init__(actions=self.actions, subjects=self.subjects, callback=self.set_alarm, name=name)

    def set_alarm(self, when):
        # Remove the clutter
        when.replace(' minutes', '')
        when.replace(' from now', '')

        #Parse the number

        text_to_speech("Setting an alarm in " + when )

def text_to_number(text):
    """
    Parses a number between 1 and 99 from a given string (like "twenty four")
    """
    while text:
        text = text.strip()

        # Get the first word, keep the rest of the string
        text = string.split(' ',1)
        text = text[1]  # The rest of the string
        first_word = text[0]
        
        # Get the value of the word

    if not numwords:
        units = [
            "zero", "one", "two", "three", "four", "five", "six", "seven", "eight",
            "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen",
            "sixteen", "seventeen", "eighteen", "nineteen",
        ]

        tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]

        scales = ["hundred", "thousand", "million", "billion", "trillion"]

        numwords["and"] = (1, 0)
        for idx, word in enumerate(units):    numwords[word] = (1, idx)
        for idx, word in enumerate(tens):     numwords[word] = (1, idx * 10)
        for idx, word in enumerate(scales):   numwords[word] = (10 ** (idx * 3 or 2), 0)

    current = result = 0
    for word in textnum.split():
        if word not in numwords:
          raise Exception("Illegal word: " + word)

        scale, increment = numwords[word]
        current = current * scale + increment
        if scale > 100:
            result += current
            current = 0

    return result + current