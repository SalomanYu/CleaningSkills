from colorama import Style, Fore

import redis

import tools
import storage

NAME_SET_BANAL_SKILLS = "banal"
NAME_SET_WITHOUT_BANAL = "without_banal"

def remove_banal_from_skills(skills: list[str]) -> list[str]:
    """Не учитывается перечисление по типу: в навыке вакансии 'коммуникабельность, ответственность' не будет найден навык 'коммуникабельность' """
    banal = storage.get_banal_skills()
    print(f"Count skills with banal words: {Fore.RED}{len(skills)}{Style.RESET_ALL}")
    skills_without_banal = set(i.lower() for i in skills) - set(i.lower() for i in banal)
    print(f"Count skills without banal words: {Fore.GREEN}{len(skills_without_banal)} (-{tools.calculate_the_difference_in_percentages(len(skills), len(skills_without_banal))}%){Style.RESET_ALL}")
    return skills_without_banal


if __name__ == "__main__":
    banal = storage.get_banal_skills_from_json()
    storage.save_skills_banal(banal)

    red = redis.StrictRedis("localhost", 6379)
    skills = [i.decode("utf-8") for i in red.smembers("without_repeats")]
    without_banal = remove_banal_from_skills(skills)
    storage.save_skills_without_banal(without_banal)