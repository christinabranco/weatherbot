#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  1 19:11:26 2019

@author: cbranco
"""

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import requests
import json
from datetime import datetime, date, timedelta
import logging

#Credentials for OpenWeather API and Telegram bot stored elsewhere
weather_credentials = json.load(open('weather_credentials.json'))
bot_credentials = json.load(open('bot_credentials.json'))


#initialise logger
logging.basicConfig(filename='bot.log',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

def to_celsius(temp):
    """Converts temperature in Kelvin to Celsius"""
    temp_in_c = round(temp-273.15)
    return temp_in_c

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Welcome to WeatherBot!")

def message(item):
    """Formats each 'chunk' of weather info into a nice message."""
    item_time = datetime.fromtimestamp(item['dt']).time()
    item_string = 'At {} hours it will be {} degrees and the sky will be {}.\n'.format(
            item_time,
            to_celsius(item['main']['temp']),
            item['weather'][0]['main'].lower())
    return item_string

def today(update, context):
    """If given /today command, fetches weather message for today from get_weather() and sends it"""
    logger.info('Received {} message from {}'.format(update.effective_message['text'],
                update.effective_user['username']))
    todays_message = get_weather(date.today())
    context.bot.send_message(chat_id=update.message.chat_id, text=todays_message)
    
def tomorrow(update, context):
    """If given /today command, fetches weather message for tomorrow from get_weather() and sends it"""
    logger.info('Received {} message from {}'.format(update.effective_message['text'],
                update.effective_user['username']))
    tomorrows_message = get_weather(date.today() + timedelta(1))
    context.bot.send_message(chat_id=update.message.chat_id, text=tomorrows_message)
    
def get_weather(weather_date):
    """Calls OpenWeather API, returns weather items formatted in nice message with message()"""
    params = {'id':2643743} #id for London, UK
    params.update(weather_credentials)
    r = requests.get(
            'http://api.openweathermap.org/data/2.5/forecast',
            params = params
            )
    weather= r.json()['list']
    day_weather = [
            item for item in weather 
            if datetime.fromtimestamp(item['dt']).date() == weather_date
            ]
    weather_message = ''
    for hour in day_weather:
        weather_message += message(hour)
    return weather_message

#initializes the bot
updater = Updater(token=bot_credentials['token'],
                  use_context = True)

#creates handler objects for today and tomorrow commands
today_handler = CommandHandler('today', today)
tomorrow_handler = CommandHandler('tomorrow', tomorrow)
start_handler = CommandHandler('start', start)

#adds aforementioned command handler objects to dispatcher
updater.dispatcher.add_handler(today_handler)
updater.dispatcher.add_handler(tomorrow_handler)
updater.dispatcher.add_handler(start_handler)

#starts listening for events  
updater.start_polling() 
