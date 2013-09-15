import re

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
    _interpreter = None
    _callback = None

    def __init__(self, actions=[], subjects=[], callback=None, name='command', interpreter=None, always_active=False):
        self.name = name  # Used as a named group identifier in the regex
        self.actions = actions
        self.subjects = subjects
        self.callback = callback
        self.interpreter = interpreter  # Reference to the interpreter that will run this command
        self.always_active = always_active  # This command will not run when the interpreter is inactive

    def dispatch(self, command, subject):
        """
        Dispatches the command to the callback with the specified subject
        as a callback. Easily overridden.

        command: The full matched command ('turn on the lights')
        subject: The variable part of the command ('the lights')
        """
        # Don't perform actions if the interpreter isn't active
        if self.interpreter.active or (not self.interpreter) or self.always_active:
            # Validate the existence of a subject, if any are specified
            if not self.subjects:
                self.callback(command)
            elif isinstance(self.subjects, (tuple, list)) and subject in self.subjects:
                # Match a subject list
                self.callback(command, subject)
            elif (not isinstance(self.subjects, (tuple, list))) and re.match(self.subjects, subject):
                # Match a regex subject
                self.callback(command, subject)
            else:
                print("Subject {0} does not exist for command {1}".format(subject, self.name))

    @property
    def regex(self, group_name=None):
        """
        Returns a regex string matching the command.
        """
        # Build the command
        # e.g. (open|turn on) (the lights|the television)
        command = ""
        if self.subjects:
            regex_actions = self.actions
            regex_subjects = self.subjects

            # If the actions is a list (and not a regex), join it into a single regex:
            if isinstance(self.actions, (tuple, list)):
                regex_actions = "|".join(regex_actions)

            # If the subjects is a list (and not a regex), join it into a single regex:
            if isinstance(self.subjects, (tuple, list)):
                regex_subjects = "|".join(regex_subjects)

            command = "({actions}) (?P<{name}Subject>({subject}))".format(
                name = self.name,
                actions = regex_actions,
                subject = regex_subjects,
            )
        else:
            regex_actions = self.actions

            # If the actions is a list (and not a regex), join it into a single regex:
            if isinstance(self.actions, (tuple, list)):
                command = "({actions})".format(
                    actions = "|".join(self.actions),
                )
            else:
                command = regex_actions

        # Put the regex in a named group
        named_group = "(?P<{name}>({command}))".format(
            name = self.name,
            command = command,
        )

        # Return a regex pattern string
        return named_group

    @property
    def interpreter(self):
        return self._interpreter

    @interpreter.setter
    def interpreter(self, value):
        """
        Since this function is called when the interpreter is set,
        this is the perfect place to attach initiation logic that
        concerns the command's Interpreter.

        For example, this is the place to add events to the interpreter's
        scheduler.
        """
        self._interpreter = value

    @property
    def callback(self):
        return self._callback

    @callback.setter
    def callback(self, value):
        self._callback = value