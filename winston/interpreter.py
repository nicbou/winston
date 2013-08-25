import re

class Interpreter(object):
    """
    The interpreter turns matches commands with functions. It strongly relies
    on the Command object, bundling them together into a bigger regex.

    Strings come from the Listener, which is just a wrapper around pocketsphinx.
    It only returns lowercase strings without punctuation.
    """

    # The name with which all commands begin. Can be a word or a regex.
    # Example: jenkins, alfred, robot. "Jenkins! Turn on the lights!"
    signal = "winston"

    # Command prefixes and suffixes. Can be a tuple of words or a regex
    prefixes = "( can you| could you)?( please)?"
    suffixes = "( please)?"

    # The actual commands. Expects a list of Command objects
    commands = ()

    def __init__(self, commands):
        """
        Prepares the interpreter, compile the regex strings
        """
        # Keep a reference to the interpreter
        for command in commands:
            command.interpreter = self

        self.commands = commands
        self.regex = self.regex()  # Build the command matcher

        # Commands can access self.interpreter.active and decide whether or not
        # to perform an action. Commands can also "shut down" winston by setting
        # active to false.

        # We still let the commands go through so a command can reactivate an
        # interpreter.
        self.active = True

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

        # Return the compiled regex, ready to be used
        return re.compile(final_regex)

    def match(self, command):
        # Try matching the command to an action
        result = self.regex.match(command)
        if result:
            groups = result.groupdict()  # Get all the group matches from the regex

            print("Got '%s'" % command)

            if not self.active:
                print("(interpreter is inactive)")

            for command in self.commands:
                # Check if the command name matches a regex group
                if command.name in groups and groups[command.name] is not None:
                    print('matched ' + command.name)
                    subject = None
                    if command.subjects:
                        subject = groups[command.name + 'Subject']  # The group of the subject ('the lights' in 'turn on the lights')
                    command.dispatch(subject)
        else:
            print("Could not match '{0}' to a command using regex".format(command))
