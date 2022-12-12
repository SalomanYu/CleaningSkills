import os
from enum import Enum
from typing import NamedTuple

import pymysql 


class SimilarCouple(NamedTuple):
    Id              :int
    SkillId       :int
    SkillName     :str
    DuplicateId   :int
    DuplicateName :str
    Similarity      :int
    IsDuplicate    :bool

class MYSQL(Enum):
    HOST = os.getenv("EDWICA_DB_HOST")
    USER = os.getenv("EDWICA_DB_USER")
    PASSWORD = os.getenv("EDWICA_DB_PASS")
    PORT = 3306
    DB = "edwica"
    TABLE = "demand_duplicate"


def connect_to_db() -> pymysql.connections.Connection:
    try:
        connection = pymysql.connect(
                host=MYSQL.HOST.value,
                port=MYSQL.PORT.value,
                database=MYSQL.DB.value,
                user=MYSQL.USER.value,
                password=MYSQL.PASSWORD.value,
                cursorclass=pymysql.cursors.DictCursor
            )
        print("Success connection to db..")
        return connection

    except Exception as ex:
        exit(f"Error by connection: {ex}")

def __collect_duplicates() -> list[SimilarCouple]:
    result: list[SimilarCouple] = []

    connection = connect_to_db()
    try:
        with connection.cursor() as cursor:
            query = f"SELECT * FROM {MYSQL.TABLE.value} WHERE is_duplicate=1;"
            cursor.execute(query)
            result = [SimilarCouple(*i.values()) for i in cursor.fetchall()]
    except:
        print("Не удалось подключиться к базе")
    finally:
        return result

def get_duplicates() -> list[str]:
    couples = __collect_duplicates()
    return [i.DuplicateName for i in couples]


if __name__ == "__main__":
    get_duplicates()