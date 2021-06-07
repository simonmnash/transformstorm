# TRANSFORMSTORM
![Screenshot](https://github.com/simonmnash/transformstorm/blob/main/assets/version_zero_screenshot.png)

## About

This is a small interface built to play with small language models in the terminal.

I think language models are most interesting as a way of exploring common patterns in the parts of languge they are fine tuned on, but I am not a huge fan of sentence completion or conversation as a way of interacting with them. I fine tuned gpt2 on RPGs from the 200 Word RPG Challenge (https://200wordrpg.github.io/), and I wanted a new way of exploring the kind of language the model would generate, so I built a terminal interface to provide an interactive way to see what kinds of phrases, idioms, and patterns of speech the model would generate in an interactive environment, where the user can guide text generation, but can't prompt the model directly.


## Installing and Running
To install run

`pip install transformstorm`

After installing, you can run

`transformstorm`

to download the 200wordrpg model and run. If you run `transformstorm` in a directory with a `model` subdirectory, it will attempt to load a pytorch model from that directory instead of pulling and loading the default model.

You can also run

`transformstorm --name NAMEOFAMODELONHUGGINGFACE`

to download any other huggingface CasualLM model and run the interface with it.
