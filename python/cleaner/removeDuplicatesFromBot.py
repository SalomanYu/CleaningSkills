import tools
import storage
import sqldb

def removeSkillsIfTheyInSQLDuplicatesDatabase(skills: list[str], duplicates: list[str]):
    without_duplicates = set((i.lower() for i in skills)) - set((i.lower() for i in duplicates))
    print(set((i.lower() for i in skills)) & set((i.lower() for i in duplicates)))
    print(f"Количество навыков до удаления повторений {len(skills)}")
    print(f"Количество навыков после удаления повторений {len(without_duplicates)} (-{tools.calculate_the_difference_in_percentages(len(skills), len(without_duplicates))}%)")

