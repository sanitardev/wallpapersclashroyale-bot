from aiogram.dispatcher import FSMContext
from aiogram.types.mixins import Downloadable

from config import TOKEN
from dispatcher import dp, bot
from middleware import rate_limit
from aiogram import types
from filters import IsAdmin
from utils.states import Dialog
from utils.buttons import admin_buttons, add_buttons
from utils.api_requests import API


@dp.message_handler(IsAdmin(), text="Добавить обои")
async def add_wallpapers(message: types.Message):
    await message.reply("Отправь фото:", reply_markup=add_buttons(["Отмена"]))
    await Dialog.add.set()


@dp.message_handler(content_types=[types.ContentType.TEXT], state=Dialog.add)
async def add_photo(message: types.Message, state: FSMContext):
    if message.text == "Отмена":
        await state.finish()
        await message.reply("Отменено", reply_markup=admin_buttons())
        return


@dp.message_handler(content_types=[types.ContentType.PHOTO], state=Dialog.add)
async def add_photo(message: types.Message, state: FSMContext):
    photo_file_id = message.photo[0].file_id
    photo = message.photo[-1]

    # Get file information
    file_info = await bot.get_file(photo.file_id)

    # Construct the URL using the file_path
    photo_url = f"https://api.telegram.org/file/bot{TOKEN}/{file_info.file_path}"

    json = API().add_wallpaper_by_url(photo_url)

    if json["success"] == False:
        await message.reply(f"Ошибка {json['code']}", reply_markup=admin_buttons())
        await state.finish()
        return
    else:
        await message.reply(f"""Фото успешно добавленно! 
url: {json["imageUrl"]}
name: {json["imageName"]}""", reply_markup=admin_buttons())
        await state.finish()


@dp.message_handler(IsAdmin(), text="Удалить обои")
async def delete_wallpapers(message: types.Message):
    await message.reply("Отправь название фото:", reply_markup=add_buttons(["Отмена"]))
    await Dialog.delete.set()


@dp.message_handler(content_types=[types.ContentType.TEXT], state=Dialog.delete)
async def delete_photo(message: types.Message, state: FSMContext):
    if message.text == "Отмена":
        await state.finish()
        await message.reply("Отменено", reply_markup=admin_buttons())
        return
    json = API().delete_wallpaper(message.text)
    if json["success"] == False:
        await message.reply(f"Ошибка {json['code']}", reply_markup=admin_buttons())
        await state.finish()
        return
    else:
        await message.reply(f"""Фото успешно удалено! 
{json["message"]}""", reply_markup=admin_buttons())
        await state.finish()