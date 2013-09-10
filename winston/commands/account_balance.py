from utils.texttospeech import text_to_speech
from commands import Command

class AccountBalanceCommand(Command):
    """
    Simple Q/A commands: say hello, say the time, tell us goodbye etc.
    """
    def __init__(self, name='command'):
        format1_part1 = "(tell me |show me |read me )?"
        format1_part2_v1 = "((what's |what is )?my (bank )?account balance(like)?)"
        format1_part2_v2 = "((what's |what is (there )?|how much (do )?i have |how much (is there |there is ))in my (bank )?account)"
        format1 = "{p1}({p2v1}|{p2v2})".format(
            p1 = format1_part1,
            p2v1 = format1_part2_v1,
            p2v2 = format1_part2_v2,
        )

        format2 = "give me my account balance"

        actions = "({f1}|{f2})".format(
            f1 = format1,
            f2 = format2,
        )
        callback = self.say_balance
        super(AccountBalanceCommand, self).__init__(actions=actions, callback=callback, name=name)

    def say_balance(self, command):
        """
        Reads the account balance from selenium-td.py. The text file
        is a human-readable string.
        """
        try:
            with open('/var/www/scripts/winston_balance.txt') as file:
                text = file.read()
            text_to_speech(text)
        except:
            text_to_speech("I am afraid I cannot get your account balance, sorry.")