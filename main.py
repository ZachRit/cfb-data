import cfbd
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

secret = 'Z0sh/62ooMzlOGDfmLOxCdO8GQKeEg8js4xMvvhZYO/6YptN8jF2TvLI3Dd2tjTJ'

configuration = cfbd.Configuration()
configuration.api_key['Authorization'] = secret
configuration.api_key_prefix['Authorization'] = 'Bearer'

api_instance = cfbd.PlaysApi(cfbd.ApiClient(configuration))

#filter data
year = 2023 # int | Year filter
week = 7 # int | Week filter (required if team, offense, or defense, not specified)
season_type = 'regular' # str | Season type filter (optional) (default to regular)
team = 'Ohio State' # str | Team filter (optional)
offense = 'offense_example' # str | Offensive team filter (optional)
defense = 'defense_example' # str | Defensive team filter (optional)
conference = 'conference_example' # str | Conference filter (optional)
offense_conference = 'offense_conference_example' # str | Offensive conference filter (optional)
defense_conference = 'defense_conference_example' # str | Defensive conference filter (optional)
play_type = 56 # int | Play type filter (optional)
classification = 'classification_example' # str | Division classification filter (fbs/fcs/ii/iii) (optional)

try:
	 # Play by play data
	api_response = api_instance.get_plays(year, week, team=team)
	df=pd.DataFrame(api_response)
except Exception as e:
	print("Exception when calling PlaysApi->get_plays: %s\n" % e)

pbp_df = pd.DataFrame.from_records([dict(offense = g.offense, down=g.down, distance=g.distance, yards_gained=g.yards_gained, play_type=g.play_type) for g in api_response])

def is_successful_play(row):
    down, distance, yards_gained = row['down'], row['distance'], row['yards_gained']
    if down == 1:
        return yards_gained >= 0.5 * distance
    elif down == 2:
        return yards_gained >= 0.7 * distance
    elif down in [3, 4]:
        return yards_gained >= distance
    return False

def calculate_success_rate(pbp_df, team_name, play_types=None):
    # Filter plays for the specified team and play types
    query_str = f"offense == '{team_name}'"
    if play_types:
        play_types_str = " | ".join([f"play_type == '{play}'" for play in play_types])
        query_str += f" & ({play_types_str})"
    
    team_plays = pbp_df.query(query_str).copy()
    
    # Convert columns to numeric types
    team_plays[['down', 'distance', 'yards_gained']] = team_plays[['down', 'distance', 'yards_gained']].apply(pd.to_numeric, errors='coerce')
    
    # Calculate success
    team_plays['is_successful'] = team_plays.apply(is_successful_play, axis=1)
    
    # Calculate and round success rate
    if len(team_plays) == 0:
        return 0
    success_rate = round((team_plays['is_successful'].sum() / len(team_plays)) * 100, 2)
    
    return success_rate

def rush_success_rate(team_name):
    return calculate_success_rate(pbp_df, team_name, ['Rush'])

def pass_success_rate(team_name):
    return calculate_success_rate(pbp_df, team_name, ['Pass Reception', 'Pass Incompletion'])

def success_rate(team_name):
    return calculate_success_rate(pbp_df, team_name, ['Rush', 'Pass Reception', 'Pass Incompletion'])

rush_success = rush_success_rate(team)
pass_success = pass_success_rate(team)
overall_success = success_rate(team)

print(f"Rush success rate for {team}: {rush_success}%")
print(f"Pass success rate for {team}: {pass_success}%")
print(f"Overall success rate for {team}: {overall_success}%")






