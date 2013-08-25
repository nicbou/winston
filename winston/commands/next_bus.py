from utils.texttospeech import text_to_speech
from json import load
from urllib2 import urlopen
from commands import Command
from time import strptime, strftime

class NextBusCommand(Command):
    """
    Fetches and read the bus schedule
    """
    def __init__(self, name='command'):
        actions = [
            'when will the next bus (pass|arrive|come|stop)',
            'when is the next bus (passing|coming|arriving|expected)',
        ]
        callback = self.find_bus
        super(NextBusCommand, self).__init__(actions=actions, callback=callback, name=name)

    def find_bus(self):
        """
        Get the bus schedule from the STM, return it in a readable format.
        """
        line = 107
        stop = 56685
        direction = 'N'

        try:
            data = urlopen('http://i-www.stm.info/en/lines/{line}/stops/{stop}/arrivals?direction={direction}&limit=5'.format(line=line, stop=stop, direction=direction), timeout=5)
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
