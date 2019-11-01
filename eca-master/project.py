from eca import *
import random
from eca.generators import start_offline_tweets
import datetime
import textwrap
import pprint
import eca.http
import re
import pickle

root_content_path = 'project_static'


def filter_organiser_tweets(data):
    return data['user']['screen_name'] == "Batavierenrace"
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
def filter_word(word, data):
    return word in str(data['text']).lower()
def filter_by(choice, data):

    if isinstance(choice, str):
        return filter_word(choice, data)
    if choice == 1:
        return filter_english(data)
    if choice == 2:
        return filter_dutch(data)
    if choice == 3:
        return filter_teams(data)
    if choice == 4:
        return filter_weather(data)

# simple word splitter
pattern = re.compile('\W+')
def words(message):
    result = pattern.split(message)
    result = map(lambda w: w.lower(), result)
    result = filter(lambda w: len(w) > 2, result)
    return result
def good_or_bad(word):
    f = open("PositiveWords", "rb")
    g = open("NegativeWords", "rb")
    plot = pickle.load(f)
    nlot = pickle.load(g)
    f.close()
    g.close()
    if word in plot:
        return 0
    elif word in nlot:
        return 1
    else:
        return -1

def add_request_handlers(httpd):
    httpd.add_route('/api/filter', eca.http.GenerateEvent('filter'), methods=['POST'])
    httpd.add_content('/lib/', 'project_static/lib')
    httpd.add_content('/style/', 'project_static/style')

@event('init')
def setup(ctx, e):
   ctx.choice = 1
   start_offline_tweets('bata_2014.txt', event_name = "unfiltered_tweet")


@event('filter')
def change_filter(ctx, e):
    if isinstance(e.data['value'], int):
        ctx.choice = int(e.data['value'])
    else: ctx.choice = e.data['value']

@event('unfiltered_tweet')
def echo(c, e):
    emit('unfiltered_tweet', e.data)
    fire('organiser_tweet', e.data)
    fire('filtered_tweet', e.data)
    fire('word_cloud', e.data)

@event('filtered_tweet')
@condition(lambda c,e: filter_by(c.choice, e.data))
def echo(c,e):
    emit('filtered_tweet', e.data)

@event('organiser_tweet')
@condition(lambda c,e: filter_organiser_tweets(e.data))
def echo(c,e):
    emit('organiser_tweet', e.data)

@event('word_cloud')
def echo(ctx, e):
    tweet = e.data
    for w in words(tweet['text']):
        if good_or_bad(w) == 0:
            emit('goodword', {
                'action': 'add',
                'value': (w, "g", 1)});
        elif good_or_bad(w) == 1:
            emit('badword', {
                'action': 'add',
                'value': (w, "b", 1)});
