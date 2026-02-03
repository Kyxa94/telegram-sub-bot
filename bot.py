import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

CHANNEL_USERNAME = "@zakon_koshel"
CHANNEL_ID = -1003320212459

ACCESS_LINK = "https://drive.google.com/uc?export=download&id=1aMm3UyJtWk2zGca1OFlegUlv_xMlNiAF"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🔍 Проверить подписку", callback_data='check_sub')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "Для доступа к файлам необходимо ПОДПИСАТЬСЯ на канал.\n"
        "Нажмите кнопку ниже, чтобы проверить подписку:",
        reply_markup=reply_markup
    )

async def check_subscription(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id

    try:
        member = await context.bot.get_chat_member(CHANNEL_ID, user_id)

        if member.status in ['member', 'administrator', 'creator']:
            keyboard = [
                [InlineKeyboardButton("🔗 ДЕНЕЖНЫЙ ВОЗВРАТ—2026", url=ACCESS_LINK)]
            ]
            await query.edit_message_text(
                "✅ Вы подписаны! Вот ваш файл:",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
        else:
            keyboard = [
                [InlineKeyboardButton("📢 Подписаться", url=f"https://t.me/{CHANNEL_USERNAME[1:]}")],
                [InlineKeyboardButton("🔄 Проверить подписку", callback_data='check_sub')]
            ]
            await query.edit_message_text(
                "❌ Вы не подписаны.\nПодпишитесь и проверьте снова:",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )

    except Exception:
        await query.edit_message_text("⚠ Ошибка. Попробуйте позже.")

def main():
    TOKEN = os.getenv("TOKEN")

    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(check_subscription, pattern='check_sub'))

    print("Bot started")
    app.run_polling()

if __name__ == "__main__":
    main()
