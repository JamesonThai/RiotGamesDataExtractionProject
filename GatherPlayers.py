import requests
# import json
from bs4 import BeautifulSoup

def playerSearch(file):
	FilteredFile = file
	listOfPlayers = []
	with open(FilteredFile) as f:
	    for line in f:
	    	if "data-text" in line:
	    		# This is finding first index of data-text
	    		firstBound = line.find("data-text")
	    		line = line[firstBound:]
	    		# Finding first and last index of " 
	    		secondBound = line.find('"') + 1
	    		thirdBound = line.rfind('"')
	    		found = line[secondBound:thirdBound]
	    		listOfPlayers.append(found)
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
