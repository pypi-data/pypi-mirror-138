"""TTS (text-to-speech) by 15.ai."""

import logging
import pathlib

import requests

api_endpoint = "https://api.15.ai/app/getAudioFile5"
cdn_endpoint = "https://cdn.15.ai/audio/"
max_text_len = 199


class CharacterNotFound(Exception):
    """Character could not be found."""


def tts(text, character="GLaDOS", emotion="Contextual", filename="speech.wav"):
    """Generate speech from `text` using `character` with `emotion`."""
    if len(text) > max_text_len:
        logging.warning(f"text longer than {max_text_len} characters; trimming")
        text = text[:max_text_len]
    if not text.endswith((".", "!", "?")):
        text += "."
    filename = pathlib.Path(filename)
    generation = requests.post(
        api_endpoint, json={"text": text, "character": character, "emotion": emotion}
    )
    if generation.status_code == 422:
        raise CharacterNotFound(character)
    audio = requests.get(cdn_endpoint + generation.json()["wavNames"][0])
    with filename.open("wb") as fp:
        fp.write(audio.content)
