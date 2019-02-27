"""
	getFiles is meant to go through a list of users and then extract them with accordance to the 
	data extraction limits
	20 requests every 1 second
	100 requests every 2 minutes => 100 requests every 120 seconds 

	Written and Documented by: Jameson Thai
"""
import requests, json, time

"""
	param region:	the corresponding region that is being called
	param accID:	the accountID of the summoner account in question
	param API_KEY:	my API keyused for development, for publishing purposes this has been removed due to 
			riot games policies, if you want to create your own you need to make your own account and 
			request from there
	param version:	the version called in regards to Riot Games API calls 
	Return: 
		returns the extracted JSON file 
"""
def getPlayerMatches(region, accID, API_KEY, version):
	# https://na1.api.riotgames.com/lol/match/v3/matchlists/by-account/46262064
	URL = "https://" + region + ".api.riotgames.com/lol/match/" + version + "/matchlists/by-account/" + str(accID) + "?api_key=" + API_KEY
	response = requests.get(URL)
	return response.json(), response.status_code

"""
	param region:	the corresponding region that is being called
	param matchID: 	the match ID
	param API_KEY:	our API KEY BEING CALLED blocked out for certain reasons...
	param version:	version of current patch
	return
		returns extracted json file
"""
def getPlayerMatch(region, matchID, API_KEY, version):
	URL = "https://" + region + ".api.riotgames.com/lol/match/" + version + "/matches/" + str(matchID) + "?api_key=" + API_KEY
	response = requests.get(URL)
	return response.json(), response.status_code

"""
	param region:	the corresponding region that is being called
	param matchID: 	the match ID
	param API_KEY:	our API KEY BEING CALLED blocked out for certain reasons...
	param version:	version of current patch
	return
		returns extracted json file
"""
def getPlayerTimeline(region, matchID, API_KEY, version):
	URL = "https://" + region + ".api.riotgames.com/lol/match/" + version + "/timelines/by-match/" + str(matchID) + "?api_key=" + API_KEY
	response = requests.get(URL)
	return response.json(), response.status_code

"""
	param region:			the corresponding region that is being called
	param summonerName: 	the summoner name being searched for his encrypted account ID
	param API_KEY:			our API KEY BEING CALLED blocked out for certain reasons...
	param version:			version of current patch
	return
		returns extracted json file
"""
def getSummonerName(region, summonerName, API_KEY, version):
	# Sample https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/RiotSchmick?api_key=<key>
	URL = "https://" + region + ".api.riotgames.com/lol/summoner/" + version + "/summoners/by-name/" + summonerName + "?api_key=" + API_KEY
	# URL = "https://na1.api.riotgames.com/lol/summoner/" + version + "/summoners/by-name/" + summonerName
	response = requests.get(URL)
	# if response == 200:
	statusCode = response.raise_for_status()
	if statusCode == None:
		return response.json(), response.status_code
	else:
		return "error"

"""
	getProPlayers extracts from the list of proplayers already extracted into a list format
	return:
		dictionary of ProPlayers with their summonerName : Person Name
"""
def getProPlayers():
	path = "data/ProPlayers.txt"
	proList = {}
	with open(path,"r") as outfile:
		for line in outfile:
			ign = line[:line.find("|")].strip()
			region = line[line.find("|")+1:].strip()
			proList[ign] = region
	outfile.close()
	return proList

"""
	returns list of seen games
"""
def getSeenGames():
	path = "data/seenGameIDs.txt"
	seenGames = []
	with open(path, "r") as outfile:
		for line in outfile:
			seenGames.append(line)
	outfile.close()
	return seenGames

"""
	param regions:			the corresponding regions that is being called
	param proPlayerList: 	proPlayer list 
	param API_KEY:			our API KEY BEING CALLED blocked out for certain reasons...
	param version:			version of current patch
	return
		returns extracted json file

	Return: In the format of a dictionary of PlayerID(SummonerName) and region as key value pairing 
"""
def getPlayerAccId(proPlayerList, regions, API_KEY, version):
	tempString = ""
	listOfAccounts = {}
	# Temp read and write for now
	with open ("data/tempAccs.txt", "w",  encoding="utf8") as outfile:
		for player in proPlayerList:
			try:
				playerID = getSummonerName(regions[proPlayerList[player]], player, API_KEY, version)
				listOfAccounts[playerID["accountId"]] = player + " : " + str(regions[proPlayerList[player]])
				# Temporary write for now
				outfile.write(player + "|" + str(regions[proPlayerList[player]]) + "|" + playerID["accountId"] + "\n")
			except:
				print("No Data for ", player)
			time.sleep(1.5)
	return listOfAccounts

