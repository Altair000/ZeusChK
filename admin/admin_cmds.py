import telebot
from telebot import TeleBot
from utils.bot_config import *
from database.db import *

# Función para agregar un usuario plus
@bot.message_handler(commands=['add_plus'])
def add_plus(message):
    user_id = message.from_user.id
    if is_owner(user_id):
        chat_id = message.text.split()[1] # Obtén el chat_id del comando

        db = connect_to_db()
        if db is None:
            return

        with db.cursor() as cursor:
        # Verifica si el usuario ya está en la tabla premium
             query = "SELECT 1 FROM premium WHERE chat_id = %s"
             cursor.execute(query, (chat_id,))
             result = cursor.fetchone()

             if result:
                bot.send_message(message.chat.id, f"El usuario con chat_id {chat_id} ya es premium.")
             else:
            # Agrega el usuario a la tabla premium
                query = "INSERT INTO premium (chat_id, plus) VALUES (%s, 1)"
                cursor.execute(query, (chat_id,))
                db.commit()
        db.close()
        bot.send_message(message.chat.id, f"El usuario con chat_id {chat_id} ha sido agregado como premium.")
    else:
        bot.send_message(message.chat.id, "No tienes permisos para agregar usuarios premium.")

@bot.message_handler(commands=['remove_plus'])
def remove_plus(message):
    user_id = message.from_user.id
    if is_owner(user_id):
        try:
            chat_id = message.text.split()[1] # Obtiene el chat_id del mensaje

            with connect_to_db() as db:
                with db.cursor() as cursor:
                    query = "DELETE FROM premium WHERE chat_id = %s"
                    cursor.execute(query, (chat_id,))
                    db.commit()

                    bot.send_message(message.chat.id, f"Usuario con chat_id {chat_id} eliminado de la lista 'plus'.")
        except (pymysql.Error, Exception) as e:
            bot.send_message(message.chat.id, f"Error al eliminar usuario: {e}")
    else:
        bot.send_message(message.chat.id, "No tienes permisos para eliminar usuarios 'plus'.")

# Función para verificar usuarios plus
@bot.message_handler(commands=['verify_plus'])
def verify_plus(message):
    user_id = message.from_user.id
    if is_owner(user_id):
        try:
            with connect_to_db() as db:
                with db.cursor() as cursor:
                    query = "SELECT chat_id FROM premium WHERE plus = 1"
                    cursor.execute(query)
                    usuarios_plus = cursor.fetchall()
                    if usuarios_plus:
                        mensaje = "Usuarios plus:\n"
                        for user_id in usuarios_plus:
                            mensaje += f"- {user_id}\n"
                            bot.send_message(message.chat.id, mensaje)
                    else:
                        bot.send_message(message.chat.id, "No hay usuarios plus registrados.")
   
        except (pymysql.Error, Exception) as e:
            bot.send_message(message.chat.id, f"Error al verificar usuario plus: {e}")
  
    else:
        bot.send_message(message.chat.id, "No tienes permisos para verificar usuarios plus.")

# Comando para agregar tokens
@bot.message_handler(commands=['add_tokens'])
def add_tokens(message):
    user_id = message.from_user.id
    if is_owner(user_id):
        args = message.text.split()
        if len(args) < 3:
            bot.reply_to(message, "Uso incorrecto. Usa: /add_tokens <chat_id> <cantidad>")
            return
        
        try:
            chat_id = int(args[1])  # Asegúrate de que chat_id sea un entero
            tokens_to_add = int(args[2])
            
            if tokens_to_add <= 0:
                bot.reply_to(message, "La cantidad de tokens debe ser mayor que 0.")
                return
            
            new_balance = add_tokens_to_user(chat_id, tokens_to_add)
            if new_balance is None:
                bot.reply_to(message, f"El usuario con chat_id {chat_id} no existe.")
            else:
                bot.reply_to(message, f"Se han agregado {tokens_to_add} tokens al usuario con chat_id {chat_id}. Nuevo saldo: {new_balance}")
        except ValueError:
            bot.reply_to(message, "El chat_id y la cantidad de tokens deben ser números válidos.")
    else:
        bot.reply_to(message, "No tienes permisos para agregar tokens.")

# Comando para quitar tokens
@bot.message_handler(commands=['remove_tokens'])
def remove_tokens(message):
    user_id = message.from_user.id
    if is_owner(user_id):
        args = message.text.split()
        if len(args) < 3:
            bot.reply_to(message, "Uso incorrecto. Usa: /remove_tokens <chat_id> <cantidad>")
            return
        
        try:
            chat_id = int(args[1])  # Asegúrate de que chat_id sea un entero
            tokens_to_remove = int(args[2])
            
            if tokens_to_remove <= 0:
                bot.reply_to(message, "La cantidad de tokens debe ser mayor que 0.")
                return
            
            new_balance = remove_tokens_from_user(chat_id, tokens_to_remove)
            if new_balance is None:
                bot.reply_to(message, f"El usuario con chat_id {chat_id} no existe.")
            elif new_balance == "Saldo insuficiente.":
                bot.reply_to(message, f"No hay suficientes tokens para quitar al usuario con chat_id {chat_id}.")
            else:
                bot.reply_to(message, f"Se han quitado {tokens_to_remove} tokens al usuario con chat_id {chat_id}. Nuevo saldo: {new_balance}")
        except ValueError:
            bot.reply_to(message, "El chat_id y la cantidad de tokens deben ser números válidos.")
    else:
        bot.reply_to(message, "No tienes permisos para quitar tokens.")

# Comando para verificar la cantidad de tokens
@bot.message_handler(commands=['check_tokens'])
def check_tokens(message):
    args = message.text.split()
    if len(args) < 2:
        bot.reply_to(message, "Uso incorrecto. Usa: /check_tokens <chat_id>")
        return
    
    try:
        chat_id = int(args[1])  # Asegúrate de que chat_id sea un entero
        
        # Obtener el saldo de tokens
        tokens = get_tokens(chat_id)
        if tokens is None:
            bot.reply_to(message, f"El usuario con chat_id {chat_id} no existe.")
        else:
            bot.reply_to(message, f"El usuario con chat_id {chat_id} tiene {tokens} tokens.")
    except ValueError:
        bot.reply_to(message, "El chat_id debe ser un número válido.")

def register_admin_command_handlers(bot: TeleBot):
    from handlers.command_handlers import start
    bot.register_message_handler(start, commands=['add_plus'])
    bot.register_message_handler(start, commands=['remove_plus'])
    bot.register_message_handler(start, commands=['verify_plus'])
    bot.register_message_handler(start, commands=['add_tokens'])
    bot.register_message_handler(start, commands=['remove_tokens'])
    bot.register_message_handler(start, commands=['check_tokens'])

