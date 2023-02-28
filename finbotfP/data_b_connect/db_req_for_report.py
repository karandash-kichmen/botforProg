import pymysql
from config import user, password, host, db_name, port


def sql_get_rem_for_sat(name_of_table_category: str):
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
                insert_query = f"SELECT remainder FROM {name_of_table_category} " \
                               f"ORDER BY {name_of_table_category}.`id` DESC LIMIT 1;"
                cursor.execute(insert_query)
                result_remainder_money_categ = cursor.fetchone()[0]
                connection.commit()
        finally:
            connection.close()
        return result_remainder_money_categ
    except Exception as ex:
        print('Connection error...')
        print(ex)
