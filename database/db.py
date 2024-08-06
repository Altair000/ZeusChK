import pymysql
from config.config import *

# Función para conectarse a la base de datos
def connect_to_db():
    conn = pymysql.connect(
        host=Host,
        user=User,
        password=Password,
        database=Database,
        cursorclass=pymysql.cursors.DictCursor
    )
    return conn

def close_db(conn):
    connection.close()

# Verificar owner
def is_owner(user_id):
    if user_id == OWNER:
        return True
    else:
        return False

# Función para obtener el owner.id
def get_owner_id():
    conn = connect_to_db()
    try:
        with conn.cursor() as cursor:
            cursor.execute('SELECT owner_id FROM owner LIMIT 1')  # Ajusta la consulta según tu estructura
            result = cursor.fetchone()
            return result['owner_id'] if result else None
    except pymysql.Error as err:
        print(f"Error: {err}")
        return None
    finally:
        conn.close()

# Obtener el owner_id al iniciar el bot
def OWNER():
    OWNER = get_owner_id()

OWNER = get_owner_id()
if OWNER is None:
    print("No se pudo obtener el owner_id.")

def is_owner(owner_id):
    conn = connect_to_db()
    try:
        with conn.cursor() as cursor:
            cursor.execute('SELECT COUNT(*) as count FROM owner WHERE owner_id = %s', (owner_id,))
            result = cursor.fetchone()
            if result is None:
                return False

            count = result['count']
            return count > 0  # Devuelve True si el propietario existe
    except pymysql.Error as err:
        print(f"Error: {err}")
        return False      
    finally:
        conn.close()

def is_plus(chat_id):
    conn = connect_to_db()
    try:
        with conn.cursor() as cursor:
            cursor.execute('SELECT COUNT(*) AS count FROM premium WHERE chat_id = %s AND plus = 1', (chat_id,))
            result = cursor.fetchone()
            if result is None:
                return False

            count = result['count']
            return count > 0
    except pymysql.Error as err:
        print(f"Error: {err}")
        return False
    finally:
        conn.close()

def get_tokens(chat_id):
    conn = connect_to_db()
    cursorclass=DictCursor
    try:
        with conn.cursor() as cursor:
            cursor.execute('SELECT tokens FROM users WHERE chat_id = %s', (chat_id,))
            result = cursor.fetchone()
            return result['tokens'] if result else 0  # Retorna la cantidad de tokens o 0 si no existe
    except pymysql.Error as err:
        print(f"Error: {err}")
        return 0  # Retorna 0 en caso de error
    finally:
        conn.close()

# Función para obtener el token del bot desde la base de datos
def get_bot_token():
    conn = connect_to_db()
    try:
        with conn.cursor() as cursor:
            cursor.execute('SELECT bot_token FROM settings LIMIT 1')
            result = cursor.fetchone()
            return result['bot_token'] if result else None
    except pymysql.Error as err:
        print(f"Error: {err}")
        return None
    finally:
        conn.close()  # Asegúrate de cerrar la conexión

def add_tokens_to_user(chat_id, tokens_to_add):
    try:
        with connect_to_db() as db:
            with db.cursor(pymysql.cursors.DictCursor) as cursor:  # Usar DictCursor para resultados como diccionario
                # Consulta para obtener el saldo actual del usuario
                query_saldo = "SELECT tokens FROM users WHERE chat_id = %s"
                cursor.execute(query_saldo, (chat_id,))
                current_balance_row = cursor.fetchone()

                # Imprimir el resultado de la consulta para depuración
                print(f"Resultado de la consulta para chat_id {chat_id}: {current_balance_row}")

                # Verificar si se obtuvo un resultado
                if current_balance_row is not None:
                    current_balance = current_balance_row['tokens']  # Acceder al valor de tokens usando la clave
                    new_balance = current_balance + tokens_to_add

                    # Actualiza el saldo del usuario
                    query_update = "UPDATE users SET tokens = %s WHERE chat_id = %s"
                    cursor.execute(query_update, (new_balance, chat_id))
                    db.commit()
                    return new_balance
                else:
                    return None  # El usuario no existe
    except pymysql.Error as e:
        print(f"Error en la base de datos: {e}")
        return "Error en la base de datos."

# Función para quitar tokens
def remove_tokens_from_user(chat_id, tokens_to_remove):
    try:
        with connect_to_db() as db:
            with db.cursor(pymysql.cursors.DictCursor) as cursor:
                # Consulta para obtener el saldo actual del usuario
                query_saldo = "SELECT tokens FROM users WHERE chat_id = %s"
                cursor.execute(query_saldo, (chat_id,))
                current_balance_row = cursor.fetchone()

                # Imprimir el resultado de la consulta para depuración
                print(f"Resultado de la consulta para chat_id {chat_id}: {current_balance_row}")

                # Verificar si se obtuvo un resultado
                if current_balance_row is not None:
                    current_balance = current_balance_row['tokens']  # Acceder al valor de tokens
                    if current_balance >= tokens_to_remove:
                        new_balance = current_balance - tokens_to_remove

                        # Actualiza el saldo del usuario
                        query_update = "UPDATE users SET tokens = %s WHERE chat_id = %s"
                        cursor.execute(query_update, (new_balance, chat_id))
                        db.commit()
                        return new_balance
                    else:
                        return "Saldo insuficiente."  # No hay suficientes tokens
                else:
                    return None  # El usuario no existe
    except pymysql.Error as e:
        print(f"Error en la base de datos: {e}")
        return "Error en la base de datos."

def get_tokens(chat_id):
    try:
        with connect_to_db() as db:
            with db.cursor(pymysql.cursors.DictCursor) as cursor:
                # Consulta para obtener el saldo actual del usuario
                query_saldo = "SELECT tokens FROM users WHERE chat_id = %s"
                cursor.execute(query_saldo, (chat_id,))
                current_balance_row = cursor.fetchone()

                # Imprimir el resultado de la consulta para depuración
                print(f"Resultado de la consulta para chat_id {chat_id}: {current_balance_row}")

                # Verificar si se obtuvo un resultado
                if current_balance_row is not None:
                    return current_balance_row['tokens']  # Acceder al valor de tokens
                else:
                    return None  # El usuario no existe
    except pymysql.Error as e:
        print(f"Error en la base de datos: {e}")
        return "Error en la base de datos."
