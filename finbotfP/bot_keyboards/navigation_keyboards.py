from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder

list_category_transaction_nav = ['cashbox_nav', 'terminal_nav', 'tov_nav', 'strongbox_nav'
                                 'rent_nav', 'services_nav', 'advertising_nav', 'office_nav', 'sto_nav', 'taxes_nav'
                                 ]

# Запит для логіну
get_number_button = [
    [types.KeyboardButton(text="Надати номер ☎️", request_contact=True)]
]
get_number_keyboard = types.ReplyKeyboardMarkup(keyboard=get_number_button, resize_keyboard=True)

# Стартове меню
start_menu_buttons = [
    [types.InlineKeyboardButton(text="Надходження➕", callback_data='add_income_nav')],
    [types.InlineKeyboardButton(text="Витрата ➖", callback_data='add_spending_nav')],
    [types.InlineKeyboardButton(text="Переказ 🔄", callback_data='money_transfer_nav')],
    [types.InlineKeyboardButton(text="Рахунки, звіт", callback_data='report_on_accounts_nav')],
    [types.InlineKeyboardButton(text="Меню 📖", callback_data='menu_nav')]

]
start_menu_keyboard = types.InlineKeyboardMarkup(inline_keyboard=start_menu_buttons)

# Головне меню
main_menu_buttons = [
    [types.InlineKeyboardButton(text="Кошти 💰", callback_data='funds_nav')],
    [types.InlineKeyboardButton(text="Постачальники 🚚", callback_data='suppliers_nav')],
    [types.InlineKeyboardButton(text="Витрати ➖", callback_data='spending_nav')],
    [types.InlineKeyboardButton(text="ЗП/Дивіденди 🤑", callback_data='dividends_nav')],
    [types.InlineKeyboardButton(text="Стартове меню 📖", callback_data='start_menu_nav')]
]
main_menu_keyboard = types.InlineKeyboardMarkup(inline_keyboard=main_menu_buttons)

# Кошти
menu_money = [
    [types.InlineKeyboardButton(text="Касса 💰", callback_data='cashbox_nav')],
    [types.InlineKeyboardButton(text="Термінал 💳", callback_data='terminal_nav')],
    [types.InlineKeyboardButton(text="Сейф 🔐", callback_data='strongbox_nav')],
    [types.InlineKeyboardButton(text="Нова пошта 🚚", callback_data='newpost_nav')]
    [types.InlineKeyboardButton(text="Меню 📖", callback_data='menu_nav')]
]
money_menu_keyboard = types.InlineKeyboardMarkup(inline_keyboard=menu_money)

# Постачальники
menu_suppliers = [[types.InlineKeyboardButton(text="Меню 📖", callback_data='menu_nav')]
]
suppliers_menu_keyboard = types.InlineKeyboardMarkup(inline_keyboard=menu_suppliers)

# Витрати
menu_spending = [
    [types.InlineKeyboardButton(text="Оренда 🏢", callback_data='rent_nav')],
    [types.InlineKeyboardButton(text="Реклама та сервіси 🎟", callback_data='servicesads_nav')],
    [types.InlineKeyboardButton(text="СТО та Офіс 🏢", callback_data='officesto_nav')],
    [types.InlineKeyboardButton(text="Податки 👔", callback_data='taxes_nav')],
    [types.InlineKeyboardButton(text="Доставка 🚚", callback_data='delivery_nav')],
    [types.InlineKeyboardButton(text="Гарантія ✅", callback_data='guarantee_nav')],
    [types.InlineKeyboardButton(text="Комісія %", callback_data='commission_nav')],
    [types.InlineKeyboardButton(text="Меню 📖", callback_data='menu_nav')]
]
spending_menu_keyboard = types.InlineKeyboardMarkup(inline_keyboard=menu_spending)

# ЗП/Дивіденти
menu_dividends = [
    [types.InlineKeyboardButton(text="ЗП Офіс 🏢", callback_data='dividends_office_nav')],
    [types.InlineKeyboardButton(text="ЗП СТО 🛠", callback_data='dividends_sto_nav')],
    [types.InlineKeyboardButton(text="Меню 📖", callback_data='menu_nav')]
]
menu_dividends_keyboard = types.InlineKeyboardMarkup(inline_keyboard=menu_dividends)

# Меню в категорії # Додати Інлайн кейборд білдер
menu_buttons_in_category = [
    [types.InlineKeyboardButton(text="Зведена статистика", callback_data='summary_statistics_nav')],
    [types.InlineKeyboardButton(text="Видалити транзакцію", callback_data='del_transaction_nav')],
    [types.InlineKeyboardButton(text="Меню 📖", callback_data='menu_nav')]
]
menu_keyboard_in_category = types.InlineKeyboardMarkup(inline_keyboard=menu_buttons_in_category)

builder = InlineKeyboardBuilder()
builder.row(types.InlineKeyboardButton(text="test", callback_data='calb'))
