import asyncio
import aiocron
import aiogram
import pymysql
import report_on_accounts

from datetime import date
from aiogram.dispatcher.fsm.state import StatesGroup, State
from aiogram import Router, types
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config import user, password, host, db_name, port

from data_b_connect import admin_number, sql_сursor_request, config, sql_request_for_salary
from bot_keyboards import navigation_keyboards, operstions_keyboards
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)
# Об'єкт боту
bot = aiogram.Bot('TOKEN')
# Диспечер
dp = aiogram.Dispatcher()

router = Router()


# ### Підрахунок залишку на кінець місяця ###
# 1. Отримання залишку на кінець місяця по категоріях. Отримання поточного місяця, -1
@aiocron.crontab('0 1 1 * *')
async def monthly_reminder_fo_sql():
    last_month_for_sql = str(date.today().month - 1)  # last month
    this_month_for_sql = str(date.today().month)  # this month
    this_year_for_sql = str(date.today().year)  # this month
    monthly_reminder_common = 0  # monthly reminder
    for i in range(len(operstions_keyboards.list_category_transaction)):
        category_for_sql_rem = operstions_keyboards.list_category_transaction[i]
        monthly_reminder_get = sql_сursor_request.sql_get_rem_mons_cats(category_for_sql_rem,
                                                                        last_month_for_sql,
                                                                        this_month_for_sql)
        # Пеневірка, чи вже доданий схожий запис.
        monthly_reminder = list(sql_сursor_request.sql_get_rem_per_last_month(category=category_for_sql_rem,
                                                                              last_month_for_sql=last_month_for_sql))
        if len(monthly_reminder) == 0:
            # 2. Залишок загальний за місяць + Запис залишку в таблицю
            if monthly_reminder_get is not None:
                monthly_reminder_common = monthly_reminder_common + monthly_reminder_get
                # 3. Запис залишку в таблицю
                sql_сursor_request.sql_add_rem_mons_cats(category=category_for_sql_rem,
                                                         last_month_for_sql=last_month_for_sql,
                                                         remainder=monthly_reminder_get)
        else:
            print('Не нада создавать')
        print('***********************************************')
    # 4. Архівування всі старі транзакції. Поки що не бачу сенсу в архівуванні


# Перевірити логіки роботи архівування та видалення транзакцій

# Робота з бюджетом
@dp.callback_query(text='budget_month_nav')
async def callback_category_nav_get_budget(callback: aiogram.types.CallbackQuery):
    list_of_budgets = list(sql_сursor_request.sql_get_budget_month())
    builder_menu_keyboard_in_category = InlineKeyboardBuilder()
    try:
        builder_menu_keyboard_in_category = InlineKeyboardBuilder()
        for i in range(len(list_of_budgets)):
            print(list_of_budgets[i])
            print(list_of_budgets[i][1])
            print(list_of_budgets[i][2])
            builder_menu_keyboard_in_category.row(
                types.InlineKeyboardButton(text=f"Категорія: {list_of_budgets[i][3]},  "
                                                f"Бюджет: {list_of_budgets[i][2]},  ",
                                           callback_data=f'{list_of_budgets[i][0]}'
                                                         f'_{list_of_budgets[i][1]}'))
    except Exception as ex:
        print('NoneType object is not iterable')
        print(ex)
    builder_menu_keyboard_in_category.row(types.InlineKeyboardButton(text=f"До категорій",
                                                                     callback_data=f'menu_nav'))
    # builder_menu_keyboard_in_category.add(types.InlineKeyboardButton(text=f"→",
    #                                                                  callback_data=f'next_'
    #                                                                                f'{last_id_for_next_req}_'
    #                                                                                f'{ressss}'))
    # await bot.send_message(callback.message.from_user.id, "Вийди звідси розбійник!")
    sum_of_budgets = sql_сursor_request.sql_get_sum_budget_month()[0]
    await bot.send_message(text=f"Загальний бюджет витрат: {sum_of_budgets}",
                           chat_id=callback.from_user.id,
                           reply_markup=builder_menu_keyboard_in_category.as_markup())

    await callback.answer()


@dp.callback_query(lambda txt: txt.data.startswith('next_'))
async def callback_cashbox_nav_next(callback: aiogram.types.CallbackQuery):
    category_for_sql_req_f = callback.data.split('_')[2]

    builder_menu_keyboard_in_category = InlineKeyboardBuilder()
    remainder_money = (int(list(sql_сursor_request.sql_get_balance_money_incategory(category_for_sql_req_f))[0]))

    id_callback_f = str(int(callback.data.split('_')[1]) - 1)
    id_for_next_step_to = str(int(callback.data.split('_')[1]) - 5)
    sql_next_5_orders = list(sql_сursor_request.sql_get_next_5_orders(category_for_sql_req_f,
                                                                      id_for_next_step=id_for_next_step_to,
                                                                      id_for_next_step_to=id_callback_f)
                             )
    last_id_for_next_req = sql_next_5_orders[0][0]
    for i in range(len(sql_next_5_orders)):
        last_id_for_next_req = sql_next_5_orders[i][0]
        builder_menu_keyboard_in_category.row(types.InlineKeyboardButton(text=f"Сума: {sql_next_5_orders[i][1]},  "
                                                                              f"Комент: {sql_next_5_orders[i][2]},  "
                                                                              f"Дата: {sql_next_5_orders[i][4]}",
                                                                         callback_data=f'id_tr_{sql_next_5_orders[i][0]}'
                                                                                       f'_{category_for_sql_req_f}'))
    builder_menu_keyboard_in_category.row(types.InlineKeyboardButton
                                          (text=f"←", callback_data=f'past_'
                                                                    f'{last_id_for_next_req}_'
                                                                    f'{category_for_sql_req_f}'))
    builder_menu_keyboard_in_category.add(types.InlineKeyboardButton
                                          (text=f"До категорій", callback_data=f'menu_nav'))
    builder_menu_keyboard_in_category.add(types.InlineKeyboardButton
                                          (text=f"→", callback_data=f'next_'
                                                                    f'{last_id_for_next_req}_'
                                                                    f'{category_for_sql_req_f}'))

    await bot.edit_message_text(text=f"Кошти 💰 \n"
                                     f"Баланс: {remainder_money} \n"
                                     f"Бюджет: ",
                                chat_id=callback.from_user.id,
                                message_id=callback.message.message_id,
                                reply_markup=builder_menu_keyboard_in_category.as_markup())

    await callback.answer()


# Точка входу в бота, з запитом номеру
@dp.message(commands=["start"])
async def message_handler_start(message: aiogram.types.Message):
    await bot.send_message(message.from_user.id, "Ти хто?",
                           reply_markup=navigation_keyboards.get_number_keyboard)


