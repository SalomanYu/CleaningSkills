from fuzzywuzzy import process
from rich.progress import track
import storage

def match_skills_by_fuzzy(skills: list[storage.Infinitive], autosave: bool = False):
    lones: list[str] = []
    pairs: list[str] = []
    for index1 in track(range(len(skills)), description="[red]Finding by fuzzy"):
        infinitive = skills[index1].InfinitiveForm
        normal = skills[index1].NormalForm
        pair = process.extractOne(normal, (skills[index2].NormalForm for index2 in range(index1+1, len(skills))))
        print(pair, normal)

    return (lones, pairs)
