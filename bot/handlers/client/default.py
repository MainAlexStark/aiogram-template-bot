""" third party imports """
import os

from aiogram import Router, F, types
from aiogram.filters import Command, CommandObject, CommandStart

""" internal imports """
from db import Config, DataBaseInterface

router = Router()

""" OPEN DataBase """
file_path = 'data/DataBase.db'
if os.path.exists(file_path):
    db = DataBaseInterface(file_path, "users")
else:
    raise Exception(f'File {file_path} not found')

""" OPEN STRINGS """
file_path = 'data/strings.json'
if os.path.exists(file_path):
    config_client = Config(file_path)
    strings = config_client.get()
else:
    raise Exception(f'File {file_path} not found')


@router.message(Command("start"))
async def cmd_start(message: types.Message):
    # Private chat check 
    if message.chat.type == "private":
        # Get user id
        user_id = message.from_user.id

        if db.is_user(user_id=user_id):
            await message.answer(text=strings['handlers']['start'])
        # If the user is new
        else:
            db.add_user(user_id=user_id)
            await message.answer(text=strings['handlers']['new_user_start'])