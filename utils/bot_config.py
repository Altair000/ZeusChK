import telebot
from database.db import get_bot_token

# Obtener el token del bot
bot_token = get_bot_token()

if bot_token:
    # Iniciar el bot con el token obtenido
    bot = telebot.TeleBot(bot_token)

# BOT INFO
bot_info = bot.get_me()
BOT_USERNAME = bot_info.username
BOT_NAME = bot_info.first_name
BOT_ID = bot_info.id