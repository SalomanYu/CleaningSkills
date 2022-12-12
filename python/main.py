import cleaner
import pairs
import storage
import sys
from typing import Literal

errorMessage = f"\n".join((
                "Используйте следующие команды:",
                "-all \t очищает навыки от точных повторений, банальных навыках, приводит слова к инфинитиву и составляет пары",
                "-simple \t очищает навыки от точных повторений, банальных навыках",
                "-inf \t приводит слова к инфинитиву",
                "-pairs \t составляет пары. Требуется передать дополнительный аргумент (spacy, fuzzy)"
            ))

def start():
    if len(sys.argv) <= 1: exit(errorMessage)    
    match sys.argv[1]:
        case "-all":
            if len(sys.argv) <= 2: exit("Укажите метод обработки скиллов! (spacy or fuzzy)") 
            run_simple_cleaning()
            run_transformation_to_infinitive()
            run_combining_skills(method=sys.argv[2])
        case "-simple": 
            run_simple_cleaning()
        case "-inf":
            run_transformation_to_infinitive()
        case "-pairs":
            if len(sys.argv) <= 2: exit("Укажите метод обработки скиллов! (spacy or fuzzy)") 
            run_combining_skills(method=sys.argv[2])
        case _:
            exit(errorMessage)

def run_simple_cleaning():

    startSkills = storage.get_vacancies_skills()
    if not startSkills: exit("Мы не смогли вытащить из вакансий ни одного навыка")
    withoutRepeats = cleaner.clean(startSkills)
    storage.save_skills_without_repeats(withoutRepeats)

    withoutRepeats = storage.get_skills_without_repeats()
    banalSkills = storage.get_banal_skills_from_json()
    storage.save_skills_banal(banalSkills)

    withoutBanal = cleaner.remove_banal_from_skills(withoutRepeats)
    storage.save_skills_without_banal(withoutBanal)

    # Пауза... Golang проверяет грамматику

def run_transformation_to_infinitive():
    grammaticalCorrected = storage.get_skills_grammatical_correction()
    infinitiveSkills = cleaner.infinitive_skills(grammaticalCorrected)
    storage.save_skills_infinitive(infinitiveSkills)
    print("Привели навыки к начальной форме слов...")


def run_simple_cleaning_after_grammatical_correction():
    grammaticalCorrected = storage.get_skills_grammatical_correction()
    withoutRepeats = cleaner.clean(grammaticalCorrected)
    storage.save_skills_without_repeats(withoutRepeats)
    print("Снова очистили от дубликатов")

    withoutBanal = cleaner.remove_banal_from_skills(withoutRepeats)
    storage.save_skills_without_banal(withoutBanal)
    print("Снова очистили от банальных навыков")

def run_combining_skills(method: Literal["fuzzy", "spacy"]):
    infinitiveSkills = storage.get_skills_infinitive()
    match method:
        case "fuzzy":
            lones, finded_pairs = pairs.match_skills_by_fuzzy(infinitiveSkills, autosave=True) # тут нужно передавать инфинитив
        case "spacy":
            lones, finded_pairs = pairs.match_skills_by_spacy(infinitiveSkills, autosave=True) # тут нужно передавать инфинитив
        case _:
            exit("выбран неправильный метод обработки скиллов. Доступно два варианта: spacy, fuzzy")

    if lones or finded_pairs:
        print(f"{len(lones)} lone")
        print(f"{len(pairs)} finded_pairs")
        storage.save_skills_lone(lones)
        storage.save_skills_pairs(finded_pairs)

if __name__ == "__main__":
    start()
    