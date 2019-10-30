from eca import *

import random

root_content_path = 'project_static'

from eca.generators import start_offline_tweets
import datetime
import textwrap
import eca.http

def filter_organiser_tweets(data):
    return data['user']['default_profile']
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
    English = [" air ", " cloudy ", " sunny ", " rain ", " drizzle ", " thunder ", " fog ", \
        " forecast ", " hail ", " humid ", " heat ", " high ", " low ", " temp ", " kelvin ", \
        " lightning ", " meteorolog ", " overcast ", " precipitation ", " pressure ",
        " wind ", " smoke ", " snow ", " storm ", " temp ", " thunder ", " tornado ", " warm ", \
        " weather ", " celcius ", " farenheit "]
    Dutch = [" lucht ", " wolk ", " zon ", " regen ", " miezer ", " onweer ", " mist ", \
        " weersverwachting ", " hagel ", " vochtig ", " hitte ", " hoog ", " laag ", \
        " temp ", " kelvin ", " bliksem ", " meteorloog ", " zwaarbewolkt ", " regen ", \
        " druk ", " wind ", " rook ", " sneeuw ", " storm ", " temp ", " onweer ", \
        " tornado ", " warm ", " weer ", " celsius ", " fahrenheit "]

    for word in English:
        if word in str(data).lower():
            return 1

    for word in Dutch:
        if word in str(data).lower():
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
    if choice == 4:
        return filter_weather(data)

@event('init')
def setup(ctx, e):
   ctx.choice = 1
   start_offline_tweets('bata_2014.txt', event_name = "unfiltered_tweet")

def add_request_handlers(httpd):
    httpd.add_route('/api/filter', eca.http.GenerateEvent('filter'), methods=['POST'])

@event('filter')
def change_filter(ctx, e):
    ctx.choice = int(e.data['value'])

@event('unfiltered_tweet')
def echo(c, e):
    emit('unfiltered_tweet', e.data)
    fire('organiser_tweet', e.data)
    fire('filtered_tweet', e.data)

@event('filtered_tweet')
@condition(lambda c,e: filter_by(c.choice, e.data))
def echo(c,e):
    emit('filtered_tweet', e.data)

@event('organiser_tweet')
@condition(lambda c,e: filter_organiser_tweets(e.data))
def echo(c,e):
    emit('organiser_tweet', e.data)
