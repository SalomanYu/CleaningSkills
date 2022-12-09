import ru_core_news_lg
from rich.progress import track
import storage


def match_skills(skills: list[str]) -> tuple[list[str], list[storage.Pair]]:
    nlp = ru_core_news_lg.load()
    lones: list[str] = []
    pairs: list[storage.Pair] = []
    for index1 in track(range(len(skills)), description="[yellow]Find pairs..."):
        skill = skills[index1]
        doc1 = nlp(skill)
        try:
            pair_for_skill = next(skills[index2] for index2 in range(index1+1, len(skills)) if doc1.similarity(nlp(skills[index2]))*100 > 80)
            pairs.append(storage.Pair(skill, pair_for_skill))
        except StopIteration: 
            lones.append(skill)
    return lones, pairs