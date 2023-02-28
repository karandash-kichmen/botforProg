from aiogram import types

list_category_transaction = ['cashbox', 'terminal']

list_category_transaction_to = ['cashbox', 'terminal']
# Головне меню
main_menu_buttons = [
    [types.InlineKeyboardButton(text="Кошти 💰", callback_data='funds')],
    [types.InlineKeyboardButton(text="Постачальники 🚚", callback_data='suppliers')],
    [types.InlineKeyboardButton(text="Витрати ➖", callback_data='spending')],
    [types.InlineKeyboardButton(text="ЗП/Дивіденди 🤑", callback_data='dividends')]
]
main_menu_keyboard = types.InlineKeyboardMarkup(inline_keyboard=main_menu_buttons)

# Кошти
menu_money = [
    [types.InlineKeyboardButton(text="Касса 💰", callback_data='cashbox')],
    [types.InlineKeyboardButton(text="Термінал 💳", callback_data='terminal')],
    [types.InlineKeyboardButton(text="Сейф 🔐", callback_data='strongbox')],
    [types.InlineKeyboardButton(text="Нова пошта 🚚", callback_data='newpost')]
]
money_menu_keyboard = types.InlineKeyboardMarkup(inline_keyboard=menu_money)

# Постачальники
menu_suppliers = []
suppliers_menu_keyboard = types.InlineKeyboardMarkup(inline_keyboard=menu_suppliers)

# Витрати
menu_spending = [
    [types.InlineKeyboardButton(text="Оренда 🏢", callback_data='rent')],
    [types.InlineKeyboardButton(text="Реклама та сервіси 🎟", callback_data='servicesads')],
    [types.InlineKeyboardButton(text="СТО та Офіс 🏢", callback_data='officesto')],
    [types.InlineKeyboardButton(text="Податки 👔", callback_data='taxes')],
    [types.InlineKeyboardButton(text="Доставка 🚚", callback_data='taxes')],
    [types.InlineKeyboardButton(text="Гарантія ✅", callback_data='taxes')],
    [types.InlineKeyboardButton(text="Комісія %", callback_data='taxes')]
]
spending_menu_keyboard = types.InlineKeyboardMarkup(inline_keyboard=menu_spending)

# ЗП/Дивіденти
menu_dividends = [
    [types.InlineKeyboardButton(text="ЗП Офіс 🏢", callback_data='dividends_office')],
    [types.InlineKeyboardButton(text="ЗП СТО 🛠", callback_data='dividends_sto')],
    [types.InlineKeyboardButton(text="Кредити 👔", callback_data='creditstrust')],
]
menu_dividends_keyboard = types.InlineKeyboardMarkup(inline_keyboard=menu_dividends)

# ЗП СТО
menu_dividends_sto = [
    [types.InlineKeyboardButton(text="Шеріф", callback_data='sherif_1_salarysto')]]
menu_dividends_keyboard_sto = types.InlineKeyboardMarkup(inline_keyboard=menu_dividends_sto)

# ЗП Офіс
menu_dividends_office = []
menu_dividends_keyboard_office = types.InlineKeyboardMarkup(inline_keyboard=menu_dividends_office)
