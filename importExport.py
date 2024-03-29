import json
import sys


def getIgnoreList():
        with open('ignoreList.txt', 'r') as f:
            ignoreIDs = f.read().splitlines()
            print("IgnoreList Loaded!")
        return set(ignoreIDs)

def importSettings():
    try:
        with open('settings.json','r') as json_file:
            data = json.load(json_file)
            print("Settings loaded!")
        return data['season-year'],data['mode'],data['date'][0], data['scoring'][0], data['thresholds'][0]
    except IOError:
        data = {}
        data['season-year'] = 2022
        data['mode'] = 'nba'
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
            with open('playerIDs.json') as f:
                print("PlayerIDs loaded!")
                return json.load(f)
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
    count = 0
    with open('exportReddit.txt', 'w') as f:
        print("exportReddit Loaded!")
        f.write(f'{currentDate} NBA GEMS\n\n')
        for item in passedList:
            if count % 5 == 4:
                if(count != len(passedList) - 1):
                    f.writelines([f'{item}', '\n'])
                    f.writelines(['\\', '\n','&nbsp;', '\n\n'])
                else:
                    f.writelines([f'{item}', '\n'])
            else:
                if(count != len(passedList) - 1):
                    f.write(f'{item}\n\n')
                else:
                    f.write(f'{item}\n')
            count += 1
        f.writelines(['\\', '\n','&nbsp;', '\n'])
        f.write(f'\nGet the next newsletter at www.sendfox.com/nbagems\n')
        f.writelines(['\\', '\n','&nbsp;', '\n'])
        f.writelines(['\\', '\n','&nbsp;', '\n'])
        f.write(f'\n[nbaGemsScript](https://github.com/JordanBradshaw/nbaGemsScript) written by u/AuToMaTiCx88')


if __name__ == "__main__":
    importSettings()