# Перевірка номеру телефону, чи відповідає він номеру з бд
# Потрібно ще зробити функціонал для Х адмінів
@dp.message(content_types=aiogram.types.ContentType.CONTACT)
async def message_handler_admin_phone(message: aiogram.types.Message):
    # приведення номеру до відповідного вигляду
    phone_number_user = '+380' + str(message.contact.phone_number)[-9:]
    adm_phone = list(admin_number.get_admin_number())
    if phone_number_user in adm_phone[0][0]:
        await bot.send_message(message.from_user.id, "Привіт 👋 бро! Поїхали",
                               reply_markup=navigation_keyboards.start_menu_keyboard)
    else:
        await bot.send_message(message.from_user.id, "Вийди звідси розбійник!")


# Меню навігації бота
# Колбеки для меню, так як бот працює з інлайн копками
@dp.callback_query(text='menu_nav')
async def callback_menu_nav(callback: aiogram.types.CallbackQuery):
    await bot.edit_message_text(text='Куди підемо?',
                                chat_id=callback.from_user.id,
                                message_id=callback.message.message_id,
                                reply_markup=navigation_keyboards.main_menu_keyboard)
    await callback.answer()


# Звіт по залишках
@dp.callback_query(text='report_on_accounts_nav')
async def callback_menu_nav(callback: aiogram.types.CallbackQuery):
    await bot.edit_message_text(text=report_on_accounts.report_on_acc_func(),
                                chat_id=callback.from_user.id,
                                message_id=callback.message.message_id,
                                parse_mode='HTML',
                                reply_markup=navigation_keyboards.main_menu_keyboard)
    await callback.answer()


# Стартове меню навігації бота

@dp.callback_query(text='start_menu_nav')
async def callback_start_menu_nav(callback: aiogram.types.CallbackQuery):
    await bot.edit_message_text(text="😎",
                                chat_id=callback.from_user.id,
                                message_id=callback.message.message_id,
                                reply_markup=navigation_keyboards.start_menu_keyboard)
    await callback.answer()


# Колбек для підкатегорій. Отримання транзакцій
@dp.callback_query(lambda txt: txt.data in navigation_keyboards.list_category_transaction_nav)
async def callback_category_nav_get_transact(callback: aiogram.types.CallbackQuery):
    last_id_for_next_req = ''
    remainder_money = ''
    sql_last_5_orders = []

    category_for_sql_req_f = callback.data.split('_nav')[0]
    print(category_for_sql_req_f)
    builder_menu_keyboard_in_category = InlineKeyboardBuilder()
    try:
        remainder_money = (int(list(sql_сursor_request.sql_get_balance_money_incategory(category_for_sql_req_f))[0]))
    except Exception as ex:
        print(f'На балансі: {category_for_sql_req_f} грошей нема!')
        print(ex)
    try:
        sql_last_5_orders = list(sql_сursor_request.sql_get_last_5_orders(category_for_sql_req_f))
        last_id_for_next_req = sql_last_5_orders[0][0]
    except Exception as ex:
        print(f'В категорії: {category_for_sql_req_f} транзакцій нема!')
        print(ex)

    try:
        builder_menu_keyboard_in_category = InlineKeyboardBuilder()
        for i in range(len(sql_last_5_orders)):
            builder_menu_keyboard_in_category.row(types.InlineKeyboardButton(text=f"Сума: {sql_last_5_orders[i][1]},  "
                                                                                  f"Комент: {sql_last_5_orders[i][2]},  "
                                                                                  f"Дата: {sql_last_5_orders[i][4]}",
                                                                             callback_data=f'id_tr_'
                                                                                           f'{sql_last_5_orders[i][0]}'
                                                                                           f'_{category_for_sql_req_f}'))
            last_id_for_next_req = sql_last_5_orders[i][0]
    except Exception as ex:
        print('NoneType object is not iterable')
        print(ex)
    builder_menu_keyboard_in_category.row(types.InlineKeyboardButton(text=f"До категорій",
                                                                     callback_data=f'menu_nav'))
    builder_menu_keyboard_in_category.add(types.InlineKeyboardButton(text=f"→",
                                                                     callback_data=f'next_'
                                                                                   f'{last_id_for_next_req}_'
                                                                                   f'{category_for_sql_req_f}'))
    await bot.edit_message_text(text=f"Залишок: {remainder_money}",
                                chat_id=callback.from_user.id,
                                message_id=callback.message.message_id,
                                reply_markup=builder_menu_keyboard_in_category.as_markup())

    await callback.answer()


@dp.callback_query(lambda txt: txt.data.startswith('next_'))
async def callback_cashbox_nav_next(callback: aiogram.types.CallbackQuery):
    category_for_sql_req_f = callback.data.split('_')[2]

    builder_menu_keyboard_in_category = InlineKeyboardBuilder()
    remainder_money = (int(list(sql_сursor_request.sql_get_balance_money_incategory(category_for_sql_req_f))[0]))

    id_callback_f = str(int(callback.data.split('_')[1]) - 1)
    id_for_next_step_to = str(int(callback.data.split('_')[1]) - 5)
    sql_next_5_orders = list(sql_сursor_request.sql_get_next_5_orders(category_for_sql_req_f,
                                                                      id_for_next_step=id_for_next_step_to,
                                                                      id_for_next_step_to=id_callback_f)
                             )
    last_id_for_next_req = sql_next_5_orders[0][0]
    for i in range(len(sql_next_5_orders)):
        last_id_for_next_req = sql_next_5_orders[i][0]
        builder_menu_keyboard_in_category.row(types.InlineKeyboardButton(text=f"Сума: {sql_next_5_orders[i][1]},  "
                                                                              f"Комент: {sql_next_5_orders[i][2]},  "
                                                                              f"Дата: {sql_next_5_orders[i][4]}",
                                                                         callback_data=f'id_tr_{sql_next_5_orders[i][0]}'
                                                                                       f'_{category_for_sql_req_f}'))
    builder_menu_keyboard_in_category.row(types.InlineKeyboardButton
                                          (text=f"←", callback_data=f'past_'
                                                                    f'{last_id_for_next_req}_'
                                                                    f'{category_for_sql_req_f}'))
    builder_menu_keyboard_in_category.add(types.InlineKeyboardButton
                                          (text=f"До категорій", callback_data=f'menu_nav'))
    builder_menu_keyboard_in_category.add(types.InlineKeyboardButton
                                          (text=f"→", callback_data=f'next_'
                                                                    f'{last_id_for_next_req}_'
                                                                    f'{category_for_sql_req_f}'))

    await bot.edit_message_text(text=f"Залишок: {remainder_money}",
                                chat_id=callback.from_user.id,
                                message_id=callback.message.message_id,
                                reply_markup=builder_menu_keyboard_in_category.as_markup())

    await callback.answer()


