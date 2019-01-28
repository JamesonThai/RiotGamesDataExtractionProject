# Made by Jameson Thai
import requests
import json

def getSummonerName(region, summonerName, API_KEY, version):
	# Sample https://na1.api.riotgames.com/lol/summoner/v3/summoners/by-name/RiotSchmick?api_key=<key>
	URL = "https://" + region + ".api.riotgames.com/lol/summoner/" + version + "/summoners/by-name/" + summonerName + "?api_key=" + API_KEY
	# URL = "https://na1.api.riotgames.com/lol/summoner/" + version + "/summoners/by-name/" + summonerName
	response = requests.get(URL)
	return response.json()


def getAllPlayersInSpecDivision(region, summonerID, API_KEY, version):
	# https://na1.api.riotgames.com/lol/league/v3/positions/by-summoner/31576070
	URL = "https://" + region + ".api.riotgames.com/lol/league/" + version + "/positions/by-summoner/" + str(summonerID) + "?api_key=" + API_KEY
	response = requests.get(URL)
	temp = response.json()
	# leagueIDs = str(temp[summonerID]['leagueId'])
	# print("len: " + type(temp))
	leagueIDs = str(temp[0]['leagueId'])
	print(str(temp[0]))
	return response.json()

def getPlayerMatches(region, accID, API_KEY, version):
	# https://na1.api.riotgames.com/lol/match/v3/matchlists/by-account/46262064
	URL = "https://" + region + ".api.riotgames.com/lol/match/" + version + "/matchlists/by-account/" + str(accID) + "?api_key=" + API_KEY
	response = requests.get(URL)
	return response.json()

def getPlayerMatch(region, matchID, API_KEY, version):
	URL = "https://" + region + ".api.riotgames.com/lol/match/" + version + "/matches/" + str(matchID) + "?api_key=" + API_KEY
	response = requests.get(URL)
	return response.json()

# Rename such that it is labeled by gameID
def getPlayerTimeline(region, matchID, API_KEY, version):
	URL = "https://" + region + ".api.riotgames.com/lol/match/" + version + "/timelines/by-match/" + str(matchID) + "?api_key=" + API_KEY
	response = requests.get(URL)
	return response.json()

def aggregateData(matches, summonerName, region, API_KEY, version):
	# Need to get list of matches
	matchID = matches[0]
	match = getPlayerMatch(region, matchID, API_KEY, version)
	matchTimeline = getPlayerTimeline(region, matchID, API_KEY, version)
	matchName = "data/matches/" + str(matchID) + "match.json"
	matchTimelineName = "data/matchTimelines/" + str(matchID) + "matchTimeline.json"
	with open(matchName,"w") as outfile:
		json.dump(match, outfile, sort_keys = True, indent = 4, ensure_ascii=False)

	with open(matchTimelineName,"w") as outTime:
		json.dump(matchTimeline, outTime, sort_keys = True, indent = 4, ensure_ascii=False)

def saveDF():
	value


class player:
	# Player class where we can get user information and they're static and can be constantly called within a csv df
	region, summonerName, league, summonerID, profileIcon = "", "", "", 0,0

class matches:
	# Breaking into two parts
	# Part 1 main generic information like player information
	# Detail about players is broken down into their own json 
	value = ""
class matchTimeline: 
	value = ""



def main():
	regions = {
		"NA"   : "na1",
		"BR"   : "br1",
		"EUNE" : "eun1",
		"EUW"  : "euw1",
		"JP"   : "jp1",
		"KR"   : "kr1",
		"LAS"  : "la1",
		"LAN"  : "la2",
		"OCE"  : "oc1",
		"TR"   : "tr1",
		"RU"   : "ru1",
		"PBE"  : "pbe1",
	}
	# print("Regions: NA, BR, EUNE, EUW, JP, KR, LAN, LAS, OCE, TR, RU, PBE \n")
	# region = (str)(input("Type in one of the regions above: "))
	# summonerName = (str)(input("SummonerName with no Spaces: "))
	region = regions["NA"]
	# Older versions will have NA whereas newever ones will have na1
	summonerName = "DoctorMister"
	# In analysis look at Win or not, if not win look at kda, if KDA is low then ignore entirely
	# summonerID = 31576070
	league = ""
	API_KEY = ""
	version = "v4"
	responseJson = getSummonerName(region, summonerName, API_KEY, version)
	summonerID = responseJson['id']
	profileIcon = responseJson['profileIconId']
	# ID = str(responseJson[summonerName]['id'])

	# Get all players in a league
	# responseJson = getAllPlayersInSpecDivision(region, summonerID, API_KEY, version)

	# get match information 
	# responseJson = getPlayerMatch(region, accID, API_KEY, version)

	# print(responseJson)
	accID = responseJson['accountId']
	playerMatches = getPlayerMatches(region, accID, API_KEY, version)
	# print(playerMatches['matches'][0]['gameId'])
	matchlistsize = len(playerMatches['matches'])
	# playerMatches = []
	matches = []
	i = 0
	while i < matchlistsize:
		# print(playerMatches['matches'][i]['gameId'])
		matchID = playerMatches['matches'][i]['gameId']
		matches.append(matchID)
		i += 1

	aggregateData(matches, summonerName, region, API_KEY, version)

	# Note 100 Requests every 2 minutes
	
	# Breaking Information
	# GameInformation 
		# gameCreation, gameDuration, gameId, gameMode, gameType, gameVersion, 
		# mapId, queueId, platformId, seasonId
	# participantIdentities
		# participantId
		# player
			# accountId, currentAccountId, currentPlatformId, matchHistoryUri, 
			# platformId, profileIcon, summonerId, summonerName
	# participants
		# championId, highestAchievedSeasonTier, participantId, spell1Id, spell2Id
		# stats
			# assists, champLevel, combatPlayerScore, damageDealtToObjectives, 
			# damageDealtToTurrets, damageSelfMitigated, deaths, doubleKills
			# firstBloodAssist, firstBloodKill, firstInhibitorAssist, 
			# firstInhibitorKill, firstTowerAssist, firstTowerKill, goldEarned
			# goldSpent, inhibitorKills, item0, item1, item2, item3, item4, item5, item6
			# killingSprees,kills, largestCriticalStrike, largestKillingSpree, 
			# largestMultiKill, longestTimeSpentLiving, magicDamageDealt, 
			# magicDamageDealtToChampions, magicalDamageTaken, neutralMinionsKilled,
			# neutralMinionsKilledEnemyJungle, neutralMinionsKilledTeamJungle
			# objectivePlayerScore, participantId, pentaKills, perk0, perk0Var1,
			# perk0Var2, perk0Var3, perk1, perk1Var2, perk1Var3, perk2, perk2Var1, 
			# perk2Var2, perk2Var3, 
	# teams
	




if __name__ == "__main__":
	main()