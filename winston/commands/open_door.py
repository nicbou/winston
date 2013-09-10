from utils.texttospeech import text_to_speech
from commands import Command
import serial
import time

class OpenDoorCommand(Command):
    """
    Dispatches commands to turn things on/off
    """
    def __init__(self, name='command'):
        actions = [
            'open',
            'unlock',
        ]
        subjects = [
            'the door',
        ]
        callback = self.open
        super(OpenDoorCommand, self).__init__(actions=actions, subjects=subjects, callback=callback, name=name)

    def open(self, command, subject):
        if subject == 'the door':
            openDoor()


def openDoor():
    """
    Gets the arduino to open the the door for four seconds
    All we need to do is send the arduino a byte
    """
    try:
        text_to_speech("Opening the door")
        ser = serial.Serial('/dev/ttyACM0', 9600)
        time.sleep(2) #Deal with the stupid-ass DTR

        #Send a byte to the arduino, and it will open the door
        ser.write('a')
        ser.close()
    except:
        text_to_speech("I am sorry. I can't open the door.")