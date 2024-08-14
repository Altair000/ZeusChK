import telebot
from flask import Flask, request
from handlers.command_handlers import register_command_handlers
from handlers.callback_handlers import register_callback_handlers
from utils.bot_config import *
from admin.admin_cmds import register_admin_command_handlers

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return '', 200

# Registra los manejadores de comandos y callbacks
register_command_handlers(bot)
register_callback_handlers(bot)
register_admin_command_handlers(bot)

# Main
if __name__ == '__main__':
    app.run()
