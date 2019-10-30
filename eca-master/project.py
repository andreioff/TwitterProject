from eca import *

import random

root_content_path = 'project_static'

from eca.generators import start_offline_tweets
import datetime
import textwrap
import eca.http

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
def filter_by(choice, data):
    if choice == 0:
        return 1
    if choice == 1:
        return filter_english(data)
    if choice == 2:
        return filter_dutch(data)
    if choice == 3:
        return filter_teams(data)

@event('init')
def setup(ctx, e):
   ctx.choice = 0
   start_offline_tweets('bata_2014.txt')

def add_request_handlers(httpd):
    httpd.add_route('/api/filter', eca.http.GenerateEvent('filter'), methods=['POST'])

@event('filter')
def change_filter(ctx, e):
    ctx.choice = int(e.data['value'])

@event('tweet')
@condition(lambda c,e: filter_by(c.choice, e.data))
def echo(c,e):
    emit('tweet', e.data)
