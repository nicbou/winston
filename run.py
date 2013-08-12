from listener import Listener
from interpreter import *
from commands import Command
from commands.say import SayCommand, sayTime

# The list of commands passed to the interpreter
commands = []

# A command defined by extending the Command object
commands.append(SayCommand(name='say'))

# A command defined by instanciating the Command object
commands.append(Command(name='whatTime', actions=('what time is it',), callback=sayTime))

# Load the commands in the interpreter
interpreter = Interpreter(commands=commands)

# Get a listener
listener = Listener(interpreter=interpreter)

# And wait...
raw_input()