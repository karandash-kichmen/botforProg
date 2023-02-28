import pymysql
from config import user, password, host, db_name, port
from datetime import date


def funds_SQL_add(funds: int, funds_category: str, comment: str, order: str, remainder: int = 0,
                  type_transaction: int = 1,
                  archived: bool = 0, deleted: bool = 0, done_in_crm: bool = 0):
    '''
    for the function to work, you need to create a file config with such fields

    host = ""
    user = ""
    password = ""
    db_name = ""
    port = integer value

    in order for the function to work, you need to create a file
    :param funds: integer value of fund money. Get from customer
    :param funds_category: category of funds. For each section its own
    :param comment: srt comment from customer for transaction
    :param order: srt comment with order information from customer for transaction
    :param type_transaction: integer number of type transaction
    :param archived: true or false
    :param deleted: true or false
    :param done_in_crm: true or false
    :param remainder: balance of funds taking into account this transaction
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
                insert_query = f"INSERT INTO `{funds_category}` (`id`, `funds`, `comment`, `order_coment`, " \
                               f"`transfer`, `operation_date`, `operationDateTime`, `type_transaction`, " \
                               f"`archived`, `deleted`, `done_in_crm`, `remainder`) " \
                               f"VALUES (NULL, '{funds}', '{comment}', '{order}', '0', " \
                               f"NOW(), CURRENT_DATE(), '{type_transaction}', '{archived}', '{deleted}', " \
                               f"'{done_in_crm}','{remainder}'); "
                cursor.execute(insert_query)
                connection.commit()
        finally:
            connection.close()
    except Exception as ex:
        print('Connection error...')
        print(ex)


def res_remainder_money(category: str):
    """
    for the function to work, you need to create a file config with such fields

    host = ""
    user = ""
    password = ""
    db_name = ""
    port = integer value

    :return:
    """
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
                insert_query = f"SELECT remainder FROM {category} " \
                               f"WHERE {category}.`deleted` = 0 ORDER BY id DESC LIMIT 1"
                cursor.execute(insert_query)
                result_remainder_money = int(list(cursor.fetchone())[0])
                print(result_remainder_money)
                connection.commit()
        finally:
            connection.close()
        return result_remainder_money
    except Exception as ex:
        print('Connection error...')
        print(ex)


def sql_get_balance_money_incategory(category: str):
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
                insert_query = f'SELECT remainder FROM {category} ORDER BY id DESC LIMIT 1;'
                cursor.execute(insert_query)
                result_remainder_money = cursor.fetchone()
                connection.commit()
        finally:
            connection.close()
        return result_remainder_money
    except Exception as ex:
        print('Connection error...')
        print(ex)


def sql_get_last_5_orders(category: str):
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
                insert_query = f'SELECT id, funds, comment, order_coment, operation_date FROM {category} ' \
                               f'ORDER BY id DESC LIMIT 5;'
                cursor.execute(insert_query)
                result_remainder_money = cursor.fetchall()
                connection.commit()
        finally:
            connection.close()
        return result_remainder_money
    except Exception as ex:
        print('Connection error...')
        print(ex)


def sql_get_next_5_orders(category: str, id_for_next_step, id_for_next_step_to):
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
                insert_query = f'SELECT id, funds, comment, order_coment, operation_date FROM {category} ' \
                               f'WHERE id BETWEEN {id_for_next_step} AND {id_for_next_step_to} ORDER BY id DESC;'
                cursor.execute(insert_query)
                result_remainder_money = cursor.fetchall()
                connection.commit()
        finally:
            connection.close()
        return result_remainder_money
    except Exception as ex:
        print('Connection error...')
        print(ex)


def sql_get_past_5_orders(category: str, id_for_past_step, id_for_past_step_to):
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
                insert_query = f'SELECT id, funds, comment, order_coment, operation_date FROM {category} ' \
                               f'WHERE id BETWEEN {id_for_past_step} AND {id_for_past_step_to} ORDER BY id DESC;'
                cursor.execute(insert_query)
                result_remainder_money = cursor.fetchall()
                connection.commit()
        finally:
            connection.close()
        return result_remainder_money
    except Exception as ex:
        print('Connection error...')
        print(ex)


def sql_delete_transaction_from_category(category: str, id_of_transaction_for_delet: str):
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
                insert_query = f"UPDATE `{category}` SET `deleted` = '1' " \
                               f"WHERE `{category}`.`id` = {id_of_transaction_for_delet};"
                cursor.execute(insert_query)
                result_remainder_money = cursor.fetchall()
                connection.commit()
        finally:
            connection.close()
        return result_remainder_money
    except Exception as ex:
        print('Connection error...')
        print(ex)


def sql_archived_transaction_from_category(category: str, id_of_transaction_for_delet: str):
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
                insert_query = f"UPDATE `{category}` SET `archived` = '1' " \
                               f"WHERE `{category}`.`id` = {id_of_transaction_for_delet};"
                cursor.execute(insert_query)
                result_remainder_money = cursor.fetchall()
                connection.commit()
        finally:
            connection.close()
        return result_remainder_money
    except Exception as ex:
        print('Connection error...')
        print(ex)


def sql_get_transaction_info_in_cats(category: str, id_of_transaction_for_delet: str):
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
                insert_query = f'SELECT * FROM {category} ' \
                               f'WHERE `{category}`.`id` = {id_of_transaction_for_delet}'
                cursor.execute(insert_query)
                result_remainder_money = cursor.fetchone()
                connection.commit()
        finally:
            connection.close()
        return result_remainder_money
    except Exception as ex:
        print('Connection error...')
        print(ex)


def sql_get_rem_mons_cats(category: str, last_month_for_sql: str, this_month_for_sql: str):
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
                insert_query = f"SELECT remainder FROM {category} WHERE operationDateTime " \
                               f"BETWEEN '2023-0{last_month_for_sql}-01 00:00:00' " \
                               f"AND '2023-0{this_month_for_sql}-01 00:00:00' " \
                               f"AND {category}.`deleted` = 0 AND {category}.`archived` = 0 " \
                               f"ORDER BY `operation_date` DESC LIMIT 1;"
                cursor.execute(insert_query)
                result_remainder_money_categ = cursor.fetchone()[0]
                connection.commit()
        finally:
            connection.close()
        return result_remainder_money_categ
    except Exception as ex:
        print('Connection error...')
        print(ex)


def sql_add_rem_mons_cats(category: str, last_month_for_sql: str, remainder: str):
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
                this_year_for_sql = str(date.today().year)
                insert_query = f"INSERT INTO `balance_monthly` (`id`, `category`, `remainder`, `date_time`," \
                               f" `month_reminder`, `year_reminder`) " \
                               f"VALUES (NULL, '{category}', '{remainder}', NOW(), " \
                               f"{last_month_for_sql}, {this_year_for_sql}); "
                cursor.execute(insert_query)
                connection.commit()
        finally:
            connection.close()
    except Exception as ex:
        print('Connection error...')
        print(ex)


def sql_get_rem_per_last_month(category: str, last_month_for_sql: str):
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
                this_year_for_sql = str(date.today().year)
                insert_query = f"SELECT * FROM `balance_monthly` WHERE `category` = '{category}' " \
                               f"AND `month_reminder` = {last_month_for_sql} AND `year_reminder` = {this_year_for_sql}"
                cursor.execute(insert_query)
                result_remainder_money_categ = cursor.fetchall()
                print(result_remainder_money_categ)
                connection.commit()
        finally:
            connection.close()
        return result_remainder_money_categ
    except Exception as ex:
        print('Connection error...')
        print(ex)


# Бюджети
def sql_get_budget_month():
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
                this_year_for_sql = str(date.today().year)
                insert_query = f"SELECT * FROM `intro_budget`"
                cursor.execute(insert_query)
                result_remainder_money_categ = cursor.fetchall()
                connection.commit()
        finally:
            connection.close()
        return result_remainder_money_categ
    except Exception as ex:
        print('Connection error...')
        print(ex)


def sql_get_sum_budget_month():
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
                this_year_for_sql = str(date.today().year)
                insert_query = f"SELECT SUM(budget) FROM `intro_budget`"
                cursor.execute(insert_query)
                result_remainder_money_categ = cursor.fetchone()
                connection.commit()
        finally:
            connection.close()
        return result_remainder_money_categ
    except Exception as ex:
        print('Connection error...')
        print(ex)


# Отримання залишку ЗП

def sql_get_rem_divident_bud(category: str, personid: str):
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
                insert_query = f"SELECT name, reminder FROM {category} " \
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
