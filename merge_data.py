def add_run_line(games_df, run_line_df):

    games_df['game_lookup'] = games_df['#Away Team City'] + ' ' + games_df['#Away Team Name'] \
                              + ' @ ' + games_df['#Home Team City'] + ' ' + games_df['#Home Team Name']

    return games_df.merge(run_line_df, left_on='game_lookup', right_on='game_lookup')


def add_projected_stats(player_df, batter_proj_df, pitcher_proj_df):

    batter_proj_df['#player_lookup'] = batter_proj_df['Name'] + '-' + batter_proj_df['Team']
    pitcher_proj_df['#player_lookup'] = pitcher_proj_df['Name'] + '-' + pitcher_proj_df['Team']

    # merge projection files
    batter_proj_df = batter_proj_df.loc[:, ['#player_lookup', 'wOBA']]
    batter_proj_df = batter_proj_df.rename(index=str, columns={"#player_lookup": "#player_lookup", "wOBA": "#proj_wOBA"})
    player_df = player_df.merge(batter_proj_df, how='left', left_on="#player_lookup", right_on="#player_lookup")

    pitcher_proj_df = pitcher_proj_df.loc[:, ['#player_lookup', 'WHIP']]
    pitcher_proj_df = pitcher_proj_df.rename(index=str, columns={"#player_lookup": "#player_lookup", "WHIP": "#proj_WHIP"})
    return player_df.merge(pitcher_proj_df, how='left', left_on="#player_lookup", right_on="#player_lookup")


def add_split_stats(player_df, batter_splits_df, pitcher_splits_df):
    player_df = player_df.merge(batter_splits_df, how='left', left_on="#player_lookup", right_on="lookup")
    return player_df.merge(pitcher_splits_df, how='left', left_on="#player_lookup", right_on="lookup")


def add_pitcher_throws(player_df, pitcher_info_df):
    return player_df.merge(pitcher_info_df, how='left', left_on="#player_lookup", right_on="lookup")
