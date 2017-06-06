import base64
import requests
import datetime as dt
import os.path
import pandas as pd


pull_games_url = "https://www.mysportsfeeds.com/api/feed/pull/mlb/current/daily_game_schedule.csv"
username = "snohooper"
password = "VTinACC06"
today_date = dt.date.today().strftime("%Y%m%d")

path = 'games.csv'

def send_games_request():
    # Request
    if today_date != get_modified_date():
        try:
            response = requests.get(
                url=pull_games_url,
                params={
                    #"team": "stl"
                    "fordate": today_date
                },
                headers={
                    "Authorization": "Basic " + base64.b64encode(username + ":" + password)
                }
            )
            print('Response HTTP Status Code: {status_code}'.format(
                status_code=response.status_code))
            #print('Response HTTP Response Body: {content}'.format(
            #    content=response.content))

            with open(path, 'wb') as f:
                f.write(response.text)
                f.close()

            games_df = pd.read_csv('games.csv')
            games_df['analyzed'] = 0
            games_df.to_csv('games.csv', index=False)

            #return response.text
        except requests.exceptions.RequestException:
            print('HTTP Request failed')


def get_modified_date():
    return dt.datetime.fromtimestamp(os.path.getmtime(path)).strftime("%Y%m%d")

send_games_request()



