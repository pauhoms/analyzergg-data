import pandas as pd
import urllib3
from config import RIOT_API_KEY


_ALL_TIERS = ['IRON', 'BRONZE', 'SILVER', 'GOLD',
              'PLATINUM', 'DIAMOND']
_ALL_DIVISIONS = ['I', 'II', 'III', 'IV']
_HTTP = urllib3.PoolManager()


def _init():
    _generate_file(_get_all_summoners())


def _get_all_summoners() -> pd.DataFrame:
    all_players = pd.DataFrame()
    for tier in _ALL_TIERS:
        for division in _ALL_DIVISIONS:

            get_all_players_from_that_division = \
                "https://euw1.api.riotgames.com/lol/league/v4/entries/"

            get_all_players_from_that_division = \
                get_all_players_from_that_division + \
                "RANKED_SOLO_5x5/"+tier+"/"+division+"?api_key=" + RIOT_API_KEY

            request = _HTTP.request(
                    'GET',
                    get_all_players_from_that_division
                )

            all_players = pd.concat([
                pd.read_json(request.data),
                all_players
            ])

    return all_players.summonerName


def _generate_file(players) -> None:
    players.to_csv('training/data/summoners_clean.csv')


if __name__ == "__main__":
    _init()
