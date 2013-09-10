from commands import Command
from datetime import time
from os import system
from random import choice
from utils.texttospeech import __file__ as tts_path
from utils.texttospeech import text_to_speech

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

    def set_alarm(self, command, when):
        # Remove the clutter
        when = when.replace('tomorrow', '')

        #Parse the number
        time_value = text_to_time(when)
        time_string = time_value.strftime("%H:%M")
        command = 'echo python {script} "{message}" | at -m {time}AM'

        messages = [
            "Sir, you asked me to set an alarm at this precise moment.",
            "It is time sir. You asked me to set an alarm at this precise moment.",
            "Hello sir. You asked me to wake you up at this time.",
        ]

        system(command.format(script=tts_path, time=time_string, message=choice(messages)))
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
        super(RelativeAlarmCommand, self).__init__(actions=self.actions, subjects=self.subjects, callback=self.set_alarm, name=name)

    def set_alarm(self, when):
        """
        Sets an alarm using the 'at' command.
        """

        # Remove the clutter
        when.replace(' minutes', '')
        when.replace(' from now', '')

        #Parse the number
        if "hours" in when:
            command = 'echo python {script} "{message}" | at now + {time} hours'
        else:
            command = 'echo python {script} "{message}" | at now + {time} minutes'

        messages = [
            "Sir, {time} ago, you asked me to set an alarm at this precise moment.".format(time=when),
            "It is time sir. You asked me to set an alarm at this precise moment {time} ago.".format(time=when),
        ]

        system(command.format(script=tts_path, time=text_to_number(when), message=choice(messages)))
        text_to_speech("Setting an alarm in " + when )


def text_to_number(text):
    """
    Parses a number between 1 and 99 from a given string (like "twenty four").
    This function expects space-separated words, not grammatically correct
    numbers.
    """
    total_value = 0
    while text:
        text = text.strip()

        # Get the first word, keep the rest of the string
        split = text.split(' ',1)
        if len(split) > 1:
            text = split[1]  # The rest of the string
        else:
            text = ''
        current_word = split[0]  # The first word
        
        # Get the value of the word
        try:
            total_value += one_to_ten.index(current_word) + 1
        except:
            pass

        try:
            total_value += eleven_to_nineteen.index(current_word) + 11
        except:
            pass

        try:
            total_value += (twenty_to_ninety.index(current_word) * 10) + 20
        except:
            pass

    return total_value


def text_to_time(text):
    """
    Parses a time from a given string (like "six thirty" or "four forty four").
    This function expects space-separated words, not grammatically correct
    numbers.
    """
     # Get the first word, keep the rest of the string
    split = text.split(' ',1)

    hour = text_to_number(split[0])  # The first word is the hour
    if len(split) > 1:
        minutes = text_to_number(split[1])  # The rest of the string
    else:
        minutes = 0

    return time(hour, minutes)