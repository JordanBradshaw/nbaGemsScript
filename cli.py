import yahoo_fantasy_api as yfa
from yahoo_oauth import OAuth2


class cli():
    def __init__(self, passedOAuth):
        self.oauth = passedOAuth

    def getLeagueName(self,passedLeagueValue):
        return yfa.League(self.oauth, passedLeagueValue).settings()['name']

    def chooseLeague(self, possibleChoices,possibleLeagues):
        print('Choose from the following League IDs:')
        print('----------------------------------')
        for index, league in enumerate(possibleLeagues):
            leagueName = self.getLeagueName(league)
            print(
                f'Index: {index} League Name: {leagueName} League ID: {league}'
            )
        print('----------------------------------')
        while True:
            returnLeague = input(
                "Input the index you're selecting or type -1 to exit: ")
            try:
                if returnLeague == '-1':
                    print('Exiting...')
                    exit()
                elif int(returnLeague) > -1 and int(
                        returnLeague) <= possibleChoices:
                    return int(returnLeague)
                    break
                else:
                    print('-Error: Invalid Index!-')
            except ValueError:
                print('-Error: Invalid Input!-')
