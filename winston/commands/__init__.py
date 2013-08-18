class Command(object):
    """
    Stores a command:
    - name: an identifier for the regex and JSGF file generation. Should be unique.
    - actions: a list of action variations: (say, tell us, tell me, tell)
    - subjects: a list of action targets passed to the callback: (the time, the weather)
    - callback: a function that executes the command with a subject string as the argument

    You can create a new command by extending it or by instanciating it. Extending the Command
    object gives you the ability to keep application state and redefine how commands are
    dispatched.
    """
    def __init__(self, actions=[], subjects=[], callback=None, name='command'):
        self.name = name  # Used as a named group identifier in the regex
        self.actions = actions
        self.subjects = subjects
        self.callback = callback

    def dispatch(self, subject):
        """
        Dispatches the command to the callback with the specified subject
        as a callback. Easily overridden.
        """
        # Validate the existence of a subject, if any are specified
        if not self.subjects:
            self.callback()
        elif subject in self.subjects:
            self.callback(subject)
        else:
            print("Subject {0} does not exist for command {1}".format(subject, self.name))

    @property
    def regex(self, group_name=None):
        """
        Returns a regex string matching the command.
        """
        # Build the command
        # e.g. (open|turn on) (the lights|the television)
        if self.subjects:
            command = "({actions}) (?P<{name}Subject>({subject}))".format(
                name = self.name,
                actions = "|".join(self.actions),
                subject = "|".join(self.subjects),
            )
        else:
            command = "({actions})".format(
                actions = "|".join(self.actions),
            )

        # Put the regex in a named group
        named_group = "(?P<{name}>({command}))".format(
            name = self.name,
            command = command,
        )

        # Return a regex pattern string
        return named_group