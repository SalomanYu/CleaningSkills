import pymorphy2
from rich.progress import track

import storage


def infinitive_skills(skills: list[str]) -> list[storage.Infinitive]:
    pairs: list[storage.Infinitive] = []
    for item in track(range(len(skills)), description="[green]Transform skills to infinitive:"):
        infinitive_skills = bring_all_words_to_the_infinitive(skills[item])
        pairs.append(infinitive_skills)
    return pairs

def bring_all_words_to_the_infinitive(skill: str) -> str:
    morph = pymorphy2.MorphAnalyzer()
    infinitive = " ".join(morph.parse(i)[0].normal_form for i in skill.split())
    return storage.Infinitive(skill, infinitive)  


if __name__ == "__main__":
    infinitive_skills()