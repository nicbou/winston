import re

class Command(object):
    """
    Stores a command that is executed by external events such as a voice command,
    a change of state or a notification.
    """

    def on_event(self, event, sender):
        """
        Handles events from the interpreter and other sources
        """
        # Do something here.