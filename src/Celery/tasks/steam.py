from Extensions.Parsers.steam_parse import SteamParser

from celery import Celery
from flask import Flask
import requests

app = Flask(__name__)
app.config.update(
    CELERY_BROKER_URL='redis://localhost:8000/0',
    CELERY_RESULT_BACKEND='redis://localhost:8000/0'
)
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

@app.route('/user_profile', methods=['GET'])
def get_user_profile():
    # Get the user's Steam ID from the query parameter
    steam_id = request.args.get('steam_id')

    # Call the Steam API to retrieve the user's profile information
    api_url = f'https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=<your_api_key>&steamids={steam_id}'
    response = requests.get(api_url)

    # Parse the JSON response and return the user's profile information as a JSON object
    data = response.json()
    profile = data['response']['players'][0]
    return {
        'steam_id': profile['steamid'],
        'username': profile['personaname'],
        'avatar': profile['avatarfull'],
        'profile_url': profile['profileurl'],
        'last_logoff': profile['lastlogoff']
    }

@celery.task
def sync_user_profile(steam_id):
    with app.app_context():
        # Retrieve the user's profile information
        profile = get_user_profile(steam_id)

        # TODO: Add code to sync the user's profile to your application's database

if __name__ == '__main__':
    app.run(debug=True)




