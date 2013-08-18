# This file can be called from the command line, and will run Winston

from listener import Listener
from interpreter import *
from commands import Command
from commands.say import SayCommand, sayTime
from commands.open_door import OpenDoorCommand
from commands.set_alarm import AlarmCommand
import os

# The grammar.fsg is a finite state grammar file generated from jsgf.txt
# using sphinx_jsgf2fsg. It helps the listener associate words to the correct
# commands. 
script_path = os.path.dirname(__file__)
grammar_file = os.path.join(script_path, "grammar.fsg")

# The list of commands passed to the interpreter
commands = []

# Commands defined by extending the Command object
commands.append(SayCommand(name='say'))
commands.append(OpenDoorCommand(name='openDoor'))
commands.append(AlarmCommand(name='setAlarm'))

# A command defined by instanciating the Command object
commands.append(Command(name='whatTime', actions=('what time is it',), callback=sayTime))

# Load the commands in the interpreter
interpreter = Interpreter(commands=commands)

# Get a listener. The grammar argument is optional, see Listener's doc for details
listener = Listener(interpreter=interpreter, fsg_path=grammar_file)

# And wait...
raw_input()