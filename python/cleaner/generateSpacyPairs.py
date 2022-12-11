import ru_core_news_lg
from rich.progress import track
import storage


def match_skills(skills: list[storage.Infinitive]) -> tuple[list[str], list[storage.Pair]]:
    nlp = ru_core_news_lg.load()
    lones: list[str] = []
    pairs: list[storage.Pair] = []
    for index1 in track(range(len(skills)), description="[yellow]Find pairs..."):
        infinitive = skills[index1].InfinitiveForm
        normal = skills[index1].NormalForm
        doc1 = nlp(infinitive)
        try:
            pair_for_skill = next(skills[index2].NormalForm for index2 in range(index1+1, len(skills)) if doc1.similarity(nlp(skills[index2].InfinitiveForm))*100 > 80)
            pairs.append(storage.Pair(normal, pair_for_skill))
        except StopIteration: 
            lones.append(normal)
    return lones, pairs