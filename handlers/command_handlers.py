from telebot import TeleBot, types
from database.db import *
from handlers.callback_handlers import *
from services.card_generator import *
from gates.shopify import *
from gates.stripe import *
from gates.braintree import *
import random
import requests
import re

# Manejador /start
@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    bot.send_message(message.chat.id, f'''=========================|
            🤖 {BOT_NAME} 🤖
         
            Si tienes algun problemas o
            necesitas ayuda no dudes en
            contactar a mi programador😃
         
            By: <a href="tg://user?id={OWNER}">@Altaïr</a>
            =========================|
            ''', disable_web_page_preview=True, parse_mode="HTML", reply_markup=create_main_keyboard())
    if not user_exists(chat_id):
       add_user(chat_id)

def user_exists(chat_id):
    conn = connect_to_db()
    try:
        with conn.cursor() as cursor:
            cursor.execute('SELECT COUNT(*) AS count FROM users WHERE chat_id = %s', (chat_id,))
            result = cursor.fetchone()
            return result['count'] > 0
    except pymysql.Error as err:
        print(f"Error: {err}")
        return False
    finally:
        conn.close()

def add_user(chat_id):
    conn = connect_to_db()
    try:
        with conn.cursor() as cursor:
            cursor.execute('INSERT INTO users (chat_id, tokens) VALUES (%s, 0)', (chat_id,))
            conn.commit()
    except pymysql.Error as err:
        print(f"Error: {err}")
    finally:
        conn.close()

@bot.message_handler(commands=['info'])
def info(message):
    bot.send_chat_action(message.chat.id, 'typing')
    if message.reply_to_message:
        user = message.reply_to_message.from_user
    else:
        user = message.from_user
    chat_id = message.chat.id
    user_info = f"""
    ===============================|
    🤖 INFORMACIÓN DE USUARIO 🤖
    🆔 ID: <code>{user.id}</code>
    👤 Usuario: @{user.username}
    🏅 Nombre: {user.first_name}
    🏆 Plus: {'✅' if is_plus(chat_id) else '❌'}
    💵 Créditos: {get_tokens(chat_id)}
    👑 Es Propietario: {'✅' if is_owner(user.id) else '❌'}
    💻 CMDS: /info, /gen, /chk, /bin
    ===============================|
    """
    bot.reply_to(message, user_info, parse_mode="HTML")

admin_commands = {
    '/add_plus': 'Agrega un usuario la suscripcion plus. Uso: /add_plus <chat_id>',
   
    'remove_plus': 'Remueve a un usuario la suscripcion plus. Uso: /remove_plus <chat_id>',
   
    'verify_plus': 'Verifica los usuarios con suscripcion plus. Uso: /verify_plus',
 
    '/add_tokens': 'Agrega tokens a un usuario. Uso: /add_tokens <chat_id> <cantidad>',
 
    '/remove_tokens': 'Quita tokens a un usuario. Uso: /remove_tokens <chat_id> <cantidad>',
 
    '/check_tokens': 'Verifica la cantidad de tokens de un usuario. Uso: /check_tokens <chat_id>',
 
    '/admin': 'Muestra esta ayuda sobre los comandos de administración.'
}

# Comando para mostrar ayuda de comandos de administración
@bot.message_handler(commands=['admin'])
def admin(message):
    user_id = message.from_user.id
    if is_owner(user_id):
        help_message = "Comandos de Administración:\n\n"
        for command, description in admin_commands.items():
            help_message += f"{command}: {description}\n"
        bot.reply_to(message, help_message)
    else:
        bot.reply_to(message, "No tienes permisos para usar este comando.")

# Comando para obtener información del BIN
@bot.message_handler(commands=['bin'])
def bin(message):
    # Obtener el BIN del mensaje del usuario
    bin_number = message.text.split()[1] if len(message.text.split()) > 1 else None
    
    if bin_number:
        try:
            # Realizar una solicitud a la API para obtener información del BIN
            response = requests.get(f'https://lookup.binlist.net/{bin_number}')
            response.raise_for_status()
            bin_data = response.json()
            
            # Construir el mensaje de respuesta con la información del BIN
            response_message = f"Información del BIN {bin_number}:\n\n"
            response_message += f"País: {bin_data['country']['name']}\n"
            response_message += f"Código de país: {bin_data['country']['alpha2']}\n"
            response_message += f"Moneda: {bin_data['country']['currency']}\n"
            response_message += f"Banco emisor: {bin_data['bank']['name']}\n"
            response_message += f"Tipo de tarjeta: {bin_data['type']}\n"
            response_message += f"Marca: {bin_data['scheme']}\n"
            response_message += f"Nivel: {bin_data['brand']}"
            
            bot.reply_to(message, response_message)
        except requests.exceptions.RequestException as e:
            bot.reply_to(message, f"Error al obtener información del BIN: {e}")
    else:
        bot.reply_to(message, "Por favor, proporciona un número BIN válido.")

