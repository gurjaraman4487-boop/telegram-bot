import uuid
import requests
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
#              CASHFREE CREDENTIALS (TEST/PROD)
# ==================================================
# Education purpose ke liye test credentials default hain. Production me change karein.
CASHFREE_APP_ID = "77152048f182445d66a3602069025177"
CASHFREE_SECRET_KEY = "cfsk_ma_prod_752eb9dd24a3cf3da7e74f9a90208af6_7e75a8b5"
CASHFREE_ENV = "PROD"  # PROD ke liye "PROD" likhein

CASHFREE_ENV = "PROD"
CASHFREE_URL = "https://api.cashfree.com/pg/orders"

# ==================================================
#                    IMAGES
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

# Active order IDs ko map karne ke liye { order_id: { user_id, amount } }
active_orders = {}

# ==================================================
#                 CASHFREE UTILS
# ==================================================
def create_cashfree_order(order_id: str, amount: float, user_id: int):
    """Cashfree PG API v3 ke rules ke hisab se order create karta hai"""
    headers = {
        "x-api-version": "2023-08-01",
        "x-client-id": CASHFREE_APP_ID,
        "x-client-secret": CASHFREE_SECRET_KEY,
        "Content-Type": "application/json"
    }
    
    payload = {
        "order_id": order_id,
        "order_amount": amount,
        "order_currency": "INR",
        "customer_details": {
            "customer_id": str(user_id),
            "customer_phone": "9999999999"  # Dummy for TG bot context
        },
        "order_meta": {
            # Webhook ya status check me return hone wala user tracking URL parameter
            "return_url": f"https://t.me/Pre_mmsbot?start=verify_{order_id}"
        }
    }
    
    try:
        response = requests.post(CASHFREE_URL, json=payload, headers=headers)
        if response.status_code == 200:
            return response.json().get("payment_link")
    except Exception as e:
        print(f"Error creating order: {e}")
    return None

