import Globals
import json
import os


class SplitValues:
    def __init__(self, splitMatches=0, splitMatchWins=0, splitSeries=0, splitSeriesWins=0):
        self._splitMatches = splitMatches
        self._splitMatchWins = splitMatchWins
        self._splitSeries = splitSeries
        self._splitSeriesWins = splitSeriesWins

    @property
    def splitMatches(self):
        return self._splitMatches

    @splitMatches.setter
    def splitMatches(self, splitMatches):
        self._splitMatches = splitMatches

    @property
    def splitMatchWins(self):
        return self._splitMatchWins

    @splitMatchWins.setter
    def splitMatchWins(self, splitMatchWins):
        self._splitMatchWins = splitMatchWins

    @property
    def splitSeries(self):
        return self._splitSeries

    @splitSeries.setter
    def splitSeries(self, splitSeries):
        self._splitSeries = splitSeries

    @property
    def splitSeriesWins(self):
        return self._splitSeriesWins

    @splitSeriesWins.setter
    def splitSeriesWins(self, splitSeriesWins):
        self._splitSeriesWins = splitSeriesWins

    def matchWinPercentage(self):
        if self._splitMatches == 0:
            return 0
        else:
            return self._splitMatchWins / self._splitMatches

    def seriesWinPercentage(self):
        if self._splitSeries == 0:
            return 0
        else:
            return self._splitSeriesWins / self._splitSeries


class SeasonValues:
    def __init__(self, seasonMatches=0, seasonMatchWins=0, seasonSeries=0, seasonSeriesWins=0):
        self._seasonMatches = seasonMatches
        self._seasonMatchWins = seasonMatchWins
        self._seasonSeries = seasonSeries
        self._seasonSeriesWins = seasonSeriesWins
        self._splitValues = []

    @property
    def seasonMatches(self):
        return self._seasonMatches

    @seasonMatches.setter
    def seasonMatches(self, seasonMatches):
        self._seasonMatches = seasonMatches

    @property
    def seasonMatchWins(self):
        return self._seasonMatchWins

    @seasonMatchWins.setter
    def seasonMatchWins(self, seasonMatchWins):
        self._seasonMatchWins = seasonMatchWins

    @property
    def seasonSeries(self):
        return self._seasonSeries

    @seasonSeries.setter
    def seasonSeries(self, seasonSeries):
        self._seasonSeries = seasonSeries

    @property
    def seasonSeriesWins(self):
        return self._seasonSeriesWins

    @seasonSeriesWins.setter
    def seasonSeriesWins(self, seasonSeriesWins):
        self._seasonSeriesWins = seasonSeriesWins

    @property
    def splitValues(self):
        return self._splitValues

    @splitValues.setter
    def splitValues(self, splitValues):
        self._splitValues = splitValues

    def addSplitValues(self, splitValues):
        self._splitValues.append(splitValues)

    def matchWinPercentage(self):
        if self._seasonMatches == 0:
            return 0
        else:
            return self._seasonMatchWins / self._seasonMatches

    def seriesWinPercentage(self):
        if self._seasonSeries == 0:
            return 0
        else:
            return self._seasonSeriesWins / self._seasonSeries