"""
	param playerAccIds: 	playerAccIds list 
	param API_KEY:			our API KEY BEING CALLED blocked out for certain reasons...
	param version:			version of current patch
	param seenGames:		list of seen games for checking
"""
def getAllOfPlayersMatches(playerAccIds, API_KEY, version, seenGames):
	ListOfMatches = []
	for playerACC in playerAccIds: 
		region = playerAccIds[playerACC][playerAccIds[playerACC].find(":") + 1:].strip()
		matches, responseCode = getPlayerMatches(region, playerACC, API_KEY, version)
		# If matches can be found
		if responseCode == 200:
			numberOfGames = len(matches['matches'])
			# If response code does not equal to 429
			i = 0
			wait = 0
			while i < numberOfGames:
				matchID = matches['matches'][i]['gameId']
				temp = str(matchID) + "\n"
				print("Checking:", playerACC, str(matchID))
				if temp not in seenGames:
					matchData, matchResponseCode = getPlayerMatch(region, matchID, API_KEY, version)
					matchTimeline, matchTimeResponseCode = getPlayerTimeline(
						region, matchID, API_KEY, version)
					if matchResponseCode == 200 and matchTimeResponseCode == 200:
						print("Response is 200")
						matchName = "data/matches/" + str(matchID) + "match.json"
						matchTimelineName = "data/matchTimelines/" + str(matchID) + "matchTimeline.json"
						# Dump that data
						with open(matchName,"w",  encoding="utf8") as outfile:
							json.dump(matchData, outfile, sort_keys = True, indent = 4, ensure_ascii=False)
						outfile.close()
						with open(matchTimelineName,"w",  encoding="utf8") as outTime:
							json.dump(matchTimeline, outTime, sort_keys = True, indent = 4, ensure_ascii=False)
						outTime.close()
						with open("data/seenGameIDs.txt","a",  encoding="utf8") as outSeen:
							outSeen.write(str(matchID) + "\n")
						outSeen.close()
						wait = 2
					elif matchResponseCode == 429 and matchTimeResponseCode == 429:
						print("Waiting for response times")
						i -= 1
						wait = 8
					else:
						print("failedEntry detected", matchResponseCode, matchTimeResponseCode)
						with open("data/failedEntries.txt", "a",  encoding="utf8") as unseen:
							unseen.write(temp)
						unseen.close()
						wait = 20
				else:
					wait = 0.01
				i += 1
				time.sleep(wait)
		else:
			print("no match data detected", playerACC)
			with open("data/failedAccounts.txt", "a", encoding="utf8") as failedAcc:
				failedAcc.write(playerACC)
			failedAcc.close()

"""
	Temporary Main File For testing Remove Later
"""
def main():
	API_KEY = "RGAPI-ea7587e8-cf05-4a2d-bcfc-51d4ccb0684e"
	version = "v4"
	regions = {
		"NA"   : "na1",
		"BR"   : "br1",
		"EUNE" : "eun1",
		"EUW"  : "euw1",
		"JP"   : "jp1",
		"KR"   : "kr",
		"LAS"  : "la1",
		"LAN"  : "la2",
		"OCE"  : "oc1",
		"TR"   : "tr1",
		"RU"   : "ru",
		"PBE"  : "pbe1",
	}
	proList = getProPlayers()
	seenGames = getSeenGames()
	# playerAccIds = getPlayerAccId(proList, regions, API_KEY, version)
	# Temporarily for utility 
	playerAccIds = {}
	with open("data/tempAccs.txt", "r",  encoding="utf8") as outfile:
		for line in outfile:
			temp = line[line.find("|") + 1:] 
			region = temp[:temp.find("|")].strip()
			accID = temp[temp.find("|") + 1 :].strip()
			playerAccIds[accID] = region
	outfile.close()
	getAllOfPlayersMatches(playerAccIds, API_KEY, version, seenGames)
	# Need to do a rerun of failed entries
	
if __name__ == "__main__":
	main()