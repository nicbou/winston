from utils.texttospeech import spell_integer, text_to_speech
from commands import Command
import re

class AlarmCommand(Command):
    """
    Sets an alarm
    """
    def __init__(self, name='command'):
        # This command uses regular expressions
        actions = '(set an alarm|wake me up|wake us up)( tomorrow)? at'
        subjects = '(six|seven|eight|nine|ten|eleven)( fifteen| thirty| forty five)?( tomorrow)?'
        callback = self.set_alarm
        super(AlarmCommand, self).__init__(actions=actions, subjects=subjects, callback=callback, name=name)

    def dispatch(self, subject):
        """
        This dispatcher uses regex to match against possible subjects
        """
        # Validate the existence of a subject, if any are specified
        if re.match(self.subjects, subject):
            self.callback(subject)
        else:
            print("Subject {0} does not exist for command {1}".format(subject, self.name))

    def set_alarm(self, when):
        text_to_speech("Setting an alarm at " + when)