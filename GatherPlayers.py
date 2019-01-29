import requests
# import json
from bs4 import BeautifulSoup

# Include region into the dictionary
def playerSearch(file):
	FilteredFile = file
	listOfPlayers = []
	player, region = "",""
	with open(FilteredFile) as f:
		for line in f:
			if "data-text" in line:
				# This is finding first index of data-text
				firstBound = line.find("data-text")
				line = line[firstBound:]
				# Finding first and last index of " 
				secondBound = line.find('"') + 1
				thirdBound = line.rfind('|')
				player = line[secondBound:thirdBound]
			if "server light" in line:
				line = next(f)
				region = line.strip()
				temp = player + "|" + region
				player, region = "",""
				listOfPlayers.append(temp)

	with open("data/ProPlayers.txt", "w") as outfile:
		for player in listOfPlayers:
			outfile.write(player + "\n")

def main():
	URL = "https://" + "www.probuilds.net/pros"
	file = "data/ResultList.txt"
	response = requests.get(URL)
	filteredResponse = BeautifulSoup(response.text, "html.parser")

	with open(file,"w") as outfile:
		outfile.write(filteredResponse.prettify())

	playerSearch("data/ResultList.txt")

if __name__ == "__main__":
	main()
