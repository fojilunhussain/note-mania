# IMPORT MODULES
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

# WINDOW FOR ALL SCREEN FRAMES

class NoteManiaClass(tk.Tk):

    # initialise the container in which all screens
    #   will be available
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # attributes of the main frame in which everything
        #    will be visible
        container = tk.Frame(self,
                             width = 1280,
                             height = 720)
        container.grid()

        # holds the current frame
        self.frame = {}

        # in the navigation, can switch between dif frames
        #   thus switching between different screens      
        for F in (MenuScreenClass, SongSelectionScreenClass, GameScreenClass, PauseScreenClass, ResultsScreenClass):
            frame = F(container, self)
            self.frame[F] = frame
            frame.grid(row=0, column=0, sticky="NSEW")

        # the first frame which will be visible
        self.show_frame(MenuScreenClass)

    # a function to raise the first frame above,
    #   then raise the one which the user selects        
    def show_frame(self, cont):
        
        frame = self.frame[cont]
        frame.tkraise()


# MENU SCREEN

class MenuScreenClass(tk.Frame):

    # inheriting the frame attributes of the
    #   main container
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # MENU SCREEN FRAME

        menuScreenFrame = tk.Frame(self,
                                   bg = "Black")
        menuScreenFrame.grid()

        # GAME NAME FRAME

        gameNameFrame = tk.Frame(menuScreenFrame,
                                 bg = "Black")
        gameNameFrame.grid(sticky = "W")# frame is on left of window
        
        # game name label - can be hidden and destroyed,
        #   based on which buttons the user presses
        gameNameLabel = tk.Label(gameNameFrame,
                                 text = "Note Mania",
                                 font = "Trebuchet 79 bold",
                                 fg = "red4",
                                 bg = "Black")
        gameNameLabel.grid(row = 0,
                           column = 0,
                           padx = (20,0),
                           pady = (0,225))

        # MENU BUTTONS FRAME

        menuButtonsFrame = tk.Frame(menuScreenFrame,
                                    bg = "Black")
        menuButtonsFrame.grid(sticky = "E", # frame is on right of window
                              row = 0,
                              column = 1,
                              padx = (99,0),
                              pady = (239,0),
                              ipady = 221)

        # start button - takes to song select
        startButton = tk.Button(menuButtonsFrame,
                                relief = "sunken",
                                width = 18,
                                text = "Start ",
                                anchor = "e",# align text to right
                                font = "Trebuchet 40 bold",
                                fg = "White",
                                activeforeground = "grey46",
                                bg = "Black",
                                activebackground = "Black",
                                bd = 8,
                                command = lambda: controller.show_frame(SongSelectionScreenClass))
        startButton.grid(sticky = "E")

        # when 'quit' button is clicked in the menu
        def closeMenu():

            #hide the game name label and replace with quit options
            gameNameLabel.grid_forget()

            # yes/no quit buttons frame - keeps them together,
            #   since they keep separating
            quitBtnsFrame = tk.Frame(gameNameFrame,
                                     bg = "Black")
            quitBtnsFrame.grid(pady = (0,200))      

            # quit label
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

            # if the user decides not to quit
            #   and presses 'no'
            def hideQuitLabels():
                
                # destroy the quit options and get the game name back
                quitBtnsFrame.destroy()
                askQuitLabel.destroy()
                gameNameLabel.grid(row = 0,
                                   padx = (20,0),
                                   pady = (0,225))
                #enable the quit button, since the quit options are now closed
                quitButton.config(state="active",
                                  activeforeground = "White")
                #enable other buttons too
                startButton.config(state = "active",
                                   activeforeground = "White")

            # user decides to quit
            yesQuitButton = tk.Button(quitBtnsFrame,
                                      text = "Yes",
                                      font = "Trebuchet 15 bold",
                                      fg = "White",
                                      activeforeground = "grey46",
                                      bg = "Black",
                                      activebackground = "Black",
                                      borderwidth = 0,
                                      command = lambda: game.destroy())
                                      #^ closes everything
            yesQuitButton.grid(column = 0,
                               row = 1,
                               padx = (130,0),
                               sticky = "EW")

            # user decides not to quit, involves function 'hideQuitLabels'
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

            # disable the quit button, so multiple quit options
            #   don't show up again
            quitButton.config(state = "disabled")
            # and disable other menu buttons
            startButton.config(state = "disabled",
                               disabledforeground = "White")

        # quit button
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


