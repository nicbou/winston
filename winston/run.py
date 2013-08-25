# This file can be called from the command line, and will run Winston

from listener import Listener
from interpreter import *
from commands import Command
from commands.say import SayCommand, sayTime
from commands.open_door import OpenDoorCommand
from commands.set_alarm import AbsoluteAlarmCommand, RelativeAlarmCommand
from commands.activate import ActivateCommand
from commands.deactivate import DeactivateCommand
from commands.account_balance import AccountBalanceCommand
import os

# The grammar.fsg is a finite state grammar file generated from jsgf.txt
# using sphinx_jsgf2fsg. It helps the listener associate words to the correct
# commands. 
script_path = os.path.dirname(__file__)
grammar_file = os.path.join(script_path, "grammar.fsg")
dict_file = os.path.join(script_path, "dict.dic")

# The list of commands passed to the interpreter
commands = []

# Commands defined by extending the Command object
commands.append(ActivateCommand(name='activate'))  # Can activate winston
commands.append(DeactivateCommand(name='deactivate'))  # Can deactivate winston
commands.append(AccountBalanceCommand(name='account_balance'))
commands.append(SayCommand(name='say'))
commands.append(OpenDoorCommand(name='openDoor'))
commands.append(AbsoluteAlarmCommand(name='set_abs_alarm'))
commands.append(RelativeAlarmCommand(name='set_rel_alarm'))

# A command defined by instanciating the Command object
commands.append(Command(name='whatTime', actions=('what time is it',), callback=sayTime))

# Load the commands in the interpreter
interpreter = Interpreter(commands=commands)

# Get a listener. The grammar argument is optional, see Listener's doc for details
listener = Listener(interpreter=interpreter, fsg_path=grammar_file, dict_path=dict_file)

# And wait...
raw_input()