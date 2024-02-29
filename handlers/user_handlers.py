from dispatcher import dp 
from utils.buttons import menu_inline, user_buttons, admin_buttons
from middleware import rate_limit
from aiogram import types
from config import URL, ADMIN
from utils.api_requests import API


@rate_limit(2, "start")
@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply(f"Привет! Я бот с обоями клеш рояль, {URL}", reply_markup=user_buttons() if message.from_user.id != int(ADMIN) else admin_buttons())


@rate_limit(2, "random")
@dp.message_handler(text="Случайные обои")
async def send_random_wallpaper(message: types.Message):
    msg = await message.reply(f'Загрузка...')

    photo_url, code_url = API().get_random_url()

    if not photo_url is None:
        photo, code_image = API().get_wallpaper_by_url(photo_url)

        if not photo_url is None:
            
            await msg.delete()
            await message.answer_photo(photo, caption="Держи!")
        else:
            await msg.edit_text(f"Ошибка {code_image}!")
        return

    await msg.edit_text(f"Ошибка {code_url}!")


@rate_limit(2, "all")
@dp.message_handler(text="Все обои")
async def send_all_wallpapers(message: types.Message):
    wallpapers_all = eval(API().get_all_urls())
    wallpaper = wallpapers_all[0]

    photo, code = API().get_wallpaper_by_url(wallpaper)
   
    if not photo is None:
        await message.reply_photo(photo, reply_markup=menu_inline(0, wallpapers_all))
    else:
        await message.reply(f"Ошибка {code}!")


@dp.callback_query_handler(text=["next", "back"])
async def process_next_callback(callback_query: types.CallbackQuery):
    id = int(callback_query.message.reply_markup.inline_keyboard[0][1].text)

    current_id = id
    if callback_query.data == "next":
        current_id = id + 1
    elif callback_query.data == "back":
        current_id = id - 1

    wallpapers_all = eval(API().get_all_urls())
    photo, code = API().get_wallpaper_by_url(wallpapers_all[current_id])
    if not photo is None:
        await callback_query.message.edit_media(types.InputMediaPhoto(photo),
    reply_markup=menu_inline(current_id, wallpapers_all))
    else:
        await callback_query.message.delete()
        await callback_query.answer(f"Ошибка {code}!")