# SONG SELECTION SCREEN
class SongSelectionScreenClass(tk.Frame):

    # inheriting the frame attributes of the
    #   main container
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)

        # SONG SELECTION SCREEN FRAME

        songSelectionScreenFrame = tk.Frame(self,
                                            bg = "Black",
                                            width = 1280,
                                            height = 720)
        songSelectionScreenFrame.grid(ipady = 1)

        # LEADERBOARD FRAME

        leaderboardFrame = tk.Frame(songSelectionScreenFrame,
                                 bg = "Black",
                                    width = 591)
        leaderboardFrame.grid()

        # leaderboard buttons frame - for local and own scores
        #   no time to provide functionality for
        leaderboardButtonsFrame = tk.Frame(leaderboardFrame,
                                           bg = "Black")
        leaderboardButtonsFrame.grid(row = 0,
                                     column = 0,
                                     columnspan = 2,
                                     pady = (94,0))

        # local leaderboard button
        #   displays all local scores on selected song from database
        localLeaderboardButton = tk.Button(leaderboardButtonsFrame,
                                           text = "All local scores",
                                           font = "Helvetica 25",
                                           fg = "White",
                                           #when clicked, text is grey
                                           activeforeground = "grey46",
                                           bg = "Black",
                                           #when clicked, bg stays black
                                           activebackground = "Black",
                                           borderwidth = 0)
        localLeaderboardButton.grid(row = 0,
                                    column = 0,
                                    padx = (0,20))
        
        # own leaderboard button
        #   displays all own scores on selected song from database
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

        # scroll through scores in leaderboard
        leaderboard = tk.Listbox(leaderboardFrame,
                                 width = 35,
                                 height = 12,
                                 bg = "Black",
                                 bd = 8,
                                 relief = "sunken",
                                 font = "Trebuchet 20",
                                 fg = "White")

        # set up lists so contents can be sorted and appended
        leaderboardList = [] # list for all values to be added to 
        leaderboardNames = [] # list for all names
        leaderboardScores = [] # list for all scores, will sort by highest score

        leaderboard.delete(0,tk.END) # clear contents of leaderboard
        with open(score_file) as f: # open file
            for line in f: # iterate over lines
                leaderboardList += line.split() # split by delimiter and add to list
        for name in range(0,(len(leaderboardList)),2): # for every other item in list
            leaderboardNames.append(leaderboardList[name]) # add to name list
        for score in range(1,(len(leaderboardList)),2): # for every other score in list
            leaderboardScores.append(leaderboardList[score]) # add to score list

        sortHighScores = zip(leaderboardScores,leaderboardNames) # zip lists together
        sortHighScores.sort(reverse = True) # sort descending by score
        sortedHighScores = [leaderboardList for leaderboardScores, leaderboardList in sortHighScores]

        for result in range(len(leaderboardList)): # for the number of items now in the leaderboard list
            leaderboard.insert(tk.END, leaderboardList[result]) # insert item into leaderboard
        
        # scroll through leaderboard
        leaderboardScrollBar = tk.Scrollbar(leaderboardFrame)
        leaderboardScrollBar.grid(row = 1,
                                  column = 0,
                                  sticky = "NSW",
                                  pady = (0,0))
        leaderboard.config(yscrollcommand = leaderboardScrollBar.set)

        # SONG SELECTION FRAME

        songSelectionFrame = tk.Frame(songSelectionScreenFrame,
                                      bg = "Black")
        songSelectionFrame.grid(row = 0,
                                column = 2,
                                columnspan = 3,
                                padx = (86,0),
                                pady = (109,0))
        
        # song selection list box and search bar frame
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
        
        # sort songs function
        #   takes path as parameter
        def sortSongs(path):

            value = sortBy.get() # getting val of what user chooses to sort by
            userSongList = [] # set up empty array for songs to be added to
            userSongLengthList = [] # set up empty array for song lengths to be added to
            songList.delete(0,tk.END) # clear the contents of the scrollbox

            for filename in path: # for every filename in the song folder
                if filename.endswith('mp3'): # if the file is an mp3 file
                    userSongList.append(filename) # add filename to userSongList

            if value == "A-Z": # if the value in the sortBy menu is 'A-Z':
                userSongList.sort() # sort filenames in song list alphabetically
            elif value == "Z-A": # and so on..
                userSongList.sort(reverse = True)
            elif value == "Length (ascending)":
                for i in userSongList:
                    if filename.endswith('mp3'):
                        y, sr = librosa.load(path + "'\'" + filename) # get the song from user dir
                        length = librosa.get_duration(y=y, sr=sr) # get length
                        userSongLengthList.append(length) # add the lengths to length list
                sortByLengthA = zip(userSongLengthList,userSongList) # zip lists together
                sortByLengthA.sort()
                sortedSongLengthA = [userSongList for userSongListLength, userSongList in sortByLengthA]
                # ^sorting both lists by length (ascending)
            elif value == "Length (descending)":
                for i in userSongList:
                    if filename.endswith('mp3'):
                        y,sr = librosa.load(path + "'\'" + filename) # get the song from user dir
                        length = librosa.get_duration(y=y,sr=sr) # get length
                        userSongLengthList.append(length) # add the lengths to length list
                sortByLengthD = zip(userSongLengthList,userSongList) # zips lists together
                sortByLengthD.sort(reverse = True) # reverse sort lengths
                sortedSongLengthD = [userSongList for userSongListLength, userSongList in sortByLengthD]
                # ^sorting both lists by length (descending)
            else:
                pass

            for file in range(len(userSongList)): # for the number of files in the song list
                songList.insert(tk.END, userSongList[file]) # add file to the scrollbox

        # sort songs button
        sortbtn = tk.Button(songSelectionFrame,
                            text = "Sort",
                            command = lambda: sortSongs(path))
        sortbtn.grid(row = 0,
                     column = 3)                    

        # textbox to search through songs
        searchSongsEntry = tk.Entry(songSelectionFrame)
        searchSongsEntry.grid(row = 0,
                              column = 5,
                              padx = (0,20),
                              sticky = "EW")

        # search songs function
        #   tales path as parameter
        def searchSongs(path):

            entryValue = searchSongsEntry.get() # getting val of what user chooses to sort by
            userSongList = [] # set up empty array for songs to be added to
            songList.delete(0,tk.END) # clear the contents of the scrollbox

            for filename in path: # for every filename in the song folder
                if filename.endswith('.mp3'): # for all mp3 files
                    if entryValue in filename: # user entered val in filename
                        userSongList.append(filename) # add file to song list

            for file in range(len(userSongList)): # for each file in song list
                    songList.insert(tk.END, userSongList[file]) # add to listbox

        # search button to search through song listbox
        searchbtn = tk.Button(songSelectionFrame,
                              text = "Search",
                              command = lambda: searchSongs(path))
        searchbtn.grid(row = 0,
                       column = 4)

        # function to get user selected song
        def getSelectedSong():
            # the selected song is the one the user clicks on
            selectedSong = songList.get(songList.curselection())
            gameRunning == True
            controller.show_frame(GameScreenClass)

        # scroll through song list
        songList = tk.Listbox(songSelectionFrame,
                              bg = "Black",
                              width = 35,
                              height = 12,
                              bd = 8,
                              relief = "sunken",
                              font = "Trebuchet 20",
                              fg = "White")
        songList.bind("<Double-Button>",
                      # on selection of an item
                      lambda x: getSelectedSong())
                      # bind to function getSelectedSong,
                      #     so when item from the list is selected,
                      #     function runs
        songList.grid(row = 1,
                      column = 2,
                      columnspan = 4,
                      pady = (8,0))

        # scrollbar for song listbox
        songScrollBar = tk.Scrollbar(songSelectionFrame)
        songScrollBar.grid(row = 1,
                        column = 4,
                        sticky = "NES",
                        padx = (0,7),
                        pady = (8,0))
        
        songList.config(yscrollcommand = songScrollBar.set)

        # back to menu button
        startToMenuButton = tk.Button(songSelectionScreenFrame,
                                      text = "< MENU",
                                      font = "Helvetica 33",
                                      fg = "red4",
                                      activeforeground = "grey46",
                                      # when clicked, text is grey
                                      bg = "Black",
                                      # when clicked, bg stays black
                                      activebackground = "Black",
                                      borderwidth = 0,
                                      command = lambda: controller.show_frame(MenuScreenClass))

        startToMenuButton.grid(row = 2,
                               column = 0,
                               padx = (0,400),
                               pady = (55,0))

        def getSongs(): # function to get songs from selected dir
            fileList = askdirectory() # list of files = files in selected dir
            global path
            path = os.listdir(fileList) # the folder is the user's chosen dir - pop up box asks
            for filename in path: # for every filename in the song folder
                if filename.endswith('.mp3'): # if the file is an mp3 file
                    songList.insert(tk.END, filename) # insert filename into songlist

        # choose song dir button
        #   involves function 'getSongs()'
        chooseSongDirButton = tk.Button(songSelectionScreenFrame,
                                        text = "Song folder..",
                                        font = "Helvetica 33",
                                        fg = "grey46",
                                        activeforeground = "White",
                                        # text is white when clicked
                                        bg = "Black",
                                        activebackground = "Black",
                                        borderwidth = 0,
                                        command = getSongs)
                                        # function is called when clicked
        chooseSongDirButton.grid(row = 2,
                                 column = 2,
                                 columnspan = 3,
                                 padx = (350,0),
                                 pady = (50,10),
                                 ipady = 5)

