from twidi.admin import db
from twidi.admin.models import Configuration
from twidi.twitch.midi_bot import TwidiBot
from twidi.twitch.pub_sub_client import PubSubHandler

c = db.session.query(Configuration).first()
bot = TwidiBot(config=c)
pubsub_handler = PubSubHandler(bot=bot, config=c)
