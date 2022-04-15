import tkinter as tk
import random

import EventHandler
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
                    event.formatDict = EventHandler.submitScore(int(team1Entry.get()), int(team2Entry.get()), event.formatDict)

                    event.saveData()

                    scoreWindow.destroy()
                else:
                    print("Score is equal")
            else:
                print("Invalid Entry Text")

        def simulate():
            condition = True
            while condition:
                score1 = random.randint(0, 10)
                score2 = random.randint(0, 10)
                if not score1 == score2:
                    condition = False
                    event.formatDict = EventHandler.submitScore(score1, score2, event.formatDict)

                    event.saveData()

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

        scoreWindowBtn = tk.Button(mainWindow, text="Open Score Window", command=openScoreWindow)
        closeBtn = tk.Button(mainWindow, text="Close", command=close)
        viewCurrentSeasonBtn = tk.Button(mainWindow, text="View current Season", command=openSeasonOverviewWindow)
        createSeasonBtn = tk.Button(mainWindow, text="Create new Season", command=openSeasonCreateWindow)

        scoreWindowBtn.grid(row=0, column=0)
        viewCurrentSeasonBtn.grid(row=1, column=0)
        createSeasonBtn.grid(row=2, column=0)
        closeBtn.grid(row=3, column=0)

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

        def create():
            #Season.addSeason()
            EventHandler.initializeSeason()

            seasonCreateWindow.destroy()

        noteLbl = tk.Label(seasonCreateWindow, text="Note: The new Season will be marked as current")
        closeBtn = tk.Button(seasonCreateWindow, text="Create new Season", command=create)

        noteLbl.grid(row=0, column=0)
        closeBtn.grid(row=1, column=0)

        seasonCreateWindow.mainloop()
