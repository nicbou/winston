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
    def __init__(self, actions=[], subjects=[], callback=None, name='command', interpreter=None, always_active=False):
        self.name = name  # Used as a named group identifier in the regex
        self.actions = actions
        self.subjects = subjects
        self.callback = callback
        self.interpreter = interpreter  # Reference to the interpreter that will run this command
        self.always_active = always_active  # This command will not run when the interpreter is inactive

    def dispatch(self, subject):
        """
        Dispatches the command to the callback with the specified subject
        as a callback. Easily overridden.
        """
        # Don't perform actions if the interpreter isn't active
        if self.interpreter.active or (not self.interpreter) or self.always_active:
            # Validate the existence of a subject, if any are specified
            if not self.subjects:
                self.callback()
            elif isinstance(self.subjects, (tuple, list)) and subject in self.subjects:
                # Match a subject list
                self.callback(subject)
            elif (not isinstance(self.subjects, (tuple, list))) and re.match(self.subjects, subject):
                # Match a regex subject
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