class Team:
    def __init__(self, name, region, id, totalMatches=0, totalMatchWins=0, totalSeries=0, totalSeriesWins=0):
        self._name = name
        for i in Globals.regions:
            if region == i:
                self._region = region
                break
        self._id = region + "_" + id
        self._totalMatches = totalMatches
        self._totalMatchWins = totalMatchWins
        self._totalSeries = totalSeries
        self._totalSeriesWins = totalSeriesWins
        self._seasonValues = []
        self._dict = {}

    def __str__(self):
        return self._id

    def loadData(self):
        if not (os.path.isfile(Globals.settings["path"] + "teams\\" + self._region + "\\" + self._id + ".json")):
            file = open(Globals.settings["path"] + "teams\\" + self._region + "\\" + self._id + ".json", "a")
            file.write("{\n\"name\": \"" + self._name + "\"\n}")
            file.close()
        else:
            file = open(Globals.settings["path"] + "teams\\" + self._region + "\\" + self._id + ".json")
            self._dict = json.load(file)

            self._totalMatches = self._dict["totalMatches"]
            self._totalMatchWins = self._dict["totalMatchWins"]
            self._totalSeries = self._dict["totalSeries"]
            self._totalSeriesWins = self._dict["totalSeriesWins"]
            file.close()

    def saveData(self):
        #Loading Values to dict
        self._dict.update({"totalMatches": self._totalMatches, "totalMatchWins": self._totalMatchWins, "totalSeries": self._totalSeries, "totalSeriesWins": self._totalSeriesWins})

        file = open(Globals.settings["path"] + "teams\\" + self._region + "\\" + self._id + ".json", "w")
        file.write(json.dumps(self._dict, indent=5))
        file.close()

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def region(self):
        return self._region

    @region.setter
    def region(self, region):
        self._region = region

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        self._id = id

    @property
    def seasonValues(self):
        return self._seasonValues

    @seasonValues.setter
    def seasonValues(self, seasonValues):
        self._seasonValues = seasonValues

    def addSeasonValues(self, seasonValues):
        self._seasonValues.append(seasonValues)

    @property
    def totalMatches(self):
        return self._totalMatches

    @totalMatches.setter
    def totalMatches(self, totalMatches):
        self._totalMatches = totalMatches

    @property
    def totalMatchWins(self):
        return self._totalMatchWins

    @totalMatchWins.setter
    def totalMatchWins(self, totalMatchWins):
        self._totalMatchWins = totalMatchWins

    @property
    def totalSeries(self):
        return self._totalSeries

    @totalSeries.setter
    def totalSeries(self, totalSeries):
        self._totalSeries = totalSeries

    @property
    def totalSeriesWins(self):
        return self._totalSeriesWins

    @totalSeriesWins.setter
    def totalSeriesWins(self, totalSeriesWins):
        self._totalSeriesWins = totalSeriesWins

    def matchWinPercentage(self):
        if self._totalMatches == 0:
            return 0
        else:
            return self._totalMatchWins / self._totalMatches

    def seriesWinPercentage(self):
        if self._totalSeries == 0:
            return 0
        else:
            return self._totalSeriesWins / self._totalSeries


def sort(list):
    less = []
    equal = []
    greater = []

    if len(list) > 1:
        pivot = list[0].name

        for team in list:
            if team.name < pivot:
                less.append(team)
            elif team.name == pivot:
                equal.append(team)
            elif team.name > pivot:
                greater.append(team)

        return sort(less) + equal + sort(greater)

    else:
        return list


def removeDuplicates(list):
    indicies = []
    for i in range(len(list)):
        if i == 0:
            continue
        else:
            if str(list[i]) == str(list[i-1]):
                indicies.append(i - len(indicies))

    for i in indicies:
        list.pop(i)

    return list


europeanTeams = []
europeanTeamsUnsorted = []
northAmericanTeams = []
northAmericanTeamsUnsorted = []
southAmericanTeams = []
southAmericanTeamsUnsorted = []
oceanicTeams = []
oceanicTeamsUnsorted = []
middleEastNorthAfricanTeams = []
middleEastNorthAfricanTeamsUnsorted = []
asiaPacificNorthTeams = []
asiaPacificNorthTeamsUnsorted = []
asiaPacificSouthTeams = []
asiaPacificSouthTeamsUnsorted = []
subSaharanAfricanTeams = []
subSaharanAfricanTeamsUnsorted = []
placeholder = Team("TBD", "", "tbd")
defwin = Team("BYE", "", "bye")


def readTeamsJson():
    with open(Globals.settings["path"] + "config\\teams.json") as teamsFile:
        teamsJson = json.load(teamsFile)
        for team in teamsJson["teams"]:
            if team["region"] == "EU":
                europeanTeamsUnsorted.append(Team(team["name"], "EU", team["id"]))
            elif team["region"] == "NA":
                northAmericanTeamsUnsorted.append(Team(team["name"], "NA", team["id"]))
            elif team["region"] == "SAM":
                southAmericanTeamsUnsorted.append(Team(team["name"], "SAM", team["id"]))
            elif team["region"] == "OCE":
                oceanicTeamsUnsorted.append(Team(team["name"], "OCE", team["id"]))
            elif team["region"] == "MENA":
                middleEastNorthAfricanTeamsUnsorted.append(Team(team["name"], "MENA", team["id"]))
            elif team["region"] == "APACN":
                asiaPacificNorthTeamsUnsorted.append(Team(team["name"], "APACN", team["id"]))
            elif team["region"] == "APACS":
                asiaPacificSouthTeamsUnsorted.append(Team(team["name"], "APACS", team["id"]))
            elif team["region"] == "SSA":
                subSaharanAfricanTeamsUnsorted.append(Team(team["name"], "SSA", team["id"]))

        teamsFile.close()

    _europeanTeams = removeDuplicates(sort(europeanTeamsUnsorted))
    for team in _europeanTeams:
        team.loadData()
        europeanTeams.append(team)
    _northAmericanTeams = removeDuplicates(sort(northAmericanTeamsUnsorted))
    for team in _northAmericanTeams:
        team.loadData()
        northAmericanTeams.append(team)
    _southAmericanTeams = removeDuplicates(sort(southAmericanTeamsUnsorted))
    for team in _southAmericanTeams:
        team.loadData()
        southAmericanTeams.append(team)
    _oceanicTeams = removeDuplicates(sort(oceanicTeamsUnsorted))
    for team in _oceanicTeams:
        team.loadData()
        oceanicTeams.append(team)
    _middleEastNorthAfricanTeams = removeDuplicates(sort(middleEastNorthAfricanTeamsUnsorted))
    for team in _middleEastNorthAfricanTeams:
        team.loadData()
        middleEastNorthAfricanTeams.append(team)
    _asiaPacificNorthTeams = removeDuplicates(sort(asiaPacificNorthTeamsUnsorted))
    for team in _asiaPacificNorthTeams:
        team.loadData()
        asiaPacificNorthTeams.append(team)
    _asiaPacificSouthTeams = removeDuplicates(sort(asiaPacificSouthTeamsUnsorted))
    for team in _asiaPacificSouthTeams:
        team.loadData()
        asiaPacificSouthTeams.append(team)
    _subSaharanAfricanTeams = removeDuplicates(sort(subSaharanAfricanTeamsUnsorted))
    for team in _subSaharanAfricanTeams:
        team.loadData()
        subSaharanAfricanTeams.append(team)


