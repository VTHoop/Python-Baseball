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

batter_splits = {
            31: 'vL',
            32: 'vR',
            33: 'Home',
            34: 'Away'}

pitcher_splits = {
            33: 'Home',
            34: 'Away'}


def get_wOBA(bb, hits, doubles, triples, hr, ab):
    if (ab+bb) == 0:
        return 0
    else:
        return (.69*bb +
                (.89* hits-doubles-triples-hr) +
                1.27*doubles + 1.62*triples + 2.1*hr)\
                / (ab + bb)


def extract_batter_data():

    batter_split = []

    for t in teams.keys():
        for s in batter_splits.keys():
            link = "http://www.espn.com/mlb/team/stats/batting/_/name/"+t+"/split/"+str(s)
            page = urllib2.urlopen(link)

            soup = BeautifulSoup(page, "lxml")
            table = soup.find('table', attrs={'class': 'tablehead'})

            rows = table.find_all('tr')[2:-2]
            for row in rows:
                d = {
                    "lookup": None,
                    "wOBA_away": None,
                    "wOBA_home": None,
                    "wOBA_vL": None,
                    "wOBA_vR": None
                }

                col = row.find_all('td')

                bb = int(col[10].string.strip())
                hits = int(col[4].string.strip())
                doubles = int(col[5].string.strip())
                triples = int(col[6].string.strip())
                hr = int(col[7].string.strip())
                ab = int(col[2].string.strip())
                lookup = str(col[0].text.encode('ascii', 'ignore').strip()) + '-' + teams[t]
                wOBA = get_wOBA(bb, hits, doubles, triples, hr, ab)

            # Create a variable of the value of the columns
                d = {
                       "wOBA_"+str(batter_splits[s]): wOBA,
                       'lookup': lookup
                }
                batter_split.append(d)

    df = pd.DataFrame(batter_split)
    df = df.groupby(['lookup'], as_index=True).sum()

    return df

def extract_pitcher_data():

    pitcher_split = []

    for t in teams.keys():
        for s in pitcher_splits.keys():

            link = "http://www.espn.com/mlb/team/stats/pitching/_/name/"+t+"/split/"+str(s)
            page = urllib2.urlopen(link)

            soup = BeautifulSoup(page, "lxml")
            table = soup.find('table', attrs={'class': 'tablehead'})

            rows = table.find_all('tr')[2:-2]
            for row in rows:
                d = {
                    "lookup": None,
                    "whip_away": None,
                    "whip_home": None
                }
                col = row.find_all('td')

                # Create a variable of the value of the columns
                d = {
                    "lookup": str(col[0].text.encode('ascii', 'ignore').strip()) + '-' + teams[t],
                    "whip_"+str(pitcher_splits[s]): float(col[15].string.strip())
                }
                pitcher_split.append(d)
    df = pd.DataFrame(pitcher_split)
    df = df.groupby(['lookup'], as_index=True).sum()
    return df


def update_batter_splits():
    batter_espn = extract_batter_data()
    batter_espn.to_csv('batter_splits.csv')


def update_pitcher_splits():
    pitcher_espn = extract_pitcher_data()
    pitcher_espn.to_csv('pitcher_splits.csv')
