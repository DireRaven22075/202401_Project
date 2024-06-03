import os
import django
import sys
import discord
import warnings
import aiohttp
from asgiref.sync import sync_to_async
from dotenv import load_dotenv

# 프로젝트의 절대 경로를 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Django 설정 모듈 지정
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'combina.settings')  # 프로젝트 이름에 맞게 수정

# Django 설정 초기화
django.setup()

from platformDiscord.models import DiscordMessage, DiscordChannel

warnings.filterwarnings("ignore", category=ResourceWarning, message="unclosed.*<TCPTransport.*>")

class DiscordBotService:
    def __init__(self, token):
        self.token = token
        self.intents = discord.Intents.default()
        self.intents.message_content = True

    class MyClient(discord.Client):
        def __init__(self, token, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.token = token

        async def setup_hook(self):
            self.loop.create_task(self.fetch_messages())

        async def fetch_messages(self):
            await self.wait_until_ready()
            channel_id_obj = await sync_to_async(DiscordChannel.objects.first)()
            if channel_id_obj:
                channelID = channel_id_obj.channel_id
            else:
                print("Error: No channel ID found in the database.")
                return

            channel = self.get_channel(channelID)
            if not channel or not isinstance(channel, discord.TextChannel):
                print(f"Error: Channel with ID {channelID} not found or is not a text channel.")
                return

            await sync_to_async(DiscordMessage.objects.all().delete)()
            messages = [message async for message in channel.history(limit=20)]
            for message in messages:
                await sync_to_async(DiscordMessage.objects.create)(
                    content=message.content,
                    author=message.author.name
                )
            await self.close()

    async def run_bot(self):
        client = self.MyClient(self.token, intents=self.intents)
        try:
            await client.start(self.token)
        except Exception as e:
            print(f"Error running bot: {e}")
        finally:
            await client.close()

    async def send_message_to_discord(self, message):
        client = self.MyClient(self.token, intents=self.intents)
        try:
            await client.login(self.token)
            await client.connect()

            channel_id_obj = await sync_to_async(DiscordChannel.objects.first)()
            if channel_id_obj:
                channelID = channel_id_obj.channel_id
            else:
                print("Error: No channel ID found in the database.")
                return False

            channel = client.get_channel(channelID)
            if channel and isinstance(channel, discord.TextChannel):
                await channel.send(message)
                return True
            return False
        except Exception as e:
            print(f"Error sending message: {e}")
            return False
        finally:
            try:
                await client.close()
            except Exception as e:
                print(f"Error closing client: {e}")

    async def update_bot_profile(self, bot_name=None, bot_avatar=None):
        async with aiohttp.ClientSession() as session:
            headers = {
                'Authorization': f'Bot {self.token}',
                'Content-Type': 'application/json'
            }
            json_data = {
                'username': bot_name,
                'avatar': bot_avatar
            }
            async with session.patch('https://discord.com/api/v9/users/@me', headers=headers, json=json_data) as response:
                if response.status == 200:
                    print("Bot profile updated successfully.")
                    return True
                else:
                    print(f"Error updating bot profile: {response.status}")
                    return False
