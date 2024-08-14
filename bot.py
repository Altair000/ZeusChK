import telebot
import os
from flask import Flask, request
from handlers.command_handlers import register_command_handlers
from handlers.callback_handlers import register_callback_handlers
from utils.bot_config import *
from admin.admin_cmds import register_admin_command_handlers

app = Flask(__name__)

@app.route('/' + bot_token, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "¡Mensaje recibido!", 200

@app.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://zeuschk-64ea0cb25362.herokuapp.com/' + bot_token)
    return "¡Webhook configurado!", 200

# Registra los manejadores de comandos y callbacks
register_command_handlers(bot)
register_callback_handlers(bot)
register_admin_command_handlers(bot)

# Main
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
