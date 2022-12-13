import tkinter as tk
from tkinter.filedialog import askdirectory
import os
import librosa
import pygame
import time
import random

global path
global filename
global score_file

score_file = "score_file.txt"

class NoteManiaClass(tk.Tk):
    
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        container = tk.Frame(self,
                             width = 1280,
                             height = 720)
        container.grid()

        self.frame = {}
   
        for F in (MenuScreenClass, SongSelectionScreenClass, GameScreenClass, PauseScreenClass, ResultsScreenClass):
            frame = F(container, self)
            self.frame[F] = frame
            frame.grid(row=0, column=0, sticky="NSEW")

        self.show_frame(MenuScreenClass)
     
    def show_frame(self, cont):
        
        frame = self.frame[cont]
        frame.tkraise()

class MenuScreenClass(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        menuScreenFrame = tk.Frame(self,
                                   bg = "Black")
        menuScreenFrame.grid()

        gameNameFrame = tk.Frame(menuScreenFrame,
                                 bg = "Black")
        gameNameFrame.grid(sticky = "W")

        gameNameLabel = tk.Label(gameNameFrame,
                                 text = "Note Mania",
                                 font = "Trebuchet 79 bold",
                                 fg = "red4",
                                 bg = "Black")
        gameNameLabel.grid(row = 0,
                           column = 0,
                           padx = (20,0),
                           pady = (0,225))

        menuButtonsFrame = tk.Frame(menuScreenFrame,
                                    bg = "Black")
        menuButtonsFrame.grid(sticky = "E",
                              row = 0,
                              column = 1,
                              padx = (99,0),
                              pady = (239,0),
                              ipady = 221)

        startButton = tk.Button(menuButtonsFrame,
                                relief = "sunken",
                                width = 18,
                                text = "Start ",
                                anchor = "e",
                                font = "Trebuchet 40 bold",
                                fg = "White",
                                activeforeground = "grey46",
                                bg = "Black",
                                activebackground = "Black",
                                bd = 8,
                                command = lambda: controller.show_frame(SongSelectionScreenClass))
        startButton.grid(sticky = "E")

        def closeMenu():

            gameNameLabel.grid_forget()

            quitBtnsFrame = tk.Frame(gameNameFrame,
                                     bg = "Black")
            quitBtnsFrame.grid(pady = (0,200))      

            askQuitLabel = tk.Label(quitBtnsFrame,
                                    text = "Are you sure you\nwould like to quit?",
                                    font = "Trebuchet 30 bold",
                                    fg = "red4",
                                    bg = "Black")
            askQuitLabel.grid(column = 0,
                              columnspan = 2,
                              row = 0,
                              padx = (108,126),
                              pady = (0,50))

            def hideQuitLabels():

                quitBtnsFrame.destroy()
                askQuitLabel.destroy()
                gameNameLabel.grid(row = 0,
                                   padx = (20,0),
                                   pady = (0,225))
                
                quitButton.config(state="active",
                                  activeforeground = "White")
                startButton.config(state = "active",
                                   activeforeground = "White")

            yesQuitButton = tk.Button(quitBtnsFrame,
                                      text = "Yes",
                                      font = "Trebuchet 15 bold",
                                      fg = "White",
                                      activeforeground = "grey46",
                                      bg = "Black",
                                      activebackground = "Black",
                                      borderwidth = 0,
                                      command = lambda: game.destroy())
            yesQuitButton.grid(column = 0,
                               row = 1,
                               padx = (130,0),
                               sticky = "EW")

            noQuitButton = tk.Button(quitBtnsFrame,
                                     width = 10,
                                     text = "No",
                                     font = "Trebuchet 15 bold",
                                     fg = "White",
                                     activeforeground = "grey46",
                                     bg = "Black",
                                     activebackground = "Black",
                                     borderwidth = 0,
                                     anchor = "w",
                                     command = hideQuitLabels)
            noQuitButton.grid(column = 1,
                              row = 1,
                              sticky = "W")

            quitButton.config(state = "disabled")
            startButton.config(state = "disabled",
                               disabledforeground = "White")

        quitButton = tk.Button(menuButtonsFrame,
                               relief = "sunken",
                               width = 18,
                               text = "Quit ",
                               anchor = "e",# align text to right
                               font = "Trebuchet 40 bold",
                               fg = "White",
                               activeforeground = "grey46",
                               bg = "Black",
                               activebackground = "Black",
                               bd = 8,
                               command = closeMenu)
        quitButton.grid(sticky = "E")

class SongSelectionScreenClass(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)

        songSelectionScreenFrame = tk.Frame(self,
                                            bg = "Black",
                                            width = 1280,
                                            height = 720)
        songSelectionScreenFrame.grid(ipady = 1)

        leaderboardFrame = tk.Frame(songSelectionScreenFrame,
                                 bg = "Black",
                                    width = 591)
        leaderboardFrame.grid()

        leaderboardButtonsFrame = tk.Frame(leaderboardFrame,
                                           bg = "Black")
        leaderboardButtonsFrame.grid(row = 0,
                                     column = 0,
                                     columnspan = 2,
                                     pady = (94,0))

        localLeaderboardButton = tk.Button(leaderboardButtonsFrame,
                                           text = "All local scores",
                                           font = "Helvetica 25",
                                           fg = "White",
                                           activeforeground = "grey46",
                                           bg = "Black",
                                           activebackground = "Black",
                                           borderwidth = 0)
        localLeaderboardButton.grid(row = 0,
                                    column = 0,
                                    padx = (0,20))
        
        ownLeaderboardButton = tk.Button(leaderboardButtonsFrame,
                                      text = "Own scores",
                                      font = "Helvetica 25",
                                      fg = "White",
                                      #when clicked, text is grey
                                      activeforeground = "grey46",
                                      bg = "Black",
                                      #when clicked, bg stays black
                                      activebackground = "Black",
                                      borderwidth = 0)
        ownLeaderboardButton.grid(row = 0,
                                  column = 1,
                                  padx = (20,0))

        leaderboard = tk.Listbox(leaderboardFrame,
                                 width = 35,
                                 height = 12,
                                 bg = "Black",
                                 bd = 8,
                                 relief = "sunken",
                                 font = "Trebuchet 20",
                                 fg = "White")

        # set up lists so contents can be sorted and appended
        leaderboardList = [] 
        leaderboardNames = []
        leaderboardScores = []

        leaderboard.delete(0,tk.END) # clear contents of leaderboard
        with open(score_file) as f:
            for line in f:
                leaderboardList += line.split()
        for name in range(0,(len(leaderboardList)),2):
            leaderboardNames.append(leaderboardList[name])
        for score in range(1,(len(leaderboardList)),2):
            leaderboardScores.append(leaderboardList[score])

        sortHighScores = zip(leaderboardScores,leaderboardNames) # zip lists together
        sortHighScores.sort(reverse = True)
        sortedHighScores = [leaderboardList for leaderboardScores, leaderboardList in sortHighScores]

        for result in range(len(leaderboardList)):
            leaderboard.insert(tk.END, leaderboardList[result])
        
        leaderboardScrollBar = tk.Scrollbar(leaderboardFrame)
        leaderboardScrollBar.grid(row = 1,
                                  column = 0,
                                  sticky = "NSW",
                                  pady = (0,0))
        leaderboard.config(yscrollcommand = leaderboardScrollBar.set)

        songSelectionFrame = tk.Frame(songSelectionScreenFrame,
                                      bg = "Black")
        songSelectionFrame.grid(row = 0,
                                column = 2,
                                columnspan = 3,
                                padx = (86,0),
                                pady = (109,0))

        searchSongsFrame = tk.Frame(songSelectionFrame,
                                    bg = "Black",
                                    width = 591,
                                    height = 40)
        searchSongsFrame.grid(row = 0,
                              column = 2,
                              columnspan = 3,
                              padx = (10,0))

        # drop down list to sort through songs
        #   A-Z, Z-A, ascending length, descending length
        sortBy = tk.StringVar(leaderboardFrame)
        sortBy.set("Sort by..")

        # drop down list gives the following options to sort by
        sortSongsOption = tk.OptionMenu(songSelectionFrame,
                                     sortBy,
                                     "(Unsorted)",
                                     "A-Z",
                                     "Z-A",
                                     "Length (ascending)",
                                     "Length (descending)")
        sortSongsOption.grid(row = 0,
                             column = 2,
                             padx = (20,0),
                             sticky = "EW")
        
        def sortSongs(path):

            value = sortBy.get()
            userSongList = []
            userSongLengthList = []
            songList.delete(0,tk.END)

            for filename in path:
                if filename.endswith('mp3'):
                    userSongList.append(filename)

            if value == "A-Z":
                userSongList.sort()
            elif value == "Z-A":
                userSongList.sort(reverse = True)
            elif value == "Length (ascending)":
                for i in userSongList:
                    if filename.endswith('mp3'):
                        y, sr = librosa.load(path + "'\'" + filename)
                        length = librosa.get_duration(y=y, sr=sr)
                        userSongLengthList.append(length)
                sortByLengthA = zip(userSongLengthList,userSongList)
                sortByLengthA.sort()
                sortedSongLengthA = [userSongList for userSongListLength, userSongList in sortByLengthA]
            elif value == "Length (descending)":
                for i in userSongList:
                    if filename.endswith('mp3'):
                        y,sr = librosa.load(path + "'\'" + filename)
                        length = librosa.get_duration(y=y,sr=sr)
                        userSongLengthList.append(length)
                sortByLengthD = zip(userSongLengthList,userSongList)
                sortByLengthD.sort(reverse = True)
                sortedSongLengthD = [userSongList for userSongListLength, userSongList in sortByLengthD]
            else:
                pass

            for file in range(len(userSongList)):
                songList.insert(tk.END, userSongList[file])

        sortbtn = tk.Button(songSelectionFrame,
                            text = "Sort",
                            command = lambda: sortSongs(path))
        sortbtn.grid(row = 0,
                     column = 3)                    

        searchSongsEntry = tk.Entry(songSelectionFrame)
        searchSongsEntry.grid(row = 0,
                              column = 5,
                              padx = (0,20),
                              sticky = "EW")

        def searchSongs(path):

            entryValue = searchSongsEntry.get()
            userSongList = []
            songList.delete(0,tk.END)

            for filename in path:
                if filename.endswith('.mp3'):
                    if entryValue in filename:
                        userSongList.append(filename)

            for file in range(len(userSongList)):
                    songList.insert(tk.END, userSongList[file])

        searchbtn = tk.Button(songSelectionFrame,
                              text = "Search",
                              command = lambda: searchSongs(path))
        searchbtn.grid(row = 0,
                       column = 4)

        def getSelectedSong():
            selectedSong = songList.get(songList.curselection())
            gameRunning == True
            controller.show_frame(GameScreenClass)

        songList = tk.Listbox(songSelectionFrame,
                              bg = "Black",
                              width = 35,
                              height = 12,
                              bd = 8,
                              relief = "sunken",
                              font = "Trebuchet 20",
                              fg = "White")
        songList.bind("<Double-Button>",
                      lambda x: getSelectedSong())
        songList.grid(row = 1,
                      column = 2,
                      columnspan = 4,
                      pady = (8,0))

        songScrollBar = tk.Scrollbar(songSelectionFrame)
        songScrollBar.grid(row = 1,
                        column = 4,
                        sticky = "NES",
                        padx = (0,7),
                        pady = (8,0))
        
        songList.config(yscrollcommand = songScrollBar.set)

        startToMenuButton = tk.Button(songSelectionScreenFrame,
                                      text = "< MENU",
                                      font = "Helvetica 33",
                                      fg = "red4",
                                      activeforeground = "grey46",
                                      bg = "Black",
                                      activebackground = "Black",
                                      borderwidth = 0,
                                      command = lambda: controller.show_frame(MenuScreenClass))

        startToMenuButton.grid(row = 2,
                               column = 0,
                               padx = (0,400),
                               pady = (55,0))

        def getSongs():
            fileList = askdirectory()
            global path
            path = os.listdir(fileList)
            for filename in path:
                if filename.endswith('.mp3'):
                    songList.insert(tk.END, filename)

        chooseSongDirButton = tk.Button(songSelectionScreenFrame,
                                        text = "Song folder..",
                                        font = "Helvetica 33",
                                        fg = "grey46",
                                        activeforeground = "White",
                                        bg = "Black",
                                        activebackground = "Black",
                                        borderwidth = 0,
                                        command = getSongs)
        chooseSongDirButton.grid(row = 2,
                                 column = 2,
                                 columnspan = 3,
                                 padx = (350,0),
                                 pady = (50,10),
                                 ipady = 5)

class PauseScreenClass(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)

        pauseScreenFrame = tk.Frame(self,
                                    bg = "Black",
                                    width = 1280,
                                    height = 720)
        pauseScreenFrame.grid(padx = (275,0),
                              pady = (140,0))

        pauseObjectsFrame = tk.Frame(pauseScreenFrame,
                                     bg = "Black")
        pauseObjectsFrame.grid()

        pauseTextLabel = tk.Label(pauseObjectsFrame,
                                  text = "- PAUSED -",
                                  font = "Trebuchet 59",
                                  fg = "red4",
                                  bg = "Black")
        pauseTextLabel.grid(padx = (250,0),
                            pady = 20)

        pauseOptionsFrame = tk.Frame(pauseObjectsFrame,
                                  bg = "Black")
        pauseOptionsFrame.grid()

        def resumeSong():
            pauseScreenFrame.grid_forget()
            time.sleep(3)
            
        resumeButton = tk.Button(pauseOptionsFrame,
                                 text = "Resume",
                                 borderwidth = 0,
                                 font = "Trebuchet 20 bold",
                                 fg = "White",
                                 activeforeground = "grey46",
                                 bg = "Black",
                                 activebackground = "Black",
                                 command = resumeSong)
        resumeButton.grid(padx = (250,0))            

        def restartSong(filename):
            controller.show_frame(GameScreenClass)

        restartButton = tk.Button(pauseOptionsFrame,
                                  text = "Restart",
                                  borderwidth = 0,
                                  font = "Trebuchet 20 bold",
                                  fg = "White",
                                  activeforeground = "grey46",
                                  bg = "Black",
                                  activebackground = "Black",
                                  command = restartSong)
        restartButton.grid(padx = (250,0),
                           pady = 20)

        songSelectionButton = tk.Button(pauseOptionsFrame,
                                        text = "Back to song selection",
                                        borderwidth = 0,
                                        font = "Trebuchet 20 bold",
                                        fg = "White",
                                        activeforeground = "grey46",
                                        bg = "Black",
                                        activebackground = "Black",
                                        command = lambda: controller.show_frame(SongSelectionScreenClass))
        songSelectionButton.grid(padx = (250,0))

class GameScreenClass(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

    filename = SongSelectionScreenClass.getSelectedSong(selectedSong)

    def analyseSong():
        
        y, sr = librosa.load(filename)

        tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)

        beat_times = librosa.frames_to_time(beat_frames, sr=sr)
        beat_times.tolist()
        beat_times_list_length = len(beat_times)
        int(beat_times_list_length)

        song_length = librosa.get_duration(y=y, sr=sr)

        beats_per_minute = (((beat_times_list_length)/song_length)*60)
        return beats_per_minute

    analyseSong()

    WHITE = (255,255,255)
    BLACK = (0,0,0)
    RED = (130,0,0)
    GREY = (140,140,140)

    DISPLAY_WIDTH = 1280
    DISPLAY_HEIGHT = 720

    gameDisplay = pygame.display.set_mode((DISPLAY_WIDTH,DISPLAY_HEIGHT))
    pygame.display.set_caption("Note Mania")


    clock = pygame.time.Clock()
    
    pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=4096)
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()

    class ArrowClass(pygame.sprite.Sprite):
        def __init__(self,image):
            pygame.sprite.Sprite().__init__(self)
            super().__init__()

            self.image = pygame.Surface(image)

            self.rect = self.image.get_rect()

    arrow_group = pygame.sprite.Group()

    up_arrow = ArrowClass(pygame.image.load('Sprites/up_arrow.png').convert_alpha())
    left_arrow = ArrowClass(pygame.image.load('Sprites/left_arrow.png').convert_alpha())
    right_arrow = ArrowClass(pygame.image.load('Sprites/right_arrow.png').convert_alpha())
    down_arrow = ArrowClass(pygame.image.load('Sprites/down_arrow.png').convert_alpha())

    arrow_group.add(up_arrow, left_arrow, right_arrow, down_arrow)
    arrow_list = list(arrow_group)
    arrow_type = random.choice(arrow_list)

    def arrows(x_coord,y_coord,width,height):
        gameDisplay.blit(up_arrow,(x_coord,y_coord))

    font_name = pygame.font.match_font('Trebuchet 40')

    def showScore(surf,text,size,x,y):
        font = pygame.font.Font(font_name,size)
        text_surface = font.render(text,True,RED)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x,y)
        surf.blit(text_surface,text_rect) # update

    def gameLoop():

        beat_times = analyseSong() 
        beats_per_minute = analyseSong()

        x_coord = random.choice([774,879,985,1091])
        y_coord = -88

        gameExit = False

        while not gameExit:
            
            song_playing = pygame.mixer.music.get_busy()
            if song_playing == False:
                ResultsScreenClass.tkraise()
                
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameExit = True
                    
                if event.type == pygame.KEYDOWN:
                    arrow_y = arrow_type.get_rect().y
                    arrow_x = arrow_type.get_rect().x
                    if event.key == pygame.K_UP:
                        if arrow_x == 774:
                            if arrow_y in range(520,599):
                                running_score = running_score + 1
                            elif arrow_y in range(600,640):
                                running_score = running_score + 2
                            elif arrow_y in range(641,720):
                                running_score = running_score + 1
                    if event.key == pygame.K_LEFT:
                        if arrow_x == 879:
                            if arrow_y in range(520,599):
                                running_score = running_score + 1
                            elif arrow_y in range(600,640):
                                running_score = running_score + 2
                            elif arrow_y in range(641,720):
                                running_score = running_score + 1
                    if event.key == pygame.K_RIGHT:
                        if arrow_x == 985:
                            if arrow_y in range(520,599):
                                running_score = running_score + 1
                            elif arrow_y in range(600,640):
                                running_score = running_score + 2
                            elif arrow_y in range(641,720):
                                running_score = running_score + 1                    
                    if event.key == pygame.K_DOWN:
                        if arrow_x == 1091:
                            if arrow_y in range(520,599):
                                running_score = running_score + 1
                            elif arrow_y in range(600,640):
                                running_score = running_score + 2
                            elif arrow_y in range(641,720):
                                running_score = running_score + 1
                            
                    if event.key == pygame.K_ESCAPE:
                        from Container import PauseScreenClass
                        pygame.sleep()

            gameDisplay.fill(BLACK)

            pygame.draw.line(gameDisplay, GREY, [769,0], [769,720], 5)
            pygame.draw.line(gameDisplay, GREY, [876,0], [876,720], 5)
            pygame.draw.line(gameDisplay, GREY, [982,0], [982,720], 5)
            pygame.draw.line(gameDisplay, GREY, [1088,0], [1088,720], 5)
            pygame.draw.line(gameDisplay, GREY, [1195,0], [1195,720], 5)
            pygame.draw.line(gameDisplay, GREY, [769,620], [1195,620], 5)

            arrows(x_coord,y_coord)
            y_coord += (song_length/beats_per_minute/60)

            for i in range(beat_times):
                if y_coord > 0:
                    time_dif = beat_times[i+1] - beat_times[i]
                    time.sleep(time_dif)
                    x_coord = random.choice([774,879,985,1091])
                    y_coord = -88

            showScore(gameDisplay,("Score: " + running_score),20,100,100)

            pygame.display.update()
            clock.tick(60)  

    gameLoop()
    pygame.quit()


