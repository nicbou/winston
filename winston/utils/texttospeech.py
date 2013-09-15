from os import system
import sys

def text_to_speech(text):
    """
    Sends a command for TTS processing
    """
    # This is linux-specific. Use the say command on OS X
    system('echo "%s" | festival --tts' % text)

def spell_integer(n):
    TENS = [None, None, "twenty", "thirty", "forty",
            "fifty", "sixty", "seventy", "eighty", "ninety"]
    SMALL = ["zero", "one", "two", "three", "four", "five",
             "six", "seven", "eight", "nine", "ten", "eleven",
             "twelve", "thirteen", "fourteen", "fifteen",
             "sixteen", "seventeen", "eighteen", "nineteen"]
    HUGE = [None, None] + [h + "illion" 
                           for h in ("m", "b", "tr", "quadr", "quint", "sext", 
                                      "sept", "oct", "non", "dec")]


    def nonzero(c, n, connect=''):
        return "" if n == 0 else connect + c + spell_integer(n)
     
    def last_and(num):
        if ',' in num:
            pre, last = num.rsplit(',', 1)
            if ' and ' not in last:
                last = ' and' + last
            num = ''.join([pre, ',', last])
        return num
     
    def big(e, n):
        if e == 0:
            return spell_integer(n)
        elif e == 1:
            return spell_integer(n) + " thousand"
        else:
            return spell_integer(n) + " " + HUGE[e]
     
    def base1000_rev(n):
        # generates the value of the digits of n in base 1000
        # (i.e. 3-digit chunks), in reverse.
        while n != 0:
            n, r = divmod(n, 1000)
            yield r

    if n < 0:
        return "minus " + spell_integer(-n)
    elif n < 20:
        return SMALL[n]
    elif n < 100:
        a, b = divmod(n, 10)
        return TENS[a] + nonzero("-", b)
    elif n < 1000:
        a, b = divmod(n, 100)
        return SMALL[a] + " hundred" + nonzero(" ", b, ' and')
    else:
        num = ", ".join([big(e, x) for e, x in
                         enumerate(base1000_rev(n)) if x][::-1])
        return last_and(num)

if __name__ == "__main__":
    """
    This module can be called from the command line. It takes
    a string as its second argument, and sends it to the
    text_to_speech function.
    """
    parts = sys.argv[1:]
    string = " ".join(parts).strip()
    text_to_speech(string)