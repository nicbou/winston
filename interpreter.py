import re
from commands.say import *

class Command(object):
    """
    Stores a command:
    - name: a UNIQUE identifier for the regex and JSGF file generation
    - verbs: a list of action variations: (say, tell us, tell me, tell)
    - subjects: a list of action targets passed to the callback: (the time, the weather)
    - callback: a function that executes the command with a subject string as the argument
    """
    def __init__(self, name, verbs, subjects, callback):
        self.name = name
        self.verbs = verbs
        self.subjects = subjects
        self.callback = callback

    def dispatch(self, subject):
        """
        Dispatches the command to the callback with the specified subject
        as a callback. Easily overridden.
        """
        if subject in self.subjects:
            self.callback(subject)
        else:
            raise Exception("Subject {0} does not exist for command {1}".format(subject, self.name))

    @property
    def regex(self):
        """
        Returns a regex string for the command.
        """
        # Build the command
        # (open|turn on) (the lights|the television)
        # The second group is a named group called subjectWhat (sayWhat, openWhat...)
        command = "({verb}) (?P<{name}What>({subject}))".format(
            name = self.name,
            verb = "|".join(self.verbs),
            subject = "|".join(self.subjects),
        )

        # Put the regex in a named group
        named_group = "(?P<{name}>({command}))".format(
            name = self.name,
            command = command,
        )

        # Return a regex pattern string
        return named_group


class Interpreter(object):
    """
    The interpreter turns matches commands with functions. It strongly relies
    on the Command object, bundling them together into a bigger regex.
    """

    # The name with which all commands begin. Can be a word or a regex.
    # Example: jenkins, alfred, robot. "Jenkins! Turn on the lights!"
    signal = "jenkins"

    # Command prefixes and suffixes. Can be a tuple of words or a regex
    prefixes = "( can you| could you)?( please)?"
    suffixes = "( please)?"

    # The actual commands. Expects a list of Command objects
    commands = ()

    def __init__(self, commands):
        """
        Prepares the interpreter, compile the regex strings
        """
        self.commands = commands
        self.regex = self.regex()

    def regex(self):
        """
        Build a regex to match all possible commands
        """
        # Basic command structure
        basic_command = "{signal}{prefix} {command}{suffix}"

        # Build the command regex by joining individual regexes
        # e.g. (command_1|command_2|command_3)
        command_regexes = []
        for command in self.commands:
            command_regexes.append(command.regex)
        command_regex = "({0})".format("|".join(command_regexes))

        # Wrap the command with the prefix and suffix regexes
        final_regex = basic_command.format(
            signal = self.signal,
            command = command_regex,
            prefix = self.prefixes,
            suffix = self.suffixes,
        )

        print(final_regex)

        # Return the compiled regex, ready to be used
        return re.compile(final_regex)

    def match(self, command):
        # Try matching the command to an action
        result = self.regex.match(command)
        if result:
            groups = result.groupdict()  # Get all the group matches from the regex

            print("Got '%s'" % command)

            for command in self.commands:
                # Check if the command name matches a regex group
                if command.name in groups and groups[command.name] is not None:
                    subject_group = command.name + 'What'  # The group of the subject ('the lights' in 'turn on the lights')
                    
                    # Call the function's callback
                    print("Matched command '%s'" % command.name)
                    print("With subject '%s'" % groups[subject_group])
                    command.dispatch(groups[subject_group])
        else:
            print("Could not match '{0}' to a command using regex".format(command))

# Leaving that here for a moment
def play(what):
    pass

def open(what):
    pass
