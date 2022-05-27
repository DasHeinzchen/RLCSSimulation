import tkinter as tk
import random

import EventHandler
import Globals
import Team


class ScoreWindow:
    def __init__(self):
        scoreWindow = tk.Tk()
        scoreWindow.title("Score Window")
        scoreWindow.eval('tk::PlaceWindow . center')

        season, split, event = EventHandler.load()
        series = EventHandler.loadFormat(event.formatDict)[2]

        team1Lbl = tk.Label(scoreWindow, text=Team.getTeamById(series["team1"]).name)
        team2Lbl = tk.Label(scoreWindow, text=Team.getTeamById(series["team2"]).name)
        seriesScoreLblMid = tk.Label(scoreWindow, text="Series Score")
        seriesScoreLblT1 = tk.Label(scoreWindow, text=str(series["score1"]))
        seriesScoreLblT2 = tk.Label(scoreWindow, text=str(series["score2"]))
        enterScoreLbl = tk.Label(scoreWindow, text="Enter match score")
        team1Entry = tk.Entry(scoreWindow)
        team2Entry = tk.Entry(scoreWindow)

        def submit():
            if team1Entry.get().isdigit() and team2Entry.get().isdigit():
                if int(team1Entry.get()) is not int(team2Entry.get()):
                    event.formatDict, condition = EventHandler.submitScore(
                        int(team1Entry.get()), int(team2Entry.get()), event.formatDict)

                    event.saveData()

                    if condition: EventHandler.eventFinished()

                    scoreWindow.destroy()
                else:
                    print("Score is equal")
            else:
                print("Invalid Entry Text")

        def simulate():
            loopCondition = True
            while loopCondition:
                score1 = random.randint(0, 10)
                score2 = random.randint(0, 10)
                if not score1 == score2:
                    loopCondition = False
                    event.formatDict, condition = EventHandler.submitScore(score1, score2, event.formatDict)

                    event.saveData()

                    if condition: EventHandler.eventFinished()

                    scoreWindow.destroy()

        cnfrmBtn = tk.Button(scoreWindow, text="Confirm", command=submit)
        simulateBtn = tk.Button(scoreWindow, text="Simulate", command=simulate)

        team1Lbl.grid(row=0, column=0)
        team2Lbl.grid(row=0, column=2)
        seriesScoreLblMid.grid(row=1, column=1)
        seriesScoreLblT1.grid(row=1, column=0)
        seriesScoreLblT2.grid(row=1, column=2)
        enterScoreLbl.grid(row=2, column=1)
        team1Entry.grid(row=2, column=0)
        team2Entry.grid(row=2, column=2)
        cnfrmBtn.grid(row=3, column=1)
        simulateBtn.grid(row=4, column=1)

        scoreWindow.mainloop()


class MainWindow:
    def __init__(self):
        mainWindow = tk.Tk()
        mainWindow.title("Main Window")
        mainWindow.eval('tk::PlaceWindow . center')

        def openScoreWindow():
            ScoreWindow()

        def close():
            EventHandler.close()
            mainWindow.destroy()

        def openSeasonOverviewWindow():
            SeasonOverviewWindow()

        def openSeasonCreateWindow():
            SeasonCreateWindow()

        def simulateBracket():
            season, split, event = EventHandler.load()
            bracket = EventHandler.loadFormat(event.formatDict)[0]

            while bracket["current"] and not bracket["currentPart"] == "":
                loopCondition = True
                while loopCondition:
                    score1 = random.randint(0, 10)
                    score2 = random.randint(0, 10)
                    if not score1 == score2:
                        loopCondition = False
                        event.formatDict, condition = EventHandler.submitScore(score1, score2, event.formatDict)

                        event.saveData()

                        if condition: EventHandler.eventFinished()
            print("simulated Bracket: " + bracket["id"])

        scoreWindowBtn = tk.Button(mainWindow, text="Open Score Window", command=openScoreWindow)
        closeBtn = tk.Button(mainWindow, text="Close", command=close)
        viewCurrentSeasonBtn = tk.Button(mainWindow, text="View current Season", command=openSeasonOverviewWindow)
        createSeasonBtn = tk.Button(mainWindow, text="Create new Season", command=openSeasonCreateWindow)
        simulateBracketBtn = tk.Button(mainWindow, text="Simulate Bracket", command=simulateBracket)

        scoreWindowBtn.grid(row=0, column=0)
        viewCurrentSeasonBtn.grid(row=1, column=0)
        createSeasonBtn.grid(row=2, column=0)
        simulateBracketBtn.grid(row=3, column=0)
        closeBtn.grid(row=4, column=0)

        mainWindow.mainloop()


