#!/usr/bin/env python

import sys,os
from os import system
from datetime import datetime
from time import strftime

import wave
import pyaudio

def decodeSpeech(hmmd,lmdir,dictp,jsgf,wavfile):
    """
    Decodes a speech file
    """
    try:
      from pocketsphinx import Decoder
    except:
      from pocketsphinx import Decoder

    import sphinxbase
    speechRec = Decoder(hmm=hmmd, lm=lmdir, dict=dictp, jsgf=jsgf, rate=16000)
    wavFile = file(wavfile,'rb')
    speechRec.decode_raw(wavFile)
    result = speechRec.get_hyp()

    return result[0]

def record():

    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
    RECORD_SECONDS = 3
    WAVE_OUTPUT_FILENAME = "output.wav"

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("* recording")

    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("* done recording")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))

if __name__ == "__main__":

    hmdir = "/users/nicolas/Dropbox/ReposiTories/SpeechRec/model/hmm/wsj1"
    lmd = "/usr/local/Cellar/cmu-pocketsphinx/0.8/share/pocketsphinx/model/lm/en_US/wsj0vp.5000.DMP"
    dictd = "/usr/local/Cellar/cmu-pocketsphinx/0.8/share/pocketsphinx/model/lm/en_US/cmu07a.dic"
    jsgf = "/users/nicolas/Dropbox/ReposiTories/SpeechRec/jsgf.txt"
    wavfile = "/users/nicolas/Dropbox/ReposiTories/SpeechRec/output.wav"

    record()

    phrase = decodeSpeech(hmdir,lmd,dictd,jsgf,wavfile)

    answer = 'I am sorry. I did not understand that'
    if phrase == 'jenkins what time is it':
      answer = 'I do not know'
    elif phrase == 'jenkins what day is it' or phrase == 'jenkins what is the date':
      answer = 'It is ' + strftime("%B %d")
    elif phrase == 'jenkins say hello':
      answer = 'Hello'


    system('say %s' % answer)

    print "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"

    print phrase

    print "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"