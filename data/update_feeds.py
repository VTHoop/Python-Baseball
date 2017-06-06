from espn_splits import update_batter_splits, update_pitcher_splits
from games import send_games_request
from player_basics import get_player_basics
from player_main_stats import send_stats_request
from team_main_stats import send_team_request

#get updated files

send_stats_request()
send_games_request()
send_team_request()
update_batter_splits()
update_pitcher_splits()

get_player_basics()
