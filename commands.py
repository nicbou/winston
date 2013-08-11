from os import system
from datetime import datetime
from random import choice
import re

class Interpreter(object):
    """
    The interpreter turns commands into functions. The interpreter
    supports command variations, and builds them into a regex matcher.
    """
    def __init__(self):
        self.regex = self.buildRegex()
        self.action_dict = self.buildActionDict()

    def buildRegex(self):
        """
        Build a regex matching all possible commands
        """
        # Basic command structure
        basic_command = "{signal}{startPolite} {command}{endPolite}"

        # Command prefixes and suffixes.
        signal = "jenkins"  # This is where you rename your assistant
        startPolite = "( can you| could you)?( please )?"
        endPolite = "( please)?"

        # jenkins, say ...
        sayKeywords = (
            'say',
            'tell me',
            'tell us',
        )
        thingsToSay = (
            'a joke',
            'goodbye',
            'hello',
            'the date',
            'the time',
            'the weather',
        )

        # jenkins, play ...
        playKeywords = (
            'play',
        )
        thingsToPlay = (
            '(some )?music',  # jenkins, play (some) music
        )

        # jenkins, turn on ...
        openKeywords = (
            'open',
            'turn on',
        )
        thingsToOpen = (
            'the television',
            'the lights',
            'the door',
        )

        playRegex = "({verb}) (?P<playWhat>({subject}))".format(
            verb = "|".join(playKeywords),
            subject = "|".join(thingsToPlay),
        )
        sayRegex = "({verb}) (?P<sayWhat>({subject}))".format(
            verb = "|".join(sayKeywords),
            subject = "|".join(thingsToSay),
        )
        openRegex = "({verb}) (?P<openWhat>({subject}))".format(
            verb = "|".join(openKeywords),
            subject = "|".join(thingsToOpen),
        )

        command_regex = "((?P<play>({play}))|(?P<say>({say}))|(?P<open>({open})))".format(
            play = playRegex,
            say = sayRegex,
            open = openRegex,
        )

        final_regex = basic_command.format(
            signal = signal,
            command = command_regex,
            startPolite = startPolite,
            endPolite = endPolite,
        )

        return re.compile(final_regex)

    def buildActionDict(self):
        """
        Builds a dict matching commands to callback functions.

        The dicts here are actually regex group names
        """
        action_dict = {
            'say': say,
            'play': play,
            'open': open,
        }

        return action_dict

    def match(self, command):
        # Try matching the command to an action
        result = self.regex.match(command)
        groups = result.groupdict()  # Get all the group matches

        print("Got '%s'" % command)

        for action in self.action_dict:
            if action in groups and groups[action] is not None:
                callback = self.action_dict[action]
                print("Matched action '%s'" % action)
                print("With argument '%s'" % groups['sayWhat'])
                callback(groups['sayWhat'])

def say(what):
    if what == "hello":
        sayHello()
    elif what == "the time":
        textToSpeech("I'm not ready for that")
    elif what == "goodbye":
        textToSpeech("I'm not ready for that")
    elif what == "the date":
        textToSpeech("I'm not ready for that")
    elif what == "a joke":
        textToSpeech("I'm not ready for that")
    elif what == "the weather":
        textToSpeech("I'm not ready for that")

def play(what):
    pass

def open(what):
    pass

def textToSpeech(text):
    """
    Sends a command for TTS processing
    """
    # This is linux-specific. Use the say command on OS X
    system('echo "%s" | festival --tts' % text)

def sayHello():
    """
    Returns a random, personalized greeting
    """
    interpreter = Interpreter()
    interpreter.buildRegex()
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
    textToSpeech(choice(greetings))