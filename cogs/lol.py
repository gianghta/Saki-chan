import discord
import os

from discord.ext import commands
from utils.league import LeagueWatcher
from dotenv import load_dotenv

load_dotenv()
LEAGUE_API_KEY = os.getenv('LEAGUE_API_KEY')

class LeagueStats(commands.Cog, name="League Of Legends"):

    def __init__(self, bot):
        self.bot = bot
        self.api_key = LEAGUE_API_KEY

    @commands.command(
    name="find-lol",
    help='Get a LoL player profile/stats, use "-" for spacing words. Input format: saki find-lol {player name} {region}',
    brief='Find LoL player account info'
    )
    async def get_lol_player_stat(self, ctx, player, region):
        player = player.replace("-", " ")
        watcher = LeagueWatcher(api_key=self.api_key, region=region)
        new_player = watcher.find_player_stats(player)
        if not isinstance(new_player, str):
            await ctx.channel.send(f"```Player: {new_player['summonerName']}\nTier: {new_player['tier']}\nRank: {new_player['rank']}\nWins: {new_player['wins']}\nLosses: {new_player['losses']}```")
        else:
            await ctx.channel.send(f'No player name {player} found')

def setup(bot):
    bot.add_cog(LeagueStats(bot))