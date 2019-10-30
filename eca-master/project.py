from eca import *

import random

root_content_path = 'project_static'

from eca.generators import start_offline_tweets
import datetime
import textwrap
import eca.http

choice = 0

def filter_english(data):
    if data['lang'] == 'en':
        return 1
    return 0
def filter_dutch(data):
    if data['lang'] == 'nl':
        return 1
    return 0
def filter_teams(data):
    if "team" in data['text']:
        return 1
    return 0
def filter_weather(data):
#add weather function priya made
        return 1 
    return 0 
def filter_by(data):
    print(choice)
    if choice == 0:
        return 1
    elif choice == 1:
        filter_english(data)
    elif choice == 2:
        filter_dutch(data)
    elif choice == 3:
        filter_teams(data)
    elif choice == 4:
        filter_weather(data)

@event('init')
def setup(ctx, e):
   start_offline_tweets('bata_2014.txt')

def add_request_handlers(httpd):
    httpd.add_route('/api/filter', eca.http.GenerateEvent('filter'), methods=['POST'])

@event('filter')
def change_filter(ctx, e):
    choice = e.data['value']

@event('tweet')
@condition(lambda c,e: filter_by(e.data))
def echo(c,e):
    emit('tweet', e.data)
