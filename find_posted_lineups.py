from bs4 import BeautifulSoup
import urllib2

link = "http://www.rotowire.com/baseball/daily_lineups.htm"
page = urllib2.urlopen(link)

soup = BeautifulSoup(page, "lxml")


def get_posted_lineups():
    lineups = soup.find_all('div', attrs={'class': 'span15 dlineups-mainbox'})

    # teams with lineups
    twl = []

    for l in lineups:
        mainbar = l.find('div', attrs={'class': 'span15 dlineups-mainbar'})
        away = mainbar.find('div', attrs={'class': 'dlineups-mainbar-away'})
        home = mainbar.find('div', attrs={'class': 'dlineups-mainbar-home'})
        awayteam = away.find('a')
        # just return the team abbreviation found in the parameters of the link
        at = awayteam['href'][(len(awayteam['href'])-awayteam['href'].find('=')-1)*-1:]
        hometeam = home.find('a')
        # just return the team abbreviation found in the parameters of the link
        ht = hometeam['href'][(len(hometeam['href'])-hometeam['href'].find('=')-1)*-1:]
        # t = teams['href'][(len(teams['href'])-teams['href'].find('=')-1)*-1:]

        if not l.find_all('div', attrs={'class': 'dlineups-empty'}):
            twl.append(at + "@" + ht)

    return twl

get_posted_lineups()
