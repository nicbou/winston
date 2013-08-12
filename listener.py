import gobject
import pygst
pygst.require('0.10')
gobject.threads_init()
import gst

class Listener(object):
    """
    Listens, understands and processes speeches using the
    python-gstreamer plugin.
    """
    def __init__(self, interpreter, start=True):
        """
        Initialize the listener
        """

        # Init gstreamer
        self.init_gstreamer()

        # Get an interpreter
        self.interpreter = interpreter

        # Start listening
        if start:
            self.start()

    def init_gstreamer(self):
        # Get the pipeline
        self.pipeline = gst.parse_launch('gconfaudiosrc ! audioconvert ! audioresample '
                                         + '! vader name=vad auto_threshold=true '
                                         + '! pocketsphinx name=asr ! fakesink')
        asr = self.pipeline.get_by_name('asr')

        # Bind the pipeline results
        # asr.connect('partial_result', self.asr_partial_result)
        asr.connect('result', self.asr_result)

        # Load the grammar file (generated from the jsgf file)
        asr.set_property("fsg", "grammar.fsg")
        asr.set_property('configured', True)

        bus = self.pipeline.get_bus()
        bus.add_signal_watch()
        
        self.pipeline.set_state(gst.STATE_PAUSED)

    def asr_result(self, asr, parsed_text, utterance_id):
        """
        Receives a result from the pipeline, and forwards the parsed
        text to process_result, which is intended to be overridden.
        """
        self.process_result(parsed_text)

    def start(self):
        self.pipeline.set_state(gst.STATE_PLAYING)

    def pause(self):
        self.pipeline.set_state(gst.STATE_PAUSED)

    def process_result(self, parsed_text):
        """
        Does something with the recognized sentence. Override this function
        to define custom functionality.
        """
        self.interpreter.match(parsed_text)