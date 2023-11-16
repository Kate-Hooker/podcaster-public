import sys
import os
import locale

import torch
from TTS.api import TTS


# TTS dependency num2words isn't happy with NZ Locale 
os.environ['LC_ALL'] = 'en_US.UTF-8'
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

device = "cuda" if torch.cuda.is_available() else "cpu"

def record(filename=None, duet=True):
    if filename:
        with open(filename, 'r') as file:
            script = file.read()
    else:
        if sys.stdin.isatty():
            print("Type or paste in the podcast script and hit ctrl D to process")
        script = sys.stdin.read()
    if duet:
        create_podcast_duet(script)
    else:
        create_podcast_vctk(script)

def create_podcast_vctk(text):
    tts = TTS(model_name="tts_models/en/vctk/vits", progress_bar=True).to(device)
    tts.tts_to_file(
        text=text, 
        speaker='p225',
        file_path="./assets/podcast.wav"
    )

def create_podcast_duet(text):
    tts = TTS(model_name="tts_models/en/vctk/vits", progress_bar=True).to(device)
    lines, _, _ = split_lines(text)
    recordings = []
    for line in lines:
        if line.startswith('Jenny:'):
            recordings.append(
                tts.tts( text=line[7:], speaker='p225')
            )
        elif line.startswith('Tim:'):
            recordings.append(
                tts.tts( text=line[4:], speaker='p226')
            )
    import numpy as np
    import soundfile as sf
    combined = np.concatenate(recordings)
    sf.write("./assets/duet.wav", combined, samplerate=24000)
    

def split_lines(text):
    lines = text.split('\n')
    lines = [line.strip() for line in lines if line.strip() != '']
    jenny_lines = [line for line in lines if line.startswith('Jenny:')]
    tim_lines = [line for line in lines if line.startswith('Tim:')]
    if (len(lines) != len(jenny_lines) + len(tim_lines)):
        raise Exception("Lines do not match", len(lines), len(jenny_lines), len(tim_lines))
    return lines, jenny_lines, tim_lines

