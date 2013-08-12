from listener import Listener
from interpreter import *
from commands.say import say
commands = []

# Prepare some sommands
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
commands.append(Command(name='say', verbs=sayKeywords, subjects=thingsToSay, callback=say))

# jenkins, play ...
playKeywords = (
    'play',
)
thingsToPlay = (
    '(some )?music',  # jenkins, play (some) music
)
commands.append(Command(name='play', verbs=playKeywords, subjects=thingsToPlay, callback=play))

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
commands.append(Command(name='open', verbs=openKeywords, subjects=thingsToOpen, callback=open))

# Load the commands in the interpreter
interpreter = Interpreter(commands=commands)

# Get a listener
listener = Listener(interpreter=interpreter)

# And wait...
raw_input()