import json
import sys


def getIgnoreList():
        with open('IgnorePlayers.txt', 'r') as f:
            ignoreIDs = f.read().splitlines()
            print("IgnoreList Loaded!")
        return set(ignoreIDs)

def importSettings():
    try:
        with open('settings.json','r') as json_file:
            data = json.load(json_file)
            print("Settings loaded!")
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

def getPlayerIDs(currentLeague):
        try:
            with open('PlayerIDs.txt') as f:
                print("PlayerIDs loaded!")
                return f.read().splitlines()
        except FileNotFoundError:
            print("Attempting to create PlayerIDs file...")
            with open('PlayerIDs.txt', 'a') as f:
                setList = []
                for i in currentLeague.taken_players():
                    try:
                        setList.append(i['player_id'])
                        print(f"{i['player_id']}:  {i['name']}")
                        # f.write(f'{i["player_id"]}\n')
                    except RuntimeError:
                        continue
                for i in currentLeague.free_agents('Util'):
                    try:
                        setList.append(i['player_id'])
                        print(f"{i['player_id']}:  {i['name']}")
                        # f.write(f'{i["player_id"]}\n')
                    except RuntimeError:
                        continue
                setList = list(set(setList))
                setList.sort()
                #print(setList)
                for item in setList:
                    f.write(f'{item}\n')
                print("PlayerIDs created successfully!")
                return setList
                sys.exit("Players Loaded successfully please restart the script!")

def exportReddit(currentDate,passedList):
    with open('exportReddit.txt', 'w') as f:
        print("exportReddit Loaded!")
        f.write(f'{currentDate} NBA GEMS\n\n')
        for item in passedList:
            f.write(f'{item}\n\n')
        f.write(f'Get the next newsletter at www.sendfox.com/nbagems\n\n\n\n')
        f.write(f'[nbaGemsScript](https://github.com/JordanBradshaw/nbaGemsScript) written by u/AuToMaTiCx88')


if __name__ == "__main__":
    importSettings()
