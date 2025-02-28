from nba_api.stats.endpoints import LeagueGameLog
from nba_api.live.nba.endpoints import boxscore
from datetime import datetime, timedelta
import pytz
import pandas as pd
import json

# Get yesterday's date in local timezone
local_tz = pytz.timezone('Australia/Sydney')
now_local = datetime.now(local_tz)

# Convert local time to US Eastern Time (NBA time zone)
us_tz = pytz.timezone('US/Eastern')
now_us = now_local.astimezone(us_tz)

# Subtract one day to get yesterday's date in US Eastern Time
yesterday_us = now_us - timedelta(1)

# Format the date as 'YYYY-MM-DD'
yesterday_str = yesterday_us.strftime('%Y-%m-%d')

# Fetch the games played yesterday in the US timezone
game_log = LeagueGameLog(date_from_nullable=yesterday_str, date_to_nullable=yesterday_str)

# Get the game data from the response
games = game_log.get_data_frames()[0]

# Get unique game ids
sorted_games = games.sort_values(['GAME_ID'], ascending=True)
game_ids = sorted_games.groupby('GAME_ID').first().reset_index()['GAME_ID']
print(game_ids)

for game_id in game_ids:
    temp_game_box = boxscore.BoxScore(game_id)
    outfile_name = "{game}"
    with open("{}.json".format(game_id), 'w') as out_file:
        json.dump(temp_game_box.game.get_dict(), out_file, indent=4)

# game_data = []
# for game_id in game_ids:
#     temp_game_box = boxscore.BoxScore(game_id)
#     game_data.append(temp_game_box.game.get_dict())
#     df_game = pd.DataFrame(temp_game_box.game.get_dict())
#     df_game.to_csv("{gameid}.csv".format(game_id))