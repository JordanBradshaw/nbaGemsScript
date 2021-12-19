import argparse
import datetime
import json
import time

import pandas as pd
import yahoo_fantasy_api as yfa
from nba_api.stats.endpoints import playergamelog
from nba_api.stats.static import players
from yahoo_oauth import OAuth2

import importExport as iE
from cli import cli as cli
from yahooConnect import connect
from yahooLeague import yahooLeague as yahooLeague

playerExceptions = {'Enes Freedom': 202683, 'Cameron Thomas': 1630560,'PJ Washington': 1629023,'Xavier Tillman': 1630214, 'Bones Hyland': 1630538, 'Guillermo Hernangómez': 1626195}
calcScore = lambda x: (x['PTS'] * 1) + (x['REB'] * 1.2 )+ (x['AST'] * 1.5) + (x['ST'] * 3) + (x['BLK'] * 3) + (x['TO'] * -1)
customFilter = lambda x: (x['PTS'] * 1) + (x['REB'] * 1.2 )+ (x['AST'] * 1.5) + (x['ST'] * 3) + (x['BLK'] * 3) + (x['TO'] * -1) >= weightedScoreMinimum

player_dict = players.get_players()
# Variables

date,scoring,thresholds,oauthDict = iE.importSettings()
#print(date)
logDate = datetime.date(date['Year'], date['Month'], date['Day'])
yahooOwnershipMaximum = thresholds['YahooOwnership%Maximum']
weightedScoreMinimum = thresholds['WeightedScoreMinimum']

nbaLogDate = f"{date['Month']}/{date['Day']}/{date['Year']}"

def nbaGemsScript():
    ignoreList = iE.getIgnoreList()
    # Setup up connection to yahoo and select NBA
    oauth = connect(oauthDict)
    sport = yfa.Game(oauth, 'nba')

    possibleLeagues = sport.league_ids(year=2021)
    temp2 = cli(oauth)
    leagueIndex = temp2.chooseLeague(len(possibleLeagues)-1, possibleLeagues)
    currentLeague = sport.to_league(possibleLeagues[leagueIndex])
    temp = yahooLeague(currentLeague)

    playerIDs = iE.getPlayerIDs(currentLeague)
    playerIDs = [int(i) for i in playerIDs]

    #ignoreList = getIgnoreList()
    gameLog = temp.getStats(playerIDs, logDate)
    gameLog = [x for x in gameLog if x['name'] not in ignoreList]
    gameLog = list(filter(customFilter,gameLog))
    #print(gameLog)
    ownershipIDs = [(x['player_id'],x['name']) for x in gameLog]
    ownershipIDs = temp.getOwnership(ownershipIDs,yahooOwnershipMaximum)
    #print(ownershipIDs)
    gameLog = [x for x in gameLog if x['player_id'] in ownershipIDs]
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
            if (int(currentYahooLog['ST']) < 3):
                retString += f"{int(playerLog['ST'])} stl/ "
            else:
                retString += f"**{int(playerLog['ST'])} stl/** "
            if (int(currentYahooLog['BLK']) < 3):
                retString += f"{int(playerLog['BLK'])} blk/ "
            else:
                retString += f"**{int(playerLog['BLK'])} blk/** "
        return retString

    name = playerLog['name']
    apiID = None
    try:
        apiID = [x['id'] for x in player_dict if x['full_name'] == name][0]
    except IndexError:
        if name in playerExceptions:
            apiID = playerExceptions.get(name)
        else:
            print(f'{name} has not been added to the exception list!')

    try:
        gameLogResult = playergamelog.PlayerGameLog(player_id=apiID,date_from_nullable = nbaLogDate, date_to_nullable = nbaLogDate)
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
        print(error)
        print(f"{playerLog['name']}- ? min/ {int(playerLog['PTS'])} pts/ ? 3pm/ {int(playerLog['REB'])} reb/ {int(playerLog['AST'])} ast/ {int(playerLog['ST'])} stl/ {int(playerLog['TO'])} TO/ ? fgm")
        return(f"{playerLog['name']}- ? min/ {int(playerLog['PTS'])} pts/ ? 3pm/ {int(playerLog['REB'])} reb/ {int(playerLog['AST'])} ast/ {int(playerLog['ST'])} stl/ {int(playerLog['TO'])} TO/ ? fgm")


if __name__ == '__main__':
    nbaGemsScript()
