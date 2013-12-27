from listener import Listener
from interpreter import *
import config

def main():
    """
    Allows Winston to be installed as a package and to be run from the command line.

    This simply inits Winston using the config file.
    """

    # Define and start a scheduler. These store tasks that are run at given times
    scheduler = config.SCHEDULER
    scheduler.start()

    # Load the commands in the interpreter. These dispatch commands. See the Interpreter's doc for details.
    interpreter = Interpreter(scheduler=config.SCHEDULER)
    for command in config.COMMANDS:
        interpreter.register(command)

    # Create a listener for pocketsphinx. It forwards recognized strings to Interpreters. See Listener's doc for details.
    listener = Listener(fsg_path=config.GRAMMAR_FILE, dict_path=config.DICT_FILE)
    listener.register(interpreter)

    # And wait...
    raw_input()

if __name__ == "__main__":
    main()