# the pause screen
class PauseScreenClass(tk.Frame):

    # inheriting the frame attributes of the
    #   main container
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)

        # PAUSE SCREEN FRAME

        pauseScreenFrame = tk.Frame(self,
                                    bg = "Black",
                                    width = 1280,
                                    height = 720)
        pauseScreenFrame.grid(padx = (275,0),
                              pady = (140,0))

        # PAUSE OBJECTS FRAME

        pauseObjectsFrame = tk.Frame(pauseScreenFrame,
                                     bg = "Black")
        pauseObjectsFrame.grid()

        # pause text label
        pauseTextLabel = tk.Label(pauseObjectsFrame,
                                  text = "- PAUSED -",
                                  font = "Trebuchet 59",
                                  fg = "red4",
                                  bg = "Black")
        pauseTextLabel.grid(padx = (250,0),
                            pady = 20)

        # pause options frame
        pauseOptionsFrame = tk.Frame(pauseObjectsFrame,
                                  bg = "Black")
        pauseOptionsFrame.grid()

        # resume song from pause screen
        def resumeSong():
            pauseScreenFrame.grid_forget() # hides the pause screen
            time.sleep(3) # waits 3 seconds before continuing the song
            
        # resume button - allow user to continue the song from where they left off
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

        # restart song from pause screen
        def restartSong(filename): # takes filename as parameter for all game functions
            controller.show_frame(GameScreenClass) # show game screen

        #restart button - play the song from the beginning
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

        #back to song selection button - quit to song select
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


