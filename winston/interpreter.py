import re

class Interpreter(object):
    """
    The interpreter turns matches command strings with the right Commands. It's
    purpose is to notify all Commands of a new command string.

    The command strings come from the Listener, which is just a wrapper around pocketsphinx.
    """

    def __init__(self, scheduler=None):
        """
        Prepares the interpreter
        """
        # Keep a reference to the scheduler
        self.scheduler = scheduler

        # The commands
        self.commands = []

    def register(self, command):
        """
        Registers new commands to the interpreter's events
        """
        if not command in self.commands:
            self.commands.append(command)

    def unregister(self, command):
        """
        Unregisters a command from the interpreter's events
        """
        if command in self.commands:
            self.commands.remove(command)

    def notify(self, event):
        """
        Notifies all commands of a change in the state of
        the interpreter.
        """
        for command in self.commands:
            command.on_event(event, self)

    def on_event(self, event, sender):
        """
        Handles events from the listener and other classes
        it is registered to.
        """
        print('Interpreter received: {0}'.format(event['text']))

        self.notify(event)
