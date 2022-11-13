import argparse
import datetime
import json
import time

import nba_api
import pandas as pd
import yahoo_fantasy_api as yfa
from nba_api.stats.endpoints import playergamelog
from nba_api.stats.static import players
from yahoo_oauth import OAuth2

import importExport as iE
from cli import cli as cli
from yahooConnect import connect
from yahooLeague import yahooLeague as yahooLeague

#print(playergamelog.PlayerGameLog(player_id=202683,date_from_nullable = "10/19/2022", date_to_nullable = "10/19/2022"))
playerExceptions = {'Enes Freedom': 202683, 'Cameron Thomas': 1630560,'PJ Washington': 1629023,'Xavier Tillman': 1630214, 'Bones Hyland': 1630538, 'Guillermo Hernangómez': 1626195}
calcScore = lambda x: (x['PTS'] * 1) + (x['REB'] * 1.2 )+ (x['AST'] * 1.5) + (x['ST'] * 3) + (x['BLK'] * 3) + (x['TO'] * -1)
customFilter = lambda x: (x['PTS'] * 1) + (x['REB'] * 1.2 )+ (x['AST'] * 1.5) + (x['ST'] * 3) + (x['BLK'] * 3) + (x['TO'] * -1) >= weightedScoreMinimum

player_dict = players.get_players()
# Variables
jsonFilter = lambda x: (x['PTS'] * scoring['Points']) + (x['REB'] * scoring['Rebounds'])+ (x['AST'] * scoring['Assists']) + (x['ST'] * scoring['Steals']) + (x['BLK'] * scoring['Blocks']) + (x['TO'] * scoring['Turnovers']) >= weightedScoreMinimum
season,mode,date,scoring,thresholds = iE.importSettings()
oauthDict = {}
with open('oauth.json','r') as oauth_file:
    oauthDict = json.load(oauth_file)
#print(date)
#jsonSettings={}
#with open('settings.json','w+') as f:
#    jsonSettings = json.loads(f)
#season,mode,date,scoring,thresholds,oauthDict = jsonSettings
logDate = datetime.date(date['Year'], date['Month'], date['Day'])
yahooOwnershipMaximum = thresholds['YahooOwnership%Maximum']
weightedScoreMinimum = thresholds['WeightedScoreMinimum']

nbaLogDate = f"{date['Month']}/{date['Day']}/{date['Year']}"
#apiID = 1629655
#playergamelog.PlayerGameLog(player_id=apiID,season = '2022',season_type_all_star = 'Regular Season',date_from_nullable = nbaLogDate, date_to_nullable = nbaLogDate)
#print(players.get_players())

def nbaGemsScript():
    #ignoreList = iE.getIgnoreList()
    # Setup up connection to yahoo and select NBA
    oauth = connect(oauthDict)
    sport = yfa.Game(oauth, 'nba')
    possibleLeagues = sport.league_ids(year=season)
    temp2 = cli(oauth)
    leagueIndex = temp2.chooseLeague(len(possibleLeagues)-1, possibleLeagues)
    currentLeague = sport.to_league(possibleLeagues[leagueIndex])
    temp = yahooLeague(currentLeague)
    playerIDs = iE.getPlayerIDs(currentLeague)
    #playerIDs = [int(i) for i in playerIDs]
    #json_object = {}
    #for player in currentLeague.taken_players():
    #    json_object[player['player_id']] = {
    #        'name' : player['name']
    #    }
    #for position in ['PG','SG','SF','PF','C']:
    #    for player in currentLeague.free_agents(position):
    #        json_object[player['player_id']] = {
    #        'name' : player['name']
    #    }
    #print(json_object)
    #with open('playersNewList.txt', 'w') as f:
    #    f.write(json.dumps(json_object,indent=2))
    #return
    #ignoreList = getIgnoreList()
    #currentList = 
    #tempL = [4800,4911,5217,5249,5480,5695,5726,5821,5822,5854,5865,6034,6043,6133,6212,6231,6399,6405,6416,6421,6426,6429,6441,6468,6500]
    #for i in tempL:
    #    print(i)
    #    print(currentLeague.percent_owned([i]))
    playerIDkeys = list(playerIDs.keys())
    #subIDs = [playerIds.keys()[x:x+25] for x in range(0,len(playerIds.keys()),25)]
    validIDs = []
    for iterations in [playerIDkeys[x:x+25] for x in range(0,len(playerIDkeys),25)]:
        #print(iterations)
        try:
            currentOwned = currentLeague.percent_owned(iterations)
            for player in currentOwned:
                print(player)
            validIterations = [x['player_id'] for x in currentOwned if x.get('percent_owned') is not None and x['percent_owned'] < yahooOwnershipMaximum]
            #print(currentLeague.percent_owned(iterations))
            validIDs.extend(validIterations)
        except:
            validIDs.extend(iterations)
    #print(validIDs)
    validIDs = list(set(validIDs))


        #print(validIterations)
    #print(len(currentLeague.percent_owned(playerIDs.keys())))
    #print(validIDs)
    gameLog = temp.getStats(validIDs, logDate)
    
    #gameLog = [x for x in gameLog if x['name'] not in ignoreList]
    #print(gameLog)
    gameLog = list(filter(jsonFilter,gameLog))
    #print(gameLog)
    #ownershipIDs = [(x['player_id'],x['name']) for x in gameLog]
    #print(ownershipIDs)
    #ownershipIDs = temp.getOwnership(ownershipIDs,yahooOwnershipMaximum)
    #print(ownershipIDs)
    #gameLog = [x for x in gameLog if x['player_id'] in ownershipIDs]
    print(str(logDate) + " NBA GEMS")



    allLogs = []
    for item in gameLog:
        allLogs.append(printScore(item))
        #printScore(item)
    iE.exportReddit(str(logDate),allLogs)
    return





