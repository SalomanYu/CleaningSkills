import cleaner
import storage


def start():
    # startSkills = storage.get_vacancies_skills()
    # if not startSkills: exit("Мы не смогли вытащить из вакансий ни одного навыка")
    # withoutRepeats = cleaner.clean(startSkills)
    # storage.save_skills_without_repeats(withoutRepeats)

    withoutRepeats = storage.get_skills_without_repeats()
    banalSkills = storage.get_banal_skills_from_json()
    storage.save_skills_banal(banalSkills)

    withoutBanal = cleaner.remove_banal_from_skills(withoutRepeats)
    storage.save_skills_without_banal(withoutBanal)

    # Пауза... Golang проверяет грамматику

    # grammaticalCorrected = storage.get_skills_grammatical_correction()
    # infinitiveSkills = cleaner.infinitive_skills(grammaticalCorrected)
    # storage.save_skills_infinitive(infinitiveSkills)

    # withoutRepeats = cleaner.clean(grammaticalCorrected)
    # storage.save_skills_without_repeats(withoutRepeats)

    # withoutBanal = cleaner.remove_banal_from_skills(withoutRepeats)
    # storage.save_skills_without_banal(withoutBanal)

    # lones, pairs = cleaner.match_skills(withoutBanal) # тут нужно передавать инфинитив
    
    # storage.save_skills_lone(lones)
    # storage.save_skills_pairs(pairs)

if __name__ == "__main__":
    start()