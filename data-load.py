import cfbd
from cfbd.rest import ApiException
import pandas as pd

secret = 'Z0sh/62ooMzlOGDfmLOxCdO8GQKeEg8js4xMvvhZYO/6YptN8jF2TvLI3Dd2tjTJ'

#configure CFBD APIs
configuration = cfbd.Configuration()
configuration.api_key['Authorization'] = secret
configuration.api_key_prefix['Authorization'] = 'Bearer'

api_config =  cfbd.ApiClient(configuration)
roster_api = cfbd.TeamsApi(api_config)
metrics_api = cfbd.MetricsApi(api_config)
player_api  = cfbd.PlayersApi(api_config)
plays_api = cfbd.PlaysApi(api_config)

#CFBD API parameters
team = "Purdue"
year = 2023
week = 3
season_type = None
offense = None
defense = None
conference = None
offense_conference = None
defense_conference = None
play_type = None
classification = None

def get_plays(team, week, year):
    try:
        # Play by play data
        pbp_data= plays_api.get_plays(year, week, team=team)
        return pbp_data
    except ApiException as e:
        print("Exception when calling PlaysApi->get_plays: %s\n" % e)
        
def get_roster(team, year):
    try:
        #get roster data
        roster = roster_api.get_roster(year=year, team=team)
        return roster
    except ApiException as e:
        print("Exception when calling RosterApi->get_roster: %s\n" % e)
        
def get_player_usage(team, year):
    try:
        player_usage = player_api.get_player_usage(year=year, team=team)
        return player_usage
    except ApiException as e:
        print("Exception when calling PlayerApi->get_player_usage: %s\n" % e)
        
def get_player_stats(team, year):
    try:
        player_stats = player_api.get_player_season_stats(year=year, team=team)
        return player_stats
    except ApiException as e:
        print("Exception when calling PlayerApi->get_player_season_stats: %s\n" % e)
        
def get_team_ppa(team, year):
    try:
        team_ppa = metrics_api.get_team_ppa(year=year, team=team)
        return team_ppa
    except ApiException as e:
        print("Exception when calling MetricsApi->get_team_ppa: %s\n" % e)
    

#print(get_plays(team, year=2023, week=week))
#print(get_roster(team, year=2023))
#print(get_player_usage(team, year=2023))
#print(get_player_stats(team, year=2023))
#print(get_team_ppa(team, year=2023))