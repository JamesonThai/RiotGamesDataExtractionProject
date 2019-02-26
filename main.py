"""
	the main runner that will call everything and execute/compile for data collection and preprocessing 

	Written and Documented by: Jameson Thai	
"""
def main():
	# Constants
	API_KEY = "RGAPI-8ae14c6a-c534-48e2-a732-94054e0842ab"
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

	# Call main functions from other files

	proList = getProPlayers()
	seenGames = getSeenGames()
	# playerAccIds = getPlayerAccId(proList, regions, API_KEY, version)
	# Temporarily for utility 
	playerAccIds = {}
	with open("data/tempAccs.txt", "r") as outfile:
		for line in outfile:
			temp = line[line.find("|") + 1:] 
			region = temp[:temp.find("|")].strip()
			accID = temp[temp.find("|") + 1 :].strip()
			playerAccIds[accID] = region
	outfile.close()
	playerMatches = getAllOfPlayersMatches(playerAccIds, API_KEY, version, seenGames)

	
if __name__ == "__main__":
	main()