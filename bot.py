import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, CallbackContext

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Конфигурация
CHANNEL_USERNAME = "@zakon_koshel"
CHANNEL_ID = -1003320212459
ACCESS_LINK = "https://drive.google.com/uc?export=download&id=1aMm3UyJtWk2zGca1OFlegUlv_xMlNiAF"

# Команда /start
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

# Проверка подписки - НИКОГДА не завершается
async def check_subscription(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    
    try:
        chat_member = await context.bot.get_chat_member(CHANNEL_ID, user_id)
        
        if chat_member.status in ['member', 'administrator', 'creator']:
            # Подписан - даем ссылку + кнопку проверить снова
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
            # Не подписан
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
        # При ошибке - кнопка попробовать снова
        keyboard = [
            [InlineKeyboardButton("🔄 Попробовать снова", callback_data='check_sub')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            "⚠️ Ошибка проверки. Попробуйте снова:",
            reply_markup=reply_markup
        )

# Основная функция
def main() -> None:
    TOKEN = "8385581401:AAE9n9TqxH0IF3JqIynqWi3lmMX1gDm8Mf8"
    
    application = Application.builder().token(TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(check_subscription, pattern='check_sub'))
    
    print("Бот запущен!")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
