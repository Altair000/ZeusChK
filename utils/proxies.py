import requests
from utils.bot_config import *

def update_proxies_list(file_stream):
    proxies_list = {}
    try:
        for line in file_stream:
            proxy = line.strip().split(':')
            if len(proxy) == 4:
                ip, port, user, password = proxy
                proxies_list[ip] = {
                    'port': port,
                    'user': user,
                    'pass': password
                }
    except Exception as e:
        bot.send_message(message.chat.id, f"Error al procesar el archivo: {e}")
    
    return proxies_list

def filter_and_update_proxies(proxies_list, progress_message_id):
    functional_proxies = {}
    total_proxies = len(proxies_list)
    removed_proxies = 0
    
    for i, (ip, details) in enumerate(proxies_list.items(), 1):
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
        
        # Actualiza la barra de progreso
        progress = int((i / total_proxies) * 100)
        bot.edit_message_text(
            text=f"Progreso: {progress}%\nTotal de proxies: {total_proxies}",
            chat_id=message.chat.id,
            message_id=progress_message_id
        )

    proxies_list.clear()
    proxies_list.update(functional_proxies)

    return functional_proxies, len(functional_proxies), removed_proxies, total_proxies

@bot.message_handler(content_types=['document'])
def handle_document(message):
    if not is_owner:
        bot.send_message(message.chat.id, "SOLO ADMIN")
    else:
        if message.document:
            # Enviar mensaje de progreso inicial
            progress_message = bot.send_message(message.chat.id, "Procesando el archivo. Por favor, espere...")
            progress_message_id = progress_message.message_id
            
            # Obtener información del archivo
            file_info = bot.get_file(message.document.file_id)
            file_url = f"https://api.telegram.org/file/bot{API_TOKEN}/{file_info.file_path}"
            
            # Descargar el archivo en memoria
            response = requests.get(file_url)
            file_stream = io.StringIO(response.text)
            
            # Procesar el archivo en memoria
            proxies_list = update_proxies_list(file_stream)
            functional_proxies, functional_count, removed_proxies, total_proxies = filter_and_update_proxies(proxies_list, progress_message_id)
            
            # Enviar mensaje con el resumen
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
                    # Registro del siguiente paso para manejar el nuevo archivo
                    bot.register_next_step_handler(satisfaction_message, handle_document)
                else:
                    bot.send_message(message.chat.id, "Por favor, responde con 'sí' o 'no'.")
