import os
import sys
from dotenv import load_dotenv
import json
import csv
import redis
from enum import Enum
from typing import NamedTuple

dotenv_path = ".env"
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
else:
    exit("Не найден файл .env, содержащий переменные окружения")

SKILLS_COLUMN = 9
if sys.platform == "win32": FOLDER_VACANCIES = "C:\Projects\Go\src\Vacancies"
elif sys.platform == "linux": FOLDER_VACANCIES = "../../Vacancies"

def __check_enviroment_variables(variable: Enum):
    if None in (variable.WITHOUT_REPEATS.value, variable.WITHOUT_BANAL.value, variable.BANAL.value, variable.GRAMMATICAL_CORRECTION.value, 
    variable.GRAMMATICAL_ERRORS.value, variable.INFINITIVE.value, variable.PAIRS.value, variable.LONE.value):
        exit("Неправильно заданы переменные окружения!")

class SetRedis(Enum):
    WITHOUT_REPEATS = os.getenv("SET_WITHOUT_REPEATS")
    WITHOUT_BANAL = os.getenv("SET_WITHOUT_BANAL")
    BANAL = os.getenv("SET_BANAL")
    GRAMMATICAL_CORRECTION = os.getenv("SET_GRAMMATICAL_CORRECTION")
    GRAMMATICAL_ERRORS = os.getenv("SET_GRAMMATICAL_ERRORS")
    INFINITIVE = os.getenv("SET_INFINITIVE")
    PAIRS = os.getenv("SET_PAIRS")
    LONE = os.getenv("SET_LONE")

__check_enviroment_variables(SetRedis)

class Correction(NamedTuple):
    WrongVersion    :str
    CorrectVersion  :str

class Pair(NamedTuple):
    First           :str
    Second          :str

class Infinitive(NamedTuple):
    NormalForm      :str
    InfinitiveForm  :str


def get_vacancies_skills():
    skills = []
    files_count = len(os.listdir(FOLDER_VACANCIES))
    count = 0
    for file in os.listdir(FOLDER_VACANCIES):
        count += 1
        file_skills = __get_skills_from_CSV(os.path.join(FOLDER_VACANCIES, file))
        skills += file_skills
        print(f"{count}/{files_count}. {file}")
    return skills


def __get_skills_from_CSV(csvPath: str):
    file_skills = []
    with open(csvPath, newline="", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile, delimiter=";")
        for index, row in enumerate(reader):
            if index == 0: continue # Пропускаем название колонки
            try:
                file_skills += row[SKILLS_COLUMN].split("|")
            except IndexError:
                break
    return file_skills

def get_banal_skills_from_json():
    data = json.load(open("data/json/banalList.json", encoding="utf-8", mode="r"))
    return data

def get_skills_without_repeats() -> list[str]:
    red = redis.StrictRedis("localhost", 6379)
    try:return [i.decode("utf-8") for i in red.smembers(SetRedis.WITHOUT_REPEATS.value)]
    except:exit(f"Ключ {SetRedis.WITHOUT_REPEATS.value} не существует")

def get_skills_without_banals() -> list[str]:
    red = redis.StrictRedis("localhost", 6379)
    try:return [i.decode("utf-8") for i in red.smembers(SetRedis.WITHOUT_BANAL.value)]
    except:exit(f"Ключ {SetRedis.WITHOUT_BANAL.value} не существует")

def get_banal_skills() -> list[str]:
    red = redis.StrictRedis("localhost", 6379)
    try:return [i.decode("utf-8") for i in red.smembers(SetRedis.BANAL.value)]
    except:exit(f"Ключ {SetRedis.BANAL.value} не существует")

def get_skills_grammatical_correction() -> list[str]:
    """Возвращаем только правильные варианты"""
    red = redis.StrictRedis("localhost", 6379)
    try:return [i.decode("utf-8").split("|")[-1] for i in red.smembers(SetRedis.GRAMMATICAL_CORRECTION.value)]
    except:exit(f"Ключ {SetRedis.GRAMMATICAL_CORRECTION.value} не существует")

