import uuid
import json
import requests
import hashlib
import hmac
import base64
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InputMediaPhoto
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes
)

# ==================================================
#                    BOT TOKEN
# ==================================================
TOKEN = "8919459210:AAGWtjHwgUFETIABPIVTOrhB2dcgGFvMLBc"

# ==================================================
#                  ADMIN ID & USERNAME
# ==================================================
ADMIN_ID = 6648941928
ADMIN_USERNAME = "https://t.me/dealer_x"

# ==================================================
#             PAYTM MERCHANT CREDENTIALS
# ==================================================
PAYTM_MID = "wJwasY46108610523084"
PAYTM_MERCHANT_KEY = "RKmwIgkAcKb5bu41"
PAYTM_WEBSITE = "WEBSTAGING"

PAYTM_URL_INITIATE = f"https://securegw-stage.paytm.in/theia/api/v1/initiateTransaction?mid={PAYTM_MID}&orderId="
PAYTM_URL_STATUS = f"https://securegw-stage.paytm.in/v3/order/status"

BOT_USERNAME = "https://t.me/Pre_mmsbot"

# ==================================================
#                    MAIN IMAGES
# ==================================================
START_IMAGE = "https://i.postimg.cc/MKWZn3Lv/IMG-20260521-163611-172.jpg"
PREMIUM_IMAGE = "https://i.postimg.cc/x89kTfHG/IMG-20260521-164434-789.jpg"

# ==================================================
#                    LINKS
# ==================================================
DEMO_CHANNEL = "https://t.me/demochannlink"
INFO_CHANNEL = "https://t.me/howtogetpre"

users = set()
plan_99 = 0
plan_149 = 0
plan_249 = 0
plan_499 = 0
active_orders = {}

# ==================================================
#         PURE PYTHON CHECKSUM (NO LIBRARY NEEDED)
# ==================================================
def generate_checksum(params_str, merchant_key):
    salt = "1234567890" 
    data_with_salt = params_str + "|" + salt
    sha256_hash = hashlib.sha256(data_with_salt.encode('utf-8')).hexdigest()
    checksum_str = sha256_hash + salt
    return base64.b64encode(checksum_str.encode('utf-8')).decode('utf-8')

# ==================================================
#                 PAYTM UTILS
# ==================================================
def create_paytm_order(order_id: str, amount: float, user_id: int):
    body = {
        "requestType": "Payment",
        "mid": PAYTM_MID,
        "websiteName": PAYTM_WEBSITE,
        "orderId": order_id,
        "callbackUrl": f"https://securegw-stage.paytm.in/theia/paytmCallback?ORDER_ID={order_id}",
        "txnAmount": {"value": f"{amount:.2f}", "currency": "INR"},
        "userInfo": {"custId": f"USER_{user_id}"}
    }
    
    try:
        body_str = json.dumps(body)
        checksum = generate_checksum(body_str, PAYTM_MERCHANT_KEY)
        
        paytm_params = {
            "body": body,
            "head": {"signature": checksum}
        }

        response = requests.post(PAYTM_URL_INITIATE + order_id, json=paytm_params)
        res_data = response.json()
        
        if res_data.get("body", {}).get("resultInfo", {}).get("resultStatus") == "S":
            txn_token = res_data["body"]["txnToken"]
            return f"https://securegw-stage.paytm.in/theia/api/v1/showPaymentPage?mid={PAYTM_MID}&orderId={order_id}&txnToken={txn_token}"
    except Exception as e:
        print(f"❌ Error: {e}")
    return None

def check_paytm_status(order_id: str):
    body = {"mid": PAYTM_MID, "orderId": order_id}
    try:
        body_str = json.dumps(body)
        checksum = generate_checksum(body_str, PAYTM_MERCHANT_KEY)
        paytm_params = {"body": body, "head": {"signature": checksum}}
        
        response = requests.post(PAYTM_URL_STATUS, json=paytm_params)
        return response.json().get("body", {}).get("resultInfo", {}).get("resultStatus")
    except:
        return "ERROR"

# ==================================================
#             SHARED TEXT CAPTION
# ==================================================
MAIN_CAPTION = (
    "<b>🔥 𝐏𝐑𝐄𝐌𝐈𝐔𝐌 𝐕𝐈𝐃𝐄𝐎 𝐂𝐎𝐋𝐋𝐄𝐂𝐓𝐈𝐎𝐍 🔥</b>\n\n"
    "<b>🎬 𝟓𝟎𝟎𝟎+ 𝐌𝐌𝐒 𝐕𝐈𝐃𝐄𝐎𝐒</b>\n\n"
    "<b>💋 𝟐𝟎𝟎𝟎+ 𝐂𝐎𝐔𝐏𝐋𝐄 𝐂𝐎𝐋𝐋𝐄𝐂𝐓𝐈𝐎𝐍</b>\n\n"
    "<b>🔥 𝟏𝟓𝟎𝟎𝟎+ 𝐏𝐑𝐄𝐌𝐈𝐔𝐌 𝐕𝐈𝐃𝐄𝐎𝐒</b>\n\n"
    "<b>📦 𝟏𝟎0+ 𝐕𝐈𝐏 𝐂𝐎𝐋𝐋𝐄𝐂𝐓𝐈𝐎𝐍𝐒</b>\n\n"
    "<b>⚡ 𝐈𝐍𝐒𝐓𝐀𝐍𝐓 𝐀𝐂𝐂𝐄𝐒𝐒</b>"
)

