import discord
import random
import asyncio

from discord.ext import commands


class GeneralCog(commands.Cog, name="General"):
    """A Cog for anything, random stuff"""
    
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
    name="guess",
    help="Playing guessing game with Saki by giving her a number from 1 to 10",
    brief="Guessing game with number 1 to 10"
    )
    async def get_guess_num(self, ctx):
        await ctx.channel.send('Guess a number between 1 and 10.')

        def is_correct(m):
            return m.author == ctx.author and m.content.isdigit()

        answer = random.randint(1, 10)

        try:
            guess = await ctx.wait_for('message', check=is_correct, timeout=5.0)
        except asyncio.TimeoutError:
            return await ctx.channel.send('Sorry, you took too long it was {}.'.format(answer))

        if int(guess.content) == answer:
            await ctx.channel.send('You are right!')
        else:
            await ctx.channel.send('Oops. It is actually {}.'.format(answer))

def setup(bot):
    bot.add_cog(GeneralCog(bot))