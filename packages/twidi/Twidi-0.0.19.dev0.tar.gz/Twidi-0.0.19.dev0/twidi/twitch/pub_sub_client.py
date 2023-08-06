import twitchio
from twitchio.ext import pubsub
from twitchio.ext.commands import Bot

from twidi.admin.models import Configuration
from twidi.twitch.midi_bot import TwidiBot


class PubSubHandler:
    redemptions = []

    def __init__(self, bot: TwidiBot, config: Configuration):
        self.bot = bot
        self.config = config
        self.update_redemptions()

    def start_bot(self):
        client = twitchio.Client(token=self.config.bot_client_token)
        client.pubsub = pubsub.PubSubPool(client)
        bot = self.bot

        @client.event()
        async def event_pubsub_points_message(event: pubsub.PubSubChannelPointsMessage):
            print('Received redemption', event.__str__())
            try:
                for command in self.redemptions:
                    if command.point_redemption.title == event.reward.title:
                        command.trigger_command_redemption()
            except Exception as e:
                print(e)

        async def main():
            topics = [
                pubsub.channel_points(self.config.broadcaster_access_token)[self.config.channel_id],
            ]
            await client.pubsub.subscribe_topics(topics)
            await client.start()

        client.loop.run_until_complete(main())

    def update_redemptions(self):
        self.redemptions.clear()
        for name, command in self.bot.commands.items():
            if command.point_redemption:
                self.redemptions.append(command)
