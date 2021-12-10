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
    def getIgnoreList():
        with open('IgnorePlayers.txt', 'r') as f:
            ignoreIDs = f.read().splitlines()
        return set(ignoreIDs)

    def getPlayerIDs():
        try:
            with open('PlayerIDs.txt') as f:
                return f.read().splitlines()
        except FileNotFoundError:
            with open('PlayerIDs.txt', 'a') as f:
                setList = []
                for i in currentLeague.taken_players():
                    try:
                        setList.append(i['player_id'])
                        print(i['player_id'])
                        # f.write(f'{i["player_id"]}\n')
                    except RuntimeError:
                        continue
                for i in currentLeague.free_agents('Util'):
                    try:
                        setList.append(i['player_id'])
                        print(i['player_id'])
                        # f.write(f'{i["player_id"]}\n')
                    except RuntimeError:
                        continue
                setList = list(set(setList))
                setList.sort()
                print(setList)
                for item in setList:
                    f.write(f'{item}\n')
                print("Restart Script!")
                getPlayerIDs()



    # Setup up connection to yahoo and select NBA
    oauth = connect(oauthDict)
    sport = yfa.Game(oauth, 'nba')

    possibleLeagues = sport.league_ids(year=2021)
    temp2 = cli(oauth)
    leagueIndex = temp2.chooseLeague(len(possibleLeagues)-1, possibleLeagues)
    currentLeague = sport.to_league(possibleLeagues[leagueIndex])
    temp = yahooLeague(currentLeague)

    playerIDs = getPlayerIDs()
    playerIDs = [int(i) for i in playerIDs]

    ignoreList = getIgnoreList()
    gameLog = temp.getStats(playerIDs, logDate)
    gameLog = [x for x in gameLog if x['name'] not in ignoreList]
    gameLog = list(filter(customFilter,gameLog))
    #print(gameLog)
    ownershipIDs = [(x['player_id'],x['name']) for x in gameLog]
    ownershipIDs = temp.getOwnership(ownershipIDs,yahooOwnershipMaximum)
    #print(ownershipIDs)
    gameLog = [x for x in gameLog if x['player_id'] in ownershipIDs]
    print(str(logDate) + " NBA GEMS")
    for item in gameLog:
        printScore(item)
    #print(gameLog)
    return





def printScore(playerLog):
    def reduceLog(currentYahooLog,currentNBALog):
        retString = ""
        #print(currentYahooLog)
        #print(currentNBALog)
        if (currentNBALog['FG3M'] != 0):
            retString += f"{gameLog['FG3M']} 3pm/ "
        if (int(currentYahooLog['REB']) != 0):
            retString += f"{int(playerLog['REB'])} reb/ "
        if (int(currentYahooLog['AST']) != 0):
            retString += f"{int(playerLog['AST'])} ast/ "
        if (int(currentYahooLog['BLK']) != 0):
            retString += f"{int(playerLog['BLK'])} blk/ "
        if (int(currentYahooLog['ST']) != 0):
            retString += f"{int(playerLog['ST'])} stl/ "
        #print(retString)
        return retString

    name = playerLog['name']
    #print(str(logDate))
    try:
        apiID = [x['id'] for x in player_dict if x['full_name'] == name][0]
        #print(apiID)
        gameLogResult = playergamelog.PlayerGameLog(player_id=apiID,date_from_nullable = nbaLogDate, date_to_nullable = nbaLogDate)
        gameLogDict = gameLogResult.get_dict()['resultSets'][0]
        gameLog = dict(zip(gameLogDict['headers'], gameLogDict['rowSet'][0]))
        #print(gameLog)
        #reducedLine = reduceLog(playerLog,gameLog)
        #print(reducedLine)
        print(f"{playerLog['name']}- {gameLog['MIN']} min/ {reduceLog(playerLog,gameLog)}{int(playerLog['TO'])} TO/ {gameLog['FGM']}-{gameLog['FGA']} fgm")
        #print(f"{playerLog['name']}- {gameLog['MIN']} min/ {int(playerLog['PTS'])} pts/ {gameLog['FG3M']} 3pm/ {int(playerLog['REB'])} reb/ {int(playerLog['AST'])} ast/ {int(playerLog['BLK'])} blk/ {int(playerLog['ST'])} stl/ {int(playerLog['TO'])} TO/ {gameLog['FGM']}-{gameLog['FGA']} fgm")
    except BaseException as error:
        print(error)
        print(f"{playerLog['name']}- ? min/ {int(playerLog['PTS'])} pts/ ? 3pm/ {int(playerLog['REB'])} reb/ {int(playerLog['AST'])} ast/ {int(playerLog['ST'])} stl/ {int(playerLog['TO'])} TO/ ? fgm")

    
    time.sleep(1)
    

if __name__ == '__main__':
    nbaGemsScript()
