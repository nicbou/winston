from utils.texttospeech import text_to_speech
from commands import RegexCommand
from json import load
from urllib2 import urlopen
from config import WEATHER_API_URL
from random import choice
import re

class WeatherCommand(RegexCommand):
    """
    Reads the weather
    """

    def __init__(self):
        """
        Build the basic regex command. Generate the regex without the help
        of regexcommand's init, since it combines polite and standalone sentences
        """
        super(WeatherCommand, self).__init__("")  # Empty regex

        polite_willrain = "( (if|whether) it will (rain|snow)( today)?)"
        polite_expected = "( (if|whether) (rain|snow) is expected( today)?)"
        polite_weather = "( the (weather|temperature))"
        polite_regex = '(say|tell me|tell us)({0}|{1}|{2})'.format(polite_weather,polite_willrain,polite_expected)

        standalone_willrain = '((will it|is it (going to|gonna)) (rain|snow)( today)?)'
        standalone_expected = '(is (rain|snow) expected( today)?)'
        standalone_regex = '({0}|{1})'.format(standalone_expected,standalone_willrain)

        final_regex = "{signal}(({prefix} {polite}{suffix})|( {standalone}))".format(
                signal = self.signal,
                polite = polite_regex,
                standalone = standalone_regex,
                prefix = self.prefixes,
                suffix = self.suffixes,
        )
        self.regex = re.compile(final_regex)

    def match(self, text):
        return self.regex.match(text)

    def on_event(self, event, sender):
        """
        Fetches and reads the weather
        """
        if self.match(event['text']):
            try:
                data = urlopen(WEATHER_API_URL, timeout=5)
            except:
                text_to_speech("I am afraid I cannot get the weather, sorry.")
            else:
                json = load(data)

                current_temp = int(json['currently']['apparentTemperature'])
                min_temp = int(json['daily']['data'][0]['temperatureMin'])
                max_temp = int(json['daily']['data'][0]['temperatureMax'])
                precip_probability = int(json['daily']['data'][0]['precipProbability'])
                precip_type = json['daily']['data'][0]['precipType']
                current_weather = json['daily']['data'][0]['summary']

                output = ""

                if "temperature" in event['text']:
                    output = "It is {0} degrees outside.".format(current_temp)
                elif "rain" in event['text']:
                    if precip_probability < 15:
                        answers = (
                            "Not a chance in the world, sir.",
                            "I highly doubt so.",
                            "No sir",
                            "No rainfall expected, sir.",
                            "No rain is expected today",
                            "You can leave your umbrella at home. It will not rain today.",
                        )
                        output = choice(answers)
                    else:
                        if precip_type == "rain":
                            output = "There is a {0} percent chance of rain for the day".format(precip_probability)
                        else:
                            output = "There is a {0} percent chance of {1} for the day, but no rain is expected".format(precip_probability, precip_type)
                elif "snow" in event['text']:
                    if precip_probability < 15:
                        answers = (
                            "Not a chance in the world, sir.",
                            "I highly doubt so.",
                            "No sir",
                            "No snowfall expected, sir.",
                            "No snow is expected today",
                        )
                        output = choice(answers)
                    else:
                        if precip_type == "snow":
                            output = "There is a {0} percent chance of snow for the day".format(precip_probability)
                        else:
                            output = "There is a {0} percent chance of {1} for the day, but no snow is expected".format(precip_probability, precip_type)
                else:
                    output = "{weather} with a temperature between {min} and {max}.".format(
                        weather = current_weather,
                        min = min_temp,
                        max = max_temp,
                    )

                text_to_speech(output)