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

# ================= TOKEN =================
TOKEN = "8919459210:AAGWtjHwgUFETIABPIVTOrhB2dcgGFvMLBc"

# ================= IMAGES =================
START_IMAGE = "https://i.postimg.cc/MKWZn3Lv/IMG-20260521-163611-172.jpg"

PREMIUM_IMAGE = "https://i.postimg.cc/x89kTfHG/IMG-20260521-164434-789.jpg"

# ================= QR IMAGES =================
QR_99 = "https://i.postimg.cc/C5tMMsbG/Screenshot-20260521-231011.png"

QR_149 = "https://i.postimg.cc/DyXndsqs/Screenshot-20260521-231036.png"

QR_249 = "https://i.postimg.cc/2SdYgD9Q/Screenshot-20260521-231058.png"

QR_499 = "https://i.postimg.cc/MTH8cj6m/Screenshot-20260521-231113.png"

# ================= DELIVERY LINKS =================
LINK_99 = "https://t.me/bsbsjklalalala"

LINK_149 = "https://t.me/najskalalalal"

LINK_249 = "https://t.me/nakakalalal"

LINK_499 = "https://t.me/nwkskalal"

# ================= EXTRA LINKS =================
DEMO_CHANNEL = "https://t.me/demochannlink"

INFO_CHANNEL = "https://t.me/howtogetpre"


# ================= START BUTTONS =================
def start_keyboard():

    return InlineKeyboardMarkup([
        [InlineKeyboardButton("💎 Get Premium", callback_data="premium")],

        [InlineKeyboardButton("🎬 Demo Videos", url=DEMO_CHANNEL)],

        [InlineKeyboardButton("📖 How To Get Premium", url=INFO_CHANNEL)],
    ])


# ================= START =================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    caption = (
        "<b>🎬 Available Videos Collection</b>\n\n"

        "<b>➊ MOM Son Videos - 5000+</b>\n\n"

        "<b>➋ Sister Brother Videos - 2000+</b>\n\n"

        "<b>➌ Premium Videos - 15000+</b>\n\n"

        "<b>➍ Teen Collection - 6000+</b>\n\n"

        "<b>➎ Indian Desi Collection - 10000+</b>\n\n"

        "<b>➏ Hidden Style Videos - 2000+</b>"
    )

    await update.message.reply_photo(
        photo=START_IMAGE,
        caption=caption,
        parse_mode="HTML",
        reply_markup=start_keyboard()
    )


# ================= PREMIUM MENU =================
async def premium(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    await query.answer()

    keyboard = InlineKeyboardMarkup([

        [InlineKeyboardButton("👉 MMS Videos - ₹99", callback_data="p1")],

        [InlineKeyboardButton("👉 REP Videos - ₹149", callback_data="p2")],

        [InlineKeyboardButton("👉 ALL IN ONE - ₹249", callback_data="p3")],

        [InlineKeyboardButton("👉 VIP ALL - ₹499", callback_data="p4")],

        [InlineKeyboardButton("⬅ Back", callback_data="home")]
    ])

    await query.message.edit_media(
        media=InputMediaPhoto(
            media=PREMIUM_IMAGE,
            caption="<b>💎 Select Your Plan Below 👇</b>",
            parse_mode="HTML"
        ),
        reply_markup=keyboard
    )


# ================= HOME =================
async def home(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    await query.answer()

    caption = (
        "<b>🎬 Available Videos Collection</b>\n\n"

        "<b>➊ MOM Son Videos - 5000+</b>\n\n"

        "<b>➋ Sister Brother Videos - 2000+</b>\n\n"

        "<b>➌ Premium Videos - 15000+</b>\n\n"

        "<b>➍ Teen Collection - 6000+</b>\n\n"

        "<b>➎ Indian Desi Collection - 10000+</b>\n\n"

        "<b>➏ Hidden Style Videos - 2000+</b>"
    )

    await query.message.edit_media(
        media=InputMediaPhoto(
            media=START_IMAGE,
            caption=caption,
            parse_mode="HTML"
        ),
        reply_markup=start_keyboard()
    )


# ================= QR MENU =================
async def show_qr(query, qr_image, amount, delivery_link):

    keyboard = InlineKeyboardMarkup([

        [InlineKeyboardButton("✅ I Have Paid", url=delivery_link)],

        [InlineKeyboardButton("⬅ Back", callback_data="premium")]
    ])

    await query.message.edit_media(
        media=InputMediaPhoto(
            media=qr_image,
            caption=f"💸 Scan QR To Pay ₹{amount}",
        ),
        reply_markup=keyboard
    )


# ================= BUTTON HANDLER =================
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    await query.answer()

    data = query.data

    # PREMIUM PAGE
    if data == "premium":

        await premium(update, context)

    # HOME PAGE
    elif data == "home":

        await home(update, context)

    # ₹99
    elif data == "p1":

        await show_qr(query, QR_99, 99, LINK_99)

    # ₹149
    elif data == "p2":

        await show_qr(query, QR_149, 149, LINK_149)

    # ₹249
    elif data == "p3":

        await show_qr(query, QR_249, 249, LINK_249)

    # ₹499
    elif data == "p4":

        await show_qr(query, QR_499, 499, LINK_499)


# ================= RUN =================
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))

app.add_handler(CallbackQueryHandler(button_handler))

print("Bot is running...")

app.run_polling()
