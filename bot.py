import telebot
import os
import bugsnag
from bugsnag.flask import handle_exceptions
from flask import Flask, request
from handlers.command_handlers import register_command_handlers
from handlers.callback_handlers import register_callback_handlers
from utils.bot_config import *
from admin.admin_cmds import register_admin_command_handlers
from admin.admin_cmds import *
from gates.stripe import *
from utils.proxies import *

# Configure BugSnag
bugsnag.configure(
  api_key = "d2055e6398e4602fb88c70a77cf896ac",
  project_root = "https://zeuschk-64ea0cb25362.herokuapp.com/",
)

@bot.message_handler(content_types=['document'])
def handle_document(message):
    if not is_owner(message.from_user.id):
        bot.send_message(message.chat.id, "No tienes permiso para usar este comando.")
    else:
        bot.send_message(message.chat.id, "ACCESO CONCEDIDO.")
    if message.document.file_name == 'proxies.txt':
        file_info = bot.get_file(message.document.file_id)
        file_path = file_info.file_path
        proxies_list = update_proxies_list(file_path)

        # Mensaje de inicio de adquisición de proxies
        sent_message = bot.send_message(message.chat.id, "Comenzando adquisición de proxies...")
        for i in range(10):
            bot.edit_message_text(chat_id=message.chat.id,
                                  text=f'• ADQUIRIENDO PROXIES DE FILE: {i * 10}%',
                                  reply_markup=None,
                                  message_id=sent_message.message_id,
                                  parse_mode="HTML"
                                  )
            time.sleep(1)

        # Filtrar y actualizar proxies
        functional_proxies, functional_count, removed_proxies, total_proxies = filter_and_update_proxies(proxies_list)

        # Mensaje de inicio de verificación de proxies
        sent_message_1 = bot.send_message(message.chat.id, "Comenzando verificación de proxies...")
        for i in range(10):
            bot.edit_message_text(chat_id=message.chat.id,
                                  text=f'• VERIFICANDO PROXIES: {i * 10}%',
                                  reply_markup=None,
                                  message_id=sent_message_1.message_id,
                                  parse_mode="HTML"
                                  )
            time.sleep(1)

        # Mensaje con resultados finales
        response_message = (
            f"Total de proxies: {total_proxies}\n"
            f"Proxies funcionales: {functional_count}\n"
            f"Proxies eliminados: {removed_proxies}\n"
            "¿Estás satisfecho con la respuesta? (sí/no)"
        )
        bot.send_message(message.chat.id, response_message)

        # Manejador para la respuesta de satisfacción
        @bot.message_handler(func=lambda m: m.chat.id == message.chat.id)
        def satisfaction_response(satisfaction_message):
            if satisfaction_message.text.lower() == 'sí':
                bot.send_message(message.chat.id, "¡PROXIES ACTUALIZADOS!")
            elif satisfaction_message.text.lower() == 'no':
                bot.send_message(message.chat.id, "Por favor, envía un nuevo archivo de proxies.")
                bot.register_next_step_handler(satisfaction_message, handle_document)
            else:
                bot.send_message(message.chat.id, "Por favor, responde con 'sí' o 'no'.")

    else:
        bot.send_message(message.chat.id, "Por favor, envía un archivo 'proxies.txt'.")

app = Flask(__name__)
handle_exceptions(app)
TOKEN = os.environ.get('TELEGRAM_TOKEN')

@app.route('/' + TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "¡Mensaje recibido!", 200

@app.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://zeuschk-64ea0cb25362.herokuapp.com/' + TOKEN)
    return "¡Webhook configurado!", 200

# Registra los manejadores de comandos y callbacks
register_command_handlers(bot)
register_callback_handlers(bot)
register_admin_command_handlers(bot)

# Main
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
