from eca import *

import random

## You might have to update the root path to point to the correct path
## (by default, it points to <rules>_static)
root_content_path = 'test_static'

from eca.generators import start_offline_tweets
import datetime
import textwrap

@event('init')
def setup(ctx, e):
   start_offline_tweets('bata_2014.txt')

@event('tweet')
@condition(lambda c,e: "team" in e.data['text'])
def echo(c,e):
    emit('tweet', e.data)
