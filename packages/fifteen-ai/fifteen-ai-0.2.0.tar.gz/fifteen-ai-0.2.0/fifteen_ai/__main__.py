"""Speak given text."""

import sys

import playsound

import fifteen_ai

fifteen_ai.tts(sys.argv[1])
playsound.playsound("speech.wav")
