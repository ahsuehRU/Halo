from pyhalo import PyHalo
from pprint import pprint
import requests
import timeit

start = timeit.default_timer() #TIMER START

Ocp_Apim_Subscription_Key = 'd65bd4c8343a46b098e70bd95d07f1b5'

h = PyHalo(Ocp_Apim_Subscription_Key)
player_matches_json = h.get_player_matches('Honkbune','arena',0,5)

def win_loss(matchJSON, teamId):
    winner = None
    top_score = 0
    for team in matchJSON["TeamStats"]:
        if team["Score"] > top_score:
            top_score = team["Score"]
            winner = team["TeamId"]
    if teamId == winner:
        return True
    else:
        return False

teammates = {}
for match in player_matches_json["Results"]:
    matchId = match["Id"]["MatchId"]
    teamId = match["Players"][0]["TeamId"]
    matchData_json = h.get_arena_match(matchId)
    for player in matchData_json["PlayerStats"]:
        
        gamertag = player["Player"]["Gamertag"] #gamertag
        kills = player["TotalKills"]            #Kills
        assists = player["TotalAssists"]        #Assists
        deaths = player["TotalDeaths"]          #Deaths
        win = win_loss(matchData_json, teamId)  #Win
        
        if player["TeamId"] == teamId:
            if not gamertag in teammates:
                teammates[gamertag] = {}
                teammates[gamertag]["games"] = 1
                teammates[gamertag]["kills"] = kills
                teammates[gamertag]["assists"] = assists
                teammates[gamertag]["deaths"] = deaths
                if win:
                    teammates[gamertag]["win"] = 1
                else:
                    teammates[gamertag]["win"] = 0
            else:
                teammates[gamertag]["games"] += 1
                teammates[gamertag]["kills"] += kills
                teammates[gamertag]["assists"] += assists
                teammates[gamertag]["deaths"] += deaths
                if win:
                    teammates[gamertag]["win"] += 1

stop = timeit.default_timer() #TIMER STOP

pprint(teammates)
print stop - start