@dp.callback_query(lambda txt: txt.data.startswith('past_'))
async def callback_cashbox_nav_next(callback: aiogram.types.CallbackQuery):
    category_for_sql_req_f = callback.data.split('_')[2]

    builder_menu_keyboard_in_category = InlineKeyboardBuilder()
    remainder_money = (int(list(sql_сursor_request.sql_get_balance_money_incategory(category_for_sql_req_f))[0]))

    id_callback_f = str(int(callback.data.split('_')[1]) + 4)
    id_for_past_step_to = str(int(callback.data.split('_')[1]) + 9)
    sql_past_5_orders = list(sql_сursor_request.sql_get_past_5_orders(category_for_sql_req_f,
                                                                      id_for_past_step=id_callback_f,
                                                                      id_for_past_step_to=id_for_past_step_to)
                             )
    last_id_for_next_req = sql_past_5_orders[0][0]
    for i in range(len(sql_past_5_orders)):
        last_id_for_next_req = sql_past_5_orders[i][0]
        builder_menu_keyboard_in_category.row(types.InlineKeyboardButton(text=f"Сума: {sql_past_5_orders[i][1]},  "
                                                                              f"Комент: {sql_past_5_orders[i][2]},  "
                                                                              f"Дата: {sql_past_5_orders[i][4]}",
                                                                         callback_data=f'id_tr_{sql_past_5_orders[i][0]}'
                                                                                       f'_{category_for_sql_req_f}'))
    builder_menu_keyboard_in_category.row(types.InlineKeyboardButton
                                          (text=f"←", callback_data=f'past_'
                                                                    f'{last_id_for_next_req}_'
                                                                    f'{category_for_sql_req_f}'))
    builder_menu_keyboard_in_category.add(types.InlineKeyboardButton
                                          (text=f"До категорій", callback_data=f'menu_nav'))
    builder_menu_keyboard_in_category.add(types.InlineKeyboardButton
                                          (text=f"→", callback_data=f'next_'
                                                                    f'{last_id_for_next_req}_'
                                                                    f'{category_for_sql_req_f}'))

    await bot.edit_message_text(text=f"Залишок: {remainder_money}",
                                chat_id=callback.from_user.id,
                                message_id=callback.message.message_id,
                                reply_markup=builder_menu_keyboard_in_category.as_markup())

    await callback.answer()


# ######################################################################################################################

# Інформація по транзакції

@dp.callback_query(lambda txt: txt.data.startswith('id_tr_'))
async def get_transaction_info_in_cats(callback: aiogram.types.CallbackQuery):
    print(callback.data)
    builder_menu_keyboard_in_category = InlineKeyboardBuilder()
    id_of_transaction_for_delet = callback.data.split('_')[2]
    category = callback.data.split('_')[3]
    sql_response_get_transaction = sql_сursor_request.sql_get_transaction_info_in_cats(category,
                                                                                       id_of_transaction_for_delet)
    print(sql_response_get_transaction)
    id_transaction = sql_response_get_transaction[0]
    funds = sql_response_get_transaction[1]
    comment_transaction = sql_response_get_transaction[2]
    order_comment_transaction = sql_response_get_transaction[3]
    transfer_transaction = sql_response_get_transaction[4]
    operation_date_transaction = sql_response_get_transaction[5]
    type_transaction = sql_response_get_transaction[7]
    archived = sql_response_get_transaction[8]
    deleted = sql_response_get_transaction[9]
    done_in_crm = sql_response_get_transaction[10]
    remainder = sql_response_get_transaction[11]

    text_for_transc_info = f'''
Якщо в пункті є <b>?</b>, то:

<b>'0' = НІ, '1' = ТАК</b>

Номер в БД : {id_transaction}
Сума :       {funds}
Коментарій:  {comment_transaction}
Замовлення:  {order_comment_transaction}
Дата транзакції: {operation_date_transaction}
Тип транзакції:  {type_transaction}
Переказ?:    {transfer_transaction} 
Архівовано?: {archived}
Видалено?:   {deleted}
Проведено в ЦРМ?: {done_in_crm}
Залишок: {remainder}'''
    builder_menu_keyboard_in_category.row(types.InlineKeyboardButton
                                          (text=f"Видалити", callback_data=f'de_l_{id_transaction}_{category}'))
    builder_menu_keyboard_in_category.add(types.InlineKeyboardButton
                                          (text=f"Архівувати", callback_data=f'archi_ved_{id_transaction}_{category}'))
    builder_menu_keyboard_in_category.row(types.InlineKeyboardButton
                                          (text=f"Назад", callback_data=f'{category}_nav'))
    await bot.edit_message_text(text=text_for_transc_info,
                                chat_id=callback.from_user.id,
                                message_id=callback.message.message_id,
                                parse_mode='HTML',
                                reply_markup=builder_menu_keyboard_in_category.as_markup())
    await callback.answer()


