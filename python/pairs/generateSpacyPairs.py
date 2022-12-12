import ru_core_news_lg
from rich.progress import track
import storage


def match_skills_by_spacy(skills: list[storage.Infinitive], autosave: bool = False) -> tuple[list[str], list[storage.Pair]]:
    nlp = ru_core_news_lg.load()
    lones: list[str] = []
    pairs: list[storage.Pair] = []
    for index1 in track(range(10,len(skills)), description="[yellow]Find pairs by spacy..."):
        has_pair = False
        infinitive = skills[index1].InfinitiveForm
        normal = skills[index1].NormalForm
        doc1 = nlp(infinitive)
        if not doc1.vector_norm: continue
        for index2 in range(index1+1, len(skills)):
            doc2 = nlp(skills[index2].InfinitiveForm)
            if not doc2.vector_norm: continue
            similarity = doc1.similarity(doc2) * 100
            if similarity >= 95:
                has_pair = True
                if autosave:storage.save_skills_lone((normal,)) # Сохраняем только один вариант, т.к понимаем, что у него есть пара, для которой вероятно не требуется подтверждения
                else: lones.append(normal)
                break
            elif similarity >= 80:
                has_pair = True
                if autosave:storage.save_skills_pairs((storage.Pair(normal, skills[index2].NormalForm), ))
                else: pairs.append(storage.Pair(normal, skills[index2].NormalForm))
                break
        if not has_pair:
            if autosave:storage.save_skills_lone((normal, ))
            else:lones.append(normal)
    return lones, pairs