class SeasonOverviewWindow:
    def __init__(self):
        seasonOverviewWindow = tk.Tk()
        seasonOverviewWindow.title("Season Overview")
        seasonOverviewWindow.eval('tk::PlaceWindow . center')

        seasonOverviewWindow.mainloop()


class SeasonCreateWindow:

    def __init__(self):
        seasonCreateWindow = tk.Tk()
        seasonCreateWindow.title("Create Season")
        seasonCreateWindow.eval('tk::PlaceWindow . center')

        regions = [[], [], []]
        dictionaryQual = {"invit": {}, "open": {}}

        def create():
            EventHandler.initializeSeason(dictionaryQual)

            seasonCreateWindow.destroy()

        def switchEU():
            switch("EU")

        def switchNA():
            switch("NA")

        def switchSAM():
            switch("SAM")

        def switchOCE():
            switch("OCE")

        def switchMENA():
            switch("MENA")

        def switchAPACN():
            switch("APACN")

        def switchAPACS():
            switch("APACS")

        def switchSSA():
            switch("SSA")

        def switch(region):
            if regions[0][Globals.regions.index(region)]["text"] == region:
                regions[0][Globals.regions.index(region)].config(text="")
                regions[1][Globals.regions.index(region)].config(text=region)
                dictionaryQual["invit"][region] = False
                dictionaryQual["open"][region] = True
            else:
                regions[0][Globals.regions.index(region)].config(text=region)
                regions[1][Globals.regions.index(region)].config(text="")
                dictionaryQual["invit"][region] = True
                dictionaryQual["open"][region] = False

        for region in Globals.regions:
            dictionaryQual["invit"].update({region: False})
            dictionaryQual["open"].update({region: True})
            regions[0].append(tk.Label(seasonCreateWindow))
            regions[1].append(tk.Label(seasonCreateWindow, text=region))
            if region == "EU":
                regions[2].append(tk.Button(seasonCreateWindow, text="<-->", command=switchEU))
            elif region == "NA":
                regions[2].append(tk.Button(seasonCreateWindow, text="<-->", command=switchNA))
            elif region == "SAM":
                regions[2].append(tk.Button(seasonCreateWindow, text="<-->", command=switchSAM))
            elif region == "OCE":
                regions[2].append(tk.Button(seasonCreateWindow, text="<-->", command=switchOCE))
            elif region == "MENA":
                regions[2].append(tk.Button(seasonCreateWindow, text="<-->", command=switchMENA))
            elif region == "APACN":
                regions[2].append(tk.Button(seasonCreateWindow, text="<-->", command=switchAPACN))
            elif region == "APACS":
                regions[2].append(tk.Button(seasonCreateWindow, text="<-->", command=switchAPACS))
            elif region == "SSA":
                regions[2].append(tk.Button(seasonCreateWindow, text="<-->", command=switchSSA))

        noteLbl = tk.Label(seasonCreateWindow, text="Note: The new Season will be marked as current")
        invitLbl = tk.Label(seasonCreateWindow, text="Invitational Qualifier")
        openLbl = tk.Label(seasonCreateWindow, text="Open Qualifier")
        closeBtn = tk.Button(seasonCreateWindow, text="Create new Season", command=create)

        noteLbl.grid(row=0, column=1)
        invitLbl.grid(row=1, column=0)
        openLbl.grid(row=1, column=2)
        closeBtn.grid(row=15, column=1)

        for i in range(len(Globals.regions)):
            regions[0][i].grid(row=2+i, column=0)
            regions[1][i].grid(row=2+i, column=2)
            regions[2][i].grid(row=2+i, column=1)

        seasonCreateWindow.mainloop()
