from riotwatcher import LolWatcher, RiotWatcher, ApiError
import json

API_KEY = "RGAPI-b6af20cb-4e3a-4afa-acb2-571f3a71ac03"
#API_KEY = "RGAPI-93300605-bf88-4d55-ad19-5055c0710c3e"


def get_puuid(key):

    lol_watcher = LolWatcher(key)

    riot_watcher = RiotWatcher(key)

    my_account = riot_watcher.account.by_riot_id('AMERICAS', 'choopedpotat', 'Bruhy')
    #my_account = riot_watcher.account.by_riot_id('AMERICAS', 'ahtisi', 'cmpt')

    return (my_account['puuid'])

puuid = get_puuid(API_KEY)
print(puuid)

def get_match(key, puuid):
        
    lol_watcher = LolWatcher(key, puuid=puuid, count=20)

    my_region = 'na1'
    aa = lol_watcher.match.matchlist_by_puuid(my_region, puuid=puuid)
    return aa


ee = get_match(API_KEY, puuid)
print(ee)


def match_info(key, matchID):
    lol_watcher = LolWatcher(key, puuid=puuid, count=20)
    ea = lol_watcher.match.by_id('AMERICAS', matchID);
    return ea

Match = match_info(API_KEY, ee[2])
print(Match['metadata']['participants'])
