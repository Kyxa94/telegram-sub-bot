import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Получаем токен из Railway
TOKEN = os.getenv("BOT_TOKEN", "")
if not TOKEN:
    logging.error("❌ ОШИБКА: BOT_TOKEN не найден!")
    exit(1)

# Конфигурация
CHANNEL_USERNAME = "@zakon_koshel"
CHANNEL_ID = -1003320212459

# --- ДВЕ ССЫЛКИ ---
# Первая ссылка (основной файл)
ACCESS_LINK_1 = os.getenv("ACCESS_LINK_1", "https://drive.google.com/uc?export=download&id=1MP8lLYRbeHVskh6gaC2KSiT5JhcEBGWj")
# Вторая ссылка (спортивный вычет) - ВАША НОВАЯ ССЫЛКА
ACCESS_LINK_2 = "https://drive.google.com/uc?export=download&id=1bJKy-WMYiQgHRwaQHzVWuMCAz23eos1Z"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("🔍 Проверить подписку", callback_data='check_sub')]]
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
            # ✅ Подписан — ДВЕ кнопки с ссылками
            keyboard = [
                [InlineKeyboardButton("🔗 ДЕНЕЖНЫЙ ВОЗВРАТ—2026", url=ACCESS_LINK_1)],
                [InlineKeyboardButton("🏋️‍♂️ Вычет за спорт (инструкция)", url=ACCESS_LINK_2)]
            ]
            await query.edit_message_text(
                "✅ Вы подписаны! Вот ваши файлы:",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
        else:
            # ❌ Не подписан
            keyboard = [
                [InlineKeyboardButton("📢 Подписаться", url=f"https://t.me/{CHANNEL_USERNAME[1:]}")],
                [InlineKeyboardButton("🔄 Проверить подписку", callback_data='check_sub')]
            ]
            await query.edit_message_text(
                "❌ Вы не подписаны.\nПодпишитесь и проверьте снова:",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )

    except Exception:
        keyboard = [[InlineKeyboardButton("🔄 Попробовать снова", callback_data='check_sub')]]
        await query.edit_message_text(
            "⚠️ Ошибка. Попробуйте снова:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(check_subscription, pattern='check_sub'))
    logging.info("🤖 Бот запущен (две ссылки)!")
    app.run_polling()

if __name__ == "__main__":
    main()
