from pydub import AudioSegment
import requests
from main import get_record

def concatenate():
    # 요청받은 횟수만큼 get_record진행
    sound1 = get_record()
    sound2 = get_record()

    sound1 + sound2
    file_handle = overlay.export('output.m4a', format="m4a")



def overlay():
    # 요청받은 겹치는 트랙만큼 get_record 진행.
    sound1 = get_record()
    sound2 = get_record()

    overlay = sound1.overlay(sound2, position =0)
    file_handle = overlay.export('output.m4a', format="m4a")
