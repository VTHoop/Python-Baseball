def total_run_count(team_df):

    #send_team_request()

    run_baseline = (team_df['#Runs']/team_df['#GamesPlayed']).mean()
    return run_baseline


def league_avg_wOBA(team_df):

    team_wOBA = (.69*team_df['#BatterWalks']+.72*team_df['#HitByPitch'] +\
            .89*(team_df['#Hits']-team_df['#SecondBaseHits']-team_df['#ThirdBaseHits']-team_df['#Homeruns'])\
            + 1.27*team_df['#SecondBaseHits'] + 1.62*team_df['#ThirdBaseHits'] + 2.1*team_df['#Homeruns'])\
           / (team_df['#AtBats'] + team_df['#BatterWalks'] + team_df['#HitByPitch']\
              + team_df['#BatterSacrificeFlies'])

    return team_wOBA.mean()

def league_avg_WHIP(team_df):

    return team_df['#WalksAndHitsPerInningPitched'].mean()

