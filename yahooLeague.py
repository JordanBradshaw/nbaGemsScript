
class yahooLeague:
    def __init__(self, passedLeague):
        self.currentLeague = passedLeague

    def getTopFreeAgents(self):
        print(self.currentLeague.matchups())

    def getOwnership(self, passedList, ownershipCutoff):
        tempList = []
        for item in passedList:
            currentPlayer = [item[0]]
            currentPercentage = self.currentLeague.percent_owned(currentPlayer)
            if (currentPercentage == []):
                tempList.append(item[0])
                print(f"{item} 0% Owned")
                continue
            if currentPercentage[0]['percent_owned'] <= ownershipCutoff:
                tempList.append(item[0])
                print(f"{item} Under {ownershipCutoff}% owned!")
            else:
                print(f"{item} Over {ownershipCutoff}% owned!")
        return tempList

    def getStats(self, passedList, logDate):
        gameLog = [x for x in self.currentLeague.player_stats(passedList, req_type='date', date=logDate) if x['PTS'] is not '-']
        return gameLog
