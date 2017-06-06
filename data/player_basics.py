from bs4 import BeautifulSoup
import urllib2
import pandas as pd

teams = {
        'ARI': 'Diamondbacks',
        'ATL': 'Braves',
        'BAL': 'Orioles',
        'BOS': 'Red Sox',
        'CHC': 'Cubs',
        'CIN': 'Reds',
        'CLE': 'Indians',
        'COL': 'Rockies',
        'CHW': 'White Sox',
        'DET': 'Tigers',
        'HOU': 'Astros',
        'KC': 'Royals',
        'LAA': 'Angels',
        'LAD': 'Dodgers',
        'MIA': 'Marlins',
        'MIL': 'Brewers',
        'MIN': 'Twins',
        'NYM': 'Mets',
        'NYY': 'Yankees',
        'OAK': 'Athletics',
        'PHI': 'Phillies',
        'PIT': 'Pirates',
        'SD': 'Padres',
        'SEA': 'Mariners',
        'SF': 'Giants',
        'STL': 'Cardinals',
        'TB': 'Rays',
        'TEX': 'Rangers',
        'TOR': 'Blue Jays',
        'WAS': 'Nationals'
         }


def get_player_basics():
    players = []

    for t in teams.keys():

        link = "http://www.espn.com/mlb/team/roster/_/name/"+t
        page = urllib2.urlopen(link)

        soup = BeautifulSoup(page, "lxml")
        table = soup.find('table', attrs={'class': 'tablehead'})

        rows = table.find_all('tr')[2:]
        for row in rows:
            d = {'lookup': None,
                 'throws': None
                 }
            col = row.find_all('td')

            if len(col) > 1:
                d = {
                    'lookup': col[1].string.strip() + '-' + teams[t],
                    'throws': col[4].string.strip()
                }
                # print(col[1].string.strip())
                # print(col[4].string.strip())
            else:
                break

            players.append(d)

    df = pd.DataFrame(players)
    df.to_csv('pitcher_info.csv')

