import discord
import random
import asyncio
import os

from dotenv import load_dotenv
from discord.ext import commands
from http_request import fetch

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

bot = commands.Bot(command_prefix="saki ")

@bot.event
async def on_ready():
    print('Starting up server...')
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command(name="guess")
async def get_guess_num(ctx):
    await ctx.channel.send('Guess a number between 1 and 10.')

    def is_correct(m):
        return m.author == ctx.author and m.content.isdigit()

    answer = random.randint(1, 10)

    try:
        guess = await bot.wait_for('message', check=is_correct, timeout=5.0)
    except asyncio.TimeoutError:
        return await ctx.channel.send('Sorry, you took too long it was {}.'.format(answer))

    if int(guess.content) == answer:
        await ctx.channel.send('You are right!')
    else:
        await ctx.channel.send('Oops. It is actually {}.'.format(answer))

@bot.command(name="grab-xkcd")
async def get_xkcd_comic(ctx):
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


bot.run(TOKEN)