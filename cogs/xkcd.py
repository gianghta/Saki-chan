import discord
import random

from discord.ext import commands


class XKCDCog(commands.Cog, name='XKCD'):
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
            async with self.bot.session.get(f'https://xkcd.com/info.0.json') as response:
                resp = await response.json()
                total_comics = response['num']
                rand_num = random.randint(1, total_comics)
        except Exception:
            return await ctx.channel.send('Couldn\'t grab the comic, something must have gone wrong')

        xkcd_url = 'http://xkcd.com/' + str(rand_num) + '/info.0.json'

        try:
            async with self.bot.session.get(xkcd_url) as response:
                resp = await response.json()
                image = resp['img']
                title = resp['title']
                await ctx.channel.send(f"```Title: {title}```")
                await ctx.channel.send(f'{image}')
        except Exception as e:
            print(f'Error: {e}')

def setup(bot):
    bot.add_cog(XKCDCog(bot))