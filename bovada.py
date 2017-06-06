import urllib
from xml.etree import ElementTree as ET


def get_run_lines():
    requestURL = 'http://sportsfeeds.bovada.lv/basic/MLB.xml'

    root = ET.parse(urllib.urlopen(requestURL)).getroot()

    games = []

    events = root.findall('./EventType/Date/Event')

    for event in events:
        if event.attrib['COMPETITION'] == 'Baseball - MLB':
            game_data = {
                'game_lookup': None,
                'home_team': None,
                'home_team_line': None,
                'away_team': None,
                'away_team_line': None,
                'run_total': None
            }
            teams = event.findall('Competitor')
            for team in teams:
                if team.attrib['NUM'] == '1':
                    game_data['home_team'] = team.attrib['NAME']
                    if team.find('./Line/Choice/Odds') is not None:
                        game_data['home_team_line'] = team.find('./Line/Choice/Odds').attrib['Line']
                    else:
                        game_data['home_team_line'] = 'None'
                elif team.attrib['NUM'] == '2':
                    game_data['away_team'] = team.attrib['NAME']
                    if team.find('./Line/Choice/Odds') is not None:
                        game_data['away_team_line'] = team.find('./Line/Choice/Odds').attrib['Line']
                    else:
                        game_data['away_team_line'] = 'None'
            game_data['game_lookup'] = game_data['away_team'] + ' @ ' + game_data['home_team']
            run = event.find('./Line/Choice')
            if run is not None:
                if isinstance(run.attrib['NUMBER'], str):
                    game_data['run_total'] = float(run.attrib['NUMBER'])
                else:
                    game_data['run_total'] = float(run.attrib['NUMBER'][:-1] + '.5')
            else:
                game_data['run_total'] = None
            games.append(game_data)

    return games
