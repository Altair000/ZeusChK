import telebot
from handlers.command_handlers import register_command_handlers
from handlers.callback_handlers import register_callback_handlers
from utils.bot_config import *
from admin.admin_cmds import register_admin_command_handlers

# Registra los manejadores de comandos y callbacks
register_command_handlers(bot)
register_callback_handlers(bot)
register_admin_command_handlers(bot)

# Main
if __name__ == '__main__':
    print('INICIANDO...')
    bot.infinity_polling()
