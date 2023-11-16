# Podcaster

This is a tool for creating a podcast with an AI presenter.

## Setup

** Fork this repo to your user account **

```
git clone https://github.com/[your-username]/podcaster.git
cd podcaster
git remote add upstream https://github.com/practical-ai-for-devs/podcaster
```

### Python Environment
```
conda create -n podcaster python=3.11
conda activate podcaster
conda install pip
pip install -r requirements.txt
```

Note this project uses pytorch so the install may be a little longer if you have to download it for the first time.

### Installing (optional)
If you want to install the cli tool globally in your machine be sure to deactivate conda first so you can call it anywhere in your terminal.

```
conda deactivate
pip install .
```

If you run `pip install .` while still in your conda environment the tool will only be available when that environment is active, which may be what you want.


## Running

```
python main.py
```

or once it has been installed with pip you can type `podcaster` in your command line. 

## Step 0: 
Review `podcaster/commands/script.py`. Notice how it has 3 modes for receiving input:

1. from a file, if the filename is passed in
2. from stdin if it is run with no args so you can paste text in
3. from stdin piped (`sys.stdin.isatty() == False`) so you can run a commaind like `summarise MyPDF.pdf | python main.py script` (assuming you have the summarise project from last year installed in the same conda env

## Step 1: Script a podcast
Use langchain and the llm of your choice to create a script for a podcast.

You will need to play around with getting a prompt that is reliable and gives you a script you are happy with. This gets close to the limits of what the free cohere model can do (JV found Mistral performed better).

You can either save the script to a file or print it out to stdout. If you are printing it out you may find it useful to send it to a file for using later with `python main.py script input.txt > script.txt`

## Step 2: Record your podcast
create a `record` command so you can turn your script into a podcast.

Use the python [TTS](https://tts.readthedocs.io/en/latest/inference.html) library to turn your script into audio.

The library supports a lot of models so feel free to experiment. The tts_models/en/vctk/vits model is fairly small (~200MB) and fast to generate on cpu as well as gpu. There are other models which sound better though.

```python
    tts = TTS(model_name="tts_models/en/vctk/vits", progress_bar=True).to(device)
    tts.tts_to_file(
        text=text, 
        speaker='p225',
        file_path="./podcast.wav"
    )

```

You can call `print(tts.speakers)` to see a list of available speakers for a multi speaker model and run `tts --list_models` in the command line to see all the available models (there are lots).

Note: if you have any problems getting the TTS library working you can still complete this challenge by using the free tier apis of - [coqui](https://coqui.ai/pricing), [elevenlabs](https://elevenlabs.io/pricing), or [playht](https://play.ht/pricing/) 

## Step 3: Script a podcast with two hosts
Add a `--duet` flag to to the script command so if it is set the llm will script the podcast for two hosts instead of one.

Something like
```
  script_subparser = cmd_parser.add_parser('script')
  script_subparser.add_argument('filename', help='The filename to process', nargs='?')
  script_subparser.add_argument('--duet', action='store_true', help='Use duet')
```
will mean you can pass have both `filename` and `duet` on your args object.

## Step 4: Record a podcast with two hosts
Add a `--duet` flag to the record command (or you could get fancy and try to auto detect the number of hosts based off the script) and record a multi speaker podcast.

You may want to use the [tts](https://github.com/coqui-ai/TTS/blob/6fef4f9067c0647258e0cd1d2998716565f59330/TTS/api.py#L305C9-L305C12) function instead of tts_to_file which will return a wav object you can join together with something like

```python
    import numpy as np
    import soundfile as sf
    combined = np.concatenate(recordings) #assuming recordings is a list of wav objects
    sf.write("./assets/duet.wav", combined, samplerate=24000)
```
Note the sample rate will be different depending on the model you use. You can look it up or just change the number until you are happy with the output.

## Step 5: Congratulations
Combined with the summariser, you've just rolled your own version of https://www.letsrecast.ai/

Feel free to share any interesting podcasts you create in discord.

## Stretch
- use [bark](https://tts.readthedocs.io/en/latest/models/bark.html) or [chirp](https://suno-ai.notion.site/Chirp-v1-Examples-cc71e6c0c79f4e03acf39aa5d5a3dd09) to create an audio intro to your podcast
- use a text to image model to make a cover for your podcast
- use the [xtts model](https://tts.readthedocs.io/en/latest/models/xtts.html) (be sure to read the license) to clone a voice
- use [coqui](https://coqui.ai/pricing), [elevenlabs](https://elevenlabs.io/pricing), or [playht](https://play.ht/pricing/) apis (all have free credits) to create a podcast with emotive presentation