# the game screen
class GameScreenClass(tk.Frame):

    # inheriting the frame attributes of the
    #   main container
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

    # ---INITIALISE GAME CODE---

    # SONG ANALYSIS

    filename = SongSelectionScreenClass.getSelectedSong(selectedSong)

    # function to analyse user selected song
    def analyseSong():
        
        y, sr = librosa.load(filename) # y - amplitude; sr - samples per seconds

        tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr) # to calculate beatframes

        # convert frames to seconds
        beat_times = librosa.frames_to_time(beat_frames, sr=sr)
        beat_times.tolist() # to generate arrow per beat, later on
        beat_times_list_length = len(beat_times) # for bpm
        int(beat_times_list_length)

        # length of song in seconds
        song_length = librosa.get_duration(y=y, sr=sr)

        # beats per minute
        beats_per_minute = (((beat_times_list_length)/song_length)*60)
        return beats_per_minute

    analyseSong()

    # CONSTANTS

    WHITE = (255,255,255) # colours
    BLACK = (0,0,0)
    RED = (130,0,0)
    GREY = (140,140,140)

    DISPLAY_WIDTH = 1280 # display
    DISPLAY_HEIGHT = 720

    gameDisplay = pygame.display.set_mode((DISPLAY_WIDTH,DISPLAY_HEIGHT))
    pygame.display.set_caption("Note Mania")


    clock = pygame.time.Clock() # clock    

    # PYGAME MUSIC

    # play song
    pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=4096)
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()

    # ARROWS

    class ArrowClass(pygame.sprite.Sprite): # class for arrows

        def __init__(self,image):
            pygame.sprite.Sprite().__init__(self)
            super().__init__() # call parent class (sprite) constructor

            # pass in image of sprite
            self.image = pygame.Surface(image)

            # fetch rectangle object that has dimensions of image
            self.rect = self.image.get_rect()

    arrow_group = pygame.sprite.Group()

    up_arrow = ArrowClass(pygame.image.load('Sprites/up_arrow.png').convert_alpha()) # up arrow
    left_arrow = ArrowClass(pygame.image.load('Sprites/left_arrow.png').convert_alpha()) # left arrow
    right_arrow = ArrowClass(pygame.image.load('Sprites/right_arrow.png').convert_alpha()) # right arrow
    down_arrow = ArrowClass(pygame.image.load('Sprites/down_arrow.png').convert_alpha()) # down arrow

    # add arrows to sprite group
    arrow_group.add(up_arrow, left_arrow, right_arrow, down_arrow)
    arrow_list = list(arrow_group)
    arrow_type = random.choice(arrow_list)

    def arrows(x_coord,y_coord,width,height):
        gameDisplay.blit(up_arrow,(x_coord,y_coord))

    # SCORE TEXT

    font_name = pygame.font.match_font('Trebuchet 40') # get font name

    # function to display running score on game screen
    def showScore(surf,text,size,x,y):
        font = pygame.font.Font(font_name,size) # font, with attributes
        text_surface = font.render(text,True,RED) # show on screen
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x,y)
        surf.blit(text_surface,text_rect) # update

    # ---GAME LOOP FUNCTION---

    def gameLoop():

        beat_times = analyseSong() 
        beats_per_minute = analyseSong()

        x_coord = random.choice([774,879,985,1091])
        y_coord = -88

        gameExit = False

        # GAME LOOP

        while not gameExit:
            
            song_playing = pygame.mixer.music.get_busy() # check if song playing
            if song_playing == False: # if song ended
                ResultsScreenClass.tkraise() # show results screen
                
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameExit = True
                    
                if event.type == pygame.KEYDOWN:
                    arrow_y = arrow_type.get_rect().y # gets coordinates of arrow sprite
                    arrow_x = arrow_type.get_rect().x
                    if event.key == pygame.K_UP: # if up arrow pressed
                        if arrow_x == 774: # for arrow with x coord 774
                            if arrow_y in range(520,599): # arrow before hitline
                                running_score = running_score + 1
                            elif arrow_y in range(600,640): # arrow on hit line
                                running_score = running_score + 2
                            elif arrow_y in range(641,720): # arrow after hitline
                                running_score = running_score + 1
                    if event.key == pygame.K_LEFT: # if left arrow pressed
                        if arrow_x == 879: # for arrow with x coord 879
                            if arrow_y in range(520,599): # arrow before hitline
                                running_score = running_score + 1
                            elif arrow_y in range(600,640): # arrow on hit line
                                running_score = running_score + 2
                            elif arrow_y in range(641,720): # arrow after hitline
                                running_score = running_score + 1
                    if event.key == pygame.K_RIGHT: # if right arrow pressed
                        if arrow_x == 985: # for arrow with x coord 985
                            if arrow_y in range(520,599): # arrow before hitline
                                running_score = running_score + 1
                            elif arrow_y in range(600,640): # arrow on hit line
                                running_score = running_score + 2
                            elif arrow_y in range(641,720): # arrow after hitline
                                running_score = running_score + 1                    
                    if event.key == pygame.K_DOWN: # if down arrow pressed
                        if arrow_x == 1091: # for arrow with x coord 1091
                            if arrow_y in range(520,599): # arrow before hitline
                                running_score = running_score + 1
                            elif arrow_y in range(600,640): # arrow on hit line
                                running_score = running_score + 2
                            elif arrow_y in range(641,720): # arrow after hitline
                                running_score = running_score + 1
                            
                    if event.key == pygame.K_ESCAPE:
                        from Container import PauseScreenClass
                        pygame.sleep()

            # ---DRAW---

            gameDisplay.fill(BLACK)

            pygame.draw.line(gameDisplay, GREY, [769,0], [769,720], 5)
            pygame.draw.line(gameDisplay, GREY, [876,0], [876,720], 5)
            pygame.draw.line(gameDisplay, GREY, [982,0], [982,720], 5)
            pygame.draw.line(gameDisplay, GREY, [1088,0], [1088,720], 5)
            pygame.draw.line(gameDisplay, GREY, [1195,0], [1195,720], 5)
            pygame.draw.line(gameDisplay, GREY, [769,620], [1195,620], 5)

            arrows(x_coord,y_coord)
            y_coord += (song_length/beats_per_minute/60)

            for i in range(beat_times): # ensures arrows only generated for the beat list
                if y_coord > 0: # once the arrow appears on the screen
                    time_dif = beat_times[i+1] - beat_times[i]
                    time.sleep(time_dif) # pause the generation of a sprite for the time dif
                    x_coord = random.choice([774,879,985,1091])
                    y_coord = -88

            showScore(gameDisplay,("Score: " + running_score),20,100,100)

            # ---UPDATE---
            
            pygame.display.update()
            clock.tick(60)  

    gameLoop()
    pygame.quit()


