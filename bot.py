import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, CallbackContext

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Получаем конфигурацию из переменных окружения
CHANNEL_USERNAME = os.getenv("CHANNEL_USERNAME", "@zakon_koshel")
CHANNEL_ID = int(os.getenv("CHANNEL_ID", "-1003320212459"))
ACCESS_LINK = os.getenv("ACCESS_LINK", "https://drive.google.com/uc?export=download&id=1aMm3UyJtWk2zGca1OFlegUlv_xMlNiAF")

async def start(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [InlineKeyboardButton("🔍 Проверить подписку", callback_data='check_sub')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "Для доступа к файлам необходимо ПОДПИСАТЬСЯ на канал.\n"
        "Нажмите кнопку ниже, чтобы проверить подписку:",
        reply_markup=reply_markup
    )

async def check_subscription(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    
    try:
        chat_member = await context.bot.get_chat_member(CHANNEL_ID, user_id)
        
        if chat_member.status in ['member', 'administrator', 'creator']:
            keyboard = [
                [InlineKeyboardButton("🔗 ДЕНЕЖНЫЙ ВОЗВРАТ—2026", url=ACCESS_LINK)],
                [InlineKeyboardButton("🔄 Проверить подписку снова", callback_data='check_sub')]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await query.edit_message_text(
                "✅ Вы подписаны! Вот ваш файл:\n\n"
                "Вы можете проверять подписку снова в любое время:",
                reply_markup=reply_markup
            )
        else:
            keyboard = [
                [InlineKeyboardButton("📢 Подписаться на канал", url=f"https://t.me/{CHANNEL_USERNAME[1:]}")],
                [InlineKeyboardButton("🔄 Проверить подписку", callback_data='check_sub')]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await query.edit_message_text(
                "❌ Вы не подписаны на канал.\n"
                "Подпишитесь и проверьте снова:",
                reply_markup=reply_markup
            )
            
    except Exception as e:
        logging.error(f"Ошибка проверки: {e}")
        keyboard = [
            [InlineKeyboardButton("🔄 Попробовать снова", callback_data='check_sub')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            "⚠️ Ошибка проверки. Попробуйте снова:",
            reply_markup=reply_markup
        )

def main() -> None:
    # Получаем токен из переменных окружения Railway
    TOKEN = os.getenv("BOT_TOKEN")
    
    if not TOKEN:
        logging.error("❌ ОШИБКА: BOT_TOKEN не найден в переменных окружения!")
        logging.error("Добавьте BOT_TOKEN в настройках Railway")
        return
    
    try:
        application = Application.builder().token(TOKEN).build()
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CallbackQueryHandler(check_subscription, pattern='check_sub'))
        
        logging.info("🤖 Бот запускается...")
        application.run_polling(allowed_updates=Update.ALL_TYPES)
        
    except Exception as e:
        logging.error(f"❌ Ошибка запуска бота: {e}")
        if "InvalidToken" in str(e):
            logging.error("⚠️ Токен недействителен! Получите новый у @BotFather")

if __name__ == '__main__':
    main()
