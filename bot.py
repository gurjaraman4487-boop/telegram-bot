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
QR_99 = "https://your-99-qr-image-link.png"
QR_149 = "https://your-149-qr-image-link.png"
QR_249 = "https://your-249-qr-image-link.png"
QR_499 = "https://your-499-qr-image-link.png"

# ================= LINKS =================
DEMO_CHANNEL = "https://t.me/demochannlink"
INFO_CHANNEL = "https://t.me/howtogetpre"


# ================= START KEYBOARD =================
def start_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("💎 Get Premium", callback_data="premium")],
        [InlineKeyboardButton("🎬 Demo Videos", url=DEMO_CHANNEL)],
        [InlineKeyboardButton("📖 How To Get Premium", url=INFO_CHANNEL)],
    ])


# ================= START =================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    caption = (
        "<b>🎬 𝐀𝐯𝐚𝐢𝐥𝐚𝐛𝐥𝐞 𝐕𝐢𝐝𝐞𝐨𝐬 𝐂𝐨𝐥𝐥𝐞𝐜𝐭𝐢𝐨𝐧</b>\n\n"

        "<b>➊ 𝐌𝐎𝐌 𝐒𝐨𝐧 𝐕𝐢𝐝𝐞𝐨𝐬 - 𝟓𝟎𝟎𝟎+</b>\n\n"

        "<b>➋ 𝐒𝐢𝐬𝐭𝐞𝐫 𝐁𝐫𝐨𝐭𝐡𝐞𝐫 𝐕𝐢𝐝𝐞𝐨𝐬 - 𝟐𝟎𝟎𝟎+</b>\n\n"

        "<b>➌ 𝐏𝐫𝐞𝐦𝐢𝐮𝐦 𝐕𝐢𝐝𝐞𝐨𝐬 - 𝟏𝟓𝟎𝟎𝟎+</b>\n\n"

        "<b>➍ 𝐓𝐞𝐞𝐧 𝐂𝐨𝐥𝐥𝐞𝐜𝐭𝐢𝐨𝐧 - 𝟔𝟎𝟎𝟎+</b>\n\n"

        "<b>➎ 𝐈𝐧𝐝𝐢𝐚𝐧 𝐃𝐞𝐬𝐢 𝐂𝐨𝐥𝐥𝐞𝐜𝐭𝐢𝐨𝐧 - 𝟏𝟎𝟎𝟎𝟎+</b>\n\n"

        "<b>➏ 𝐇𝐢𝐝𝐝𝐞𝐧 𝐒𝐭𝐲𝐥𝐞 𝐕𝐢𝐝𝐞𝐨𝐬 - 𝟐𝟎𝟎𝟎+</b>"
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

        [InlineKeyboardButton("👉 MS VID€OS - ₹99", callback_data="p1")],

        [InlineKeyboardButton("👉 R€P VID€OS - ₹149", callback_data="p2")],

        [InlineKeyboardButton("👉 ALL ¡N ONE (50 GROUP) - ₹249", callback_data="p3")],

        [InlineKeyboardButton("👉 VIP ALL (100K+ VID€OS) - ₹499", callback_data="p4")],

        [InlineKeyboardButton("⬅ Back", callback_data="back")]
    ])

    await query.message.edit_media(
        media=InputMediaPhoto(
            media=PREMIUM_IMAGE,
            caption="<b>💎 𝐒𝐞𝐥𝐞𝐜𝐭 𝐘𝐨𝐮𝐫 𝐏𝐥𝐚𝐧 𝐁𝐞𝐥𝐨𝐰 👇</b>",
            parse_mode="HTML"
        ),
        reply_markup=keyboard
    )


# ================= BACK =================
async def back(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    caption = (
        "<b>🎬 𝐀𝐯𝐚𝐢𝐥𝐚𝐛𝐥𝐞 𝐕𝐢𝐝𝐞𝐨𝐬 𝐂𝐨𝐥𝐥𝐞𝐜𝐭𝐢𝐨𝐧</b>\n\n"

        "<b>➊ 𝐌𝐎𝐌 𝐒𝐨𝐧 𝐕𝐢𝐝𝐞𝐨𝐬 - 𝟓𝟎𝟎𝟎+</b>\n\n"

        "<b>➋ 𝐒𝐢𝐬𝐭𝐞𝐫 𝐁𝐫𝐨𝐭𝐡𝐞𝐫 𝐕𝐢𝐝𝐞𝐨𝐬 - 𝟐𝟎𝟎𝟎+</b>\n\n"

        "<b>➌ 𝐏𝐫𝐞𝐦𝐢𝐮𝐦 𝐕𝐢𝐝𝐞𝐨𝐬 - 𝟏𝟓𝟎𝟎𝟎+</b>\n\n"

        "<b>➍ 𝐓𝐞𝐞𝐧 𝐂𝐨𝐥𝐥𝐞𝐜𝐭𝐢𝐨𝐧 - 𝟔𝟎𝟎𝟎+</b>\n\n"

        "<b>➎ 𝐈𝐧𝐝𝐢𝐚𝐧 𝐃𝐞𝐬𝐢 𝐂𝐨𝐥𝐥𝐞𝐜𝐭𝐢𝐨𝐧 - 𝟏𝟎𝟎𝟎𝟎+</b>\n\n"

        "<b>➏ 𝐇𝐢𝐝𝐝𝐞𝐧 𝐒𝐭𝐲𝐥𝐞 𝐕𝐢𝐝𝐞𝐨𝐬 - 𝟐𝟎𝟎𝟎+</b>"
    )

    await query.message.edit_media(
        media=InputMediaPhoto(
            media=START_IMAGE,
            caption=caption,
            parse_mode="HTML"
        ),
        reply_markup=start_keyboard()
    )


# ================= BUTTON HANDLER =================
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    data = query.data

    if data == "premium":

        await premium(update, context)

    elif data == "back":

        await back(update, context)

    elif data == "p1":

        await query.message.reply_photo(
            photo=QR_99,
            caption="💸 Scan QR To Pay ₹99"
        )

    elif data == "p2":

        await query.message.reply_photo(
            photo=QR_149,
            caption="💸 Scan QR To Pay ₹149"
        )

    elif data == "p3":

        await query.message.reply_photo(
            photo=QR_249,
            caption="💸 Scan QR To Pay ₹249"
        )

    elif data == "p4":

        await query.message.reply_photo(
            photo=QR_499,
            caption="💸 Scan QR To Pay ₹499"
        )


# ================= RUN =================
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button_handler))

print("Bot is running...")

app.run_polling()