# the results screen
class ResultsScreenClass(tk.Frame):

    # inheriting the frame attributes of the
    #   main container
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # RESULTS SCREEN FRAME

        resultsScreenFrame = tk.Frame(self,
                                      bg = "Black")
        resultsScreenFrame.grid()

        # displays the song the user has just played
        userPlayedSong = tk.Label(resultsScreenFrame,
                                  text = selectedSong,
                                  font = "Trebuchet 40 bold",
                                  fg = "red4",
                                  bg = "Black")
        userPlayedSong.grid(column = 0,
                            row = 0,
                            columnspan = 2)

        # displays the score the user has achieved
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

        # prompts user to enter their name into the scoreboard
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


        # save score to file function - called when user presses save button
        def scoreSave():
            with open(score_file,'w') as file: # open file to write to
                file.write((enterName.get()).replace(" ","") # get user name and remove space
                           + "-" + GameScreenClass.gameLoop(running_score)) # get song score, write
                file.write('\n') # write empty line for next entry
                file.close # close file

        saveScoreButton = tk.Button(resultsScreenFrame,
                                    text = "Save Score",
                                    command = scoreSave)
        saveScoreButton.grid(row = 2,
                             column = 2)

        # button to go back to song selection screen
        backToSongSelButton = tk.Button(text = "< SONG SELECT",
                                        font = "Helvetica 33",
                                        fg = "red4",
                                        activeforeground = "grey46",
                                        # when clicked, text is grey
                                        bg = "Black",
                                        # when clicked, bg stays black
                                        activebackground = "Black",
                                        borderwidth = 0,
                                        command = lambda: controller.show_frame(SongSelectionScreenClass))
        backToSongSelButton.grid(column = 0,
                                 row = 3,
                                 padx = (370,0))

        # button to go back to menu screen
        backToMenuButton = tk.Button(text = "< MENU",
                                     font = "Helvetica 33",
                                     fg = "red4",
                                     activeforeground = "grey46",
                                     # when clicked, text is grey
                                     bg = "Black",
                                     # when clicked, bg stays black
                                     activebackground = "Black",
                                     borderwidth = 0,
                                     command = lambda: controller.show_frame(MenuScreenClass))
        backToMenuButton.grid(column = 0,
                              row = 4,
                              padx = (380,0))        


game = NoteManiaClass()
# size of window
game.geometry("1280x720")
# user cannot resize window
game.resizable(0,0)
# colour of window background
game.configure(background = "Black")
# title of window
game.title("NOTE MANIA")
# keep window open
game.mainloop()
