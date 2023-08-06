from ..nba.constants import *
import types
from enum import Enum
from inspect import isclass

try:
    import importlib.resources as pkg_resources
except ImportError:
    # Try backported to PY<37 `importlib_resources`.
    import importlib_resources as pkg_resources

import requests
import requests_cache
import logging
import json

from .response_parser import ResponseParser

requests_cache.install_cache('sports', expire_after=60 * 60 * 6)  # Cache for 6 hours


################################
# Decorators for the NBA Class #
################################
def clean_inputs(func):
    """
    Iterates over a function's parameters checking for Enum, if one is found, the value is used instead

    Args:
        func: Underlying function to be wrapped

    Returns: Wrapped function

    """

    def new_func(*args, **kwargs):
        cleaned_args = []
        for i in range(len(args)):
            if isclass(type(args[i])) and issubclass(type(args[i]), Enum):
                clean_arg = args[i].value
                cleaned_args.append(clean_arg)
            else:
                cleaned_args.append(args[i])

        for key, val in kwargs.items():
            if isclass(type(val)) and issubclass(type(val), Enum):
                kwargs[key] = val.value

        data = func(*cleaned_args, **kwargs)
        return data

    return new_func


class StatsNbaApi:
    def __init__(self):
        # Get a logger
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')
        self.logger = logging.getLogger('sportsdata')

        # Read the specification file
        self.specs = json.loads(pkg_resources.read_text('sportsdata.data', 'stats.nba.com.json'))
        self.logger.info(self.specs.keys())

        self.parameters = {}
        for param in self.specs['parameters']:
            self.parameters[param['name']] = {
                'default': param['default'],
                'values': param['values']
            }

        # Create methods for each api endpoint
        for endpoint in self.specs['stats_endpoints']:
            self.add_api_method(endpoint)

    def add_api_method(self, endpoint):
        """
        Dynamically builds a method for each endpoint in the specification file
        :param endpoint:
        :param cls:
        :param name:
        :return:
        """

        def dynamic_method(self2, **kwargs):
            url = endpoint['url']
            parameters = endpoint['parameters']
            self2.logger.info(url)
            self.logger.info(kwargs)

            # Determine the ResponseType
            return_type = ReturnType.DICTIONARY.value
            if 'ReturnType' in kwargs:
                return_type = kwargs['ReturnType']

            url_parameters = {}
            # Add each parameter to the url
            for param in parameters:
                value = ''

                # Was this parameter passed into to the method?
                if param in kwargs:
                    value = kwargs[param]

                # Does this parameter have a default value
                elif param in self.parameters:
                    value = self.parameters[param]['default']

                # Is the value for the parameter a legal value for this parameter
                if param in self.parameters and value not in self.parameters[param]['values']:
                    self.logger.warning(f"The value '{value}' is not a legal value for '{param}'")
                    value = ''

                # Add the parameter and its value to the dictionary of url parameters
                url_parameters[param] = value

            self.logger.info(url_parameters)
            response = requests.get(url, params=url_parameters, timeout=10)

            if return_type == ReturnType.DICTIONARY or return_type == ReturnType.DICTIONARY.value:
                return_value = ResponseParser.get_dictionary(response)
            elif return_type == ReturnType.RESPONSE or return_type == ReturnType.RESPONSE.value:
                return_value = response
            elif return_type == ReturnType.DATA_FRAMES or return_type == ReturnType.DATA_FRAMES.value:
                return_value = ResponseParser.get_data_frames(response)

            return return_value

        dynamic_method.__name__ = endpoint['name']
        setattr(self, dynamic_method.__name__, types.MethodType(dynamic_method, self))

    base_url = "https://stats.nba.com/stats/{0}"
    headers = {
        'user-agent': (
            'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'),
        'Dnt': '1',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'en',
        'origin': 'https://stats.nba.com'
    }

    # @clean_inputs
    # def league_game_log(self,
    #                     counter=0,
    #                     direction=Direction.DESC.value,
    #                     league_id=League.NBA.value,
    #                     player_or_team_abbreviation=PlayerOrTeam.TEAM.value,
    #                     season=2021,
    #                     season_type_all_star=SeasonType.REGULAR_SEASON.value,
    #                     sorter=SortOrder.DATE.value,
    #                     date_from_nullable='',
    #                     date_to_nullable='',
    #                     proxy=None,
    #                     headers=None,
    #                     timeout=30,
    #                     ):
    #     """
    #
    #     :param counter:
    #     :param direction:
    #     :param league_id:
    #     :param player_or_team_abbreviation:
    #     :param season:
    #     :param season_type_all_star:
    #     :param sorter:
    #     :param date_from_nullable:
    #     :param date_to_nullable:
    #     :param proxy:
    #     :param headers:
    #     :param timeout:
    #     :return:
    #                 'SEASON_ID', 'TEAM_ID', 'TEAM_ABBREVIATION', 'TEAM_NAME', 'GAME_ID', GAME_DATE',
    #         'MATCHUP', 'WL', 'MIN', 'FGM', 'FGA', 'FG_PCT', 'FG3M', 'FG3A', 'FG3_PCT', 'FTM',
    #         'FTA', 'FT_PCT', 'OREB', 'DREB', 'REB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS', 'PLUS_MINUS', 'VIDEO_AVAILABLE'
    #     """
    #     url = self.base_url.format('leaguegamelog')
    #     self.logger.info(url)
    #
    #     parameters = {
    #         'Counter': counter,
    #         'Direction': direction,
    #         'LeagueID': league_id,
    #         'PlayerOrTeam': player_or_team_abbreviation,
    #         'Season': season,
    #         'SeasonType': season_type_all_star,
    #         'Sorter': sorter,
    #         'DateFrom': date_from_nullable,
    #         'DateTo': date_to_nullable
    #     }
    #
    #     self.logger.info(parameters)
    #     # response = requests.get(url, headers=self.headers, params=params, timeout=10)
    #
    #     response = requests.get('https://stats.nba.com/stats/leaguegamelog?Counter=0&DateFrom=&DateTo=&Direction=ASC&LeagueID=00&PlayerOrTeam=T&Season=2021&SeasonType=Regular+Season&Sorter=DATE')
    #     data = ResponseParser.get_data_frames(response)
    #     return data


    # @clean_inputs
    # def scoreboard_v2(self, game_date, league_id, day_offset):
    #     url = self.base_url.format("scoreboardv2")
    #     params = {'GameDate': game_date, 'LeagueID': league_id, 'DayOffset': day_offset}
    #     req = requests.get(url, headers=self.headers, params=params)
    #     data = ResponseParser.scoreboard_v2(req)
    #
    #     return data