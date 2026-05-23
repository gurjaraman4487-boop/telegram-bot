import uuid
import json
import requests
import paytmchecksum  # <-- Check karo ab ekdam sahi hai: p-a-y-t-m-c-h-e-c-k-s-u-m
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
#             PAYTM TEST CREDENTIALS & URL
# ==================================================
# ⚠️ Yahan apni test details dalo jo dashboard se mili hain
PAYTM_MID = "wJwasY46108610523084"
PAYTM_MERCHANT_KEY = "RKmwIgkAcKb5bu41"
PAYTM_WEBSITE = "WEBSTAGING"  # Test mode ke liye ye fix rahega

# Test Endpoints (Yahan humne url me "-stage" joda hai)
PAYTM_URL_INITIATE = f"https://securegw-stage.paytm.in/theia/api/v1/initiateTransaction?mid={PAYTM_MID}&orderId="
PAYTM_URL_STATUS = f"https://securegw-stage.paytm.in/v3/order/status"
# ==================================================
#                    BOT USERNAME
# ==================================================
BOT_USERNAME = "https://t.me/Pre_mmsbot"  # Bina @ ke likhein

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

# ==================================================
#                    STATS & ACTIVE ORDERS
# ==================================================
users = set()
plan_99 = 0
plan_149 = 0
plan_249 = 0
plan_499 = 0

active_orders = {}

# ==================================================
#                 PAYTM UTILS
# ==================================================
def create_paytm_order(order_id: str, amount: float, user_id: int):
    """Paytm API se secure checkout link generate karta hai"""
    paytm_params = {
        "body": {
            "requestType": "Payment",
            "mid": PAYTM_MID,
            "websiteName": PAYTM_WEBSITE,
            "orderId": order_id,
            # Pehle ye securegw.paytm.in tha, isme securegw ke aage "-stage" lagana hai:
"callbackUrl": f"https://securegw-stage.paytm.in/theia/paytmCallback?ORDER_ID={order_id}",
            "txnAmount": {
                "value": f"{amount:.2f}",
                "currency": "INR",
            },
            "userInfo": {
                "custId": f"USER_{user_id}",
            },
        }
    }

    try:
        # Checksum signature generate karna security ke liye mandatory hai
        checksum = paytmchecksum.generateSignature(json.dumps(paytm_params["body"]), PAYTM_MERCHANT_KEY)
        paytm_params["head"] = {"signature": checksum}

        response = requests.post(PAYTM_URL_INITIATE + order_id, json=paytm_params)
        res_data = response.json()
        
        if res_data.get("body", {}).get("resultInfo", {}).get("resultStatus") == "S":
            txn_token = res_data["body"]["txnToken"]
            # Ye user ko seedhe Paytm ke payment page par bhejega jahan UPI/Netbanking dikhega
            pay_link = f"https://securegw.paytm.in/theia/api/v1/showPaymentPage?mid={PAYTM_MID}&orderId={order_id}&txnToken={txn_token}"
            return pay_link
        else:
            print(f"🔴 Paytm Link Error: {res_data}")
    except Exception as e:
        print(f"❌ Paytm Connection Error: {e}")
    return None

def check_paytm_status(order_id: str):
    """User ke 'Check Status' dabane par payment verify karta hai"""
    paytm_params = {
        "body": {
            "mid": PAYTM_MID,
            "orderId": order_id
        }
    }

    try:
        checksum = paytmchecksum.generateSignature(json.dumps(paytm_params["body"]), PAYTM_MERCHANT_KEY)
        paytm_params["head"] = {"signature": checksum}

        response = requests.post(PAYTM_URL_STATUS, json=paytm_params)
        res_data = response.json()
        status = res_data.get("body", {}).get("resultInfo", {}).get("resultStatus")
        return status  # Returns: "TXN_SUCCESS", "TXN_FAILURE", "PENDING"
    except Exception as e:
        print(f"Error checking Paytm status: {e}")
    return "ERROR"

# ==================================================
#                 HOME BUTTONS
# ==================================================
def home_buttons():
    keyboard = [
        [InlineKeyboardButton("💎 𝐆𝐄𝐓 𝐏𝐑𝐄𝐌𝐈𝐔𝐌 💎", callback_data="premium")],
        [InlineKeyboardButton("🎬 𝐃𝐄𝐌𝐎 𝐕𝐈𝐃𝐄𝐎𝐒", url=DEMO_CHANNEL)],
        [InlineKeyboardButton("📖 𝐇𝐎𝐖 𝐓𝐎 𝐆𝐄𝐓 𝐏𝐑𝐄𝐌𝐈𝐔𝐌", url=INFO_CHANNEL)]
    ]
    return InlineKeyboardMarkup(keyboard)

