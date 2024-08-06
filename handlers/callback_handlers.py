from telebot import TeleBot
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from database.db import *
from utils.bot_config import *

#Crear menú principal
def create_main_keyboard():
    main_keyboard = InlineKeyboardMarkup(row_width=2)
    b1 = InlineKeyboardButton("• Cuenta •", callback_data="cuenta")
    b2 = InlineKeyboardButton("• Gateways •", callback_data="gateways")
    b3 = InlineKeyboardButton("• Tools •", callback_data="tools")
    b4 = InlineKeyboardButton("• Planes y Precios •", callback_data="precios")
    b5 = InlineKeyboardButton("• Canal Oficial •", url='https://t.me/+UggxblGvjyY3NDZh')
    main_keyboard.add(b1, b2, b3, b4, b5)
    return main_keyboard

def create_back_keyboard():
    back_keyboard = InlineKeyboardMarkup()
    back_button = InlineKeyboardButton("• Atrás •", callback_data="atras")
    back_keyboard.add(back_button)
    return back_keyboard
  
# Define el manejador de callbacks para la Opción 1
@bot.callback_query_handler(func=lambda call: call.data == "cuenta")
def handle_opción1(call):
    user = call.from_user
    owner_id = get_owner_id()
    chat_id = call.message.chat.id
    user_info = f""" ===============================
          🤖 INFORMACIÓN DE USUARIO 🤖
          🆔 ID: <code>{user.id}</code>
          🏆 Plus: {'✅' if is_plus(chat_id) else '❌'}
          💵 Créditos: {get_tokens(chat_id)}
          👑 Es Propietario: {'✅' if is_owner(user.id) or user.id == owner_id else '❌'}
        ===============================
          """

    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=user_info,
        reply_markup=create_back_keyboard(),  # Agrega el botón "Atrás"
        parse_mode="HTML"
    )

@bot.callback_query_handler(func=lambda call: call.data == "atras")
def handle_back(call):
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=f'''=========================|
            🤖 {BOT_NAME} 🤖
         
            Si tienes algun problemas o
            necesitas ayuda no dudes en
            contactar a mi programador😃
         
            By: <a href="tg://user?id={OWNER}">@Altaïr</a>
            =========================|
            ''',
        reply_markup=create_main_keyboard(),  # Regresa al teclado principal
        parse_mode="HTML",
        disable_web_page_preview=True
    )

# Define el manejador de callbacks para la opción3
@bot.callback_query_handler(func=lambda call: call.data == 'tools')
def handle_opcion3(call):
    tools_text=f'''======================|
                ✥ TOOLS ✥

           ✘ Bin Información
           ‣ Comando: /bin
           ‣ Ejemplo: /bin 445100
           ‣ Info: Muestra información 
           detallada acerca de un Bin.

           ✘ Generar CC'S
           ‣ Comando: /gen
           ‣ Ejemplo: /gen 445100
           ‣ Info: Genera 10 CC'S a partir de un Bin o Extra.
        =======================|
        '''
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=tools_text,
        reply_markup=create_back_keyboard(),
        disable_web_page_preview=True,
        parse_mode="HTML"
    )

# Define el manejador de callbacks para la opción4
def create_prices_main_keyboard():
    prices_main_keyboard = InlineKeyboardMarkup(row_width=0)
    credit_button = InlineKeyboardButton("• Créditos •", callback_data="creditos")
    plus_button = InlineKeyboardButton("• Plus •", callback_data="plus")
    buy_button = InlineKeyboardButton("• Buy •", url='https://t.me/alltallr')
    prices_main_keyboard.add(credit_button, plus_button, buy_button)
    return prices_main_keyboard

combined_keyboard = types.InlineKeyboardMarkup()
combined_keyboard.add(types.InlineKeyboardButton("✥ Buy ✥", url='https://t.me/alltallr'))
    
combined_keyboard.add(types.InlineKeyboardButton("• Atrás •", callback_data='atras'))

@bot.callback_query_handler(func=lambda call: call.data == 'precios')
def handle_opcion4(call):
    precios_text=f'''================================|
            ✥ Planes & Precios ✥

        ▹ Para realizar la compra de alguna     
        Subscripción o Paquete de Créditos,
        presione el botón de ✥ Buy ✥ 
        y sera dirijido hacia el admin.

        ♖ Métodos de Pago ♖
        ▹ USDT (binance-coinex)
        ▹ Peso Cubano (transferencia)
        ▹ Peso Mexicano (transferencia)
        ▹ Pago Móvil


        ♛ Subscripción Plus ♛
        ▸ Acceso a todos los Gateways, de forma ilimitada.
        ▸ Descuento exclusivos en la compra de Créditos.


        ✥ Subscripción Plus ✥

🜲 15/días = $5.00 USD
+25/créditos de Regalo.

🜲 30/días = $8.50 USD
+50/créditos de Regalo.


        🜲 Créditos 🜲
        ▸ Acceso a diversos comandos solo disponibles con créditos.
        ▸ Acceso a los Gateways con Modo MASS, solo disponible con créditos.


        ✥ Paquete Créditos ✥

🜲 100/créditos = $4.50 USD
🜲 200/créditos = $8.00 USD
🜲 250/créditos = $10.50 USD
        =================================|
        '''
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=precios_text,
        reply_markup=combined_keyboard,
        disable_web_page_preview=True,
        parse_mode="HTML"
    )

def register_callback_handlers(bot: TeleBot):
    bot.register_callback_query_handler(handle_back, func=lambda call: call.data == 'atras')
    bot.register_callback_query_handler(handle_back, func=lambda call: call.data == 'cuenta')
    bot.register_callback_query_handler(handle_opcion3, func=lambda call: call.data == 'tools')
    bot.register_callback_query_handler(handle_opcion4, func=lambda call: call.data == 'precios')