# Видалення транзакції
@dp.callback_query(lambda txt: txt.data.startswith('de_l_'))
async def delete_transaction_in_cats(callback: aiogram.types.CallbackQuery):
    id_of_transaction_for_delet = callback.data.split('_')[2]
    category = callback.data.split('_')[3]
    sql_сursor_request.sql_delete_transaction_from_category(category, id_of_transaction_for_delet)
    # додати перерахунок таблиці
    id_of_tr = int(id_of_transaction_for_delet)

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
                try:
                    # Отримуємо значення залишку попередньої транзакції
                    result_remainder_money = 0  # Вводимо змінну залишку кошт
                    while result_remainder_money == 0:
                        try:
                            id_of_tr -= 1
                            if id_of_tr <= 0:  # Якщо всі транзакції будуть видалені, то ми доберемось до
                                # 0ї транзакціх і підставимо 0. завершимо вайл
                                result_remainder_money = 0
                                break
                            else:
                                # Йдемо циклом, поки не зустрінемо 1й не видалений. Та візьмемо з нього залишок
                                insert_query = f"SELECT remainder FROM {category} " \
                                               f"WHERE {category}.`deleted` = 0 AND {category}.`id` = {id_of_tr};"
                                cursor.execute(insert_query)
                                result_remainder_money = cursor.fetchall()[0][0]  # Запис значення залишку в змінну
                        except Exception as ex:
                            print(ex)
                except Exception as ex:
                    print(ex)

                # Записуємо в категорію де визиваємо видалення, в транзакцію що видаляємо
                # залишок попередтої транзації, або 0
                insert_query_1 = f"UPDATE {category} SET `remainder` = '{result_remainder_money}' " \
                                 f"WHERE {category}.`id` = {id_of_transaction_for_delet};"
                cursor.execute(insert_query_1)
                connection.commit()

                # Перераховуємо всі наступні транзакції !!!! Необходно оптимізувати код, та дописати перевірку,
                # що б пропускало видалені записи
                x = 0
                while True:
                    x += 1
                    id_of_tr_1 = int(id_of_transaction_for_delet) + x
                    insert_query_2 = f"SELECT deleted FROM {category} WHERE {category}.`id` = {id_of_tr_1};"
                    cursor.execute(insert_query_2)
                    result_deleted_transac = int(cursor.fetchone()[0])
                    if result_deleted_transac == 0:
                        insert_query_2 = f"SELECT funds FROM {category} WHERE {category}.`id` = {id_of_tr_1};"
                        cursor.execute(insert_query_2)
                        result_funds_money = int(cursor.fetchone()[0])

                        id_of_tr_2 = id_of_tr_1 - 1
                        insert_query_2 = f"SELECT remainder FROM {category} WHERE {category}.`id` = {id_of_tr_2};"
                        cursor.execute(insert_query_2)
                        result_remainder_money_1 = int(cursor.fetchone()[0])

                        result_remainder_money_f = result_funds_money + result_remainder_money_1
                        insert_query_3 = f"UPDATE {category} SET `remainder` = '{result_remainder_money_f}' " \
                                         f"WHERE {category}.`id` = {id_of_tr_1};"
                        cursor.execute(insert_query_3)
                        connection.commit()

                    else:
                        insert_query_2 = f"SELECT funds FROM {category} WHERE {category}.`id` = {id_of_tr_1};"
                        cursor.execute(insert_query_2)
                        result_funds_money = int(cursor.fetchone()[0])

                        id_of_tr_22 = id_of_tr_1 - 1
                        insert_query_22 = f"SELECT remainder FROM {category} WHERE {category}.`id` = {id_of_tr_22};"
                        cursor.execute(insert_query_22)
                        result_remainder_money_1 = int(cursor.fetchone()[0])

                        insert_query_3 = f"UPDATE {category} SET `remainder` = '{result_remainder_money}' " \
                                         f"WHERE {category}.`id` = {id_of_tr_1};"
                        cursor.execute(insert_query_3)
                        connection.commit()
        finally:
            connection.close()
    except Exception as ex:
        print('Connection error...')
        print(ex)

    await bot.edit_message_text(text='<b>Транзакцію видалено!</b>',
                                chat_id=callback.from_user.id,
                                message_id=callback.message.message_id,
                                parse_mode='HTML',
                                reply_markup=navigation_keyboards.main_menu_keyboard)
    await callback.answer()


# Архівування транзакції
@dp.callback_query(lambda txt: txt.data.startswith('archi_ved_'))
async def delete_transaction_in_cats(callback: aiogram.types.CallbackQuery):
    id_of_transaction_for_delet = callback.data.split('_')[2]
    category = callback.data.split('_')[3]
    sql_сursor_request.sql_archived_transaction_from_category(category, id_of_transaction_for_delet)
    await bot.edit_message_text(text='<b>Транзакцію архівовано!</b>',
                                chat_id=callback.from_user.id,
                                message_id=callback.message.message_id,
                                parse_mode='HTML',
                                reply_markup=navigation_keyboards.main_menu_keyboard)
    await callback.answer()


# ######################################################################################################################
# Колбек для "Кошти 💰"
@dp.callback_query(text='funds_nav')
async def callback_funds_nav(callback: aiogram.types.CallbackQuery):
    await bot.edit_message_text(text='Обери категорію: ',
                                chat_id=callback.from_user.id,
                                message_id=callback.message.message_id,
                                reply_markup=navigation_keyboards.money_menu_keyboard)
    await callback.answer()


#######################################################################################################################

# Колбек для "Постачальники 🚚"
@dp.callback_query(text='suppliers_nav')
async def callback_suppliers_nav(callback: aiogram.types.CallbackQuery):
    await bot.edit_message_text(text='Обери постачальника: ',
                                chat_id=callback.from_user.id,
                                message_id=callback.message.message_id,
                                reply_markup=navigation_keyboards.suppliers_menu_keyboard)
    await callback.answer()


#######################################################################################################################

# Колбек для "Витрати ➖"
@dp.callback_query(text='spending_nav')
async def callback_spending_nav(callback: aiogram.types.CallbackQuery):
    await bot.edit_message_text(text='Категорія витрат?',
                                chat_id=callback.from_user.id,
                                message_id=callback.message.message_id,
                                reply_markup=navigation_keyboards.spending_menu_keyboard)
    await callback.answer()


#######################################################################################################################

# Колбек для "ЗП/Дивіденди 🤑"

@dp.callback_query(text='dividends_nav')
async def callback_dividends_nav(callback: aiogram.types.CallbackQuery):
    await bot.edit_message_text(text='Шо по ЗП?💲',
                                chat_id=callback.from_user.id,
                                message_id=callback.message.message_id,
                                reply_markup=navigation_keyboards.menu_dividends_keyboard)
    await callback.answer()


#######################################################################################################################

# Колбек для "ЗП Офіс 🏢"

@dp.callback_query(text='dividends_office_nav')
async def callback_dividends_office_nav(callback: aiogram.types.CallbackQuery):
    await bot.edit_message_text(text='Шо по ЗП в офісі?💲',
                                chat_id=callback.from_user.id,
                                message_id=callback.message.message_id,
                                reply_markup=operstions_keyboards.menu_dividends_keyboard_office)
    await callback.answer()


#######################################################################################################################

# Колбек для "ЗП СТО 🏢"

@dp.callback_query(text='dividends_sto_nav')
async def callback_dividends_sto_nav(callback: aiogram.types.CallbackQuery):
    await bot.edit_message_text(text='Шо по ЗП На СТО?💲',
                                chat_id=callback.from_user.id,
                                message_id=callback.message.message_id,
                                reply_markup=operstions_keyboards.menu_dividends_keyboard_sto)
    await callback.answer()


# Відкриваємо картку працівника сто
@dp.callback_query(lambda txt: txt.data.endswith("_salarysto"))
async def callback_category_nav_get_transact(callback: aiogram.types.CallbackQuery):
    id_person = callback.data.split('_')[1]
    remindermoney = sql_сursor_request.sql_get_rem_divident_bud(personid=id_person, category='salarysto')
    name = remindermoney[0]
    money_remind = remindermoney[1]
    category_salary = 'salarysto'
    menu_buttons_in_salary = [
        [types.InlineKeyboardButton(text="Зарахувати", callback_data=f'{id_person}_{category_salary}_to_count')],
        [types.InlineKeyboardButton(text="Списати", callback_data='write_off')],
        [types.InlineKeyboardButton(text="Транзакції", callback_data='transactions_by_employee')],
        [types.InlineKeyboardButton(text="Меню", callback_data='menu_nav')]
    ]
    menu_keyboard_in_salary = types.InlineKeyboardMarkup(inline_keyboard=menu_buttons_in_salary)

    await bot.edit_message_text(text=f"{name}\nЗалишок:{money_remind}",
                                chat_id=callback.from_user.id,
                                message_id=callback.message.message_id,
                                reply_markup=menu_keyboard_in_salary)
    await callback.answer()


