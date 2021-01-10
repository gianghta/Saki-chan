import discord
import random

from discord.ext import commands
from utils.http_request import fetch


class XKCD(commands.Cog, name='XKCD'):
    """A Cog for everything XKCD related"""

    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(
    name="grab-xkcd",
    help="Grab a random XKCD comic from the website",
    brief="Get XKCD comic"
    )
    async def get_xkcd_comic(self, ctx):
        total_comics, rand_num = 0, 0

        try:
            response = await fetch(f'https://xkcd.com/info.0.json')
            total_comics = response['num']
            rand_num = random.randint(1, total_comics)
        except Exception:
            return await ctx.channel.send('Couldn\'t grab the comic, something must have gone wrong')

        xkcd_url = 'http://xkcd.com/' + str(rand_num) + '/info.0.json'

        try:
            response = await fetch(xkcd_url)
            image = response['img']
            title = response['title']
            await ctx.channel.send(f"```Title: {title}```")
            await ctx.channel.send(f'{image}')
        except Exception as e:
            print(f'Error: {e}')

def setup(bot):
    bot.add_cog(XKCD(bot))