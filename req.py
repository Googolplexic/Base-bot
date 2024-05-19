from riotwatcher import LolWatcher, RiotWatcher, ApiError
import json

API_KEY = "RGAPI-b6af20cb-4e3a-4afa-acb2-571f3a71ac03"
#API_KEY = "RGAPI-93300605-bf88-4d55-ad19-5055c0710c3e"

class Player():
    def __init__(self, API_KEY , game_name, tag_line, region="AMERICAS"):
        self.API_KEY = API_KEY
        self.game_name = game_name
        self.tag_line = tag_line
        self.region = region
        self.puuid = self.get_puuid()


    def get_puuid(self):
        riot_watcher = RiotWatcher(self.API_KEY)

        my_account = riot_watcher.account.by_riot_id(self.region, self.game_name, self.tag_line)
        #my_account = riot_watcher.account.by_riot_id('AMERICAS', 'choopedpotat', 'Bruhy')
        #my_account = riot_watcher.account.by_riot_id('AMERICAS', 'ahtisi', 'cmpt')

        return (my_account['puuid'])


    def get_matchlist(self):
        lol_watcher = LolWatcher(self.API_KEY, puuid=self.puuid, count=20)
        matchList = lol_watcher.match.matchlist_by_puuid(self.region, puuid=self.puuid)
        return matchList

    def match_data(self, matchID):
        lol_watcher = LolWatcher(self.API_KEY, puuid=self.puuid, count=20)
        matchData = lol_watcher.match.by_id(self.region, matchID);
        return matchData
    
    def in_game_with(self, user, matchID):
        playerCounter = 0
        for i in range(10):
            id = game['info']['participants'][i]['puuid']
            if (id==user.puuid) or (id==self.puuid):
                playerCounter += 1
        if playerCounter == 2:
            return True
        else:
            return False
    def won_game(self, game):
        for i in range(10):
            if (game['info']['participants'][i]['puuid'] == self.puuid):
                return game['info']['participants'][i]['win']

            
##=======================Testing of Functions===================


def testing():
    # print("start")
    william = Player(API_KEY, "choopedpotat", "Bruhy")
    # print("done")
    print(william.get_puuid())


    mlist = william.get_matchlist()
    print(mlist)
    for i in range(6):
        game = william.match_data(mlist[i])
        # print(game)

        print(william.won_game(game))


if (__name__ == "__main__"):
    testing()