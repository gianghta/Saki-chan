from riotwatcher import LolWatcher, ApiError


class LeagueWatcher:
    def __init__(self, api_key, region):
        self.watcher = LolWatcher(api_key)
        self.region = region
    
    def find_player_stats(self, name):
        player = self.watcher.summoner.by_name(self.region, name)
        player_stat = self.watcher.league.by_summoner(self.region, player['id'])

        if not player_stat:
            return 'No player found'
        return player_stat[0]
    