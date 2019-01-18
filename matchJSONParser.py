import os

def parseMatchJson(listOfMatchFiles):
	# Make sure to change filename to GameID+PlayerID
	#We have 3 lists we want to separate into Core, ParticipantsID and Stats
	# More on ordering here https://docs.google.com/spreadsheets/d/1a3AvG-0e2DpzSqdabDCaInCD827hnREF0mUQQAEPbM4/edit#gid=0
	# Or you can look at DataFrameMatchesOrdering.txt to get a better understanding
	# Additionally data is aggregated into one list of dictionaries of list of ... yea you get the point
	matchListData = []
	# Basically list of tuples
	core, Participants, Stats= {},{},{}
	# List of labels
	labelCore, labelParticipants, labelStats = [],[],[]
	coreList, participantList, statsList = [],[], []
	deltas = ['creepsPerMinDeltas', 'damageTakenPerMinDeltas', 'goldPerMinDeltas', 'xpPerMinDeltas', 
	'xpDiffPerMinDeltas', 'csDiffPerMinDeltas', 'damageTakenDiffPerMinDeltas']
	constants = {"gameId":0}
	with open("data/DataFrameMatchesOrdering.txt","r") as outfile:
		next(outfile)
		listing = []
		for line in outfile:
			if "Participants" in line:
				labelCore = listing
				listing = []
			elif "Stats" in line :
				labelParticipants = listing
				listing = []
			else:			
				line = line.rstrip()
				listing.append(line)
		labelStats = listing
	outfile.close()

	for file in listOfMatchFiles:
		specfile = "data/matches/" + file
		check = False
		with open(specfile,"r") as outfile:
			for line in outfile:
				if "teams" in line:
					break
				if "participants" in line:
					check = True
				label = line[1:line.find(':')].replace('"', "").strip()
				value = line[line.find(':') + 1:len(line)-1].replace('"',"").replace(",","").strip()
				if label in "gameId":
					constants["gameId"] = value 
				# If value if found, store it in a dictionary
				if label in labelCore:
					core[label] = value
					# print(label,value)
				elif (label in labelParticipants) and (check == False):
					Participants[label] = value
					# print(label,value)
					if label in "summonerName":
						# last item push everything
						Participants["gameId"] = constants["gameId"]
						participantList.append(Participants)
						# For Resetting
						Participants = {}
				elif label in labelStats:
					# Deltas Check
					if label in deltas:
						deltaValues = {}
						count = 0
						while count < 2:
							line = next(outfile)
							label = line[line.find('"')+1:line.find(":")-1].strip()
							value = line[line.find(':') + 1:len(line)-1].replace('"',"").strip()
							deltaValues[label] = value
							count += 1
						value = deltaValues
					Stats[label] = value
					if label in "trueDamageTaken":
						Stats["gameId"] = constants["gameId"]
						statsList.append(Stats)
						# For Resetting
						Stats = {}

		outfile.close()
		coreList.append(core)
		core = {}
		# print(participantList)
		# print(statsList)
		# check for missing values can take out later
		# for key in labelCore:
		# 	if core[key] is None:
		# 		print("core",key)
		# for key in Participants:
		# 	if Participants[key] is None:
		# 		print("Participants", key)
		# for key in Stats:
		# 	if Stats[key] is None:
		# 		print("Stats", key)

		matchListData.append(coreList)
		matchListData.append(participantList)
		matchListData.append(statsList)

	return matchListData

def parseTimeline(filelist):
	# GameID is in file name
	participants, events = {},{}
	participantList, eventsLists = [],[]
	labelParticipants, labelEvents = [],[]
	timelineData = []
	# Loading in all labels
	with open("data/DataFrameOrderingMT.txt","r") as outfile:
		next(outfile)
		listing = []
		for line in outfile:
			if "Events" in line:
				labelParticipants = listing
				listing = []
			else:			
				line = line.rstrip()
				listing.append(line)
		labelEvents = listing
	outfile.close()

	# Actual Parsing
	constant = {"gameId":0}
	for file in filelist:
		specfile = "data/matchTimelines/" + file
		check = False
		with open(specfile,"r") as outfile:
			for line in outfile: 
				if "participantId" in line:
					print(line)


	return timelineData

def populateList(category):
	listing = []
	path = "./data/" + category
	for root, dirs, files in os.walk(path):  
	    for file in files:
	    	if "json" in file:
		        listing.append(file)
	return listing

def main():
	fileMatchList = populateList("matches")
	fileMatchTimelineList = populateList("matchTimelines")

	matchListing = parseMatchJson(fileMatchList)
	matchTimelines = parseTimeline(fileMatchTimelineList)

	# print(fileMatchTimelineList)
if __name__ == "__main__":
	main()
