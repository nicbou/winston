import gobject
import pygst
pygst.require('0.10')
gobject.threads_init()
import gst

class Listener(object):
    """
    Listens, understands and processes speeches using the
    python-gstreamer plugin. Notifies all attached interpreters
    when input is received.
    """
    def __init__(self, fsg_path=None, dict_path=None, start=True):
        """
        Initialize the listener
        """
        # Set the path to the finite state grammar (FSG) file
        # Don't have an FSG? Use sphinx_jsgf2fsg, or set it to None
        # to run pocketsphinx without a grammar (not recommended).
        self.fsg_path = fsg_path
        self.dict_path = dict_path

        # Init gstreamer
        self.init_gstreamer()

        # The command's interpreters
        self.interpreters = []

        # Start listening
        if start:
            self.start()

    def init_gstreamer(self):
        """
        Init the gstreamer plugin that pipes its input to pocketsphinx to be recognized
        """

        # Get the pipeline
        self.pipeline = gst.parse_launch('gconfaudiosrc ! audioconvert ! audioresample '
                                         + '! vader name=vad auto_threshold=true '
                                         + '! pocketsphinx name=asr ! fakesink')
        asr = self.pipeline.get_by_name('asr')

        # Bind the pipeline results
        asr.connect('result', self.voice_input)

        # Load the grammar file
        if self.fsg_path:
            asr.set_property("fsg", self.fsg_path)

        # Load the dictionary
        if self.dict_path:
            asr.set_property("dict", self.dict_path)

        # This tells the asr that it's ready to run
        asr.set_property('configured', True)

        bus = self.pipeline.get_bus()
        bus.add_signal_watch()
        
        self.pipeline.set_state(gst.STATE_PAUSED)

    def voice_input(self, asr, parsed_text, utterance_id):
        """
        Receive a result from the pipeline, and forward the parsed
        text to process_result.

        During the processing, voice recognition is paused so Winston
        doesn't end up talking to himself.
        """
        print('Listener received: {0}'.format(parsed_text))
        self.pause()
        self.notify({'text': parsed_text})
        self.start()

    def start(self):
        """
        Start listening
        """
        self.pipeline.set_state(gst.STATE_PLAYING)

    def pause(self):
        """
        Stop listening
        """
        self.pipeline.set_state(gst.STATE_PAUSED)

    def register(self, interpreter):
        """
        Register interpreters to be notified of new input
        """
        if not interpreter in self.interpreters:
            self.interpreters.append(interpreter)

    def unregister(self, interpreter):
        """
        Unregisters an interpreter
        """
        if interpreter in self.interpreters:
            self.interpreters.remove(interpreter)

    def notify(self, event):
        """
        Notify all interpreters of a received input
        """
        for interpreter in self.interpreters:
            interpreter.on_event(event, self)