import json
import sys


def importSettings():
    try:
        with open('settings.json','r') as json_file:
            data = json.load(json_file)
        return data['date'][0], data['scoring'][0], data['thresholds'][0], data['oauth'][0]
    except IOError:
        data = {}
        data['date'] = []
        data['scoring'] = []
        data['thresholds'] = []
        data['oauth'] = []
        data['date'].append({'Month': 12,'Day': 4,'Year': 2021})
        data['scoring'].append({'Points': 1,'Rebounds': 1.2,'Assists': 1.5,'Steals': 3,'Blocks': 3,'Turnovers': -1})
        data['thresholds'].append({'YahooOwnership%Maximum': 80,'WeightedScoreMinimum': 18})
        data['oauth'].append({'consumer_key': "", 'consumer_secret': ""})
        with open('settings.json', 'w') as outfile:
            json.dump(data, outfile, indent=4)
        sys.exit("Settings file didn't exist so now you need to file in api key and secret")


if __name__ == "__main__":
    importSettings()
