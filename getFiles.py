"""
	getFiles is meant to go through a list of users and then extract them with accordance to the 
	data extraction limits
	20 requests every 1 second
	100 requests every 2 minutes => 100 requests every 120 seconds 

	Written and Documented by: Jameson Thai
"""
import requests, json, time

"""
	param: region, the corresponding region that is being called
	param: accID, the accountID of the summoner account in question
	param: API_KEY, my API keyused for development, for publishing purposes this has been removed due to 
			riot games policies, if you want to create your own you need to make your own account and 
			request from there
	param: version , the version called in regards to Riot Games API calls 
	Return: 
		returns the extracted JSON file 
"""
def getPlayerMatches(region, accID, API_KEY, version):
	# https://na1.api.riotgames.com/lol/match/v3/matchlists/by-account/46262064
	URL = "https://" + region + ".api.riotgames.com/lol/match/" + version + "/matchlists/by-account/" + str(accID) + "?api_key=" + API_KEY
	response = requests.get(URL)
	return response.json()
"""
"""
def getSummonerName(region, summonerName, API_KEY, version):
	# Sample https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/RiotSchmick?api_key=<key>
	URL = "https://" + region + ".api.riotgames.com/lol/summoner/" + version + "/summoners/by-name/" + summonerName + "?api_key=" + API_KEY
	# URL = "https://na1.api.riotgames.com/lol/summoner/" + version + "/summoners/by-name/" + summonerName
	response = requests.get(URL)
	# if response == 200:
	statusCode = response.raise_for_status()
	if statusCode == None:
		return response.json()
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
	Return: In the format of a dictionary of PlayerID(SummonerName) and region as key value pairing 
"""
def getPlayerAccId(proPlayerList, regions, API_KEY, version):
	tempString = ""
	listOfAccounts = {}
	for player in proPlayerList:
		try:
			playerID = getSummonerName(regions[proPlayerList[player]], player, API_KEY, version)
			listOfAccounts[playerID["accountId"]] = player + " : " + str(regions[proPlayerList[player]])
		except:
			print("Error for ", player)
		time.sleep(.9)
	return listOfAccounts

"""
"""
def getAllOfPlayersMatches(playerAccIds, API_KEY, version)
	ListOfMatches = []
	getPlayerMatches(region, accID, API_KEY, version):

"""
	Temporary Main File For testing Remove Later
"""
def main():
	API_KEY = "RGAPI-95974be2-4bae-4aba-8e36-afc37d540b0a"
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
	playerAccIds = getPlayerAccId(proList, regions, API_KEY, version)
	playerMatches = getAllOfPlayersMatches(playerAccIds, proList, API_KEY, version)

if __name__ == "__main__":
	main()