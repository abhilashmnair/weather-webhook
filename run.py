from telegram import *
from telegram.ext import *
import requests
import json

token = 'BOT_TOKEN'
bot = Bot(token)
updater = Updater(token,use_context=True)
dispatcher : Dispatcher = updater.dispatcher

def getWeatherData(city_name):
    key = 'WEATHER_TOKEN'
    URL = f'https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={key}&units=metric'
    response = requests.get(url = URL)
    payload = response.json()
    try:
        cur_weather = payload['weather'][0]['main']
        cur_temp = payload['main']['temp']
        return f'Weather in {city_name}\nCurrent weather : {cur_weather}\nTemperature : {cur_temp}°C'
    except KeyError:
        return "Sorry, couldn't get the data for given location!"

def sendResponse(update:Update,context:CallbackContext):
    if update.message.text == '/start':
        bot.sendMessage(chat_id = update.effective_chat.id, text = 'Enter the city name', parse_mode = 'HTML')
    else:
        weatherData = getWeatherData(update.message.text)
        bot.sendMessage(chat_id = update.effective_chat.id,text = weatherData,parse_mode = 'HTML')

dispatcher.add_handler(MessageHandler(Filters.text,sendResponse))
updater.start_polling()
