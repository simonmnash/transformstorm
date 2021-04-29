# TRANSFORMSTORM
![Screenshot](https://github.com/simonmnash/transformstorm/blob/main/assets/version_zero_screenshot.png)

## About

This is a small interface built to play with small language models in the terminal.

I'm interested in experimenting with game-like and toy-like interactions with language models, especially when those models are small and fine tuned to operate in a  small subset of language. This is one of those experiments. The aspirational intent of this game is to explore and understand the kinds of language a given model is prone to producing.


## Installing and Running
To install either run

`pip install transformstorm`

or clone the repo and install through

`pip install -e .`

To run, put the model of interest in a directory named "model" and run 

`transformstorm`

The language model I built this interface for can be downloaded at https://www.simonmnash.com/asset_files/200_word_rpg_model.tar.gz or https://gyre.itch.io/human-machine-rpg-authoring-tool, but it should work for any huggingface/pytorch/gpt2 fine tuned model.
