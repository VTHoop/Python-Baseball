import base64
import requests

pull_games_url = "https://www.mysportsfeeds.com/api/feed/pull/mlb/current/overall_team_standings.csv"
username = "snohooper"
password = "VTinACC06"


def send_team_request():

    # Request

    try:
        response = requests.get(
            url=pull_games_url,
            params={
                #"fordate": "20161121"
            },
            headers={
                "Authorization": "Basic " + base64.b64encode(username + ":" + password)
            }
        )
        print('Response HTTP Status Code: {status_code}'.format(
            status_code=response.status_code))
        #print('Response HTTP Response Body: {content}'.format(
        #    content=response.content))
        with open('teams.csv', 'wb') as f:
            f.write(response.text)
    except requests.exceptions.RequestException:
        print('HTTP Request failed')