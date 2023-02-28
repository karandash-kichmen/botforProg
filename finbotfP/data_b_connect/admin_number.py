import pymysql
from config import user, password, host, db_name, port


def get_admin_number(user=user, password=password, db_name=db_name, port=port, host=host):
    '''
    to get admin number
    :param user: sql user
    :param password: sql password
    :param db_name: sql db_name
    :param port: sql port
    :param host: sql host
    :return:
    '''
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
                insert_query = f"SELECT phone FROM `admins`;"
                cursor.execute(insert_query)
                connection.commit()
                adph = cursor.fetchall()
        finally:
            connection.close()
    except Exception as ex:
        print('Connection error...')
        print(ex)
    return adph