# ==================================================
#                    START COMMAND
# ==================================================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    users.add(user_id)
    
    caption = (
        "<b>🔥 𝐏𝐑𝐄𝐌𝐈𝐔𝐌 𝐕𝐈𝐃𝐄𝐎 𝐂𝐎𝐋𝐋𝐄𝐂𝐓𝐈𝐎𝐍 🔥</b>\n\n"
        "<b>🎬 𝟓𝟎𝟎𝟎+ 𝐌𝐌𝐒 𝐕𝐈𝐃𝐄𝐎𝐒</b>\n\n"
        "<b>💋 𝟐𝟎0𝟎+ 𝐂𝐎𝐔𝐏𝐋𝐄 𝐂𝐎𝐋𝐋𝐄𝐂𝐓𝐈𝐎𝐍</b>\n\n"
        "<b>🔥 𝟏𝟓𝟎𝟎𝟎+ 𝐏𝐑𝐄𝐌𝐈𝐔𝐌 𝐕𝐈𝐃𝐄𝐎𝐒</b>\n\n"
        "<b>📦 𝟏𝟎𝟎+ 𝐕𝐈𝐏 𝐂𝐎𝐋𝐋𝐄𝐂𝐓𝐈𝐎𝐍𝐒</b>\n\n"
        "<b>⚡ 𝐈𝐍𝐒𝐓𝐀𝐍𝐓 𝐀𝐂𝐂𝐄𝐒𝐒</b>"
    )

    await update.message.reply_photo(
        photo=START_IMAGE,
        caption=caption,
        parse_mode="HTML",
        reply_markup=home_buttons()
    )

