import json

from yahoo_oauth import OAuth2


def connect(credentials):
    def noToken():
        with open('oauth2.json', 'w') as f:
            f.write(json.dumps(credentials))
        return OAuth2(None, None, from_file='oauth2.json')

    def checkValidOrRefreshToken():
        return OAuth2(None, None, from_file='oauth2.json')

    try:  # Check if oauth2 file exists if it does open oauth with the file
        fileExistCheck = open('oauth2.json')
        return checkValidOrRefreshToken()
    except IOError:  # if file does not exist run connection manager and create a token
        return noToken()