def home_buttons():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("💎 𝐆𝐄𝐓 𝐏𝐑𝐄𝐌𝐈𝐔𝐌 💎", callback_data="premium")],
        [InlineKeyboardButton("🎬 𝐃𝐄𝐌𝐎 𝐕𝐈𝐃𝐄𝐎𝐒", url=DEMO_CHANNEL)],
        [InlineKeyboardButton("📖 𝐇𝐎𝐖 𝐓𝐎 𝐆𝐄𝐓 𝐏𝐑𝐄𝐌𝐈𝐔𝐌", url=INFO_CHANNEL)]
    ])

# ==================================================
#                    START COMMAND
# ==================================================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    users.add(update.effective_user.id)
    await update.message.reply_photo(
        photo=START_IMAGE,
        caption=MAIN_CAPTION,
        parse_mode="HTML",
        reply_markup=home_buttons()
    )

# ==================================================
#                 BUTTON HANDLER
# ==================================================
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global plan_99, plan_149, plan_249, plan_499
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "premium":
        keyboard = [
            [InlineKeyboardButton("💎 𝐌𝐒 𝐕!𝐃€𝐎𝐒 - ₹99", callback_data="p1")],
            [InlineKeyboardButton("🔥 €𝐏 𝐕!𝐃€𝐎𝐒 - ₹149", callback_data="p2")],
            [InlineKeyboardButton("📦 𝐀𝐋🇱 𝐈𝐍 𝐎𝐍𝐄 - ₹249", callback_data="p3")],
            [InlineKeyboardButton("👑 𝐕𝐈𝐏 𝐀𝐋🇱 - ₹499", callback_data="p4")],
            [InlineKeyboardButton("⬅️ 𝐁𝐀𝐂𝐊", callback_data="home")] # <-- Yahan se HTML hata diya jo bug kar raha tha
        ]
        await query.message.edit_media(
            media=InputMediaPhoto(media=PREMIUM_IMAGE, caption="<b>💎 𝐒𝐄𝐋𝐄𝐂𝐓 𝐘𝐎𝐔Ｒ 𝐏𝐋𝐀𝐍 💎</b>", parse_mode="HTML"), 
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    
    elif data == "home":
        # Ab back karne par ye caption bina cut hue poora wapas aayega
        await query.message.edit_media(
            media=InputMediaPhoto(media=START_IMAGE, caption=MAIN_CAPTION, parse_mode="HTML"), 
            reply_markup=home_buttons()
        )
        
    elif data in ["p1", "p2", "p3", "p4"]:
        amounts = {"p1": 99, "p2": 149, "p3": 249, "p4": 499}
        amount = amounts[data]
        order_id = f"ORDER_{uuid.uuid4().hex[:10].upper()}"
        
        link = create_paytm_order(order_id, amount, query.from_user.id)
        if not link:
            link = f"https://securegw-stage.paytm.in/theia/api/v1/showPaymentPage?mid={PAYTM_MID}&orderId={order_id}"
            
        keyboard = [
            [InlineKeyboardButton("💳 𝐏𝐀𝐘 𝐍𝐎𝐖", url=link)],
            [InlineKeyboardButton("🔄 𝐂𝐇𝐄𝐂𝐊 𝐒𝐓𝐀𝐓𝐔𝐒", callback_data=f"check_{order_id}")],
            [InlineKeyboardButton("⬅️ 𝐁𝐀𝐂𝐊", callback_data="premium")]
        ]
        await query.message.edit_media(
            media=InputMediaPhoto(media=PREMIUM_IMAGE, caption=f"<b>💸 𝐏𝐋𝐀𝐍: ₹{amount}</b>\n\nOrder ID: <code>{order_id}</code>", parse_mode="HTML"), 
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif data.startswith("check_"):
        order_id = data.replace("check_", "")
        status = check_paytm_status(order_id)
        if status == "TXN_SUCCESS" or status == "PENDING": 
            await query.message.edit_caption(caption="<b>🎉 PAYMENT VERIFIED SUCCESSFULLY!</b>", parse_mode="HTML", reply_markup=None)
        else:
            await context.bot.answer_callback_query(callback_query_id=query.id, text="❌ Payment abhi receive nahi hui.", show_alert=True)

# ==================================================
#                    RUN BOT
# ==================================================
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button_handler))

print("✅ BOT STARTED WITH FIXED BACK BUTTON CAPTION...")
app.run_polling()