def check_payment_status(order_id: str):
    """Cashfree API se order status cross-check karne ke liye"""
    headers = {
        "x-api-version": "2023-08-01",
        "x-client-id": CASHFREE_APP_ID,
        "x-client-secret": CASHFREE_SECRET_KEY,
        "Content-Type": "application/json"
    }
    try:
        response = requests.get(f"{CASHFREE_URL}/{order_id}", headers=headers)
        if response.status_code == 200:
            return response.json().get("order_status")  # PAID, ACTIVE, etc.
    except Exception as e:
        print(f"Error checking status: {e}")
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
#                    START / VERIFY
# ==================================================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    users.add(user_id)
    
    # Handle deep-linking checking payload (ex: /start verify_order123)
    args = context.args
    if args and args[0].startswith("verify_"):
        order_id = args[0].replace("verify_", "")
        status = check_payment_status(order_id)
        
        if status == "PAID":
            await update.message.reply_text(
                "<b>🎉 PAYMENT SUCCESSFUL!</b>\n\nAapka premium activation complete ho gaya hai. Join karne ke liye admin ko contact karein ya VIP links generate ho chuke hain.",
                parse_mode="HTML"
            )
            return
        elif status == "ACTIVE":
            await update.message.reply_text("⏳ Payment abhi tak complete nahi hui hai. Kripya payment poori karein.")
            return
        else:
            await update.message.reply_text("❌ Payment fail ho gayi ya invalid order ID hai.")
            return

    caption = (
        "<b>🔥 𝐏𝐑𝐄𝐌𝐈𝐔𝐌 𝐕𝐈𝐃𝐄𝐎 𝐂𝐎𝐋𝐋𝐄𝐂𝐓𝐈𝐎𝐍 🔥</b>\n\n"
        "<b>🎬 𝟓𝟎𝟎𝟎+ 𝐌𝐌𝐒 𝐕𝐈𝐃𝐄𝐎𝐒</b>\n\n"
        "<b>💋 𝟐𝟎𝟎𝟎+ 𝐂𝐎𝐔𝐏𝐋𝐄 𝐂𝐎𝐋𝐋𝐄𝐂𝐓𝐈𝐎𝐍</b>\n\n"
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
#                 PREMIUM MENU
# ==================================================
async def premium_menu(query):
    keyboard = [
        [InlineKeyboardButton("💎 𝐌𝐒 𝐕!𝐃€𝐎𝐒 - ₹99", callback_data="p1")],
        [InlineKeyboardButton("🔥 €𝐏 𝐕!𝐃€𝐎𝐒 - ₹149", callback_data="p2")],
        [InlineKeyboardButton("📦 𝐀𝐋𝐋 𝐈𝐍 𝐎𝐍𝐄 ( 𝟓𝟎 𝐆𝐑𝐎𝐔𝐏 ) - ₹249", callback_data="p3")],
        [InlineKeyboardButton("👑 𝐕𝐈𝐏 𝐀𝐋𝐋 ( 𝟏𝟎0𝐊+ 𝐕!𝐃€𝐎𝐒 ) - ₹499", callback_data="p4")],
        [InlineKeyboardButton("⬅️ 𝐁𝐀𝐂𝐊", callback_data="home")]
    ]

    await query.message.edit_media(
        media=InputMediaPhoto(
            media=PREMIUM_IMAGE,
            caption="<b>💎 𝐒𝐄𝐋𝐄𝐂𝐓 𝐘𝐎𝐔𝐑 𝐏𝐋𝐀𝐍 💎</b>",
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
#               DYNAMIC CASHFREE LIVE PAGE
# ==================================================

def create_cashfree_order(order_id: str, amount: float, user_id: int, user_name: str):
    """Cashfree PG LIVE API ke liye real user details ke sath link banata hai"""
    headers = {
        "x-api-version": "2023-08-01",
        "x-client-id": CASHFREE_APP_ID,
        "x-client-secret": CASHFREE_SECRET_KEY,
        "Content-Type": "application/json"
    }
    
    # Live me email format valid hona chahiye, isliye unique email generator lagaya hai
    clean_name = "".join(e for e in user_name if e.isalnum()) or "TelegramUser"
    user_email = f"{clean_name.lower()}_{user_id}@tgbot.com"
    
    payload = {
        "order_id": order_id,
        "order_amount": float(amount),
        "order_currency": "INR",
        "customer_details": {
            "customer_id": f"USER_{user_id}",
            "customer_phone": "9000000000", # Live API active validation number series format
            "customer_email": user_email
        },
        "order_meta": {
            "return_url": f"https://t.me/your_bot_username?start=verify_{order_id}" # <--- Yahan apne bot ka username likhein
        }
    }
    
    try:
        response = requests.post(CASHFREE_URL, json=payload, headers=headers)
        if response.status_code == 200:
            return response.json().get("payment_link")
        else:
            print(f"🔴 Cashfree Live Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Connection Error: {e}")
    return None

async def cashfree_pay_page(query, amount):
    user = query.from_user
    user_id = user.id
    user_name = user.first_name or "Customer"
    
    order_id = f"ORDER_{uuid.uuid4().hex[:10].upper()}"
    
    payment_link = create_cashfree_order(order_id, amount, user_id, user_name)
    
    if not payment_link:
        await query.message.reply_text("❌ Payment link generate nahi ho paya. Kripya thodi der baad try karein ya Live keys/account status check karein.")
        return

    active_orders[order_id] = {"user_id": user_id, "amount": amount}

    keyboard = [
        [InlineKeyboardButton("💳 𝐏𝐀𝐘 𝐍𝐎𝐖 (𝐔𝐏𝐈 / 𝐂𝐀𝐑𝐃)", url=payment_link)],
        [InlineKeyboardButton("🔄 𝐂𝐇𝐄𝐂𝐊 𝐒𝐓𝐀𝐓𝐔𝐒", callback_data=f"check_{order_id}")],
        [InlineKeyboardButton("⬅️ 𝐁𝐀𝐂𝐊", callback_data="back_to_plans")]
    ]

    await query.message.edit_media(
        media=InputMediaPhoto(
            media=PREMIUM_IMAGE,
            caption=(
                f"<b>💸 𝐏𝐋𝐀𝐍: ₹{amount}</b>\n\n"
                f"<b>🆔 Order ID:</b> <code>{order_id}</code>\n\n"
                f"👉 Niche diye gye link se payment safely secure kijiye. Pay karne ke baad <b>CHECK STATUS</b> button dabayein."
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
        f"💎 ₹99 Generated: {plan_99}\n"
        f"🔥 ₹149 Generated: {plan_149}\n"
        f"📦 ₹249 Generated: {plan_249}\n"
        f"👑 ₹499 Generated: {plan_499}"
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
        
    # Plan triggers
    elif data == "p1":
        plan_99 += 1
        await cashfree_pay_page(query, 99)
    elif data == "p2":
        plan_149 += 1
        await cashfree_pay_page(query, 149)
    elif data == "p3":
        plan_249 += 1
        await cashfree_pay_page(query, 249)
    elif data == "p4":
        plan_499 += 1
        await cashfree_pay_page(query, 499)
        
    # Manual status check handling from button
    elif data.startswith("check_"):
        order_id = data.replace("check_", "")
        status = check_payment_status(order_id)
        
        if status == "PAID":
            await query.message.edit_caption(
                caption="<b>🎉 PAYMENT VERIFIED SUCCESSFULLY!</b>\n\nAapko full group ka instant access diya jata hai. Any issue contact support.",
                parse_mode="HTML",
                reply_markup=None
            )
        else:
            # Alert context user standard query verification process
            await context.bot.answer_callback_query(
                callback_query_id=query.id,
                text="❌ Payment abhi tak receive nahi hui hai. Kripya process complete karein.",
                show_alert=True
            )

# ==================================================
#                    RUN BOT
# ==================================================
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("stats", stats))
app.add_handler(CallbackQueryHandler(button_handler))

print("✅ BOT IS RUNNING SUCCESSFULLY WITH CASHFREE INTEGRATION...")
app.run_polling()
