import pandas as pd
from math import log
import datetime as dt


from baseline_stats import total_run_count, league_avg_WHIP, league_avg_wOBA
from lineups import home_team_off_stats, home_team_pit_stats, away_team_off_stats, away_team_pit_stats
from merge_data import add_run_line, add_projected_stats, add_split_stats, add_pitcher_throws
from bovada import get_run_lines
from find_posted_lineups import get_posted_lineups
from starting_lineups import send_lineups_request
from choose_bet import choose_bet


def calculate_line(win_pct):
    if win_pct >= .5:
        return "{0:.0f}".format(win_pct/(1 - win_pct) * -100)
    else:
        return "+" + "{0:.0f}".format(((1 - win_pct) / win_pct*100))


def calculate_win_pct(runs_scored, runs_against, run_total):
    #run_total = input('Expected Runs: ')
    exponent = 1.5 * log(run_total) + .45
    home_win_pct = (runs_scored ** exponent) / ((runs_against ** exponent)+(runs_scored ** exponent))
    away_win_pct = (runs_against ** exponent) / ((runs_against ** exponent) + (runs_scored ** exponent))

    home_line = calculate_line(home_win_pct)
    away_line = calculate_line(away_win_pct)
    return home_line, away_line

# create dataframes from all data sources
player_df = pd.read_csv('./data/baseball.csv')
team_df = pd.read_csv('./data/teams.csv')
games_df = pd.read_csv('./data/games.csv')
batter_proj_df = pd.read_csv('./data/batter_proj.csv')
pitcher_proj_df = pd.read_csv('./data/pitcher_proj.csv')
batter_splits_df = pd.read_csv('./data/batter_splits.csv')
pitcher_splits_df = pd.read_csv('./data/pitcher_splits.csv')
pitcher_info_df = pd.read_csv('./data/pitcher_info.csv')
model_log_df = pd.read_csv('./data/model_log.csv')
run_line_df = pd.DataFrame(get_run_lines())
twl = get_posted_lineups()



# create fullname field to merge season player statistics (baseball.csv) with projection file (batter_proj.csv)
player_df['#player_lookup'] = player_df['#FirstName'] + ' ' + player_df['#LastName'] + '-' + player_df['#Team Name']


# take run_line from bovada file and merge into games
games_df = add_run_line(games_df, run_line_df)

# take projected stats from FanGraphs and merge into players
player_df = add_projected_stats(player_df, batter_proj_df, pitcher_proj_df)

# add split stats gathered from ESPN
player_df = add_split_stats(player_df, batter_splits_df, pitcher_splits_df)

# add pitcher info from ESPN
player_df = add_pitcher_throws(player_df, pitcher_info_df)

# get league baseline statistics
baseline_runs = total_run_count(team_df)
baseline_wOBA = league_avg_wOBA(team_df)
baseline_WHIP = league_avg_WHIP(team_df)

games_updated = 0

for i, row in games_df.iterrows():
    if games_df.loc[i, 'analyzed'] == 0:
        if games_df.loc[i, '#Away Team Abbr.'] + "@" + games_df.loc[i, '#Home Team Abbr.'] in twl:
            away_pitcher_id, home_pitcher_id, away_lineup, home_lineup = send_lineups_request(
                games_df.loc[i, '#Away Team Abbr.'], games_df.loc[i, '#Home Team Abbr.'])
            # print(player_df[player_df['#Player ID'] == int(away_pitcher_id)])
            # get offensive and pitching ratings for both teams
            home_off_rating = home_team_off_stats(player_df, home_lineup, away_pitcher_id) \
                              / baseline_wOBA

            home_starter_whip, home_bp_whip = home_team_pit_stats(player_df, games_df.loc[i:'#Home Team Abbr.'],
                                                                  home_pitcher_id)
            home_pit_rating = (home_starter_whip + home_bp_whip) / baseline_WHIP

            # print(home_starter_whip, home_bp_whip)

            away_off_rating = away_team_off_stats(player_df, away_lineup, home_pitcher_id) \
                              / baseline_wOBA

            away_starter_whip, away_bp_whip = away_team_pit_stats(player_df, games_df.loc[i:'#Away Team Abbr.'],
                                                                  away_pitcher_id)
            away_pit_rating = (away_starter_whip + away_bp_whip) / baseline_WHIP

            # print(home_off_rating, home_pit_rating)
            # print(away_off_rating, away_pit_rating)

            # calculate run totals off of power ratings
            home_run_total = home_off_rating * away_pit_rating * baseline_runs
            away_run_total = away_off_rating * home_pit_rating * baseline_runs

            # print(home_run_total, away_run_total)

            # calculate betting line
            home_model_line, away_model_line = calculate_win_pct(home_run_total, away_run_total,
                                                                 games_df.loc[i, 'run_total'])

            decision, fav_dog, difference, bet_amount\
                = choose_bet(int(games_df.loc[i, 'home_team_line']), int(home_model_line),
                             int(games_df.loc[i, 'away_team_line']), int(away_model_line))

            result_cols = {
                        'Date': dt.date.today().strftime("%m/%d/%Y"),
                        'Home_Team': games_df.loc[i, '#Home Team Abbr.'],
                        'Home_Vegas_Line': games_df.loc[i, 'home_team_line'],
                        'Home_Model_Line': home_model_line,
                        'Away_Team': games_df.loc[i, '#Away Team Abbr.'],
                        'Away_Vegas_Line': games_df.loc[i, 'away_team_line'],
                        'Away_Model_Line': away_model_line,
                        'Model_Decision': decision,
                        'Fav_Dog': fav_dog,
                        'Difference': difference,
                        'Bet_Amount': bet_amount
            }

            result_df = pd.DataFrame(result_cols, index=[0])

            model_log_df = pd.concat([model_log_df, result_df])
            model_log_df.to_csv('./data/model_log.csv', index=False)

            games_df.loc[i, 'analyzed'] = 1
            games_updated += 1


del games_df['game_lookup']
del games_df['away_team']
del games_df['away_team_line']
del games_df['home_team']
del games_df['home_team_line']
del games_df['run_total']

games_df.to_csv('./data/games.csv', index=False)

print("Games Updated to Log: " + str(games_updated))
# display games to user and allow to choose which one for line
# print(games_df[['#Away Team Abbr.', '#Home Team Abbr.']])
# game_id = input('Enter Game ID: ')

# print(player_df[(player_df['#Team Abbr.'] == games_df.loc[game_id, '#Home Team Abbr.']) &
#                 (player_df['#Position'] == 'P')].loc[:, ['#Player ID', '#FirstName', "#LastName", "#InningsPitched"]]
#       .sort_values(by="#InningsPitched", ascending=False))
#
# home_pitcher_id = input('Enter Home Pitcher ID: ')
#
# print(player_df[(player_df['#Team Abbr.'] == games_df.loc[game_id, '#Away Team Abbr.']) &
#                 (player_df['#Position'] == 'P')].loc[:, ['#Player ID', '#FirstName', "#LastName", "#InningsPitched"]]
#       .sort_values(by="#InningsPitched", ascending=False))
#
# away_pitcher_id = input('Enter Away Pitcher ID: ')



# print(baseline_WHIP)


