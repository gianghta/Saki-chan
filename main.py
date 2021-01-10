import discord
import os
import platform
import traceback

from dotenv import load_dotenv
from discord.ext import commands
from datetime import datetime


DESCR = 'General purpose bot for private server'

# File names of extensions we are loading on startup
startup_extensions = ['cogs.general',
                      'cogs.lol',
                      'cogs.xkcd']

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')


class SakiBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix="saki ",
            description=DESCR,
            case_insensitive=True,
        )
    
    async def close(self):
        await super().close()

bot = SakiBot()

@bot.event
async def on_ready():
    print('Starting up server...')
    print(f'\nLogged in as: {bot.user.name} - {bot.user.id}\n'
          f'Python Version: {platform.python_version()}\n'
          f'Library Version: {discord.__version__}\n')

    print(f'Ready! {datetime.utcnow()}\n')

total = len(startup_extensions)
successes = 0
for extension in startup_extensions:
    try:
        bot.load_extension(extension)
        print(f'Successfully loaded extension {extension}.')
        successes += 1
    except Exception:
        print(f'Failed to load extension {extension}.')
        traceback.print_exc()

print('-' * 52)
print(f'Successfully loaded {successes}/{total} extensions.')

bot.run(TOKEN)