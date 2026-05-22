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
#                  ADMIN ID
# ==================================================

# Apna Telegram numeric ID yaha dalo
ADMIN_ID = 6648941928

# ==================================================
#                    MAIN IMAGES
# ==================================================

START_IMAGE = "https://i.postimg.cc/MKWZn3Lv/IMG-20260521-163611-172.jpg"

PREMIUM_IMAGE = "https://i.postimg.cc/x89kTfHG/IMG-20260521-164434-789.jpg"

# ==================================================
#                    QR IMAGES
# ==================================================

QR_99 = "https://i.postimg.cc/C5tMMsbG/Screenshot-20260521-231011.png"

QR_149 = "https://i.postimg.cc/DyXndsqs/Screenshot-20260521-231036.png"

QR_249 = "https://i.postimg.cc/2SdYgD9Q/Screenshot-20260521-231058.png"

QR_499 = "https://i.postimg.cc/MTH8cj6m/Screenshot-20260521-231113.png"

# ==================================================
#                  ADMIN USERNAME
# ==================================================

ADMIN_USERNAME = "https://t.me/dealer_x"

# ==================================================
#                    LINKS
# ==================================================

DEMO_CHANNEL = "https://t.me/demochannlink"

INFO_CHANNEL = "https://t.me/howtogetpre"

# ==================================================
#                    STATS
# ==================================================

users = set()

plan_99 = 0
plan_149 = 0
plan_249 = 0
plan_499 = 0

# ==================================================
#                 HOME BUTTONS
# ==================================================

def home_buttons():

    keyboard = [

        [
            InlineKeyboardButton(
                "💎 𝐆𝐄𝐓 𝐏𝐑𝐄𝐌𝐈𝐔𝐌 💎",
                callback_data="premium"
            )
        ],

        [
            InlineKeyboardButton(
                "🎬 𝐃𝐄𝐌𝐎 𝐕𝐈𝐃𝐄𝐎𝐒",
                url=DEMO_CHANNEL
            )
        ],

        [
            InlineKeyboardButton(
                "📖 𝐇𝐎𝐖 𝐓𝐎 𝐆𝐄𝐓 𝐏𝐑𝐄𝐌𝐈𝐔𝐌",
                url=INFO_CHANNEL
            )
        ]
    ]

    return InlineKeyboardMarkup(keyboard)

# ==================================================
#                    START
# ==================================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    users.add(update.effective_user.id)

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

        [
            InlineKeyboardButton(
                "💎 𝐌𝐒 𝐕!𝐃€𝐎𝐒 - ₹99",
                callback_data="p1"
            )
        ],

        [
            InlineKeyboardButton(
                "🔥 €𝐏 𝐕!𝐃€𝐎𝐒 - ₹149",
                callback_data="p2"
            )
        ],

        [
            InlineKeyboardButton(
                "📦 𝐀𝐋𝐋 𝐈𝐍 𝐎𝐍𝐄 ( 𝟓𝟎 𝐆𝐑𝐎𝐔𝐏 ) - ₹249",
                callback_data="p3"
            )
        ],

        [
            InlineKeyboardButton(
                "👑 𝐕𝐈𝐏 𝐀𝐋𝐋 ( 𝟏𝟎𝟎𝐊+ 𝐕!𝐃€𝐎𝐒 ) - ₹499",
                callback_data="p4"
            )
        ],

        [
            InlineKeyboardButton(
                "⬅️ 𝐁𝐀𝐂𝐊",
                callback_data="home"
            )
        ]
    ]

    await query.message.edit_media(
        media=InputMediaPhoto(
            media=PREMIUM_IMAGE,
            caption=(
                "<b>💎 𝐒𝐄𝐋𝐄𝐂𝐓 𝐘𝐎𝐔𝐑 𝐏𝐋𝐀𝐍 💎</b>"
            ),
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
#                    QR PAGE
# ==================================================

async def qr_page(query, qr_image, amount):

    keyboard = [

        [
            InlineKeyboardButton(
                "✅ 𝐈 𝐇𝐀𝐕𝐄 𝐏𝐀𝐈𝐃",
                callback_data="send_ss"
            )
        ],

        [
            InlineKeyboardButton(
                "⬅️ 𝐁𝐀𝐂𝐊",
                callback_data="back_to_plans"
            )
        ]
    ]

    await query.message.edit_media(
        media=InputMediaPhoto(
            media=qr_image,
            caption=(
                f"<b>💸 𝐒𝐂𝐀𝐍 𝐓𝐎 𝐏𝐀𝐘 ₹{amount}</b>"
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

        f"💎 ₹99 Clicks: {plan_99}\n"
        f"🔥 ₹149 Clicks: {plan_149}\n"
        f"📦 ₹249 Clicks: {plan_249}\n"
        f"👑 ₹499 Clicks: {plan_499}"
    )

    await update.message.reply_text(
        text,
        parse_mode="HTML"
    )

# ==================================================
#                 BUTTON HANDLER
# ==================================================

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    global plan_99
    global plan_149
    global plan_249
    global plan_499

    query = update.callback_query

    await query.answer()

    data = query.data

    # PREMIUM MENU
    if data == "premium":

        await premium_menu(query)

    # HOME
    elif data == "home":

        await home_page(query)

    # BACK
    elif data == "back_to_plans":

        await premium_menu(query)

    # ₹99
    elif data == "p1":

        plan_99 += 1

        await qr_page(query, QR_99, 99)

    # ₹149
    elif data == "p2":

        plan_149 += 1

        await qr_page(query, QR_149, 149)

    # ₹249
    elif data == "p3":

        plan_249 += 1

        await qr_page(query, QR_249, 249)

    # ₹499
    elif data == "p4":

        plan_499 += 1

        await qr_page(query, QR_499, 499)

    # SEND SCREENSHOT
    elif data == "send_ss":

        await query.message.edit_caption(
            caption=(
                "<b>✅ PAYMENT VERIFICATION</b>\n\n"

                "<b>📸 SEND PAYMENT SCREENSHOT TO ADMIN</b>\n\n"

                "<b>⚡ AFTER VERIFY YOU WILL GET ACCESS</b>"
            ),
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        "📩 SEND SCREENSHOT",
                        url=ADMIN_USERNAME
                    )
                ]
            ])
        )

# ==================================================
#                    RUN BOT
# ==================================================

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(
    CommandHandler("start", start)
)

app.add_handler(
    CommandHandler("stats", stats)
)

app.add_handler(
    CallbackQueryHandler(button_handler)
)

print("✅ BOT IS RUNNING SUCCESSFULLY...")

app.run_polling()
