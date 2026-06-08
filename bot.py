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
                "ðŸ’Ž ð†ð„ð“ ðð‘ð„ðŒðˆð”ðŒ ðŸ’Ž",
                callback_data="premium"
            )
        ],

        [
            InlineKeyboardButton(
                "ðŸŽ¬ ðƒð„ðŒðŽ ð•ðˆðƒð„ðŽð’",
                url=DEMO_CHANNEL
            )
        ],

        [
            InlineKeyboardButton(
                "ðŸ“– ð‡ðŽð– ð“ðŽ ð†ð„ð“ ðð‘ð„ðŒðˆð”ðŒ",
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
        "<b>ðŸ”¥ ðð‘ð„ðŒðˆð”ðŒ ð•ðˆðƒð„ðŽ ð‚ðŽð‹ð‹ð„ð‚ð“ðˆðŽð ðŸ”¥</b>\n\n"

        "<b>ðŸŽ¬ ðŸ“ðŸŽðŸŽðŸŽ+ ðŒðŒð’ ð•ðˆðƒð„ðŽð’</b>\n\n"

        "<b>ðŸ’‹ ðŸðŸŽðŸŽðŸŽ+ ð‚ðŽð”ðð‹ð„ ð‚ðŽð‹ð‹ð„ð‚ð“ðˆðŽð</b>\n\n"

        "<b>ðŸ”¥ ðŸðŸ“ðŸŽðŸŽðŸŽ+ ðð‘ð„ðŒðˆð”ðŒ ð•ðˆðƒð„ðŽð’</b>\n\n"

        "<b>ðŸ“¦ ðŸðŸŽðŸŽ+ ð•ðˆð ð‚ðŽð‹ð‹ð„ð‚ð“ðˆðŽðð’</b>\n\n"

        "<b>âš¡ ðˆðð’ð“ð€ðð“ ð€ð‚ð‚ð„ð’ð’</b>"
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
                "ðŸ’Ž ðŒð’ ð•!ðƒâ‚¬ðŽð’ - â‚¹99",
                callback_data="p1"
            )
        ],

        [
            InlineKeyboardButton(
                "ðŸ”¥ ð‘â‚¬ð ð•!ðƒâ‚¬ðŽð’ - â‚¹149",
                callback_data="p2"
            )
        ],

        [
            InlineKeyboardButton(
                "ðŸ“¦ ð€ð‹ð‹ ðˆð ðŽðð„ ( ðŸ“ðŸŽ ð†ð‘ðŽð”ð ) - â‚¹249",
                callback_data="p3"
            )
        ],

        [
            InlineKeyboardButton(
                "ðŸ‘‘ ð•ðˆð ð€ð‹ð‹ ( ðŸðŸŽðŸŽðŠ+ ð•!ðƒâ‚¬ðŽð’ ) - â‚¹499",
                callback_data="p4"
            )
        ],

        [
            InlineKeyboardButton(
                "â¬…ï¸ ðð€ð‚ðŠ",
                callback_data="home"
            )
        ]
    ]

    await query.message.edit_media(
        media=InputMediaPhoto(
            media=PREMIUM_IMAGE,
            caption=(
                "<b>ðŸ’Ž ð’ð„ð‹ð„ð‚ð“ ð˜ðŽð”ð‘ ðð‹ð€ð ðŸ’Ž</b>"
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
        "<b>ðŸ”¥ ðð‘ð„ðŒðˆð”ðŒ ð•ðˆðƒð„ðŽ ð‚ðŽð‹ð‹ð„ð‚ð“ðˆðŽð ðŸ”¥</b>\n\n"

        "<b>ðŸŽ¬ ðŸ“ðŸŽðŸŽðŸŽ+ ðŒðŒð’ ð•ðˆðƒð„ðŽð’</b>\n\n"

        "<b>ðŸ’‹ ðŸðŸŽðŸŽðŸŽ+ ð‚ðŽð”ðð‹ð„ ð‚ðŽð‹ð‹ð„ð‚ð“ðˆðŽð</b>\n\n"

        "<b>ðŸ”¥ ðŸðŸ“ðŸŽðŸŽðŸŽ+ ðð‘ð„ðŒðˆð”ðŒ ð•ðˆðƒð„ðŽð’</b>\n\n"

        "<b>ðŸ“¦ ðŸðŸŽðŸŽ+ ð•ðˆð ð‚ðŽð‹ð‹ð„ð‚ð“ðˆðŽðð’</b>\n\n"

        "<b>âš¡ ðˆðð’ð“ð€ðð“ ð€ð‚ð‚ð„ð’ð’</b>\n\n"

        "<b>ðŸ‘‡ ð‚ð‹ðˆð‚ðŠ ðð„ð‹ðŽð– ðŸ‘‡</b>"
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
                "âœ… ðˆ ð‡ð€ð•ð„ ðð€ðˆðƒ",
                callback_data="send_ss"
            )
        ],

        [
            InlineKeyboardButton(
                "â¬…ï¸ ðð€ð‚ðŠ",
                callback_data="back_to_plans"
            )
        ]
    ]

    await query.message.edit_media(
        media=InputMediaPhoto(
            media=qr_image,
            caption=(
                f"<b>ðŸ’¸ ð’ð‚ð€ð ð“ðŽ ðð€ð˜ â‚¹{amount}</b>"
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
        f"ðŸ“Š <b>BOT STATS</b>\n\n"

        f"ðŸ‘¥ Total Users: {len(users)}\n\n"

        f"ðŸ’Ž â‚¹99 Clicks: {plan_99}\n"
        f"ðŸ”¥ â‚¹149 Clicks: {plan_149}\n"
        f"ðŸ“¦ â‚¹249 Clicks: {plan_249}\n"
        f"ðŸ‘‘ â‚¹499 Clicks: {plan_499}"
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

    # â‚¹99
    elif data == "p1":

        plan_99 += 1

        await qr_page(query, QR_99, 99)

    # â‚¹149
    elif data == "p2":

        plan_149 += 1

        await qr_page(query, QR_149, 149)

    # â‚¹249
    elif data == "p3":

        plan_249 += 1

        await qr_page(query, QR_249, 249)

    # â‚¹499
    elif data == "p4":

        plan_499 += 1

        await qr_page(query, QR_499, 499)

    # SEND SCREENSHOT
    elif data == "send_ss":

        await query.message.edit_caption(
            caption=(
                "<b>âœ… PAYMENT VERIFICATION</b>\n\n"

                "<b>ðŸ“¸ SEND PAYMENT SCREENSHOT TO ADMIN</b>\n\n"

                "<b>âš¡ AFTER VERIFY YOU WILL GET ACCESS</b>"
            ),
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        "ðŸ“© SEND SCREENSHOT",
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

print("âœ… BOT IS RUNNING SUCCESSFULLY...")

app.run_polling()
