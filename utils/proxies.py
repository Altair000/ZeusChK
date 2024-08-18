import requests
from utils.bot_config import *

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
    
