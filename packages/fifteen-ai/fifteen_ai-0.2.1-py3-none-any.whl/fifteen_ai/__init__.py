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
    """
    Generate speech from `text` using `character` with `emotion`.

    Do not save audio file if `filename` is None.

    """
    if len(text) > max_text_len:
        logging.warning(f"text longer than {max_text_len} characters; trimming")
        text = text[:max_text_len]
    if not text.endswith((".", "!", "?")):
        text += "."
    generation = requests.post(
        api_endpoint, json={"text": text, "character": character, "emotion": emotion}
    )
    if generation.status_code == 422:
        raise CharacterNotFound(character)
    response = generation.json()
    if filename:
        audio_data = requests.get(cdn_endpoint + response["wavNames"][0])
        with pathlib.Path(filename).open("wb") as fp:
            fp.write(audio_data.content)
    return response