# Відкриваємо картку працівника офісу
@dp.callback_query(lambda txt: txt.data.endswith("_salary"))
async def callback_category_nav_get_transact(callback: aiogram.types.CallbackQuery):
    id_person = callback.data.split('_')[1]
    remindermoney = sql_сursor_request.sql_get_rem_divident_bud(personid=id_person, category='salaryoffise')
    name = remindermoney[0]
    money_remind = remindermoney[1]
    category_salary = 'salaryoffise'
    menu_buttons_in_salary = [
        [types.InlineKeyboardButton(text="Зарахувати", callback_data=f'{id_person}_{category_salary}_to_count')],
        [types.InlineKeyboardButton(text="Списати", callback_data=f'{id_person}_{category_salary}_write_off')],
        [types.InlineKeyboardButton(text="Транзакції", callback_data='transactions_by_employee')],
        [types.InlineKeyboardButton(text="Меню", callback_data='menu_nav')]
    ]
    menu_keyboard_in_salary = types.InlineKeyboardMarkup(inline_keyboard=menu_buttons_in_salary)

    await bot.edit_message_text(text=f"{name}\nЗалишок: {money_remind}",
                                chat_id=callback.from_user.id,
                                message_id=callback.message.message_id,
                                reply_markup=menu_keyboard_in_salary)
    await callback.answer()


class SalaryInformation(StatesGroup):
    salary_income = State()
    salary_write_off = State()


# Надходження ЗП

@dp.callback_query(lambda txt: txt.data.endswith("_to_count"))
async def callback_to_count_zp(callback: aiogram.types.CallbackQuery, state: FSMContext):
    await state.update_data(idperson=callback.data.split('_')[0])
    await state.update_data(category_salary=callback.data.split('_')[1])
    await bot.edit_message_text(text=f"Введіть зарахування:",
                                chat_id=callback.from_user.id,
                                message_id=callback.message.message_id)
    await state.set_state(SalaryInformation.salary_income)
    await callback.answer()


@dp.message(state=SalaryInformation.salary_income)
async def state_to_count_zp(message: aiogram.types.Message, state: FSMContext):
    await state.update_data(to_count=message.text)
    to_count_info = await state.get_data()
    idperson = to_count_info['idperson']
    category_salary = to_count_info['category_salary']
    to_count = to_count_info['to_count']
    reminder = sql_request_for_salary.last_remind_salary_personid(category=category_salary, personid=idperson)[0]
    all_info_person = sql_request_for_salary.last_info_salary_personid(category=category_salary, personid=idperson)
    name_person = all_info_person[1]
    surname_person = all_info_person[2]
    phone_person = all_info_person[3]
    type_tansaction = "1"
    reminder = reminder + int(to_count)
    sql_request_for_salary.sql_add_salary(category=category_salary, personid=idperson, reminder=reminder,
                                          to_count=to_count, name=name_person, surname=surname_person,
                                          phone=phone_person, type_tansaction=type_tansaction)
    await bot.send_message(message.from_user.id, f"Зараховано {to_count} грн. \nДля {surname_person} {name_person}",
                           reply_markup=navigation_keyboards.menu_dividends_keyboard)
    await state.clear()


# Списання ЗП

@dp.callback_query(lambda txt: txt.data.endswith("_write_off"))
async def callback_to_count_zp(callback: aiogram.types.CallbackQuery, state: FSMContext):
    await state.update_data(idperson=callback.data.split('_')[0])
    await state.update_data(category_salary=callback.data.split('_')[1])
    await bot.edit_message_text(text=f"Введіть зарахування:",
                                chat_id=callback.from_user.id,
                                message_id=callback.message.message_id)
    await state.set_state(SalaryInformation.salary_write_off)
    await callback.answer()


@dp.message(state=SalaryInformation.salary_write_off)
async def state_to_count_zp(message: aiogram.types.Message, state: FSMContext):
    await state.update_data(to_count=message.text)
    to_count_info = await state.get_data()
    idperson = to_count_info['idperson']
    category_salary = to_count_info['category_salary']
    to_count = to_count_info['to_count']
    reminder = sql_request_for_salary.last_remind_salary_personid(category=category_salary, personid=idperson)[0]
    all_info_person = sql_request_for_salary.last_info_salary_personid(category=category_salary, personid=idperson)
    name_person = all_info_person[1]
    surname_person = all_info_person[2]
    phone_person = all_info_person[3]
    type_tansaction = "2"
    reminder = reminder - int(to_count)
    sql_request_for_salary.sql_add_salary(category=category_salary, personid=idperson, reminder=reminder,
                                          to_count=to_count, name=name_person, surname=surname_person,
                                          phone=phone_person, type_tansaction=type_tansaction)
    await bot.send_message(message.from_user.id, f"Списано {to_count} грн. \nДля {surname_person} {name_person}",
                           reply_markup=navigation_keyboards.menu_dividends_keyboard)
    await state.clear()


# Блок внесення данних до БД за допомогою FCM та callback. Збираємо данні в FCM потім формуємо пакет для БД

# Клас для збору данних від адміна
class TransactionInformation(StatesGroup):
    funds_income = State()
    comment_income = State()
    order_income = State()
    category_transaction_income = State()

    funds_outlay = State()
    comment_outlay = State()
    order_outlay = State()
    category_transaction_outlay = State()

    funds_transfer = State()
    comment_transfer = State()
    order_transfer = State()
    category_transaction_transfer_from = State()
    category_transaction_transfer_to = State()
    transaction_transfer_entr = State()


# #######################      Надходження коштів кнопка "Надходження➕"    ######################################### #

# Запит на введення суми
@dp.callback_query(text='add_income_nav')
async def callback_add_income_nav(callback: aiogram.types.CallbackQuery, state: FSMContext):
    await bot.edit_message_text(text="Введіть суму:",
                                chat_id=callback.from_user.id,
                                message_id=callback.message.message_id)
    await state.set_state(TransactionInformation.funds_income)
    await callback.answer()


# Обробка запиту кошт, та запит введення коменту
@dp.message(state=TransactionInformation.funds_income)
async def message_entr_comment_income(message: aiogram.types.Message, state: FSMContext):
    try:
        type(int(message.text))
        if int(message.text) > 0:
            await state.update_data(funds=message.text)
            await bot.send_message(message.from_user.id, text="Введіть комент:")
            await state.set_state(TransactionInformation.comment_income)
        else:
            await state.update_data(funds=int(message.text) * -1)
            await bot.send_message(message.from_user.id, text="Введіть комент:")
            await state.set_state(TransactionInformation.comment_income)
    except:
        await bot.send_message(message.from_user.id, text="Ціле число...:")
        await state.set_state(TransactionInformation.funds_income)


