import pymysql
from config import user, password, host, db_name, port
from datetime import date


def last_remind_salary_personid(category: str, personid: str):
    try:
        connection = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=db_name
        )
        try:
            with connection.cursor() as cursor:
                insert_query = f"SELECT reminder FROM {category} " \
                               f"WHERE personid = {personid} AND deleted = 0 AND arhivated = 0  " \
                               f"ORDER BY id DESC LIMIT 1;"
                cursor.execute(insert_query)
                result_remainder_money_categ = cursor.fetchone()
                connection.commit()
        finally:
            connection.close()
        return result_remainder_money_categ
    except Exception as ex:
        print('Connection error...')
        print(ex)


def last_info_salary_personid(category: str, personid: str):
    try:
        connection = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=db_name
        )
        try:
            with connection.cursor() as cursor:
                insert_query = f"SELECT `id`, `name`, `surname`, `phone`, `koment`, `personid`,`typetransaction` FROM {category} " \
                               f"WHERE personid = {personid} AND deleted = 0 AND arhivated = 0  " \
                               f"ORDER BY id DESC LIMIT 1;"
                cursor.execute(insert_query)
                result_remainder_money_categ = cursor.fetchone()
                connection.commit()
        finally:
            connection.close()
        return result_remainder_money_categ
    except Exception as ex:
        print('Connection error...')
        print(ex)


def sql_add_salary(category: str, personid: str, reminder: str, to_count: str, name: str, surname: str, phone: str,
                   type_tansaction: str, koment: str = ""):
    try:
        connection = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=db_name
        )
        try:
            with connection.cursor() as cursor:
                insert_query = f"INSERT INTO {category} (`id`, `name`, `surname`, `phone`, " \
                               f"`profit`, `koment`, `personid`, `date`, `datetime`, `deleted`, " \
                               f"`arhivated`, `typetransaction`, `reminder`) " \
                               f"VALUES (NULL, '{name}', '{surname}', '{phone}', '{to_count}', '{koment}', '{personid}', " \
                               f"CURRENT_DATE(), NOW(), '0', '0', {type_tansaction}, '{reminder}'); "
                cursor.execute(insert_query)
                result_remainder_money_categ = cursor.fetchone()
                connection.commit()
        finally:
            connection.close()
        return result_remainder_money_categ
    except Exception as ex:
        print('Connection error...')
        print(ex)
