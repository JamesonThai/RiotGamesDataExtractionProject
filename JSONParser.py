import os, csv


# Only call this once
def getHeaders():
    coreHeaders, participantsHeaders, statsHeaders = [], [], []
    print("obtaining headers")
    with open('data/DataFrameMatchesOrdering.txt', 'r', encoding="utf8") as infile:
        next(infile)
        listing = []
        for line in infile:
            if "Participants" in line:
                coreHeaders = listing
                coreHeaders.append('gameId')
                listing = []
            elif "Stats" in line:
                participantsHeaders = listing
                participantsHeaders.append('gameId')
                listing = []
            else:
                line = line.rstrip()
                listing.append(line)
        statsHeaders = listing
        statsHeaders.append('gameId')
    infile.close()
    return coreHeaders, participantsHeaders, statsHeaders


def initCSV(coreHeaders, participantsHeaders, statsHeaders, timelinePartci, timelineEvents):
    # Obtains csv headers
    # statsHeaders += ['creepsPerMinDeltas', 'damageTakenPerMinDeltas', 'goldPerMinDeltas', 'xpPerMinDeltas',
    # 'xpDiffPerMinDeltas', 'csDiffPerMinDeltas', 'damageTakenDiffPerMinDeltas']
    # core match csv
    with open('data/dataframes/matchcores.csv', mode='w', encoding="utf8") as csv_file:
        writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(coreHeaders)
    csv_file.close()
    # participants match csv
    with open('data/dataframes/matchparticipants.csv', mode='w', encoding="utf8") as partici_file:
        writer = csv.writer(partici_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(participantsHeaders)
    partici_file.close()
    # stats match
    with open('data/dataframes/matchstats.csv', mode='w', encoding="utf8") as stats_file:
        writer = csv.writer(stats_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(statsHeaders)
    stats_file.close()
    # timeline participants
    with open('data/dataframes/timelineParticipants.csv', mode='w', encoding="utf8") as timePar:
        writer = csv.writer(timePar, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(timelinePartci)
    timePar.close()
    # timeline Events
    with open('data/dataframes/timelineEvents.csv', mode='w', encoding="utf8") as timeEvents:
        writer = csv.writer(timeEvents, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(timelineEvents)
    timeEvents.close()
    print("done with init")


# Consider writing this within the file listing in parsing Match JSON
def updateCSV(listing, file, header):
    # Be concerend about stats as there are deltas
    with open(file, mode='a', encoding="utf8") as infile:
        writer = csv.writer(infile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        listOFValues = []
        for item in listing:
            for col in header:
                if col in item:
                    # If its is a list
                    if type(item[col]) == list:
                        # Make list into a string
                        string = " ".join(item[col])
                        listOFValues.append(string)
                    # If its not a list
                    else:
                        listOFValues.append(item[col])
                else:
                    listOFValues.append('')
            writer.writerow(listOFValues)
            listOFValues = []
    infile.close()


def parseMatchJson(listOfMatchFiles):
    # Make sure to change filename to GameID+PlayerID
    # We have 3 lists we want to separate into Core, ParticipantsID and Stats
    # More on ordering here
    # https://docs.google.com/spreadsheets/d/1a3AvG-0e2DpzSqdabDCaInCD827hnREF0mUQQAEPbM4/edit#gid=0
    # Or you can look at DataFrameMatchesOrdering.txt to get a better understanding
    # Additionally data is aggregated into one list of dictionaries of list of ... yea you get the point
    matchListData = []
    # Basically list of tuples
    core, Participants, Stats = {}, {}, {}
    # List of labels
    labelCore, labelParticipants, labelStats = [], [], []
    coreList, participantList, statsList = [], [], []
    deltas = ['creepsPerMinDeltas', 'damageTakenPerMinDeltas', 'goldPerMinDeltas', 'xpPerMinDeltas',
              'xpDiffPerMinDeltas', 'csDiffPerMinDeltas', 'damageTakenDiffPerMinDeltas']
    constants = {"gameId": 0}
    with open("data/DataFrameMatchesOrdering.txt", "r", encoding="utf8") as outfile:
        next(outfile)
        listing = []
        for line in outfile:
            if "Participants" in line:
                labelCore = listing
                listing = []
            elif "Stats" in line:
                labelParticipants = listing
                listing = []
            else:
                line = line.rstrip()
                listing.append(line)
        labelStats = listing
    outfile.close()

    for file in listOfMatchFiles:
        print("Match parse on", file)
        specfile = "data/matches/" + file
        constants["gameId"] = file[:file.find("m")]
        check = False
        with open(specfile, "r", encoding="utf8") as outfile:
            core["gameId"] = constants["gameId"]
            for line in outfile:
                if "teams" in line:
                    break
                if "participants" in line:
                    check = True
                label = line[1:line.find(':')].replace('"', "").strip()
                value = line[line.find(':') + 1:len(line) - 1].replace('"', "").replace(",", "").strip()
                # If value if found, store it in a dictionary
                if label in labelCore:
                    core[label] = value
                elif (label in labelParticipants) and (check == False):
                    Participants[label] = value
                    if label in "summonerName":
                        # last item push everything
                        Participants["gameId"] = constants["gameId"]
                        participantList.append(Participants)
                        # For Resetting
                        Participants = {}
                # For Stats
                elif label in labelStats:
                    if label in "championId" and Stats != None:
                        Stats["gameId"] = constants["gameId"]
                        statsList.append(Stats)
                        Stats = {}
                    previousLabel = label
                    # Deltas Check Still a problem with deltas
                    if label in deltas:
                        listing = []
                        while label not in "}":
                            line = next(outfile)
                            label = line[line.find('"') + 1:line.find(":") - 1].replace('"', "").strip()
                            if label in "}" or label in "},":
                                break
                            numValue = line[line.find(":") + 1:].replace(",", "").strip()
                            listing.append(numValue)
                        value = listing
                    # Not A Delta
                    Stats[previousLabel] = value

        outfile.close()
        coreList.append(core)

        # check for missing values can take out later
        # for key in core:
        # print(key, core[key])
        # for parti in participantList:
        # for item in parti:
        # print(item, parti[item])
        # break
        # break
        # for st in statsList:
        # for item in st:
        # print(item, st[item])
        # break
        core = {}

        matchListData.append(coreList)
        matchListData.append(participantList)
        matchListData.append(statsList)

    return matchListData


def parseTimeline(filelist):
    # GameID is in file name
    participants, events = {}, {}
    participantList, eventsLists = [], []
    labelParticipants, labelEvents = [], []
    timelineData = []
    # Loading in all labels
    with open("data/DataFrameOrderingMT.txt", "r", encoding="utf8") as outfile:
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
    for file in filelist:
        print("parse timeline on", file)
        specfile = "data/matchTimelines/" + file
        gameId = file[:file.find("m")]
        check, innerCheck = True, True
        with open(specfile, "r", encoding="utf8") as outfile:
            for line in outfile:
                if "participantFrames" in line:
                    check = False
                    events['gameId'] = gameId
                    eventsLists.append(events)
                    events = {}
                elif "events" in line:
                    check = True
                    participants['gameId'] = gameId
                    participantList.append(participants)
                    participants = {}
                elif "levelUpType" in line:
                    count = 0
                    while count < 5:
                        line = next(outfile)
                        count += 1
                else:
                    label = line[1:line.find(':')].replace('"', "").strip()
                    value = line[line.find(':') + 1:len(line) - 1].replace('"', "").replace(",", "").strip()
                    # Events
                    if check and label in labelEvents:
                        # Adding previous to eventListing
                        if label in events.keys():
                            if events[label] != value:
                                events['gameId'] = gameId
                                eventsLists.append(events)
                                events = {}
                        events[label] = value
                    # participantFrames
                    elif check == False and label in labelParticipants:
                        participants[label] = value
                        # xp is the last thing in Events so push everything into the event list
                        if "xp" in label:
                            participants['gameId'] = gameId
                            participantList.append(participants)
                            participants = {}

        timelineData.append(eventsLists)
        timelineData.append(participantList)
        outfile.close()
    return timelineData, labelParticipants, labelEvents


def populateList(category):
    listing = []
    print("populating", category)
    path = "./data/" + category
    for root, dirs, files in os.walk(path):
        for file in files:
            if "json" in file:
                listing.append(file)
    return listing

def seenGameId(gameId):
    with open(""):

def main():
    fileMatchList = populateList("matches")
    fileMatchTimelineList = populateList("matchTimelines")

    # Parse through list of matches
    print("parsing matches")
    # Need to introduce limiter by splitting size by 1k
    # resultingList = parseMatchJson(fileMatchList)
    coreHeader, partHeaders, statsHeaders = getHeaders()
    # resultTimelines, timelinePartci, timelineEvents = parseTimeline(fileMatchTimelineList)
    timelinePartci.append("gameId")
    timelineEvents.append("gameId")
    # To initialize CSV's
    print("init CSV")
    initCSV(coreHeader, partHeaders, statsHeaders, timelinePartci, timelineEvents)
    # Actual updating
    # updateCSV(resultingList[0], "data/dataframes/matchcores.csv", coreHeader)
    # updateCSV(resultingList[1], "data/dataframes/matchparticipants.csv", partHeaders)
    # resultingList[2].pop(0)
    # n = resultingList[2]
    # updateCSV(n, "data/dataframes/matchstats.csv", statsHeaders)
    # resultTimelines[0].pop(0)
    # resultTimelines[1].pop(0)
    # updateCSV(resultTimelines[0], "data/dataframes/timelineEvents.csv", timelineEvents)
    # updateCSV(resultTimelines[1], "data/dataframes/timelineParticipants.csv", timelinePartci)


if __name__ == "__main__":
    main()
