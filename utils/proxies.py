import requests
from utils.bot_config import *

# Manejador para documentos recibidos
@bot.message_handler(content_types=['document'])
def handle_document(message):
    if not is_owner(message.from_user.id):
        bot.send_message(message.chat.id, "No tienes permiso para usar este comando.")
        return
    
    bot.send_message(message.chat.id, "ACCESO CONCEDIDO.")

    if message.document.file_name == 'proxies.txt':
        bot.send_message(message.chat.id, "ARCHIVO DE PROXIES RECIBIDO")
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

def update_proxies_list(file_path):
    proxies_list = {}
    message_id = message.chat.id
    try:
        with open(file_path, 'r') as file:
            for line in file:
                proxy = line.strip().split(':')
                if len(proxy) == 4:
                    ip, port, user, password = proxy
                    proxies_list[ip] = {
                        'port': port,
                        'user': user,
                        'pass': password
                    }
    except FileNotFoundError:
        bot.send_message(message_id, f"Error: El archivo {file_path} no existe.")
    except Exception as e:
        bot.send_message(message_id, f"Error al leer el archivo: {e}")
    
    return proxies_list

def filter_and_update_proxies(proxies_list):
    functional_proxies = {}
    total_proxies = len(proxies_list)
    removed_proxies = 0

    for ip, details in proxies_list.items():
        proxy = {
            'http': f"http://{details['user']}:{details['pass']}@{ip}:{details['port']}",
            'https': f"http://{details['user']}:{details['pass']}@{ip}:{details['port']}"
        }
        
        try:
            response = requests.get('http://httpbin.org/ip', proxies=proxy, timeout=5)
            if response.status_code == 200:
                functional_proxies[ip] = details
            else:
                removed_proxies += 1
        except requests.RequestException:
            removed_proxies += 1

    # Actualiza proxies_list con solo los proxies funcionales
    proxies_list.clear()
    proxies_list.update(functional_proxies)

    return functional_proxies, len(functional_proxies), removed_proxies, total_proxies
    
