
from config import TOKEN_TG, TOKEN_WEATHER
from weather import get_weather
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

text_dict = {
    "hello_text": "Привет!",
    "start_text": "Напиши название города и получи сводку погоды!",
    "help_text": "Чтобы получить сводку погоды, напиши название города. Например, \"Киев\"или \"Kyiv\".\
    Если не получилось получить сводку погоды, проверь написание назания города"
}

def start_c(update, context):
    """Print welcome message in tg chat"""
    update.message.reply_text(f'{text_dict["hello_text"]} {update.effective_user.first_name} {text_dict["start_text"]}')

def help_c(update, context):
    """Print help message in tg chat"""
    update.message.reply_text(text_dict["help_text"])

def weather_summary(update, context):
    """Return weather summary."""
    update.message.reply_text(get_weather(update.message.text, TOKEN_WEATHER))
    
updater = Updater(TOKEN_TG)

updater.dispatcher.add_handler(CommandHandler('start', start_c))
updater.dispatcher.add_handler(CommandHandler('help', help_c))
updater.dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, weather_summary))

updater.start_polling()
updater.idle()