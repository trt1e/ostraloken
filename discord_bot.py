import os
from dotenv import load_dotenv # For reading secrets
import discord # for discord bot
import threading # for discord bot to run separetly
import asyncio # for discord bot to run separetly

load_dotenv() # load .env
# access .env
is_linux = os.getenv("is_linux")
discord_bot_token = os.getenv("discord_bot_token")
discord_channel_id = os.getenv("discord_channel_id")
discord_role_taged_in_reminders = os.getenv("discord_role_taged_in_reminders")

intents = discord.Intents.default()
intents.message_content = True
bot = discord.Client(intents=intents)

bot_loop = None # for cross threading calls
bot_ready_event = threading.Event() # For to se if it has initialized


@bot.event
async def on_ready():
    global bot_loop
    bot_loop = asyncio.get_running_loop()
    print(f"[Discord] Bot logged in as {bot.user}")
    bot_ready_event.set()
    
async def async_send(message_text):
    if discord_channel_id:
        channel = bot.get_channel(int(discord_channel_id))
        if isinstance(channel, discord.abc.Messageable):
            await channel.send(message_text)
    else:
        print("[Discord] Error with discord_channel_id in .env")
    
def send_discord_message(message_text):
    if bot_loop and bot.is_ready():
        # pass to async bot
        asyncio.run_coroutine_threadsafe(async_send(message_text), bot_loop)
        print(f"[Discord] Sent message: {message_text}")
    else:
        print("[Discord] Bot is not ready yet. Message not sent.")

def run_discord_bot():
    bot.run(str(discord_bot_token))