def get_skills_lone() -> list[str]:
    red = redis.StrictRedis("localhost", 6379)
    try:return [i.decode("utf-8") for i in red.smembers(SetRedis.LONE.value)]
    except:exit(f"Ключ {SetRedis.LONE.value} не существует")

def get_skills_grammatical_errors() -> list[Correction]:
    red = redis.StrictRedis("localhost", 6379)
    items = (i.decode("utf-8") for i in red.smembers(SetRedis.GRAMMATICAL_ERRORS.value))
    try:return [Correction(*item.split("|")) for item in items]
    except:exit(f"Ключ {SetRedis.GRAMMATICAL_ERRORS.value} не существует")


def get_skills_infinitive() -> list[Infinitive]:
    """Возвращаем только инфинитив"""
    red = redis.StrictRedis("localhost", 6379)
    items =  [i.decode("utf-8") for i in red.smembers(SetRedis.INFINITIVE.value)]
    try:return [Infinitive(*item.split("|")) for item in items]
    except:exit(f"Ключ {SetRedis.INFINITIVE.value} не существует")

def get_skills_pairs() -> list[Pair]:
    red = redis.StrictRedis("localhost", 6379)
    items = [i.decode("utf-8") for i in red.smembers(SetRedis.PAIRS.value)]
    try:return [Pair(*item.split("|")) for item in items]
    except:exit(f"Ключ {SetRedis.PAIRS.value} не существует")


def save_skills_without_repeats(skills :list[str]):
    red = redis.StrictRedis("localhost", 6379)
    try:red.delete(SetRedis.WITHOUT_REPEATS.value) # Перезаписываем 
    except:pass 
    for item in skills:
        if item is not None:red.sadd(SetRedis.WITHOUT_REPEATS.value, item)

def save_skills_without_banal(skills :list[str]):
    red = redis.StrictRedis("localhost", 6379)
    try:red.delete(SetRedis.WITHOUT_BANAL.value) # Перезаписываем 
    except:pass
    for item in skills:
        if item is not None:red.sadd(SetRedis.WITHOUT_BANAL.value, item)

def save_skills_banal(skills :list[str]):
    red = redis.StrictRedis("localhost", 6379)
    try:red.delete(SetRedis.BANAL.value) # Перезаписываем 
    except:pass
    for item in skills:
        if item is not None:red.sadd(SetRedis.BANAL.value, item)

def save_skills_lone(skills :list[str]):
    red = redis.StrictRedis("localhost", 6379)
    try:red.delete(SetRedis.LONE.value) # Перезаписываем 
    except:pass
    for item in skills:
        if item is not None:red.sadd(SetRedis.LONE.value, item)

def save_skills_grammatical_correction(skills :list[Correction]):
    red = redis.StrictRedis("localhost", 6379)
    try:red.delete(SetRedis.GRAMMATICAL_CORRECTION.value) # Перезаписываем 
    except:pass
    for item in skills:
        if item is not None:red.sadd(SetRedis.GRAMMATICAL_CORRECTION.value, item)


def save_skills_grammatical_errors(skills :list[Correction]):
    red = redis.StrictRedis("localhost", 6379)
    try:red.delete(SetRedis.GRAMMATICAL_ERRORS.value) # Перезаписываем 
    except:pass
    for item in skills:
        value = "|".join((item.WrongVersion, item.CorrectVersion))
        if item is not None:red.sadd(SetRedis.GRAMMATICAL_ERRORS.value, value)

def save_skills_infinitive(skills :list[Infinitive]):
    red = redis.StrictRedis("localhost", 6379)
    try:red.delete(SetRedis.INFINITIVE.value) # Перезаписываем 
    except:pass
    for item in skills:
        value = "|".join((item.NormalForm, item.InfinitiveForm))
        if item is not None:red.sadd(SetRedis.INFINITIVE.value, value)

def save_skills_pairs(skills :list[Pair]):
    red = redis.StrictRedis("localhost", 6379)
    try:red.delete(SetRedis.PAIRS.value) # Перезаписываем 
    except:pass
    for item in skills:
        value = "|".join((item.First, item.Second))
        if item is not None:red.sadd(SetRedis.PAIRS.value, value)



if __name__ == "__main__":
    print(get_skills_grammatical_errors())