def printScore(playerLog):
    def reduceLog(currentYahooLog,currentNBALog):
        retString = ""
        if (int(currentYahooLog['PTS']) < 15):
            retString += f"{int(playerLog['PTS'])} pts/ "
        else:
            retString += f"**{int(playerLog['PTS'])} pts/** "
        if (currentNBALog['FG3M'] != 0):
            if (currentNBALog['FG3M'] < 3):
                retString += f"{gameLog['FG3M']} 3pm/ "
            else:
                retString += f"**{gameLog['FG3M']} 3pm/** "
            #retString += f"{gameLog['FG3M']} 3pm/ "
        if (int(currentYahooLog['REB']) != 0):
            if (int(currentYahooLog['REB']) < 6):
                retString += f"{int(playerLog['REB'])} reb/ "
            else:
                retString += f"**{int(playerLog['REB'])} reb/** "
        if (int(currentYahooLog['AST']) != 0):
            if (int(currentYahooLog['AST']) < 5):
                retString += f"{int(playerLog['AST'])} ast/ "
            else:
                retString += f"**{int(playerLog['AST'])} ast/** "
        if (int(currentYahooLog['ST']) != 0 and int(currentYahooLog['BLK']) != 0):
            if (int(currentYahooLog['ST']) == 2 and int(currentYahooLog['BLK']) == 2):
                retString += f"**{int(playerLog['ST'])} stl/** **{int(playerLog['BLK'])} blk/** "
                return retString
        if (int(currentYahooLog['ST']) != 0):
            if (int(currentYahooLog['ST']) < 3):
                retString += f"{int(playerLog['ST'])} stl/ "
            else:
                retString += f"**{int(playerLog['ST'])} stl/** "
        if (int(currentYahooLog['BLK']) != 0):
            if (int(currentYahooLog['BLK']) < 3):
                retString += f"{int(playerLog['BLK'])} blk/ "
            else:
                retString += f"**{int(playerLog['BLK'])} blk/** "
        return retString
    if (mode == 'yahoo'):
        print(f"{playerLog['name']}- ? min/ {int(playerLog['PTS'])} pts/ ? 3pm/ {int(playerLog['REB'])} reb/ {int(playerLog['AST'])} ast/ {int(playerLog['ST'])} stl/ {int(playerLog['TO'])} TO/ ? fgm")
        return(f"{playerLog['name']}- ? min/ {int(playerLog['PTS'])} pts/ ? 3pm/ {int(playerLog['REB'])} reb/ {int(playerLog['AST'])} ast/ {int(playerLog['ST'])} stl/ {int(playerLog['TO'])} TO/ ? fgm")
    name = playerLog['name']
    apiID = None
    try:
        apiID = [x['id'] for x in player_dict if x['full_name'] == name][0]
        #print(apiID)
    except IndexError:
        if name in playerExceptions:
            apiID = playerExceptions.get(name)
        else:
            print(f'{name} has not been added to the exception list!')

    try:
        gameLogResult = playergamelog.PlayerGameLog(player_id=apiID,date_from_nullable = nbaLogDate, date_to_nullable = nbaLogDate)
        #print(gameLogResult)
        gameLogDict = gameLogResult.get_dict()['resultSets'][0]
        gameLog = dict(zip(gameLogDict['headers'], gameLogDict['rowSet'][0]))
        #print(gameLog)
        #reducedLine = reduceLog(playerLog,gameLog)
        #print(reducedLine)
        time.sleep(1)
        print(f"{playerLog['name']}- {gameLog['MIN']} min/ {reduceLog(playerLog,gameLog)}{int(playerLog['TO'])} TO/ {gameLog['FGM']}-{gameLog['FGA']} fgm")
        return (f"{playerLog['name']}- {gameLog['MIN']} min/ {reduceLog(playerLog,gameLog)}{int(playerLog['TO'])} TO/ {gameLog['FGM']}-{gameLog['FGA']} fgm")
        #print(f"{playerLog['name']}- {gameLog['MIN']} min/ {int(playerLog['PTS'])} pts/ {gameLog['FG3M']} 3pm/ {int(playerLog['REB'])} reb/ {int(playerLog['AST'])} ast/ {int(playerLog['BLK'])} blk/ {int(playerLog['ST'])} stl/ {int(playerLog['TO'])} TO/ {gameLog['FGM']}-{gameLog['FGA']} fgm")
    except BaseException as error:
        print(f"{playerLog['name']}- ? min/ {int(playerLog['PTS'])} pts/ ? 3pm/ {int(playerLog['REB'])} reb/ {int(playerLog['AST'])} ast/ {int(playerLog['ST'])} stl/ {int(playerLog['TO'])} TO/ ? fgm")
        return(f"{playerLog['name']}- ? min/ {int(playerLog['PTS'])} pts/ ? 3pm/ {int(playerLog['REB'])} reb/ {int(playerLog['AST'])} ast/ {int(playerLog['ST'])} stl/ {int(playerLog['TO'])} TO/ ? fgm")


if __name__ == '__main__':
    nbaGemsScript()
