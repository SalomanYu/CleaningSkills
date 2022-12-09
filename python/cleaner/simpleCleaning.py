from colorama import Style, Fore
import tools


def clean(skills: list[str]) -> tuple[str]:
    cleared = __clear_skills_from_100_percent_duplicates(skills)
    return cleared

def __clear_skills_from_100_percent_duplicates(skills: tuple[str]) -> tuple[str]:
    if not skills: return []
    cleared_skills = tuple(set(i.lower().strip() for i in skills))    
    cleared_skills_len = len(cleared_skills)  
    skills_len = len(skills)
    print(f"Start skills count: {Fore.GREEN}{skills_len}{Style.RESET_ALL}")
    print(f"Count skills after remove 100% duplicates: {Fore.GREEN}{cleared_skills_len} (-{tools.calculate_the_difference_in_percentages(skills_len, cleared_skills_len)}%){Style.RESET_ALL}")
    return cleared_skills

