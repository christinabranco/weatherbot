#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  1 19:11:26 2019

@author: cbranco
"""

#London, GB : 2643743
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import requests
import json
from datetime import datetime, date, timedelta
import logging

weather_credentials = json.load(open('weather_credentials.json'))
bot_credentials = json.load(open('bot_credentials.json'))


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

def today(update, context):
    logger.info('Received {} message from {}'.format(update.effective_message['text'],
                update.effective_user['username']))
    params = {'id':2643743}
    params.update(weather_credentials)
    r = requests.get(
            'http://api.openweathermap.org/data/2.5/forecast',
            params = params
            )
    todays_date = date.today()
    weather= r.json()['list']
    todays_weather = [
            item for item in weather 
            if datetime.fromtimestamp(item['dt']).date() == todays_date
            ]
    todays_message = ''
    for hour in todays_weather:
        todays_message += message(hour)
    context.bot.send_message(chat_id=update.message.chat_id, text=todays_message)
    
def tomorrow(update, context):
    logger.info('Received {} message from {}'.format(update.effective_message['text'],
                update.effective_user['username']))
    params = {'id':2643743}
    params.update(weather_credentials)
    r = requests.get(
            'http://api.openweathermap.org/data/2.5/forecast',
            params=params
            )
    tomorrows_date = date.today() + timedelta(1)
    weather= r.json()['list']
    tomorrows_weather = [
            item for item in weather 
            if datetime.fromtimestamp(item['dt']).date() == tomorrows_date
            ]
    tomorrows_message = ''
    for hour in tomorrows_weather:
        tomorrows_message += message(hour)
    context.bot.send_message(chat_id=update.message.chat_id, text=tomorrows_message)
    
        

def to_celsius(temp):
    temp_in_c = round(temp-273.15)
    return temp_in_c

def message(item):
    item_time = datetime.fromtimestamp(item['dt']).time()
    item_string = 'At {} hours it will be {} degrees and the sky will be {}.\n'.format(
            item_time,
            to_celsius(item['main']['temp']),
            item['weather'][0]['main'].lower())
    return item_string


updater = Updater(token=bot_credentials['token'],
                  use_context = True)

start_handler = CommandHandler('start', start)
today_handler = CommandHandler('today', today)
tomorrow_handler = CommandHandler('tomorrow', tomorrow)
updater.dispatcher.add_handler(start_handler)
updater.dispatcher.add_handler(today_handler)
updater.dispatcher.add_handler(tomorrow_handler)
  
updater.start_polling() 