# Запит на введення інформації по замовленю

@dp.message(state=TransactionInformation.comment_income)
async def message_entr_order_income(message: aiogram.types.Message, state: FSMContext):
    await state.update_data(comment=message.text)
    await bot.send_message(message.from_user.id, text="Замовлення?")
    await state.set_state(TransactionInformation.order_income)


# Вибір категорії

@dp.message(state=TransactionInformation.order_income)
async def message_entr_category_income(message: aiogram.types.Message, state: FSMContext):
    await state.update_data(order=message.text)
    await bot.send_message(message.from_user.id,
                           text="Категорія?",
                           reply_markup=operstions_keyboards.main_menu_keyboard)
    await state.set_state(TransactionInformation.order_income)


# Вибір підкатегорії на основі категорії "Кошти 💰"

@dp.callback_query(text='funds', state=TransactionInformation.order_income)
async def callback_add_income_nav_funds(callback: aiogram.types.CallbackQuery, state: FSMContext):
    await bot.edit_message_text(text="Підкатегорія?:",
                                chat_id=callback.from_user.id,
                                message_id=callback.message.message_id,
                                reply_markup=operstions_keyboards.money_menu_keyboard)
    await state.set_state(TransactionInformation.category_transaction_income)
    await callback.answer()


# Вибір підкатегорії на основі категорії "Постачальники 🚚"
@dp.callback_query(text='suppliers', state=TransactionInformation.order_income)
async def callback_add_income_nav_suppliers(callback: aiogram.types.CallbackQuery, state: FSMContext):
    await bot.edit_message_text(text="Підкатегорія?:",
                                chat_id=callback.from_user.id,
                                message_id=callback.message.message_id,
                                reply_markup=operstions_keyboards.suppliers_menu_keyboard)
    await state.set_state(TransactionInformation.category_transaction_income)
    await callback.answer()


# Вибір підкатегорії на основі категорії "Витрати ➖"
@dp.callback_query(text='spending', state=TransactionInformation.order_income)
async def callback_add_income_nav_spending(callback: aiogram.types.CallbackQuery, state: FSMContext):
    await bot.edit_message_text(text="Підкатегорія?:",
                                chat_id=callback.from_user.id,
                                message_id=callback.message.message_id,
                                reply_markup=operstions_keyboards.spending_menu_keyboard)
    await state.set_state(TransactionInformation.category_transaction_income)
    await callback.answer()


# Вибір підкатегорії на основі категорії "ЗП/Дивіденди 🤑"
@dp.callback_query(text='dividends', state=TransactionInformation.order_income)
async def callback_add_income_nav_dividends(callback: aiogram.types.CallbackQuery, state: FSMContext):
    await bot.edit_message_text(text="Підкатегорія?:",
                                chat_id=callback.from_user.id,
                                message_id=callback.message.message_id,
                                reply_markup=operstions_keyboards.menu_dividends_keyboard)
    await state.set_state(TransactionInformation.category_transaction_income)
    await callback.answer()


# Отримання категорії та відправка данних в бд, через зовнішню ф-цію
@dp.callback_query(text=operstions_keyboards.list_category_transaction,
                   state=TransactionInformation.category_transaction_income)
