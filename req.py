from riotwatcher import LolWatcher, RiotWatcher, ApiError
from time import sleep

class Player():
    def __init__(self, API_KEY , game_name, tag_line, region="AMERICAS"):
        self.API_KEY = API_KEY
        self.game_name = game_name
        self.tag_line = tag_line
        self.region = region
        self.puuid = self.get_puuid()


    def get_puuid(self) -> str:
        riot_watcher = RiotWatcher(self.API_KEY)
        
        my_account = riot_watcher.account.by_riot_id(self.region, self.game_name, self.tag_line)
        #my_account = riot_watcher.account.by_riot_id('AMERICAS', 'choopedpotat', 'Bruhy')
        #my_account = riot_watcher.account.by_riot_id('AMERICAS', 'ahtisi', 'cmpt')

        return (my_account['puuid'])


    def get_matchlist(self) -> list:
        riot_watcher = RiotWatcher(self.API_KEY)
        
        asd = riot_watcher.account.by_puuid(self.region, self.puuid)
        lol_watcher = LolWatcher(self.API_KEY, puuid=self.puuid, count=20)
        matchList = lol_watcher.match.matchlist_by_puuid(self.region, puuid=self.puuid)

        return matchList
    
    def get_most_recent_match(self) -> dict:
        return self.match_data(self.get_matchlist()[0])

    def match_data(self, matchID) -> dict:
        lol_watcher = LolWatcher(self.API_KEY, puuid=self.puuid, count=20)
        matchData = lol_watcher.match.by_id(self.region, matchID);
        return matchData
    
    def in_game_with(self, user, game) -> bool:
        playerCounter = 0
        for i in range(10):
            id = game['info']['participants'][i]['puuid']
            if (id==user.puuid) or (id==self.puuid):
                playerCounter += 1
        if playerCounter == 2:
            return True
        else:
            return False
    def won_game(self, game) -> bool:
        for i in range(10):
            if (game['info']['participants'][i]['puuid'] == self.puuid):
                return type(game['info']['participants'][i]['win'])


def in_same_game(player1:Player, player2:Player) -> bool:
    mostRecentMatch = player1.get_most_recent_match()
    return player1.in_game_with(player2, mostRecentMatch)

##=======================Testing of Functions===================


def testing():

    API_KEY = "RGAPI-b6af20cb-4e3a-4afa-acb2-571f3a71ac03"
    #API_KEY = "RGAPI-93300605-bf88-4d55-ad19-5055c0710c3e"
    
    
    # print("start")
    william = Player(API_KEY, "choopedpotat", "Bruhy")
    # print("done")
    # print(william.get_puuid())
    

    mlist = william.get_matchlist()

    game = william.match_data(mlist[0])
    print(game)
    #print(mlist)
    # for i in range(6):
    #     print(type(game))

    #     print(william.won_game(game))



def game_data_collect():
    
    API_KEY = "RGAPI-b6af20cb-4e3a-4afa-acb2-571f3a71ac03"
    william = Player(API_KEY, "choopedpotat", "Bruhy")
    # howard = Player("RGAPI-7102b893-0f9e-4102-8dbb-991d8fabbc5a", "wurrd", "0000")
    # print("=================== William ========================= \n\n")
    print(william.get_matchlist())
    print(william.match_data(william.get_matchlist()[0]))
    # WmostRecent = william.get_most_recent_match()
    # print(str(WmostRecent["metadata"]).replace(",",",\n"))
    # print("created:", WmostRecent["info"]["gameCreation"])
    # print("end time stamp: ", WmostRecent["info"]["gameEndTimestamp"])
    # print("gameId: ", WmostRecent["info"]["gameId"])
    # print("gameMode: ", WmostRecent["info"]["gameMode"])
    # print("won game: ", william.won_game(WmostRecent))
    # sleep(10)


    # print("=================== Howard ========================= \n\n")
    # print(howard.get_matchlist())
    # HmostRecent = howard.get_most_recent_match()
    # print(str(HmostRecent["metadata"]).replace(",",",\n"))
    # print("created:", HmostRecent["info"]["gameCreation"])
    # print("end time stamp: ", HmostRecent["info"]["gameEndTimestamp"])
    # print("gameId: ", HmostRecent["info"]["gameId"])
    # print("gameMode: ", HmostRecent["info"]["gameMode"])
    # print("won game: ", howard.won_game(HmostRecent))


if (__name__ == "__main__"):
    # testing()
    game_data_collect()