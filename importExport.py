import json
import sys
import os

from nba_api.stats.static import players

fix_ascii = {
    "Č": "C",
    "ć": "c",
    "č": "c",
    "ū": "u",
    "ö": "o",
    "í": "i",
    "Ş": "S",
    "Š": "S",
    "ü": "u",
    "é": "e",
    "ņ": "n",
    "ñ": "n",
    "ģ": "g",
    "A.J.": "AJ",
    "Xavier Tillman Sr.": "Xavier Tillman",
    "P.J. Washington Jr.": "P.J. Washington"
    # ".": ""
}

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
        return data
    except IOError:
        data = {}
        data['season-year'] = 2024
        data['mode'] = 'nba'
        # data['date'] = []
        # data['scoring'] = []
        # data['thresholds'] = []
        # data['oauth'] = []
        data['date'] = {'Month': 9,'Day': 28,'Year': 2024}
        data['scoring'] = {'Points': 1,'Rebounds': 1.2,'Assists': 1.5,'Steals': 3,'Blocks': 3,'Turnovers': -1}
        data['thresholds'] = {'YahooOwnership%Maximum': 70,'WeightedScoreMinimum': 18}
        data['oauth'] = {'consumer_key': "", 'consumer_secret': ""}
        with open('settings.json', 'w') as outfile:
            json.dump(data, outfile, indent=4)
        sys.exit("Settings file didn't exist so now you need to file in api key and secret")

def convertAscii(default_name):
    temp_name = default_name
    for k,v in fix_ascii.items():
        temp_name = temp_name.replace(k,v)
    # print(temp_name)
    return temp_name

def getPlayerIDs(currentLeague):
        try:
            with open('players.json', 'r', encoding='utf-8') as f:
                f.seek(0, os.SEEK_END)
                size = f.tell()
                if size == 0:
                    print("Filesize = 0 attemping to create players.json")
                    raise FileNotFoundError('File is empty.')
                print("Players loaded!")
                f.seek(0)
                return json.load(f)
        except FileNotFoundError:
            print("Attempting to create PlayerIDs file...")
            with open('players.json', 'a', encoding='utf-8') as a:
                yahoo_api_players = {}
                for i in currentLeague.taken_players():
                    try:
                        # yahoo_api_players =.setdefault(i['player_id'], {"name": ""})

                        yahoo_api_players = yahoo_api_players | { i['player_id']: { 'name': i['name'], 'yahoo_id': i['player_id'] } }
                        # yahoo_api_players.append({i['player_id']:  )
                        print(f"{i['player_id']}:  {i['name']}")
                        # f.write(f'{i["player_id"]}\n')
                    except RuntimeError:
                        continue
                for i in currentLeague.free_agents('Util'):
                    try:
                        yahoo_api_players = yahoo_api_players | { i['player_id']: { 'name': i['name'], 'yahoo_id': i['player_id'] } }
                        # yahoo_api_players.setdefault(i['player_id'], {"name": ""})
                        # yahoo_api_players[i['player_id']].name = i['name']
                        # yahoo_api_players.append(i['player_id'])
                        print(f"{i['player_id']}:  {i['name']}")
                        # f.write(f'{i["player_id"]}\n')
                    except RuntimeError:
                        continue
                # print(yahoo_api_players)
                # yahoo_api_players = list(set(yahoo_api_players))
                
                # yahoo_api_players.sort()
                nba_api_players = players.get_players()
                print(yahoo_api_players)
                for index, player in enumerate(nba_api_players):
                    yahoo_player = [x for x in yahoo_api_players.values() if x.get("name") is not None and player['full_name'] == convertAscii(x["name"])]
                    if len(yahoo_player) < 1:
                        continue
                    elif len(yahoo_player) > 1:
                        print(f'Found multiple players for: {player}')
                    else:
                        yahoo_player = yahoo_player[0]
                    if yahoo_api_players.get(yahoo_player['yahoo_id'], False) != False:
                        yahoo_api_players[yahoo_player['yahoo_id']].setdefault("nba_api", player['id'])
                # print(yahoo_api_players)
                a.write(json.dumps(yahoo_api_players, indent=4, ensure_ascii=False))
                # for item in yahoo_api_players:
                #     f.write(f'{item}\n')
                print("PlayerIDs created successfully!")
                return yahoo_api_players
                sys.exit("Players Loaded successfully please restart the script!")

def exportReddit(currentDate,passedList):
    count = 0
    with open('exportReddit.txt', 'w', encoding='utf-8') as f:
        print("exportReddit Loaded!")
        f.write(f'{currentDate} NBA GEMS\n\n')
        for item in passedList:
            item = item.replace("** **"," ")
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
        f.write(f'\nnbaGemsScript written by u/AuToMaTiCx88')
        


if __name__ == "__main__":
    importSettings()