@bot.message_handler(commands=['gen'])
def gen(message: types.Message):
    bot.send_chat_action(message.chat.id, 'typing')
    
    # Extrae el BIN del mensaje
    args = message.text.split()
    if len(args) < 2:
        return bot.reply_to(message, "Por favor proporciona un BIN. Ejemplo: /gen 445100")
    
    bin_number = args[1]
    
    # Genera 10 tarjetas
    cards = []
    for _ in range(10):
        card = generate_card(bin_number)
        if luhn_check(card):
            mm = random.randint(1, 12)
            yy = random.randint(2023, 2028)
            cvv = random.randint(100, 999)
            cards.append(f"{card}|{mm:02}|{yy}|{cvv}")
    
    # Obtiene información del BIN
    bin_info = get_bin_info(bin_number)
    
    # Prepara la respuesta
    response = f"Se han generado 10 tarjetas a partir del BIN `{bin_number}`:\n\n"
    for i, card in enumerate(cards):
        response += f"💳 Tarjeta {i + 1}: `{card}`\n"
    
    response += f"\n**Información del BIN:**\n"
    response += f"🔹 **Marca:** {bin_info['brand']}\n"
    response += f"🔹 **Tipo:** {bin_info['type']}\n"
    response += f"🔹 **Banco:** {bin_info['bank']}\n"
    response += f"🔹 **País:** {bin_info['country']}\n"
    response += f"\n👤 Generado por: {message.from_user.first_name}"
    
    bot.reply_to(message, response, parse_mode="Markdown")

@bot.message_handler(commands=['sh'])
def sh(message):
    user_id = message.from_user.id
    if is_plus(user_id):
        card_data = message.text.split()[1]  # Asume que el usuario envía /pay ccn|mm|yyyy|cvv
        cc, mes, ano, cvv = card_data.split('|')
        # Continuar con el procesamiento de la transacción
        shopify(cc, mes, ano, cvv, message)
    else:
        bot.reply_to(message, "No tienes premiso para utilizar este comando.")

@bot.message_handler(commands=['st'])
def st(message):
      card_data = message.text.split()[1]
      cc, mes, ano, cvv = card_data.split('|')
       
      stripe(cc, mes, ano, cvv, message)

@bot.message_handler(commands=['b3'])
def b3(message):
    try:
        # Supongamos que el usuario envía los datos en el formato: número, fecha, cvv
        card_info = message.text.split()[1]  # Ignorar el comando y obtener los argumentos
        if len(card_info) != 3:
            raise ValueError("Formato incorrecto. Usa: /check número fecha_expiración cvv")
        
        card_number, expiration_date, cvv = card_info
        msg, respuesta = check_credit_card(card_number, expiration_date, cvv)

        ccvip = f"{card_number}|{expiration_date}|{cvv}"
        
        # Obtener información del BIN
        bin_info = get_bin_info(bin_number[:6])
        bank_name = bin_info.get("bank", "Desconocido")
        card_type = bin_info.get("type", "Desconocido")
        card_level = bin_info.get("level", "Desconocido")
        brand = bin_info.get("brand", "Desconocido")
        country = bin_info.get("country", "Desconocido")
        flag = bin_info.get("flag", "")

        user = message.from_user
        chat_id = message.chat.id

        # Enviar el mensaje formateado
        bot.send_message(chat_id, text=f"""
<b>Información de la Tarjeta</b> <code>{ccvip}</code>
<b>• Resultado:</b> <code>{msg}</code>
<b>Respuesta:</b> <code>{respuesta}</code>
<b>Banco:</b> <code>{bank_name}</code>
<b>Tipo:</b> <code>{card_type}</code> - <code>{card_level}</code> - <code>{brand}</code>
<b>🟢 País:</b> <code>{country} {flag}</code> 
-------------------INFO------------------- 
• Créditos: {get_tokens(chat_id)}
• BY: @{user.username}
• ID: <code>{user.id}</code>
        """, parse_mode='HTML')

    except Exception as e:
        print(f"Error inesperado: {e}")
        msg = "DECLINADA"
        ccvip = f"{card_number}|{expiration_date}|{cvv}"
        respuesta = f"Error inesperado: {e}"
        bot.send_message(message.chat.id, text=f"""
<b>Información de la Tarjeta</b> <code>{ccvip}</code>
<b>Resultado:</b> <code>{msg}</code>
<b>Respuesta:</b> <code>{respuesta}</code>
        """, parse_mode='HTML')

def register_command_handlers(bot: TeleBot):
    bot.register_message_handler(start, commands=['start'])
    bot.register_message_handler(info, commands=['info'])
    bot.register_message_handler(start, commands=['admin'])
    bot.register_message_handler(start, commands=['bin'])
    bot.register_message_handler(start, commands=['gen'])
    bot.register_message_handler(sh, commands=['sh'])
    bot.register_message_handler(st, commands=['st'])
    bot.register_message_handler(b3, commands=['b3'])
