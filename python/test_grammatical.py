import requests
import urllib.parse
from typing import NamedTuple
import storage
import time
from rich.progress import track

SUITABLE_OPTION = 0

class WrongWord(NamedTuple):
    WrongVersion    :str
    CorrectVersion  :str


def correct_the_text(text: str) -> str:
    wrong_words = check_text(text)
    if not wrong_words: return text
    for word in wrong_words:
        text = text.replace(word.WrongVersion, word.CorrectVersion)
    return text 

def check_text(text: str) -> tuple[WrongWord]:
    data = {
        "text": text,
        "lang": "ru, en"
        }
    req = requests.get("https://speller.yandex.net/services/spellservice.json/checkText?", urllib.parse.urlencode(data))
    if req.status_code != 200: return 
    result = (WrongWord(WrongVersion=item["word"], CorrectVersion=item["s"][SUITABLE_OPTION]) for item in req.json())
    return result


if __name__ == "__main__":
    start = time.time()
    skills = storage.get_skills_without_banals()[:1000]
    for skill in track(range(len(skills)), description="[green]Progress:"):
        result = correct_the_text(skill)
    print(time.time() - start, "sec.")