class ResultsScreenClass(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        resultsScreenFrame = tk.Frame(self,
                                      bg = "Black")
        resultsScreenFrame.grid()

        userPlayedSong = tk.Label(resultsScreenFrame,
                                  text = selectedSong,
                                  font = "Trebuchet 40 bold",
                                  fg = "red4",
                                  bg = "Black")
        userPlayedSong.grid(column = 0,
                            row = 0,
                            columnspan = 2)

        scoreLabel = tk.Label(resultsScreenFrame,
                              text = "Score: ",
                              font = "Trebuchet 40 bold",
                              fg = "grey46",
                              bg = "Black")
        scoreLabel.grid(column = 0,
                        row = 1)

        userScoreLabel = tk.Label(resultsScreenFrame,
                          text = running_score,
                          font = "Trebuchet 40",
                          fg = "red4",
                          bg = "Black")
        userScoreLabel.grid(column = 1,
                            row = 1)

        enterNamePromptLabel = tk.Label(resultsScreenFrame,
                                        text = "Enter name: ",
                                        font = "Trebuchet 40 bold",
                                        fg = "grey46",
                                        bg = "Black")
        enterNamePromptLabel.grid(column = 0,
                                  row = 2)

        enterName = tk.Entry(resultsScreenFrame)
        enterName.grid(column = 1,
                       row = 2)

        def scoreSave():
            with open(score_file,'w') as file:
                file.write((enterName.get()).replace(" ","")
                           + "-" + GameScreenClass.gameLoop(running_score))
                file.write('\n')
                file.close

        saveScoreButton = tk.Button(resultsScreenFrame,
                                    text = "Save Score",
                                    command = scoreSave)
        saveScoreButton.grid(row = 2,
                             column = 2)

        backToSongSelButton = tk.Button(text = "< SONG SELECT",
                                        font = "Helvetica 33",
                                        fg = "red4",
                                        activeforeground = "grey46",
                                        bg = "Black",
                                        activebackground = "Black",
                                        borderwidth = 0,
                                        command = lambda: controller.show_frame(SongSelectionScreenClass))
        backToSongSelButton.grid(column = 0,
                                 row = 3,
                                 padx = (370,0))

        backToMenuButton = tk.Button(text = "< MENU",
                                     font = "Helvetica 33",
                                     fg = "red4",
                                     activeforeground = "grey46",
                                     bg = "Black",
                                     activebackground = "Black",
                                     borderwidth = 0,
                                     command = lambda: controller.show_frame(MenuScreenClass))
        backToMenuButton.grid(column = 0,
                              row = 4,
                              padx = (380,0))        


game = NoteManiaClass()
game.geometry("1280x720")
game.resizable(0,0)
game.configure(background = "Black")
game.title("NOTE MANIA")
game.mainloop()
