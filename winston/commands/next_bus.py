from commands import RegexCommand
from config import BUS_SCHEDULE_URL
from json import load
from time import strptime, strftime
from urllib2 import urlopen
from utils.texttospeech import text_to_speech

class NextBusCommand(RegexCommand):
    """
    Finds the next bus using the STM API
    """
    def __init__(self, name='command'):
        """
        Build the basic regex command
        """
        questions = [
            'when will the next bus (pass|arrive|come|stop)',
            'when is the next bus (passing|coming|arriving|expected)',
        ]
        regex = "winston ({0}|{1})".format(questions[0],questions[1])

        super(NextBusCommand, self).__init__(regex, False)

    def on_event(self, event, sender):
        """
        Fetches the bus schedule using the STM API
        """
        if self.match(event['text']):
            line = 107
            stop = 56685
            direction = 'N'

            try:
                data = urlopen(BUS_SCHEDULE_URL.format(line=line, stop=stop, direction=direction), timeout=5)
                results = load(data)['result']
            except:
                text_to_speech('Sorry, I cannot retrieve the bus schedule at the moment.')
            else:
                # Pretty-print the results
                stops = []
                cancelled_stops = []
                for result in results:
                    stop = {
                        'cancelled': result['is_cancelled'],
                        'time': strptime(result['time'], '%H%M'),
                    }

                    if stop['cancelled']:
                        cancelled_stops.append(stop)
                    else:
                        stops.append(stop)

                # Pretty-print the times
                stops = ', then at '.join([strftime('%H:%M', stop['time']) for stop in stops[:2]])

                cancelled_stops = ', then at '.join([strftime('%H:%M', stop['time']) for stop in cancelled_stops])
                
                output = ""
                
                if stops:
                    output = "The bus will stop at {times}.".format(times=stops)
                    if cancelled_stops:
                        output += " The {times} stops were cancelled.".format(times=stops)
                else:
                    output = "It appears that all stops were cancelled for the next few hours."
                print(output)
                text_to_speech(output)
