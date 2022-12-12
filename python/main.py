import cleaner
import storage


def start():
    # startSkills = storage.get_vacancies_skills()
    # if not startSkills: exit("Мы не смогли вытащить из вакансий ни одного навыка")
    # withoutRepeats = cleaner.clean(startSkills)
    # storage.save_skills_without_repeats(withoutRepeats)

    # # withoutRepeats = storage.get_skills_without_repeats()
    # banalSkills = storage.get_banal_skills_from_json()
    # storage.save_skills_banal(banalSkills)

    # withoutBanal = cleaner.remove_banal_from_skills(withoutRepeats)
    # storage.save_skills_without_banal(withoutBanal)

    # Пауза... Golang проверяет грамматику

    # grammaticalCorrected = storage.get_skills_grammatical_correction()
    # infinitiveSkills = cleaner.infinitive_skills(grammaticalCorrected)
    # storage.save_skills_infinitive(infinitiveSkills)
    # print("Привели навыки к начальной форме слов...")

    # withoutRepeats = cleaner.clean(grammaticalCorrected)
    # storage.save_skills_without_repeats(withoutRepeats)
    # print("Снова очистили от дубликатов")

    # withoutBanal = cleaner.remove_banal_from_skills(withoutRepeats)
    # storage.save_skills_without_banal(withoutBanal)
    # print("Снова очистили от банальных навыков")

    infinitiveSkills = storage.get_skills_infinitive()
    lones, pairs = cleaner.match_skills(infinitiveSkills, autosave=True) # тут нужно передавать инфинитив
    print(f"{len(lones)} lone")
    print(f"{len(pairs)} pairs")
    storage.save_skills_lone(lones)
    storage.save_skills_pairs(pairs)
    
if __name__ == "__main__":
    start()