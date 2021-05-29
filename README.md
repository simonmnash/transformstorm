# TRANSFORMSTORM
![Screenshot](https://github.com/simonmnash/transformstorm/blob/main/assets/version_zero_screenshot.png)

## About

This is a small interface built to play with small language models in the terminal.

I'm interested in experimenting with game-like and toy-like interactions with language models, especially when those models are small and fine tuned to operate in a  small subset of language. This is one of those experiments. The aspirational intent of this game is to explore and understand the kinds of language a given model is prone to producing.


## Installing and Running
To install run

`pip install transformstorm`

After installing, you can run

`transformstorm`

to download the 200wordrpg model and run. If you run `transformstorm` in a directory with a `model` subdirectory, it will attempt to load a pytorch model from that directory instead of pulling and loading the default model.
