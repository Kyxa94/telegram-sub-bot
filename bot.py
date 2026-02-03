import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Настройка логирования для Railway
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Получаем переменные окружения
CHANNEL_USERNAME = os.getenv("CHANNEL_USERNAME", "@zakon_koshel")
CHANNEL_ID = int(os.getenv("CHANNEL_ID", "-1003320212459"))
ACCESS_LINK = os.getenv("ACCESS_LINK", "https://drive.google.com/uc?export=download&id=1aMm3UyJtWk2zGca1OFlegUlv_xMlNiAF")

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

    except Exception as e:
        logging.error(f"Ошибка проверки подписки: {e}")
        await query.edit_message_text("⚠ Ошибка. Попробуйте позже.")

def main():
    # Получаем токен из переменных окружения Railway
    TOKEN = os.getenv("BOT_TOKEN")
    
    if not TOKEN:
        logging.error("❌ BOT_TOKEN не установлен!")
        logging.error("Добавьте переменную BOT_TOKEN в настройках Railway")
        return
    
    # Создаем приложение
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(check_subscription, pattern='check_sub'))
    
    logging.info("🤖 Бот запускается...")
    logging.info(f"📢 Канал: {CHANNEL_USERNAME}")
    
    # Запускаем polling
    app.run_polling(
        drop_pending_updates=True,
        allowed_updates=Update.ALL_TYPES
    )

if __name__ == "__main__":
    main()