async def callback_add_income_sql(callback: aiogram.types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    try:
        remainder_money_sql = sql_сursor_request.res_remainder_money(callback.data) + int(user_data['funds'])
    except:
        remainder_money_sql = 0
    sql_сursor_request.funds_SQL_add(funds=int(user_data['funds']),
                                     comment=user_data['comment'],
                                     order=user_data['order'],
                                     funds_category=callback.data,
                                     remainder=remainder_money_sql)
    await bot.send_message(callback.message.chat.id, text=f"Сума: {user_data['funds']}\n"
                                                          f"Комент: {user_data['comment']}\n"
                                                          f"Замовлення: {user_data['order']}\n"
                                                          f"Категорія: {callback.data}",
                           reply_markup=navigation_keyboards.start_menu_keyboard)
    await callback.answer()
    await state.clear()


# #######################      Надходження коштів кнопка "Витрата ➖"    #############################################

# Запит на введення суми
@dp.callback_query(text='add_spending_nav')
async def callback_add_spending_nav(callback: aiogram.types.CallbackQuery, state: FSMContext):
    await bot.edit_message_text(text="Введіть суму:",
                                chat_id=callback.from_user.id,
                                message_id=callback.message.message_id)
    await state.set_state(TransactionInformation.funds_outlay)
    await callback.answer()


# Обробка запиту кошт, та запит введення коменту
@dp.message(state=TransactionInformation.funds_outlay)
async def message_await_spending_comment(message: aiogram.types.Message, state: FSMContext):
    try:
        type(int(message.text))
        if int(message.text) < 0:
            await state.update_data(funds=message.text)
            await bot.send_message(message.from_user.id, text="Введіть комент:")
            await state.set_state(TransactionInformation.comment_outlay)
        else:
            await state.update_data(funds=int(message.text) * -1)
            await bot.send_message(message.from_user.id, text="Введіть комент:")
            await state.set_state(TransactionInformation.comment_outlay)
    except:
        await bot.send_message(message.from_user.id, text="Ціле число...:")
        await state.set_state(TransactionInformation.funds_outlay)


# Запит на введення інформації по замовленю

@dp.message(state=TransactionInformation.comment_outlay)
async def message_await_spending_order(message: aiogram.types.Message, state: FSMContext):
    await state.update_data(comment=message.text)
    await bot.send_message(message.from_user.id, text="Замовлення?")
    await state.set_state(TransactionInformation.order_outlay)


# Вибір категорії

@dp.message(state=TransactionInformation.order_outlay)
async def message_await_spending_category(message: aiogram.types.Message, state: FSMContext):
    await state.update_data(order=message.text)
    await bot.send_message(message.from_user.id,
                           text="Категорія?",
                           reply_markup=operstions_keyboards.main_menu_keyboard)
    await state.set_state(TransactionInformation.order_outlay)


# Вибір підкатегорії на основі категорії "Кошти 💰"

@dp.callback_query(text='funds', state=TransactionInformation.order_outlay)
async def callback_add_spending_nav_funds(callback: aiogram.types.CallbackQuery, state: FSMContext):
    await bot.edit_message_text(text="Підкатегорія?:",
                                chat_id=callback.from_user.id,
                                message_id=callback.message.message_id,
                                reply_markup=operstions_keyboards.money_menu_keyboard)
    await state.set_state(TransactionInformation.category_transaction_outlay)
    await callback.answer()


# Вибір підкатегорії на основі категорії "Постачальники 🚚"
@dp.callback_query(text='suppliers', state=TransactionInformation.order_outlay)
async def callback_add_spending_nav_suppliers(callback: aiogram.types.CallbackQuery, state: FSMContext):
    await bot.edit_message_text(text="Підкатегорія?:",
                                chat_id=callback.from_user.id,
                                message_id=callback.message.message_id,
                                reply_markup=operstions_keyboards.suppliers_menu_keyboard)
    await state.set_state(TransactionInformation.category_transaction_outlay)
    await callback.answer()


# Вибір підкатегорії на основі категорії "Витрати ➖"
@dp.callback_query(text='spending', state=TransactionInformation.order_outlay)
async def callback_add_spending_nav_spending(callback: aiogram.types.CallbackQuery, state: FSMContext):
    await bot.edit_message_text(text="Підкатегорія?:",
                                chat_id=callback.from_user.id,
                                message_id=callback.message.message_id,
                                reply_markup=operstions_keyboards.spending_menu_keyboard)
    await state.set_state(TransactionInformation.category_transaction_outlay)
    await callback.answer()


# Вибір підкатегорії на основі категорії "ЗП/Дивіденди 🤑"
@dp.callback_query(text='dividends', state=TransactionInformation.order_outlay)
async def callback_add_spending_nav_dividends(callback: aiogram.types.CallbackQuery, state: FSMContext):
    await bot.edit_message_text(text="Підкатегорія?:",
                                chat_id=callback.from_user.id,
                                message_id=callback.message.message_id,
                                reply_markup=operstions_keyboards.menu_dividends_keyboard)
    await state.set_state(TransactionInformation.category_transaction_outlay)
    await callback.answer()


# Отримання категорії та відправка данних в бд, через зовнішню ф-цію
@dp.callback_query(text=operstions_keyboards.list_category_transaction,
                   state=TransactionInformation.category_transaction_outlay)
async def callback_add_spending_sql(callback: aiogram.types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    print(callback.data)
    try:
        remainder_money_sql = sql_сursor_request.res_remainder_money(callback.data) + int(user_data['funds'])
    except:
        remainder_money_sql = 0
    sql_сursor_request.funds_SQL_add(funds=int(user_data['funds']),
                                     comment=user_data['comment'],
                                     order=user_data['order'],
                                     funds_category=callback.data,
                                     remainder=remainder_money_sql, type_transaction=2)
    await bot.send_message(callback.message.chat.id, text=f"Сума: {user_data['funds']}\n"
                                                          f"Комент: {user_data['comment']}\n"
                                                          f"Замовлення: {user_data['order']}\n"
                                                          f"Категорія: {callback.data}",
                           reply_markup=navigation_keyboards.start_menu_keyboard)
    await state.clear()
    await callback.answer()


# #######################      Надходження коштів кнопка "Переказ 🔄"    ############################################ #

# Запит на введення суми переказу
@dp.callback_query(text='money_transfer_nav')
async def callback_money_transfer_nav(callback: aiogram.types.CallbackQuery, state: FSMContext):
    await bot.edit_message_text(text="Введіть суму:",
                                chat_id=callback.from_user.id,
                                message_id=callback.message.message_id)
    await state.set_state(TransactionInformation.funds_transfer)
    await callback.answer()


# Обробка запиту кошт, та запит введення коменту
@dp.message(state=TransactionInformation.funds_transfer)
async def message_await_entr_comment_transfer(message: aiogram.types.Message, state: FSMContext):
    try:  # перевірка чи int
        type(int(message.text))
        if int(message.text) > 0:  # Якщо число  > 0 то просто зберігаємо та йдемо далі
            await state.update_data(funds_transfer=message.text)  # збереження значення суми транзакції
            await bot.send_message(message.from_user.id, text="Введіть комент:")
            await state.set_state(TransactionInformation.comment_transfer)
        else:  # В іншому випадку міняємо знак
            await state.update_data(funds_transfer=int(message.text) * -1)
            await bot.send_message(message.from_user.id, text="Введіть комент:")
            await state.set_state(TransactionInformation.comment_transfer)
    except:  # Клієнт ввів не ціле число, ще один запит на введення цілого числа
        await bot.send_message(message.from_user.id, text="Ціле число...:")
        await state.set_state(TransactionInformation.funds_transfer)


# Запит на введення інформації по замовленю

@dp.message(state=TransactionInformation.comment_transfer)
async def message_await_entr_order_transfer(message: aiogram.types.Message, state: FSMContext):
    await state.update_data(comment_transfer=message.text)  # Зберігаємо комент
    await bot.send_message(message.from_user.id, text="Замовлення?")  # Запит поля Замовлення
    await state.set_state(TransactionInformation.order_transfer)


# Вибір категорії з якої будемо переводити

@dp.message(state=TransactionInformation.order_transfer)
async def message_await_entr_category_from(message: aiogram.types.Message, state: FSMContext):
    await state.update_data(order=message.text)
    await bot.send_message(message.from_user.id,
                           text="З категорії?",
                           reply_markup=operstions_keyboards.main_menu_keyboard)
    await state.set_state(TransactionInformation.category_transaction_transfer_from)


# Вибір підкатегорії на основі категорії "Кошти 💰"

@dp.callback_query(text='funds', state=TransactionInformation.category_transaction_transfer_from)
async def callback_await_funds_category_from(callback: aiogram.types.CallbackQuery, state: FSMContext):
    await bot.edit_message_text(text="Підкатегорія?:",
                                chat_id=callback.from_user.id,
                                message_id=callback.message.message_id,
                                reply_markup=operstions_keyboards.money_menu_keyboard)
    await state.set_state(TransactionInformation.category_transaction_transfer_to)
    await callback.answer()


# Вибір підкатегорії на основі категорії "Постачальники 🚚"
@dp.callback_query(text='suppliers', state=TransactionInformation.category_transaction_transfer_from)
async def callback_await_suppliers_category_from(callback: aiogram.types.CallbackQuery, state: FSMContext):
    await bot.edit_message_text(text="Підкатегорія?:",
                                chat_id=callback.from_user.id,
                                message_id=callback.message.message_id,
                                reply_markup=operstions_keyboards.suppliers_menu_keyboard)
    await state.set_state(TransactionInformation.category_transaction_transfer_to)
    await callback.answer()


# Вибір підкатегорії на основі категорії "Витрати ➖"
@dp.callback_query(text='spending', state=TransactionInformation.category_transaction_transfer_from)
async def callback_await_spending_category_from(callback: aiogram.types.CallbackQuery, state: FSMContext):
    await bot.edit_message_text(text="Підкатегорія?:",
                                chat_id=callback.from_user.id,
                                message_id=callback.message.message_id,
                                reply_markup=operstions_keyboards.spending_menu_keyboard)
    await state.set_state(TransactionInformation.category_transaction_transfer_to)
    await callback.answer()


# Вибір підкатегорії на основі категорії "ЗП/Дивіденди 🤑"
@dp.callback_query(text='dividends', state=TransactionInformation.category_transaction_transfer_from)
async def callback_await_dividends_category_from(callback: aiogram.types.CallbackQuery, state: FSMContext):
    await bot.edit_message_text(text="Підкатегорія?:",
                                chat_id=callback.from_user.id,
                                message_id=callback.message.message_id,
                                reply_markup=operstions_keyboards.menu_dividends_keyboard)
    await state.set_state(TransactionInformation.category_transaction_transfer_to)
    await callback.answer()


# Вибір категорії в яку будемо переводити

@dp.callback_query(text=operstions_keyboards.list_category_transaction,
                   state=TransactionInformation.category_transaction_transfer_to)
async def callback_await_entr_category_to(callback: aiogram.types.CallbackQuery, state: FSMContext):
    await bot.edit_message_text(text="В яку категорію?:",
                                chat_id=callback.from_user.id,
                                message_id=callback.message.message_id,
                                reply_markup=operstions_keyboards.main_menu_keyboard)
    await state.update_data(category_transaction_transfer_from=callback.data)
    await state.set_state(TransactionInformation.category_transaction_transfer_to)
    await callback.answer()


# Вибір підкатегорії на основі категорії "Кошти 💰"

@dp.callback_query(text='funds', state=TransactionInformation.category_transaction_transfer_to)
async def callback_await_funds_category_to(callback: aiogram.types.CallbackQuery, state: FSMContext):
    await bot.edit_message_text(text="Підкатегорія?:",
                                chat_id=callback.from_user.id,
                                message_id=callback.message.message_id,
                                reply_markup=operstions_keyboards.money_menu_keyboard)
    await state.set_state(TransactionInformation.transaction_transfer_entr)
    await callback.answer()


# Вибір підкатегорії на основі категорії "Постачальники 🚚"

@dp.callback_query(text='suppliers', state=TransactionInformation.category_transaction_transfer_to)
async def callback_await_suppliers_category_to(callback: aiogram.types.CallbackQuery, state: FSMContext):
    await bot.edit_message_text(text="Підкатегорія?:",
                                chat_id=callback.from_user.id,
                                message_id=callback.message.message_id,
                                reply_markup=operstions_keyboards.suppliers_menu_keyboard)
    await state.set_state(TransactionInformation.transaction_transfer_entr)
    await callback.answer()


# Вибір підкатегорії на основі категорії "Витрати ➖"

@dp.callback_query(text='spending', state=TransactionInformation.category_transaction_transfer_to)
async def callback_await_spending_category_to(callback: aiogram.types.CallbackQuery, state: FSMContext):
    await bot.edit_message_text(text="Підкатегорія?:",
                                chat_id=callback.from_user.id,
                                message_id=callback.message.message_id,
                                reply_markup=operstions_keyboards.spending_menu_keyboard)
    await state.set_state(TransactionInformation.transaction_transfer_entr)
    await callback.answer()


# Вибір підкатегорії на основі категорії "ЗП/Дивіденди 🤑"

@dp.callback_query(text='dividends', state=TransactionInformation.category_transaction_transfer_to)
async def callback_await_dividends_category_to(callback: aiogram.types.CallbackQuery, state: FSMContext):
    await bot.edit_message_text(text="Підкатегорія?:",
                                chat_id=callback.from_user.id,
                                message_id=callback.message.message_id,
                                reply_markup=operstions_keyboards.menu_dividends_keyboard)
    await state.set_state(TransactionInformation.transaction_transfer_entr)
    await callback.answer()


# Вибір підкатегорії на основі категорії "ЗП Офіс 🏢"

@dp.callback_query(text='dividends_office', state=TransactionInformation.category_transaction_transfer_to)
async def callback_await_dividends_category_to(callback: aiogram.types.CallbackQuery, state: FSMContext):
    await bot.edit_message_text(text="Підкатегорія?: ",
                                chat_id=callback.from_user.id,
                                message_id=callback.message.message_id,
                                reply_markup=operstions_keyboards.menu_dividends_keyboard)
    await state.set_state(TransactionInformation.transaction_transfer_entr)
    await callback.answer()


# Вибір підкатегорії на основі категорії "ЗП СТО 🛠"

@dp.callback_query(text='dividends_sto', state=TransactionInformation.category_transaction_transfer_to)
async def callback_await_dividends_category_to(callback: aiogram.types.CallbackQuery, state: FSMContext):
    await bot.edit_message_text(text="Підкатегорія?:",
                                chat_id=callback.from_user.id,
                                message_id=callback.message.message_id,
                                reply_markup=operstions_keyboards.menu_dividends_keyboard)
    await state.set_state(TransactionInformation.transaction_transfer_entr)
    await callback.answer()


# Отримання категорії та відправка данних в бд, через зовнішню ф-цію. Принципом в 1 таблиці - в іншій +
@dp.callback_query(text=operstions_keyboards.list_category_transaction_to,
                   state=TransactionInformation.transaction_transfer_entr)
async def callback_add_transfer_sql(callback: aiogram.types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    print(user_data)
    # тут необхідно зробити додаткові перевірки, зробити трай і тп.
    # створюємо запит на від'ємну тразнакцію в категорії "Категорія З"
    remainder_money_sql = sql_сursor_request.res_remainder_money(user_data['category_transaction_transfer_from']) - int(
        user_data['funds_transfer'])
    funds_for_sql_rs_request_to = int(user_data['funds_transfer']) * -1
    sql_сursor_request.funds_SQL_add(funds=funds_for_sql_rs_request_to,
                                     comment=user_data['comment_transfer'],
                                     order=user_data['order'],
                                     funds_category=user_data['category_transaction_transfer_from'],
                                     remainder=remainder_money_sql, type_transaction=3)

    # створюємо запит на плюсову тразнакцію в категорії "Категорія В"
    remainder_money_sql = sql_сursor_request.res_remainder_money(callback.data) + int(user_data['funds_transfer'])
    sql_сursor_request.funds_SQL_add(funds=int(user_data['funds_transfer']),
                                     comment=user_data['comment_transfer'],
                                     order=user_data['order'],
                                     funds_category=callback.data,
                                     remainder=remainder_money_sql, type_transaction=3)

    await bot.send_message(callback.message.chat.id, text=f"Сума: {user_data['funds_transfer']}\n"
                                                          f"Комент: {user_data['comment_transfer']}\n"
                                                          f"Замовлення: {user_data['order']}\n"
                                                          f"Категорія З якої: "
                                                          f"{user_data['category_transaction_transfer_from']}\n"
                                                          f"Категорія В яку: {callback.data}",
                           reply_markup=navigation_keyboards.start_menu_keyboard)
    await callback.answer()
    await state.clear()


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
