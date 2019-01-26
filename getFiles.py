"""
	getFiles is meant to go through a list of users and then extract them with accordance to the 
	data extraction limits
	20 requests every 1 second
	100 requests every 2 minutes => 100 requests every 120 seconds 

	Written and Documented by: Jameson Thai
"""
import requests
import json
import sched, time


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

def getSummonerName(region, summonerName, API_KEY, version):
	# Sample https://na1.api.riotgames.com/lol/summoner/v3/summoners/by-name/RiotSchmick?api_key=<key>
	URL = "https://" + region + ".api.riotgames.com/lol/summoner/" + version + "/summoners/by-name/" + summonerName + "?api_key=" + API_KEY
	# URL = "https://na1.api.riotgames.com/lol/summoner/" + version + "/summoners/by-name/" + summonerName
	response = requests.get(URL)
	return response.json()

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
			realName = line[line.find("|")+1:].strip()
			proList[ign] = realName
	outfile.close()
	return proList

def getSeenGames():
	path = "data/seenGameIDs.txt"
	seenGames = []
	with open(path, "r") as outfile:
		for line in outfile:
			seenGames.append(line)
	outfile.close()
	return seenGames

def getPlayerAccId(proPlayerList, regions, API_KEY, version):
	# proListing = {}
	# for item in proPlayerList:
		# response = getSummonerName(region, item, API_KEY, version)
		# break
	response = getSummonerName()

def runScheduler(sc):
    # print "Doing stuff..."
    # do your stuff
    s.enter(60, 1, runScheduler(), (sc,))
    print("DoingSomething")
"""
	Temporary Main File For testing Remove Later
"""
def main():
	API_KEY = "RGAPI-a692cb99-a968-4a5d-bc7c-8067b8766c87"
	version = "v4"
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
	proList = getProPlayers()
	seenGames = getSeenGames()
	playerAccIds = getPlayerAccId({"Doctor Mister", regions, API_KEY, version)

	# s = sched.scheduler(time.time, time.sleep)
	# s.enter(60, 1, runScheduler(), (s,))
	# s.run()

if __name__ == "__main__":
	main()