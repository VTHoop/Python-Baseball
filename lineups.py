from __future__ import division
import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'

#send_stats_request()

off_proj_weight = .5
off_location_weight = .2
off_hand_weight = .2
off_season_weight = .1

pit_season_weight = .2
pit_proj_weight = .5
pit_location_weight = .3


# home_starter_id = 10259
# away_starter_id = 11014


def get_wOBA(df):
    return (.69*df['#BatterWalks']+.72*df['#HitByPitch'] +
            .89*(df['#Hits']-df['#SecondBaseHits']-df['#ThirdBaseHits']-df['#Homeruns'])
            + 1.27*df['#SecondBaseHits'] + 1.62*df['#ThirdBaseHits'] + 2.1*df['#Homeruns'])\
           / (df['#AtBats'] + df['#BatterWalks'] + df['#HitByPitch'] + df['#BatterSacrificeFlies'])


def get_WHIP(df):
    return (df['#HitsAllowed'] + df['#PitcherWalks']) / df['#InningsPitched']


def home_team_off_stats(player_df, home_team_lineup, away_starter_id):
    # home_team_lineup = player_df[player_df['#Team Abbr.'] == team]\
    #                       .sort_values(by='#GamesPlayed', ascending=False)[0:9]['#Player ID']

    # home_team_lineup = [10265,10267,10272,10268,10275,10270,11374,10878,10269]
    home_team_stats = player_df[player_df['#Player ID'].isin(home_team_lineup)]
    home_team_stats['#wOBA'] = get_wOBA(home_team_stats)
    home_team_stats['#proj_wOBA'] = home_team_stats['#proj_wOBA'].fillna(home_team_stats['#wOBA'])

    #print home_team_stats

    ###if you want to overwrite pct_weight with amount of season played so far
    #pct_weight = (home_team_stats['#GamesPlayed'].max()/162)

    season_wOBA = (off_season_weight * home_team_stats['#wOBA'].mean())
    proj_wOBA = (off_proj_weight * home_team_stats['#proj_wOBA'].mean())
    location_wOBA = (off_location_weight * home_team_stats['wOBA_Home'].mean())

    if player_df[player_df['#Player ID'] == away_starter_id].throws.item() == 'L':
        hand_wOBA = (off_hand_weight * home_team_stats['wOBA_vL'].mean())
    else:
        hand_wOBA = (off_hand_weight * home_team_stats['wOBA_vR'].mean())
    
    return season_wOBA + proj_wOBA + location_wOBA + hand_wOBA


def away_team_off_stats(player_df, away_team_lineup, home_starter_id):
    # away_team_lineup = player_df[player_df['#Team Abbr.'] == team]\
    #                       .sort_values(by='#GamesPlayed', ascending=False)[0:9]['#Player ID']

    # away_team_lineup = [11025,11027,11077,11078,11023,11315,11075,11076,11370]
    away_team_stats = player_df[player_df['#Player ID'].isin(away_team_lineup)]
    away_team_stats['#wOBA'] = get_wOBA(away_team_stats)
    away_team_stats['#proj_wOBA'] = away_team_stats['#proj_wOBA'].fillna(away_team_stats['#wOBA'])
    # print(away_team_stats)

    # ##if you want to overwrite pct_weight with amount of season played so far
    # pct_weight = (away_team_stats['#GamesPlayed'].max()/162)

    season_wOBA = (off_season_weight * away_team_stats['#wOBA'].mean())
    proj_wOBA = (off_proj_weight * away_team_stats['#proj_wOBA'].mean())
    location_wOBA = (off_location_weight * away_team_stats['wOBA_Away'].mean())
    if player_df[player_df['#Player ID'] == home_starter_id].throws.item() == 'L':
        hand_wOBA = (off_hand_weight * away_team_stats['wOBA_vL'].mean())
    else:
        hand_wOBA = (off_hand_weight * away_team_stats['wOBA_vR'].mean())

    return season_wOBA + proj_wOBA + location_wOBA + hand_wOBA


