from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup


def add_buttons(buttons: list):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*buttons)
    return keyboard


def user_buttons():
    return add_buttons(["Все обои", "Случайные обои"])


def admin_buttons():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row("Все обои", "Случайные обои")
    keyboard.row("Добавить обои", "Удалить обои")
    return keyboard


def menu_inline(wallpapers_id, wallpapers_list):

    keyboard = InlineKeyboardMarkup(row_width=2)

    if wallpapers_id == 0:
        previous_button = InlineKeyboardButton("🚫", callback_data="lock")
    else:
        previous_button = InlineKeyboardButton("◄", callback_data="back")
    id_button = InlineKeyboardButton(str(wallpapers_id), callback_data="id")
    if wallpapers_id == len(wallpapers_list)-1:
        next_button = InlineKeyboardButton("🚫", callback_data="lock")
    else:
        next_button = InlineKeyboardButton("►", callback_data="next")

    keyboard.row(previous_button, id_button, next_button)

    return keyboard
