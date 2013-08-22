# Winston, a smart virtual assistant

Winston is a voice-activated virtual assistant meant to be used in home automation projects, among other things. You can ask him questions, interact with him and whatnot. Questions and commands can easily be created in seconds without a deep understanding of how everything works.

## Setup

### Requirements

To use Winston, you will need the `gstreamer0.10-pocketsphinx` package and its dependencies. You will also need `festival` so Winston can reply back. Festival can easily be replaced by any text-to-speech software by overriding the text_to_speech function in utils/texttospeech.py

*Note: there might be packages which I forgot about, so do not hesitate to open an issue or send an email if the instructions are incomplete or unclear. I take these to heart, and will respond as quickly as possible.*

### Creating commands

There is a file called run.py that will run winston from the command line. Make sure to open it as it contains a very simple example that will show you how to define commands. By default, run.py uses grammar.fsg, and will recognize these commands. Feel free to define your own grammar and commands.

### Running Winston

Once installed, run winston by running winston/run.py, or by importing the required modules in your own project.

## Creating commands

Commands can be created by extending the Command object, or by instanciating it, depending on the complexity of your commands.

You will also need to generate the grammar on your own, since the commands do not automatically translate to a JSGF grammar. There is an included grammar, `jsgf.txt` that is converted to `grammar.fsg`.

*Note: Instructions unclear? Open a ticket and I will get back to you very quickly. Publishing this code was an afterthought.*