def home_team_pit_stats(player_df, home_team, home_starter_id):
    # starter statistics

    avg_inn = 6

    home_team_starter = player_df[player_df['#Player ID'] == home_starter_id]
    # if lookup is not found in FanGraphs projected stats than Projected will equal true WHIP
    home_team_starter['#proj_WHIP'] = home_team_starter['#proj_WHIP'].\
        fillna(home_team_starter['#WalksAndHitsPerInningPitched'])

    # print(home_team_starter.loc[:, ['lookup_x', '#WalksAndHitsPerInningPitched', '#proj_WHIP', 'whip_Home', 'throws']])

    starter_season_whip = (pit_season_weight * home_team_starter['#WalksAndHitsPerInningPitched'].mean()) * avg_inn/9
    starter_proj_whip = (pit_proj_weight * home_team_starter['#proj_WHIP'].mean()) * avg_inn/9
    starter_location_whip = pit_location_weight * home_team_starter['whip_Home'].mean() * avg_inn/9

    starter_whip = starter_season_whip + starter_proj_whip + starter_location_whip

    # player with less than 2 innings pitched per game on average are considered to be part of bullpen
    bp_p_df = player_df[
        (player_df['#Position'] == 'P') &
        (player_df['#InningsPitched'] / player_df['#GamesPlayed'] < 2) &
        (player_df['#Team Abbr.'] == home_team)]

    # individual pitcher's "Importance Factor" is Innings Pitched / Team Bullpen Innings
    bp_p_df['ImpFac'] = bp_p_df['#InningsPitched'] / bp_p_df['#InningsPitched'].sum()

    # if lookup is not found in FanGraphs projected stats than Projected will equal true WHIP
    bp_p_df['#proj_WHIP'] = bp_p_df['#proj_WHIP'].fillna(bp_p_df['#WalksAndHitsPerInningPitched'])

    # combine true season stats, projected status, and home/away splits
    bp_season_whip = (pit_season_weight *
                      ((bp_p_df['#WalksAndHitsPerInningPitched'] * bp_p_df['ImpFac']).sum() * (9-avg_inn)/9))
    bp_proj_whip = (pit_proj_weight *
                    ((bp_p_df['#proj_WHIP'] * bp_p_df['ImpFac']).sum() * (9-avg_inn)/9))
    bp_location_whip = (pit_location_weight *
                        ((bp_p_df['whip_Home'] * bp_p_df['ImpFac']).sum() * (9 - avg_inn) / 9))

    bp_whip = bp_season_whip + bp_proj_whip + bp_location_whip

    # print(bp_p_df.loc[:, ['lookup_x', '#WalksAndHitsPerInningPitched', '#proj_WHIP', 'whip_Home']])

    return starter_whip, bp_whip


def away_team_pit_stats(player_df, away_team, away_starter_id):
    # starter statistics

    avg_inn = 6

    away_team_starter = player_df[player_df['#Player ID'] == away_starter_id]
    # if lookup is not found in FanGraphs projected stats than Projected will equal true WHIP
    away_team_starter['#proj_WHIP'] = away_team_starter['#proj_WHIP']. \
        fillna(away_team_starter['#WalksAndHitsPerInningPitched'])

    # combine true season stats, projected status, and home/away splits
    starter_season_whip = (pit_season_weight * away_team_starter['#WalksAndHitsPerInningPitched'].mean()) * avg_inn / 9
    starter_proj_whip = (pit_proj_weight * away_team_starter['#proj_WHIP'].mean()) * avg_inn / 9
    starter_location_whip = pit_location_weight * away_team_starter['whip_Home'].mean() * avg_inn / 9

    starter_whip = starter_season_whip + starter_proj_whip + starter_location_whip

    # player with less than 2 innings pitched per game on average are considered to be part of bullpen
    bp_p_df = player_df[
        (player_df['#Position'] == 'P') &
        (player_df['#InningsPitched'] / player_df['#GamesPlayed'] < 2) &
        (player_df['#Team Abbr.'] == away_team)]

    # individual pitcher's "Importance Factor" is Innings Pitched / Team Bullpen Innings
    bp_p_df['ImpFac'] = bp_p_df['#InningsPitched'] / bp_p_df['#InningsPitched'].sum()

    # if lookup is not found in FanGraphs projected stats than Projected will equal true WHIP
    bp_p_df['#proj_WHIP'] = bp_p_df['#proj_WHIP'].fillna(bp_p_df['#WalksAndHitsPerInningPitched'])

    # combine true season stats, projected status, and home/away splits
    bp_season_whip = (pit_season_weight *
                      ((bp_p_df['#WalksAndHitsPerInningPitched'] * bp_p_df['ImpFac']).sum() * (9 - avg_inn) / 9))
    bp_proj_whip = (pit_proj_weight *
                    ((bp_p_df['#proj_WHIP'] * bp_p_df['ImpFac']).sum() * (9 - avg_inn) / 9))
    bp_location_whip = (pit_location_weight *
                        ((bp_p_df['whip_Away'] * bp_p_df['ImpFac']).sum() * (9 - avg_inn) / 9))

    bp_whip = bp_season_whip + bp_proj_whip + bp_location_whip

    # print(bp_p_df.loc[:, ['lookup_x', '#WalksAndHitsPerInningPitched', '#proj_WHIP', 'whip_Away']])

    return starter_whip, bp_whip