def saveAllTeamData():
    for team in europeanTeams:
        team.saveData()

    for team in northAmericanTeams:
        team.saveData()

    for team in southAmericanTeams:
        team.saveData()

    for team in oceanicTeams:
        team.saveData()

    for team in middleEastNorthAfricanTeams:
        team.saveData()

    for team in asiaPacificNorthTeams:
        team.saveData()

    for team in asiaPacificSouthTeams:
        team.saveData()

    for team in subSaharanAfricanTeams:
        team.saveData()


def getTeamById(teamId):
    if teamId == placeholder.id:
        return placeholder
    elif teamId.split("_")[0] == "EU":
        for team in europeanTeams:
            if team.id == teamId:
                return team
    elif teamId.split("_")[0] == "NA":
        for team in northAmericanTeams:
            if team.id == teamId:
                return team
    elif teamId.split("_")[0] == "OCE":
        for team in oceanicTeams:
            if team.id == teamId:
                return team
    elif teamId.split("_")[0] == "SAM":
        for team in southAmericanTeams:
            if team.id == teamId:
                return team
    elif teamId.split("_")[0] == "MENA":
        for team in middleEastNorthAfricanTeams:
            if team.id == teamId:
                return team
    elif teamId.split("_")[0] == "APACN":
        for team in asiaPacificNorthTeams:
            if team.id == teamId:
                return team
    elif teamId.split("_")[0] == "APACS":
        for team in asiaPacificSouthTeams:
            if team.id == teamId:
                return team
    elif teamId.split("_")[0] == "SSA":
        for team in subSaharanAfricanTeams:
            if team.id == teamId:
                return team


def teamsByRegion(region, filter=[]):
    if not filter:
        if region == "EU":
            return europeanTeams
        elif region == "NA":
            return northAmericanTeams
        elif region == "SAM":
            return southAmericanTeams
        elif region == "OCE":
            return oceanicTeams
        elif region == "MENA":
            return middleEastNorthAfricanTeams
        elif region == "APACN":
            return asiaPacificNorthTeams
        elif region == "APACS":
            return asiaPacificSouthTeams
        elif region == "SSA":
            return subSaharanAfricanTeams
    else:
        if region == "EU":
            teams = europeanTeams
            for team in filter:
                teams.remove(team)
            return teams
        elif region == "NA":
            teams = northAmericanTeams
            for team in filter:
                teams.remove(team)
            return teams
        elif region == "SAM":
            teams = southAmericanTeams
            for team in filter:
                teams.remove(team)
            return teams
        elif region == "OCE":
            teams = oceanicTeams
            for team in filter:
                teams.remove(team)
            return teams
        elif region == "MENA":
            teams = middleEastNorthAfricanTeams
            for team in filter:
                teams.remove(team)
            return teams
        elif region == "APACN":
            teams = asiaPacificNorthTeams
            for team in filter:
                teams.remove(team)
            return teams
        elif region == "APACS":
            teams = asiaPacificSouthTeams
            for team in filter:
                teams.remove(team)
            return teams
        elif region == "SSA":
            teams = subSaharanAfricanTeams
            for team in filter:
                teams.remove(team)
            return teams