# ==================================================
#                 PREMIUM PLAN MENU
# ==================================================
async def premium_menu(query):
    keyboard = [
        [InlineKeyboardButton("💎 𝐌𝐒 𝐕!𝐃€𝐎𝐒 - ₹99", callback_data="p1")],
        [InlineKeyboardButton("🔥 €𝐏 𝐕!𝐃€𝐎𝐒 - ₹149", callback_data="p2")],
        [InlineKeyboardButton("📦 𝐀𝐋𝐋 𝐈𝐍 𝐎𝐍𝐄 ( 𝟓𝟎 𝐆𝐑𝐎𝐔𝐏 ) - ₹249", callback_data="p3")],
        [InlineKeyboardButton("👑 𝐕𝐈𝐏 𝐀𝐋𝐋 ( 𝟏𝟎𝟎𝐊+ 𝐕!𝐃€𝐎𝐒 ) - ₹499", callback_data="p4")],
        [InlineKeyboardButton("⬅️ 𝐁𝐀𝐂𝐊", callback_data="home")]
    ]

    await query.message.edit_media(
        media=InputMediaPhoto(
            media=PREMIUM_IMAGE,
            caption="<b>💎 𝐒𝐄𝐋𝐄𝐂𝐓 𝐘𝐎𝐔Ｒ 𝐏𝐋𝐀𝐍 💎</b>",
            parse_mode="HTML"
        ),
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# ==================================================
#                    HOME PAGE
# ==================================================
async def home_page(query):
    caption = (
        "<b>🔥 𝐏𝐑𝐄𝐌𝐈𝐔𝐌 𝐕𝐈𝐃𝐄𝐎 𝐂𝐎𝐋𝐋𝐄𝐂𝐓𝐈𝐎𝐍 🔥</b>\n\n"
        "<b>🎬 𝟓𝟎𝟎𝟎+ 𝐌𝐌𝐒 𝐕𝐈𝐃𝐄𝐎𝐒</b>\n\n"
        "<b>💋 𝟐𝟎𝟎𝟎+ 𝐂𝐎𝐔𝐏𝐋𝐄 𝐂𝐎𝐋𝐋𝐄𝐂𝐓𝐈𝐎𝐍</b>\n\n"
        "<b>🔥 𝟏𝟓𝟎𝟎𝟎+ 𝐏𝐑𝐄𝐌𝐈𝐔𝐌 𝐕𝐈𝐃𝐄𝐎𝐒</b>\n\n"
        "<b>📦 𝟏𝟎𝟎+ 𝐕𝐈𝐏 𝐂𝐎𝐋𝐋𝐄𝐂𝐓𝐈𝐎𝐍𝐒</b>\n\n"
        "<b>⚡ 𝐈𝐍𝐒𝐓𝐀𝐍𝐓 𝐀𝐂𝐂𝐄𝐒𝐒</b>\n\n"
        "<b>👇 𝐂𝐋𝐈𝐂𝐊 𝐁𝐄𝐋𝐎𝐖 👇</b>"
    )

    await query.message.edit_media(
        media=InputMediaPhoto(
            media=START_IMAGE,
            caption=caption,
            parse_mode="HTML"
        ),
        reply_markup=home_buttons()
    )

# ==================================================
#               PAYTM LINK GENERATION PAGE
# ==================================================
async def paytm_pay_page(query, amount):
    user_id = query.from_user.id
    order_id = f"ORDER_{uuid.uuid4().hex[:10].upper()}"
    
    # Paytm link banayein
    payment_link = create_paytm_order(order_id, amount, user_id)
    
    if not payment_link:
        await query.message.reply_text(
            "❌ Paytm payment link generate nahi ho paya.\n"
            "Kripya check karein ki aapki Merchant Keys sahi hain aur account active hai."
        )
        return

    active_orders[order_id] = {"user_id": user_id, "amount": amount}

    keyboard = [
        [InlineKeyboardButton("💳 𝐏𝐀𝐘 𝐍𝐎𝐖 (𝐏𝐀Y𝐓𝐌 / 𝐔𝐏𝐈)", url=payment_link)],
        [InlineKeyboardButton("🔄 𝐂𝐇𝐄𝐂𝐊 𝐒𝐓𝐀𝐓𝐔𝐒", callback_data=f"check_{order_id}")],
        [InlineKeyboardButton("⬅️ 𝐁𝐀𝐂𝐊", callback_data="back_to_plans")]
    ]

    await query.message.edit_media(
        media=InputMediaPhoto(
            media=PREMIUM_IMAGE,
            caption=(
                f"<b>💸 𝐏𝐋𝐀𝐍: ₹{amount}</b>\n\n"
                f"<b>🆔 Order ID:</b> <code>{order_id}</code>\n\n"
                f"👉 <b>PAY NOW</b> par click karke kisi bhi UPI app ya Paytm se safe payment karein.\n\n"
                f"Payment complete karne ke baad niche <b>CHECK STATUS</b> par click karein."
            ),
            parse_mode="HTML"
        ),
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# ==================================================
#                    STATS COMMAND
# ==================================================
async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    text = (
        f"📊 <b>BOT STATS</b>\n\n"
        f"👥 Total Users: {len(users)}\n\n"
        f"💎 ₹99 Plan: {plan_99} clicks\n"
        f"🔥 ₹149 Plan: {plan_149} clicks\n"
        f"📦 ₹249 Plan: {plan_249} clicks\n"
        f"👑 ₹499 Plan: {plan_499} clicks"
    )
    await update.message.reply_text(text, parse_mode="HTML")

# ==================================================
#                 BUTTON HANDLER
# ==================================================
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global plan_99, plan_149, plan_249, plan_499

    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "premium":
        await premium_menu(query)
    elif data == "home":
        await home_page(query)
    elif data == "back_to_plans":
        await premium_menu(query)
        
    elif data == "p1":
        plan_99 += 1
        await paytm_pay_page(query, 99)
    elif data == "p2":
        plan_149 += 1
        await paytm_pay_page(query, 149)
    elif data == "p3":
        plan_249 += 1
        await paytm_pay_page(query, 249)
    elif data == "p4":
        plan_499 += 1
        await paytm_pay_page(query, 499)
        
    elif data.startswith("check_"):
        order_id = data.replace("check_", "")
        status = check_paytm_status(order_id)
        
        if status == "TXN_SUCCESS":
            # Yahan payment verify ho chuki hai
            await query.message.edit_caption(
                caption="<b>🎉 PAYMENT VERIFIED SUCCESSFULLY!</b>\n\nAapka premium access active kar diya gaya hai. Join karne ke liye niche click karein.",
                parse_mode="HTML",
                reply_markup=None  # Aap chahein toh yahan apna channel join link button de sakte hain
            )
        elif status == "PENDING":
            await context.bot.answer_callback_query(
                callback_query_id=query.id,
                text="⏳ Payment abhi pending hai. Kripya process complete karke 10-15 seconds baad dobara check karein.",
                show_alert=True
            )
        else:
            await context.bot.answer_callback_query(
                callback_query_id=query.id,
                text="❌ Payment receive nahi hui ya transaction fail ho gaya hai.",
                show_alert=True
            )

# ==================================================
#                    RUN BOT
# ==================================================
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("stats", stats))
app.add_handler(CallbackQueryHandler(button_handler))

print("✅ BOT IS RUNNING SUCCESSFULLY WITH PAYTM GATEWAY INTEGRATION...")
app.run_polling()
