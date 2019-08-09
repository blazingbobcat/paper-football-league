# Paper Football League
# Version 1.0
# By Josh Klipstein
# August 9, 2019

import pygame as pg
import sys, os
from math import *
from random import *
from pygame.locals import *

# Main Constants
WINWIDTH = 1200
WINHEIGHT = 660
HALFWIDTH = WINWIDTH // 2
HALFHEIGHT = WINHEIGHT // 2
QUARTERWIDTH = HALFWIDTH // 2
QUARTERHEIGHT = HALFHEIGHT // 2
FPS = 30
RADIORADIUS = 20
DOTRADIUS = 16

#              R    G    B
GREY =       (128, 128, 128)
BLUE =       (  0,   0, 255)
WHITE =      (255, 255, 255)
BLACK =      (  0,   0,   0)
RED =        (192,   0,   0)
GREEN =      (  0, 255,   0)
BROWN =      (128, 128,   0)
STRAW =      (255, 255, 128)

# Color Constants
DEFAULTFONTCOLOR = BLACK
TITLEONECOLOR = RED
TITLETWOCOLOR = GREEN
DEFAULTBACKCOLOR = WHITE
BUTTONTEXTCOLOR = GREEN
BUTTONCOLOR = BROWN
ARROWCOLOR = RED
WINDCOLOR = BLUE
MENUCOLOR = BROWN
MENUTEXTCOLOR = STRAW

# Physics Constants
WINDRADIUS = 20
WINDARROW = (int(WINWIDTH - 1.25 * WINDRADIUS), WINHEIGHT - WINDRADIUS)
WINDARROW2 = (int(1.25 * WINDRADIUS), WINHEIGHT - WINDRADIUS)
GRAVITY = 9.8
FRICTION = 0.5

# Initialization function
def initialize():

    global DISPLAYSURF, VARIABLEDICT, IMGDICT, FONTDICT, RECTDICT, FPSCLOCK
    
    # Initialize pygame and declare fonts
    pg.init()
    pg.mixer.init() # Initialize sounds
    DISPLAYSURF = pg.display.set_mode((WINWIDTH, WINHEIGHT))
    pg.display.set_caption("Paper Football League Beta -- Josh Klipstein")
    FPSCLOCK = pg.time.Clock()
    TITLEFONT = pg.font.SysFont('arialblack', 40)
    DEFAULTFONT = pg.font.SysFont('calibri', 16)
    BUTTONFONT = pg.font.SysFont('impact', 20)
    WINDFONT = pg.font.Font('freesansbold.ttf', 16)
    MENUFONT = pg.font.Font('freesansbold.ttf', 48)

    # Load all images and sound files, but raise exception if folder not in
    # directory
    try:
        MENU = pg.image.load('images/pfootball.png') # Main menu screen
        OPTIONS = pg.image.load('images/pfootball2.png') # Options screen
        INSTRUCT = pg.image.load('images/pfootinstruct.png') # Instructions screen
        BACKGROUND = pg.image.load('images/pfootback.tif') # Game background
        PAPERFOOTBALLIMG = [] # Football image list
        for i in range(1, 25):
            PAPERFOOTBALLIMG.append(pg.image.load('images/pfb{0}.png'.format(i)))
        GOALIMG = pg.image.load('images/gp.png') # Goal post
        GOALIMG2 = pg.image.load('images/gp2.png') # Second goal post

        # Load all sounds
        LAUNCH = pg.mixer.Sound('sounds/Woosh-Mark_DiAngelo-4778593.wav')
        INTRO = pg.mixer.Sound('sounds/Football_Crowd-GoGo-1730947850.wav')
        SELECT = pg.mixer.Sound('sounds/Checkout Scanner Beep-SoundBible.com-593325210.wav')
        READY = pg.mixer.Sound('sounds/Tires Squealing-SoundBible.com-1814115127.wav')
        GO = pg.mixer.Sound('sounds/starting_pistol-Stephan_Schutze-613594351.wav')
        CHEER = pg.mixer.Sound('sounds/Sports_Crowd-GoGo-2100314571.wav')
        HORN = pg.mixer.Sound('sounds/Air Horn-SoundBible.com-964603082.wav')
        WIND = pg.mixer.Sound('sounds/Windy-SoundBible.com-1165996801.wav')
        SCORE = pg.mixer.Sound('sounds/Beep Ping-SoundBible.com-217088958.wav')
        BOUNCE = pg.mixer.Sound('sounds/Ball_Bounce-Popup_Pixels-172648817.wav')
    except:
        pg.quit()
        print("Necessary files not found!")
        sys.exit()
        
    # Initialize all game objects
    
    MENURECT = MENU.get_rect()
    MENURECT.center = (HALFWIDTH, HALFHEIGHT)
    
    OPTIONSRECT = OPTIONS.get_rect()
    OPTIONSRECT.center = (HALFWIDTH, HALFHEIGHT)
    
    INSTRUCTRECT = INSTRUCT.get_rect()
    INSTRUCTRECT.center = (HALFWIDTH, HALFHEIGHT)
    
    BACKGROUND = pg.transform.smoothscale(BACKGROUND, (WINWIDTH, WINHEIGHT))
    BACKGROUNDRECT = BACKGROUND.get_rect()
    BACKGROUNDRECT.center = (HALFWIDTH, HALFHEIGHT)
    PAPERFOOTBALL = pg.Rect(0, 0, 120, 120) # Football Rect
    PAPERFOOTBALL.midbottom = (HALFWIDTH + QUARTERWIDTH,
                               WINHEIGHT)
    WINDARROW = (WINWIDTH - WINDRADIUS, WINHEIGHT - WINDRADIUS) # Wind guide
    
    GOALPOST = GOALIMG.get_rect()
    GOALPOST2 = GOALIMG2.get_rect()
    GOALPOST.midbottom = (QUARTERWIDTH, WINHEIGHT + 50)
    GOALPOST2.midbottom = (HALFWIDTH + QUARTERWIDTH, WINHEIGHT + 50)
    GOALAREA = pg.Rect((GOALPOST.left + 133, GOALPOST.top + 50),
                       (37, 237))
    GOALAREA2 = pg.Rect((GOALPOST2.right - 170, GOALPOST.top + 50),
                        (37, 237))
    POSTAREA = pg.Rect((GOALAREA.left, GOALAREA.bottom),
                       (33, 333))
    POSTAREA2 = pg.Rect((GOALPOST.left + 48, POSTAREA.bottom),
                        (404, 88))
    POSTAREA3 = pg.Rect((GOALAREA2.left, GOALAREA.bottom),
                       (33, 333))
    POSTAREA4 = pg.Rect((GOALPOST2.left + 50, POSTAREA3.bottom),
                        (404, 88))

    # Main menu buttons
    # Play button
    playButton = MENUFONT.render('Play', 1, MENUTEXTCOLOR,
                                           MENUCOLOR)
    playButtonRect = playButton.get_rect()
    playButtonRect.topleft = (WINWIDTH // 20,
                              WINHEIGHT // 3)

    # Options button
    optionsButton = MENUFONT.render('Options', 1, MENUTEXTCOLOR,
                                           MENUCOLOR)
    optionsButtonRect = optionsButton.get_rect()
    optionsButtonRect.topleft = (WINWIDTH // 2 + 20,
                              WINHEIGHT // 3)

    # Instructions button
    instructButton = MENUFONT.render('Instructions', 1, MENUTEXTCOLOR,
                                           MENUCOLOR)
    instructButtonRect = instructButton.get_rect()
    instructButtonRect.topleft = (WINWIDTH // 20,
                              WINHEIGHT * 2 // 3)

    # Quit button
    quitButton2 = MENUFONT.render('Quit', 1, MENUTEXTCOLOR,
                                           MENUCOLOR)
    quitButtonRect2 = quitButton2.get_rect()
    quitButtonRect2.topleft = (WINWIDTH // 2 + 20,
                              WINHEIGHT * 2 // 3)

    # Return button
    returnButton = MENUFONT.render('Return to menu', 1, MENUTEXTCOLOR,
                                   MENUCOLOR)
    returnRect = returnButton.get_rect()
    returnRect.midtop = (HALFWIDTH, WINHEIGHT - 60)
    
    # End game buttons
    # Quit
    quitButton = BUTTONFONT.render('Quit', 1, BUTTONTEXTCOLOR,
                                           BUTTONCOLOR)
    quitButtonRect = quitButton.get_rect()
    quitButtonRect.center = (HALFWIDTH - QUARTERWIDTH // 2,
                             HALFHEIGHT + QUARTERHEIGHT)

    # Restart game
    restartButton = BUTTONFONT.render('Restart', 1, BUTTONTEXTCOLOR,
                                      BUTTONCOLOR)
    restartButtonRect = restartButton.get_rect()
    restartButtonRect.center = (HALFWIDTH,
                                HALFHEIGHT + QUARTERHEIGHT)

    # Return to menu
    menuButton = BUTTONFONT.render('Main menu', 1, BUTTONTEXTCOLOR,
                                   BUTTONCOLOR)
    menuButtonRect = menuButton.get_rect()
    menuButtonRect.center = (HALFWIDTH + QUARTERWIDTH // 2,
                             HALFHEIGHT + QUARTERHEIGHT)

    # Options menu buttons
    # Number of players label
    numPlayers = MENUFONT.render('# of players', 1, MENUTEXTCOLOR,
                                   MENUCOLOR)
    numPlayersRect = numPlayers.get_rect()
    numPlayersRect.center = (QUARTERWIDTH - 100,  WINHEIGHT // 3)

    # One player label
    onePlayer = MENUFONT.render('One player', 1, MENUTEXTCOLOR,
                                   MENUCOLOR)
    onePlayerRect = onePlayer.get_rect()
    onePlayerRect.midtop = (numPlayersRect.centerx + RADIORADIUS,
                            numPlayersRect.bottom + 100)

    # Two players label
    twoPlayers = MENUFONT.render('Two players', 1, MENUTEXTCOLOR,
                                   MENUCOLOR)
    twoPlayersRect = twoPlayers.get_rect()
    twoPlayersRect.midtop = (onePlayerRect.centerx,
                             onePlayerRect.bottom + 100)

    # Number of minutes label
    numMin = MENUFONT.render('# of minutes', 1, MENUTEXTCOLOR,
                                   MENUCOLOR)
    numMinRect = numMin.get_rect()
    numMinRect.center = (HALFWIDTH, WINHEIGHT // 3)

    # One minute label
    oneMin = MENUFONT.render('1 minute', 1, MENUTEXTCOLOR,
                                   MENUCOLOR)
    oneMinRect = oneMin.get_rect()
    oneMinRect.midtop = (numMinRect.centerx + RADIORADIUS,
                         numMinRect.bottom + 50)

    # 3 minutes label
    threeMin = MENUFONT.render('3 minutes', 1, MENUTEXTCOLOR,
                                   MENUCOLOR)
    threeMinRect = threeMin.get_rect()
    threeMinRect.midtop = (oneMinRect.centerx,
                           oneMinRect.bottom + 50)

    # 5 minutes label
    fiveMin = MENUFONT.render('5 minutes', 1, MENUTEXTCOLOR,
                                   MENUCOLOR)
    fiveMinRect = fiveMin.get_rect()
    fiveMinRect.midtop = (threeMinRect.centerx,
                          threeMinRect.bottom + 50)

    # Sound label
    soundLabel = MENUFONT.render('Sound', 1, MENUTEXTCOLOR,
                                   MENUCOLOR)
    soundLabelRect = soundLabel.get_rect()
    soundLabelRect.center = (HALFWIDTH + QUARTERWIDTH, WINHEIGHT // 3)

    # Sound on label
    soundOn = MENUFONT.render('On', 1, MENUTEXTCOLOR,
                                   MENUCOLOR)
    soundOnRect = soundOn.get_rect()
    soundOnRect.midtop = (soundLabelRect.centerx + RADIORADIUS,
                          soundLabelRect.bottom + 100)

    # Sound off label
    soundOff = MENUFONT.render('Off', 1, MENUTEXTCOLOR,
                                   MENUCOLOR)
    soundOffRect = soundOff.get_rect()
    soundOffRect.midtop = (soundOnRect.centerx,
                           soundOnRect.bottom + 100)

    # Initialize variable dictionary
    VARIABLEDICT = {'mousePos': (0, 0),
                    'draggingArrow': False,
                    'power': 50,
                    'launchAngle': 0,
                    'scoreOne': 0,
                    'scoreTwo': 0,
                    'hiScore': 0,
                    'gameTime': 60,
                    'timer': 0,
                    'windSpeed': 0,
                    'windAngle': 0,
                    'ballSpeed': 0,
                    'message': 0,
                    'rotation': 6,
                    'radius': 60,
                    'gameOver': False,
                    'showHelp': True,
                    'menu': True,
                    'options': False,
                    'instruct': False,
                    'players': 1,
                    'player': False,
                    'sound': True,
                    'start': True}

    # Initialize Rect dictionary
    RECTDICT = {'football': PAPERFOOTBALL,
                'goal': GOALPOST,
                'goal2': GOALPOST2,
                'goalArea': GOALAREA,
                'goalAreaTwo': GOALAREA2,
                'brickAreaOne': POSTAREA,
                'brickAreaTwo': POSTAREA2,
                'brickAreaThree': POSTAREA3,
                'brickAreaFour': POSTAREA4,
                'background': BACKGROUNDRECT,
                'menu': MENURECT,
                'message': (0, 0, 0, 0),
                'quit': quitButtonRect,
                'restart': restartButtonRect,
                'menuReturn': menuButtonRect,
                'play': playButtonRect,
                'quit2': quitButtonRect2,
                'options': optionsButtonRect,
                'instruct': instructButtonRect,
                'return': returnRect,
                'optionShow': OPTIONSRECT,
                'instructShow': INSTRUCTRECT,
                'sound': soundLabelRect,
                'soundOn': soundOnRect,
                'soundOff': soundOffRect,
                'minutes': numMinRect,
                'oneMin': oneMinRect,
                'threeMin': threeMinRect,
                'fiveMin': fiveMinRect,
                'numPlayers': numPlayersRect,
                'onePlayer': onePlayerRect,
                'twoPlayers': twoPlayersRect}

    # Initialize image dictionary
    IMGDICT = {'football': PAPERFOOTBALLIMG,
               'goal': GOALIMG,
               'goal2': GOALIMG2,
               'background': BACKGROUND,
               'menu': MENU,
               'message': DEFAULTFONT.render("", 1, DEFAULTFONTCOLOR),
               'quit': quitButton,
               'restart': restartButton,
               'menuReturn': menuButton,
               'play': playButton,
               'options': optionsButton,
               'instruct': instructButton,
               'quit2': quitButton2,
               'return': returnButton,
               'optionShow': OPTIONS,
               'instructShow': INSTRUCT,
                'sound': soundLabel,
                'soundOn': soundOn,
                'soundOff': soundOff,
                'minutes': numMin,
                'oneMin': oneMin,
                'threeMin': threeMin,
                'fiveMin': fiveMin,
                'numPlayers': numPlayers,
                'onePlayer': onePlayer,
                'twoPlayers': twoPlayers}

    # Initialize font dictionary
    FONTDICT = {'default': DEFAULTFONT,
                'titleOne': TITLEFONT,
                'titleTwo': TITLEFONT,
                'button': BUTTONFONT,
                'wind': WINDFONT,
                'menu': MENUFONT}

    # Sound dictionary
    SOUNDDICT = {'launch': LAUNCH,
                 'intro': INTRO,
                 'select': SELECT,
                 'ready': READY,
                 'go': GO,
                 'horn': HORN,
                 'cheer': CHEER,
                 'wind': WIND,
                 'score': SCORE,
                 'bounce': BOUNCE}

    # Go to menu function
    menu(VARIABLEDICT, RECTDICT, IMGDICT, FONTDICT, SOUNDDICT)

# Menu function
def menu(VARIABLEDICT, RECTDICT, IMGDICT, FONTDICT, SOUNDDICT):
    if VARIABLEDICT['start']:
        SOUNDDICT['intro'].play() # Play intro sound if first time playing
    VARIABLEDICT['start'] = False

    # Show menu
    while True:
        redraw_window(VARIABLEDICT, RECTDICT, IMGDICT)

        # Event Check
        for event in pg.event.get():
            if event.type == QUIT or event.type == KEYUP and event.key == K_ESCAPE:
                # Player quits
                pg.quit()
                sys.exit()
            if event.type == MOUSEMOTION:
                VARIABLEDICT['mousePos'] = event.pos
            if event.type == MOUSEBUTTONUP:
                if VARIABLEDICT['sound']:
                    SOUNDDICT['select'].play() # Play select sound
                # Check which button was clicked
                if RECTDICT['play'].collidepoint(VARIABLEDICT['mousePos']):
                    # Play button
                    VARIABLEDICT['menu'] = False # Main menu is not showing
                    run_game(VARIABLEDICT, FONTDICT, IMGDICT, RECTDICT, SOUNDDICT)
                elif RECTDICT['options'].collidepoint(VARIABLEDICT['mousePos']):
                    # Options button
                    VARIABLEDICT['menu'] = False
                    VARIABLEDICT['options'] = True # Options screen is showing
                    options(VARIABLEDICT, RECTDICT, IMGDICT, SOUNDDICT)
                    VARIABLEDICT['options'] = False # Options screen is not showing
                    VARIABLEDICT['menu'] = True
                elif RECTDICT['instruct'].collidepoint(VARIABLEDICT['mousePos']):
                    # Instructions button
                    VARIABLEDICT['menu'] = False
                    VARIABLEDICT['instruct'] = True # Instructions are showing
                    instructions(VARIABLEDICT, RECTDICT, IMGDICT, SOUNDDICT)
                    VARIABLEDICT['instruct'] = False # Main menu showing again
                    VARIABLEDICT['menu'] = True
                elif RECTDICT['quit2'].collidepoint(VARIABLEDICT['mousePos']):
                    # Quit button
                    pg.quit()
                    sys.exit()

def options(VARIABLEDICT, RECTDICT, IMGDICT, SOUNDDICT):

    # Show options
    while True:
        redraw_window(VARIABLEDICT, RECTDICT, IMGDICT)

        for event in pg.event.get():
            if event.type == QUIT or event.type == KEYUP and event.key == K_ESCAPE:
                # Player quits
                pg.quit()
                sys.exit()
            if event.type == MOUSEMOTION:
                VARIABLEDICT['mousePos'] = event.pos
            if event.type == MOUSEBUTTONUP:
                if VARIABLEDICT['sound']:
                    SOUNDDICT['select'].play()
                if RECTDICT['return'].collidepoint(VARIABLEDICT['mousePos']):
                    return
                elif RECTDICT['onePlayer'].collidepoint(VARIABLEDICT['mousePos']):
                    VARIABLEDICT['players'] = 1
                    VARIABLEDICT['player'] = False
                elif RECTDICT['twoPlayers'].collidepoint(VARIABLEDICT['mousePos']):
                    VARIABLEDICT['players'] = 2
                    VARIABLEDICT['player'] = False
                elif RECTDICT['oneMin'].collidepoint(VARIABLEDICT['mousePos']):
                    VARIABLEDICT['gameTime'] = 60
                elif RECTDICT['threeMin'].collidepoint(VARIABLEDICT['mousePos']):
                    VARIABLEDICT['gameTime'] = 180
                elif RECTDICT['fiveMin'].collidepoint(VARIABLEDICT['mousePos']):
                    VARIABLEDICT['gameTime'] = 300
                elif RECTDICT['soundOn'].collidepoint(VARIABLEDICT['mousePos']):
                    VARIABLEDICT['sound'] = True
                elif RECTDICT['soundOff'].collidepoint(VARIABLEDICT['mousePos']):
                    VARIABLEDICT['sound'] = False
                    
def instructions(VARIABLEDICT, RECTDICT, IMGDICT, SOUNDDICT):

    # Show instructions  
    while True:
        redraw_window(VARIABLEDICT, RECTDICT, IMGDICT)

        for event in pg.event.get():
            if event.type == QUIT or event.type == KEYUP and event.key == K_ESCAPE:
                # Player quits
                pg.quit()
                sys.exit()
            if event.type == MOUSEMOTION:
                VARIABLEDICT['mousePos'] = event.pos
            if event.type == MOUSEBUTTONUP:
                if VARIABLEDICT['sound']:
                    SOUNDDICT['select'].play()
                if RECTDICT['return'].collidepoint(VARIABLEDICT['mousePos']):
                    return

# Game function
def run_game(VARIABLEDICT, FONTDICT, IMGDICT, RECTDICT, SOUNDDICT):
    pg.mixer.pause() # Stop previous sounds when game starts

    # Set game time
    VARIABLEDICT['timer'] = VARIABLEDICT['gameTime']

    # Set graphics according to player settings
    if not VARIABLEDICT['player']:
        # Greet player one at start
        VARIABLEDICT['message'] = 10
        write_message(VARIABLEDICT, FONTDICT, RECTDICT, IMGDICT)
        
        RECTDICT['football'].midbottom = (HALFWIDTH + QUARTERWIDTH,
                                          WINHEIGHT)
        VARIABLEDICT['rotation'] = 6
        RECTDICT['goal'].midbottom = (QUARTERWIDTH, WINHEIGHT + 50)
    else:
        # Greet Player Two at start
        VARIABLEDICT['message'] = 11
        write_message(VARIABLEDICT, FONTDICT, RECTDICT, IMGDICT)
        
        RECTDICT['football'].midbottom = (QUARTERWIDTH,
                                          WINHEIGHT)
        VARIABLEDICT['rotation'] = 18
        RECTDICT['goal2'].midbottom = (HALFWIDTH + QUARTERWIDTH,
                                      WINHEIGHT + 50)
    
    # Call writing messages function to tell player to get ready
    if VARIABLEDICT['sound']:
        SOUNDDICT['ready'].play() # Play ready sound
    VARIABLEDICT['message'] = 1
    write_message(VARIABLEDICT, FONTDICT, RECTDICT, IMGDICT)

    # Tell player to start playing
    if VARIABLEDICT['sound']:
        SOUNDDICT['go'].play() # Play go sound
    VARIABLEDICT['message'] = 2
    write_message(VARIABLEDICT, FONTDICT, RECTDICT, IMGDICT)

    # Main loop
    while not VARIABLEDICT['gameOver']:

        # Event Check
        for event in pg.event.get():
            if event.type == QUIT or event.type == KEYUP and event.key == K_ESCAPE:
                # Player quits
                pg.quit()
                sys.exit()
            if event.type == MOUSEMOTION:
                VARIABLEDICT['mousePos'] = event.pos
            if event.type == MOUSEBUTTONDOWN:
                if RECTDICT['football'].collidepoint((VARIABLEDICT['mousePos']))\
                     and not VARIABLEDICT['draggingArrow']:
                    # Player clicked ball
                    VARIABLEDICT['draggingArrow'] = True
                    VARIABLEDICT['showHelp'] = False
            elif event.type == MOUSEMOTION and VARIABLEDICT['draggingArrow']:
                    # Player is dragging arrow
                    VARIABLEDICT['mousePos'] = event.pos
                    VARIABLEDICT['power'], VARIABLEDICT['launchAngle'] = power_gague(VARIABLEDICT, RECTDICT)
                    draw_arrow(VARIABLEDICT, RECTDICT, FONTDICT)
            elif event.type == MOUSEBUTTONUP and VARIABLEDICT['draggingArrow']:
                # Ball is launched
                VARIABLEDICT['draggingArrow'] = False
                if VARIABLEDICT['sound']:
                    SOUNDDICT['launch'].play() # Play launch sound
                launch_ball(VARIABLEDICT, RECTDICT, IMGDICT, SOUNDDICT)
                VARIABLEDICT['power'] = 50
                VARIABLEDICT['launchAngle'] = 0

        # Show instructions to play for first time in game
        if VARIABLEDICT['showHelp'] and not VARIABLEDICT['player']:
            VARIABLEDICT['message'] = 9
            write_message(VARIABLEDICT, FONTDICT, RECTDICT, IMGDICT)
        else:
            VARIABLEDICT['message'] = 0

        # Randomize wind speed and angle
        if randint(1, 100) == 50:
            VARIABLEDICT['windAngle'] = random() * 2 * pi
            VARIABLEDICT['windSpeed'] = random() * 100
            if VARIABLEDICT['sound']:
                SOUNDDICT['wind'].play(0, 3000) # Play wind sound for a few seconds


        VARIABLEDICT['timer'] -= .05 # decrease time as you go
                
        # Check if time runs out
        if VARIABLEDICT['timer'] < 0:
            VARIABLEDICT['timer'] = 0
            if VARIABLEDICT['player'] or VARIABLEDICT['players'] == 1:
                # End of player two's game
                VARIABLEDICT['gameOver'] = True
            else:
                # Reset game for player 2
                VARIABLEDICT['gameOver'] = False
                VARIABLEDICT['player'] = True
                VARIABLEDICT['windSpeed'] = 0
                VARIABLEDICT['windAngle'] = 0
                VARIABLEDICT['message'] = 0
                run_game(VARIABLEDICT, FONTDICT, IMGDICT, RECTDICT, SOUNDDICT)

        # Reset center based on settings
        if not VARIABLEDICT['player']:
            RECTDICT['football'].midbottom = (HALFWIDTH + QUARTERWIDTH,
                                              WINHEIGHT)
            VARIABLEDICT['rotation'] = 6
            RECTDICT['goal'].midbottom = (QUARTERWIDTH, WINHEIGHT + 50)
        else:
            RECTDICT['football'].midbottom = (QUARTERWIDTH,
                                              WINHEIGHT)
            VARIABLEDICT['rotation'] = 18
            RECTDICT['goal2'].midbottom = (HALFWIDTH + QUARTERWIDTH,
                                          WINHEIGHT + 50)
        redraw_window(VARIABLEDICT, RECTDICT, IMGDICT) # redraw window

    # Call function to write appropriate game over message on screen,
    # depending on which player wins or if there is a tie
    if VARIABLEDICT['players'] == 1:
        # One Player Game
        if VARIABLEDICT['scoreOne'] > VARIABLEDICT['hiScore']:
            # Player One got high score
            if VARIABLEDICT['sound']:
                SOUNDDICT['cheer'].play() # Play crow cheering sound
            VARIABLEDICT['message'] = 12
            write_message(VARIABLEDICT, FONTDICT, RECTDICT, IMGDICT)
            VARIABLEDICT['hiScore'] = VARIABLEDICT['scoreOne']
        else:
            if VARIABLEDICT['sound']:
                SOUNDDICT['horn'].play() # Play air horn sound
            VARIABLEDICT['message'] = 13
            write_message(VARIABLEDICT, FONTDICT, RECTDICT, IMGDICT)
    else:
        # Two Player Game
        if VARIABLEDICT['scoreOne'] > VARIABLEDICT['hiScore']\
            and VARIABLEDICT['scoreOne'] > VARIABLEDICT['scoreTwo']:
            # Player One beats Player Two with hi score
            if VARIABLEDICT['sound']:
                SOUNDDICT['cheer'].play() 
            VARIABLEDICT['message'] = 3
            write_message(VARIABLEDICT, FONTDICT, RECTDICT, IMGDICT)
            VARIABLEDICT['hiScore'] = VARIABLEDICT['scoreOne']
        elif VARIABLEDICT['scoreTwo'] > VARIABLEDICT['hiScore']\
            and VARIABLEDICT['scoreTwo'] > VARIABLEDICT['scoreOne']:
            # Player Two beats Player One with hi score
            if VARIABLEDICT['sound']:
                SOUNDDICT['cheer'].play()
            VARIABLEDICT['message'] = 4
            write_message(VARIABLEDICT, FONTDICT, RECTDICT, IMGDICT)
            VARIABLEDICT['hiScore'] = VARIABLEDICT['scoreTwo']
        elif VARIABLEDICT['scoreOne'] <= VARIABLEDICT['hiScore']\
            and VARIABLEDICT['scoreOne'] > VARIABLEDICT['scoreTwo']:
            # Player One beats Player Two
            if VARIABLEDICT['sound']:
                SOUNDDICT['horn'].play()
            VARIABLEDICT['message'] = 5
            write_message(VARIABLEDICT, FONTDICT, RECTDICT, IMGDICT)
        elif VARIABLEDICT['scoreTwo'] <= VARIABLEDICT['hiScore']\
            and VARIABLEDICT['scoreTwo'] > VARIABLEDICT['scoreOne']:
            # Player Two beats Player One
            if VARIABLEDICT['sound']:
                SOUNDDICT['horn'].play()
            VARIABLEDICT['message'] = 6
            write_message(VARIABLEDICT, FONTDICT, RECTDICT, IMGDICT)
        elif VARIABLEDICT['scoreOne'] > VARIABLEDICT['hiScore']\
            and VARIABLEDICT['scoreTwo'] > VARIABLEDICT['hiScore']\
            and VARIABLEDICT['scoreOne'] == VARIABLEDICT['scoreTwo']:
            # Both players tie for hi score
            if VARIABLEDICT['sound']:
                SOUNDDICT['cheer'].play()
            VARIABLEDICT['message'] = 7
            write_message(VARIABLEDICT, FONTDICT, RECTDICT, IMGDICT)
            VARIABLEDICT['hiScore'] = VARIABLEDICT['scoreOne']
        elif VARIABLEDICT['scoreOne'] == VARIABLEDICT['scoreTwo']:
            # Both players tie
            if VARIABLEDICT['sound']:
                SOUNDDICT['horn'].play()
            VARIABLEDICT['message'] = 8
            write_message(VARIABLEDICT, FONTDICT, RECTDICT, IMGDICT)

    while VARIABLEDICT['gameOver']:
        
        # Check event loop if player clicks button
        for event in pg.event.get():
            if event.type == QUIT or event.type == KEYUP and event.key == K_ESCAPE:
                pg.quit()
                sys.exit()
            if event.type == MOUSEMOTION:
                VARIABLEDICT['mousePos'] = event.pos
            if event.type == MOUSEBUTTONDOWN:
                if VARIABLEDICT['sound']:
                    SOUNDDICT['select'].play()
                if RECTDICT['quit'].collidepoint(VARIABLEDICT['mousePos']):
                    # Player quits
                    pg.quit()
                    sys.exit()
                elif RECTDICT['restart'].collidepoint(VARIABLEDICT['mousePos']):
                    # Player resets game
                    VARIABLEDICT['gameOver'] = False
                    VARIABLEDICT['scoreOne'] = 0
                    VARIABLEDICT['scoreTwo'] = 0
                    VARIABLEDICT['windSpeed'] = 0
                    VARIABLEDICT['windAngle'] = 0
                    VARIABLEDICT['message'] = 0
                    VARIABLEDICT['player'] = False
                    run_game(VARIABLEDICT, FONTDICT, IMGDICT, RECTDICT, SOUNDDICT)
                elif RECTDICT['menuReturn'].collidepoint(VARIABLEDICT['mousePos']):
                    # Player goes back to menu
                    VARIABLEDICT['gameOver'] = False
                    VARIABLEDICT['scoreOne'] = 0
                    VARIABLEDICT['scoreTwo'] = 0
                    VARIABLEDICT['windSpeed'] = 0
                    VARIABLEDICT['windAngle'] = 0
                    VARIABLEDICT['message'] = 0
                    VARIABLEDICT['menu'] = True
                    pg.mixer.pause() 
                    menu(VARIABLEDICT, RECTDICT, IMGDICT, FONTDICT, SOUNDDICT)
                    return

        redraw_window(VARIABLEDICT, RECTDICT, IMGDICT)

# Redraw window
def redraw_window(VARIABLEDICT, RECTDICT, IMGDICT):
    if VARIABLEDICT['menu']:
        # Main menu is showing
        DISPLAYSURF.blit(IMGDICT['menu'], RECTDICT['menu'])
        DISPLAYSURF.blit(IMGDICT['play'], RECTDICT['play'])
        DISPLAYSURF.blit(IMGDICT['options'], RECTDICT['options'])
        DISPLAYSURF.blit(IMGDICT['instruct'], RECTDICT['instruct'])
        DISPLAYSURF.blit(IMGDICT['quit2'], RECTDICT['quit2'])
    elif VARIABLEDICT['options']:
        # Options is showing
        # Initialize list of centers of Rect objects for radio buttons
        radioList = [(RECTDICT['onePlayer'].left - RADIORADIUS,
                      RECTDICT['onePlayer'].centery), #one player button
                     (RECTDICT['twoPlayers'].left - RADIORADIUS,
                      RECTDICT['twoPlayers'].centery), #two players button
                     (RECTDICT['oneMin'].left - RADIORADIUS,
                      RECTDICT['oneMin'].centery), #one minute button
                     (RECTDICT['threeMin'].left - RADIORADIUS,
                      RECTDICT['threeMin'].centery), #three minutes button
                     (RECTDICT['fiveMin'].left - RADIORADIUS,
                      RECTDICT['fiveMin'].centery), #five minutes button
                     (RECTDICT['soundOn'].left - RADIORADIUS,
                      RECTDICT['soundOn'].centery), #sound on button
                     (RECTDICT['soundOff'].left - RADIORADIUS,
                      RECTDICT['soundOff'].centery) #sound off button
                     ]
        DISPLAYSURF.blit(IMGDICT['optionShow'], RECTDICT['optionShow'])
        DISPLAYSURF.blit(IMGDICT['numPlayers'], RECTDICT['numPlayers'])
        DISPLAYSURF.blit(IMGDICT['onePlayer'], RECTDICT['onePlayer'])
        DISPLAYSURF.blit(IMGDICT['twoPlayers'], RECTDICT['twoPlayers'])
        DISPLAYSURF.blit(IMGDICT['minutes'], RECTDICT['minutes'])
        DISPLAYSURF.blit(IMGDICT['oneMin'], RECTDICT['oneMin'])
        DISPLAYSURF.blit(IMGDICT['threeMin'], RECTDICT['threeMin'])
        DISPLAYSURF.blit(IMGDICT['fiveMin'], RECTDICT['fiveMin'])
        DISPLAYSURF.blit(IMGDICT['sound'], RECTDICT['sound'])
        DISPLAYSURF.blit(IMGDICT['soundOn'], RECTDICT['soundOn'])
        DISPLAYSURF.blit(IMGDICT['soundOff'], RECTDICT['soundOff'])
        DISPLAYSURF.blit(IMGDICT['return'], RECTDICT['return'])
        for b in radioList:
            pg.draw.circle(DISPLAYSURF, WHITE, b, RADIORADIUS)
        if (VARIABLEDICT['players'] == 1):
            pg.draw.circle(DISPLAYSURF, BLACK, radioList[0], RADIORADIUS - 3)
        else:
            pg.draw.circle(DISPLAYSURF, BLACK, radioList[1], RADIORADIUS - 3)
        if (VARIABLEDICT['gameTime'] == 60):
            pg.draw.circle(DISPLAYSURF, BLACK, radioList[2], RADIORADIUS - 3)
        elif (VARIABLEDICT['gameTime'] == 180):
            pg.draw.circle(DISPLAYSURF, BLACK, radioList[3], RADIORADIUS - 3)
        else:
            pg.draw.circle(DISPLAYSURF, BLACK, radioList[4], RADIORADIUS - 3)
        if (VARIABLEDICT['sound'] == True):
            pg.draw.circle(DISPLAYSURF, BLACK, radioList[5], RADIORADIUS - 3)
        else:
            pg.draw.circle(DISPLAYSURF, BLACK, radioList[6], RADIORADIUS - 3)
    elif VARIABLEDICT['instruct']:
        # Instructions showing
        DISPLAYSURF.blit(IMGDICT['instructShow'], RECTDICT['instructShow'])
        DISPLAYSURF.blit(IMGDICT['return'], RECTDICT['return'])
    else:
        # Game is showing
        DISPLAYSURF.blit(IMGDICT['background'], RECTDICT['background'])
        draw_wind(VARIABLEDICT, FONTDICT)
        write_info(VARIABLEDICT, FONTDICT)
        DISPLAYSURF.blit(IMGDICT['football'][VARIABLEDICT['rotation']],
                                             RECTDICT['football'])
        if not VARIABLEDICT['player']:
            DISPLAYSURF.blit(IMGDICT['goal'], RECTDICT['goal'])
        else:
            DISPLAYSURF.blit(IMGDICT['goal2'], RECTDICT['goal2'])
        if VARIABLEDICT['message'] > 0:
            DISPLAYSURF.blit(IMGDICT['message'], RECTDICT['message'])
        if VARIABLEDICT['gameOver']:
            DISPLAYSURF.blit(IMGDICT['quit'], RECTDICT['quit'])
            DISPLAYSURF.blit(IMGDICT['restart'], RECTDICT['restart'])
            DISPLAYSURF.blit(IMGDICT['menuReturn'], RECTDICT['menuReturn'])
    pg.display.update()
    FPSCLOCK.tick(FPS)
    return

# Show player messages on screen
def write_message(VARIABLEDICT, FONTDICT, RECTDICT, IMGDICT):

    # Basically create messages and then flash them for an alloted time
    if VARIABLEDICT['message'] == 1:
        IMGDICT['message'] = FONTDICT['titleOne'].render('Ready...',
                                                    1, TITLEONECOLOR)
        RECTDICT['message'] = IMGDICT['message'].get_rect()
        for x in range(0, HALFWIDTH + RECTDICT['message'].width // 2, 100):
            RECTDICT['message'].center = (x, HALFHEIGHT)
            redraw_window(VARIABLEDICT, RECTDICT, IMGDICT)
        pg.time.wait(1000)
        for x in range(HALFWIDTH, WINWIDTH + RECTDICT['message'].width // 2,
                       100):
            RECTDICT['message'].center = (x, HALFHEIGHT)
            redraw_window(VARIABLEDICT, RECTDICT, IMGDICT)
    elif VARIABLEDICT['message'] == 2:
        IMGDICT['message'] = FONTDICT['titleOne'].render('GO!', 1,
                                                         TITLEONECOLOR)
        RECTDICT['message'] = IMGDICT['message'].get_rect()
        RECTDICT['message'].center = (HALFWIDTH, HALFHEIGHT)
        redraw_window(VARIABLEDICT, RECTDICT, IMGDICT)
        pg.time.wait(500)
    elif VARIABLEDICT['message'] == 3:
        IMGDICT['message'] = FONTDICT['titleTwo'].render('Player One got a high score!',
                                                         1, TITLETWOCOLOR)
        RECTDICT['message'] = IMGDICT['message'].get_rect()
        for y in range(0, HALFHEIGHT, 5):
            RECTDICT['message'].midbottom = (HALFWIDTH, y)
            redraw_window(VARIABLEDICT, RECTDICT, IMGDICT)
        pg.time.wait(1000)
    elif VARIABLEDICT['message'] == 4:
        IMGDICT['message'] = FONTDICT['titleTwo'].render('Player Two got a high score!',
                                                         1, TITLETWOCOLOR)
        RECTDICT['message'] = IMGDICT['message'].get_rect()
        for y in range(0, HALFHEIGHT, 5):
            RECTDICT['message'].midbottom = (HALFWIDTH, y)
            redraw_window(VARIABLEDICT, RECTDICT, IMGDICT)
        pg.time.wait(1000)
    elif VARIABLEDICT['message'] == 5:
        IMGDICT['message'] = FONTDICT['titleTwo'].render('Player One wins!', 1,
                                                         TITLETWOCOLOR)
        RECTDICT['message'] = IMGDICT['message'].get_rect()
        for y in range(0, HALFHEIGHT, 5):
            RECTDICT['message'].midbottom = (HALFWIDTH, y)
            redraw_window(VARIABLEDICT, RECTDICT, IMGDICT)
        pg.time.wait(1000)
    elif VARIABLEDICT['message'] == 6:
        IMGDICT['message'] = FONTDICT['titleTwo'].render('Player Two wins!', 1,
                                                         TITLETWOCOLOR)
        RECTDICT['message'] = IMGDICT['message'].get_rect()
        for y in range(0, HALFHEIGHT, 5):
            RECTDICT['message'].midbottom = (HALFWIDTH, y)
            redraw_window(VARIABLEDICT, RECTDICT, IMGDICT)
        pg.time.wait(1000)
    elif VARIABLEDICT['message'] == 7:
        IMGDICT['message'] = FONTDICT['titleTwo'].render('Tie with high score!',
                                                         1, TITLETWOCOLOR)
        RECTDICT['message'] = IMGDICT['message'].get_rect()
        for y in range(0, HALFHEIGHT, 5):
            RECTDICT['message'].midbottom = (HALFWIDTH, y)
            redraw_window(VARIABLEDICT, RECTDICT, IMGDICT)
        pg.time.wait(1000)
    elif VARIABLEDICT['message'] == 8:
        IMGDICT['message'] = FONTDICT['titleTwo'].render('Tie game!', 1,
                                                         TITLETWOCOLOR)
        RECTDICT['message'] = IMGDICT['message'].get_rect()
        for y in range(0, HALFHEIGHT, 5):
            RECTDICT['message'].midbottom = (HALFWIDTH, y)
            redraw_window(VARIABLEDICT, RECTDICT, IMGDICT)
        pg.time.wait(1000)

    elif VARIABLEDICT['message'] == 9:
        IMGDICT['message'] = FONTDICT['default'].render('Click and drag arrow to launch ball', 1,
                                                         DEFAULTBACKCOLOR)
        RECTDICT['message'] = IMGDICT['message'].get_rect()
        RECTDICT['message'].midbottom = (RECTDICT['football'].centerx,
                                         RECTDICT['football'].top)
        redraw_window(VARIABLEDICT, RECTDICT, IMGDICT)
        
    # Greet Player 1
    elif VARIABLEDICT['message'] == 10:
        IMGDICT['message'] = FONTDICT['titleOne'].render('Player One', 1,
                                                         TITLEONECOLOR)
        RECTDICT['message'] = IMGDICT['message'].get_rect()
        RECTDICT['message'].center = (HALFWIDTH, HALFHEIGHT)
        redraw_window(VARIABLEDICT, RECTDICT, IMGDICT)
        pg.time.wait(500)

    # Greet Player 2
    elif VARIABLEDICT['message'] == 11:
        IMGDICT['message'] = FONTDICT['titleOne'].render('Player Two', 1,
                                                         TITLEONECOLOR)
        RECTDICT['message'] = IMGDICT['message'].get_rect()
        RECTDICT['message'].center = (HALFWIDTH, HALFHEIGHT)
        redraw_window(VARIABLEDICT, RECTDICT, IMGDICT)
        pg.time.wait(500)

    # One-Player hi score
    elif VARIABLEDICT['message'] == 12:
        IMGDICT['message'] = FONTDICT['titleTwo'].render('High Score!',
                                                         1, TITLETWOCOLOR)
        RECTDICT['message'] = IMGDICT['message'].get_rect()
        for y in range(0, HALFHEIGHT, 5):
            RECTDICT['message'].midbottom = (HALFWIDTH, y)
            redraw_window(VARIABLEDICT, RECTDICT, IMGDICT)
        pg.time.wait(1000)

    # One-Player game over
    elif VARIABLEDICT['message'] == 13:
        IMGDICT['message'] = FONTDICT['titleTwo'].render('Game Over',
                                                         1, TITLETWOCOLOR)
        RECTDICT['message'] = IMGDICT['message'].get_rect()
        for y in range(0, HALFHEIGHT, 5):
            RECTDICT['message'].midbottom = (HALFWIDTH, y)
            redraw_window(VARIABLEDICT, RECTDICT, IMGDICT)
        pg.time.wait(1000)
    return

# Create and write all score and time info about on screen
def write_info(VARIABLEDICT, FONTDICT):
    
    scoreWrite1 = FONTDICT['default'].render('P1: {0}'.format(VARIABLEDICT['scoreOne']),
                                             1,
                                     DEFAULTFONTCOLOR, DEFAULTBACKCOLOR)
    score1Rect = scoreWrite1.get_rect()
    score1Rect.topleft = (5, 5)
    scoreWrite2 = FONTDICT['default'].render('P2: {0}'.format(VARIABLEDICT['scoreTwo']),
                                     1,
                                     DEFAULTFONTCOLOR, DEFAULTBACKCOLOR)
    score2Rect = scoreWrite2.get_rect()
    score2Rect.topright = (WINWIDTH - 5, 5)
    hiScoreWrite = FONTDICT['default'].render('Hi-Score: {0}'.format(VARIABLEDICT['hiScore']),
                                              1,
                                      DEFAULTFONTCOLOR, DEFAULTBACKCOLOR)
    hiScoreRect = hiScoreWrite.get_rect()
    hiScoreRect.center = (HALFWIDTH, 5)
    timeWrite = FONTDICT['default'].render('Time: {0:.0f}'.format(VARIABLEDICT['timer']),
                                           1,
                                   DEFAULTFONTCOLOR, DEFAULTBACKCOLOR)
    timeRect = timeWrite.get_rect()
    timeRect.topright = score2Rect.bottomright
    DISPLAYSURF.blit(scoreWrite1, score1Rect)
    DISPLAYSURF.blit(scoreWrite2, score2Rect)
    DISPLAYSURF.blit(hiScoreWrite, hiScoreRect)
    DISPLAYSURF.blit(timeWrite, timeRect)
    return

# Calculate launch power and angle from dragging arrow
def power_gague(VARIABLEDICT, RECTDICT):

    # Set relevant variables to names
    mousex = VARIABLEDICT['mousePos'][0]
    mousey = VARIABLEDICT['mousePos'][1]
    centerx = RECTDICT['football'].centerx
    centery = RECTDICT['football'].centery
    
    power = hypot(mousex - centerx,
                  mousey - centery)
    if power > 200:
        power = 200
    try:
        # Check if angle is straight up to avoid error
        angle = atan2(centery - mousey,
                      centerx - mousex)
    except:
        angle = pi / 2
        
    return (power, angle)

# Calculate length of arrow
def draw_arrow(VARIABLEDICT, RECTDICT, FONTDICT):

    mousex = VARIABLEDICT['mousePos'][0]
    mousey = VARIABLEDICT['mousePos'][1]
    centerx = RECTDICT['football'].centerx
    centery = RECTDICT['football'].centery
    power = VARIABLEDICT['power']
    angle = VARIABLEDICT['launchAngle']

    # Set points for arrow head          
    points = [(mousex - power * cos(angle),
              mousey - power * sin(angle)),
              (mousex  - power * cos(angle - 3 * pi / 4),
              mousey - power * sin(angle - 3 * pi / 4)),
             (mousex  - power * cos(angle + 3 * pi / 4),
              mousey - power * sin(angle + 3 * pi / 4))]

    # Check if arrow exceeds power limit    
    if hypot(mousex - centerx,
             mousey - centery) > power:

        # Set a max x and y
        maxx = centerx - power * cos(angle)
        maxy = centery - power * sin(angle)
        
        points = [(maxx - power * cos(angle),
                  maxy - power * sin(angle)),
                  (maxx  - power * cos(angle - 3 * pi / 4),
                  maxy - power * sin(angle - 3 * pi / 4)),
                 (maxx  - power * cos(angle + 3 * pi / 4),
                  maxy - power * sin(angle + 3 * pi / 4))]
        points2 = [RECTDICT['football'].center, (maxx, maxy)]

    else:
        # Arrow does not exceed power limit        

        points2 = [RECTDICT['football'].center, (mousex, mousey)]
        
    # Draw arrowhead
    pg.draw.polygon(DISPLAYSURF, ARROWCOLOR, points)

    # Draw arrow shaft
    pg.draw.polygon(DISPLAYSURF, ARROWCOLOR, points2, 50)

    # Write power level next to arrow
    powerLvl = FONTDICT['default'].render(str(int(power)),
                                          1, DEFAULTFONTCOLOR)
    DISPLAYSURF.blit(powerLvl, (mousex - 50, mousey))

    pg.display.update()
    FPSCLOCK.tick(FPS)
    return

# Calculate ball trajectory and speed
def launch_ball(VARIABLEDICT, RECTDICT, IMGDICT, SOUNDDICT):

    # Initialize all relevant variables
    launchTime = 1
    shoot = True
    center = RECTDICT['football'].center
    negative = 1 # Reversal of ball direction both x- and y-
    negative2 = 1
    negative3 = 3 # Reversal of ball rotation
    power = VARIABLEDICT['power']
    angle = VARIABLEDICT['launchAngle']
    winds = VARIABLEDICT['windSpeed']
    winda = VARIABLEDICT['windAngle']
    radius = VARIABLEDICT['radius']

    # Check which player is playing
    if not VARIABLEDICT['player']:
        # False = Player 1, True = Player 2

        # Shoot loop
        while shoot:

            # Set speed of ball
            velocity = (negative * (power * cos(angle) + winds * cos(winda)),
                        negative2 * (power * sin(angle) + winds * sin(winda)
                                     - GRAVITY * launchTime))
            
            # Set center accordingly
            center = find_center(center, velocity, launchTime)
            
            # Collision checking
            # We check if the center of the ball will be out of bounds, and correct
            # centering if it is
                
            # Goal area of goal post
            if center[0] <= RECTDICT['goalArea'].centerx\
               and center[1] >= RECTDICT['goalArea'].top - radius\
               and center[1] <= RECTDICT['goalArea'].bottom - radius:
                if VARIABLEDICT['sound']:
                    SOUNDDICT['score'].play() # Play scoring sound each time player
                                              # scores a goal
                VARIABLEDICT['scoreOne'] += 10

            # Stem of goal post
            if center[0] <= RECTDICT['brickAreaOne'].right + radius:
                if center[1] < RECTDICT['brickAreaTwo'].top - radius\
                   and center[1] >= RECTDICT['brickAreaOne'].top - radius:
                    if VARIABLEDICT['sound']:
                        SOUNDDICT['bounce'].play() # Play sound effect for ball
                                                   # rebounding off of brick area
                                                   # every time ball hits brick area
                    center = (RECTDICT['brickAreaOne'].right + radius, center[1])
                    negative = -negative * FRICTION
                    negative3 = -negative3
                elif center[1] >= RECTDICT['brickAreaTwo'].top - radius:
                    # Ball collides with stem and base of goal post
                    if VARIABLEDICT['sound']:
                        SOUNDDICT['bounce'].play()
                    center = (RECTDICT['brickAreaOne'].right + radius,
                              RECTDICT['brickAreaOne'].top - radius)
                    negative = -negative * FRICTION
                    negative2 = -negative2 * FRICTION
                    negative3 = -negative3
                    
            # Right of base of goal post
            if center[0] <= RECTDICT['brickAreaTwo'].right + radius:
                if center[1] >= RECTDICT['brickAreaTwo'].top:
                    if VARIABLEDICT['sound']:
                        SOUNDDICT['bounce'].play()
                    center = (RECTDICT['brickAreaTwo'].right + radius, center[1])
                    negative = -negative * FRICTION
                    negative3 = -negative3
                if center[1] >= RECTDICT['brickAreaTwo'].top - radius:
                    if VARIABLEDICT['sound']:
                        SOUNDDICT['bounce'].play()
                    center = (center[0], RECTDICT['brickAreaTwo'].top - radius)
                    negative2 = -negative2 * FRICTION

            # Left side of screen -- end launch
            if center[0] < radius:
                center = (radius, center[1])
                shoot = False

            # Right side of screen -- end launch
            if center[0] > WINWIDTH - radius:
                center = (WINWIDTH - radius, center[1])
                shoot = False

            # Table collision checking
            if center[1] > WINHEIGHT - radius:
                if VARIABLEDICT['sound']:
                        SOUNDDICT['bounce'].play()
                center = (center[0], WINHEIGHT - radius)
                negative2 = -negative2 * FRICTION

            RECTDICT['football'].center = center # Set new center
                
            # Do ball rotation, checking if ball is over-rotated
            if VARIABLEDICT['rotation'] + 3 > 23 \
               or VARIABLEDICT['rotation'] - 3 < 0:
                negative3 = -negative3
            else:
                VARIABLEDICT['rotation'] += negative3
                    
            # End loop if ball comes to stop
            if abs(velocity[0]) < 1 or abs(velocity[1]) < 1:
                shoot = False

            redraw_window(VARIABLEDICT, RECTDICT, IMGDICT)

            launchTime += 1 # Increase ball launch time

    else:
        # Player 2
        negative3 = -3
        
        while shoot:

            velocity = (negative * (power * cos(angle) + winds * cos(winda)),
                        negative2 * (power * sin(angle) + winds * sin(winda)
                                     - GRAVITY * launchTime))

            center = find_center(center, velocity, launchTime)
                
            # Goal area of goal post
            if center[0] >= RECTDICT['goalAreaTwo'].centerx\
               and center[1] >= RECTDICT['goalAreaTwo'].top - radius\
               and center[1] <= RECTDICT['goalAreaTwo'].bottom - radius:
                SOUNDDICT['score'].play()
                VARIABLEDICT['scoreTwo'] += 10

            # Stem of goal post
            if center[0] >= RECTDICT['brickAreaThree'].left - radius:
                if center[1] < RECTDICT['brickAreaFour'].top - radius\
                   and center[1] >= RECTDICT['brickAreaThree'].top - radius:
                    center = (RECTDICT['brickAreaThree'].left - radius, center[1])
                    negative = -negative * FRICTION
                    negative3 = -negative3
                elif center[1] >= RECTDICT['brickAreaFour'].top - radius:
                    # Ball collides with stem and base of goal post
                    center = (RECTDICT['brickAreaThree'].left - radius,
                              RECTDICT['brickAreaThree'].top - radius)
                    negative = -negative * FRICTION
                    negative2 = -negative2 * FRICTION
                    negative3 = -negative3
                    
            # Right of base of goal post
            if center[0] >= RECTDICT['brickAreaFour'].left - radius:
                if center[1] >= RECTDICT['brickAreaFour'].top:
                    center = (RECTDICT['brickAreaFour'].left - radius, center[1])
                    negative = -negative * FRICTION
                    negative3 = -negative3
                if center[1] >= RECTDICT['brickAreaFour'].top - radius:
                    center = (center[0], RECTDICT['brickAreaFour'].top - radius)
                    negative2 = -negative2 * FRICTION

            # Left side of screen -- end launch
            if center[0] < radius:
                center = (radius, center[1])
                shoot = False

            # Right side of screen -- end launch
            if center[0] > WINWIDTH - radius:
                center = (WINWIDTH - radius, center[1])
                shoot = False

            # Table collision checking
            if center[1] > WINHEIGHT - radius:
                center = (center[0], WINHEIGHT - radius)
                negative2 = -negative2 * FRICTION

            RECTDICT['football'].center = center
                
            if VARIABLEDICT['rotation'] + 3 > 23 \
               or VARIABLEDICT['rotation'] - 3 < 0:
                negative3 = -negative3
            else:
                VARIABLEDICT['rotation'] += negative3
                    
            if abs(velocity[0]) < 1 or abs(velocity[1]) < 1:
                shoot = False

            redraw_window(VARIABLEDICT, RECTDICT, IMGDICT)

            launchTime += 1
        
    return

# Find center of object
def find_center(center, velocity, time):
    
    return (int(center[0] - velocity[0] * time),
            int(center[1] - velocity[1] * time))

# Draw wind arrow
def draw_wind(VARIABLEDICT, FONTDICT):

    # Initialize point of arrow depending on which player is up
    if not VARIABLEDICT['player']:
        points = [(WINDARROW[0] - WINDRADIUS * cos(VARIABLEDICT['windAngle']),
                   WINDARROW[1] - WINDRADIUS * sin(VARIABLEDICT['windAngle'])),
                  (WINDARROW[0] + WINDRADIUS * cos(VARIABLEDICT['windAngle'] - pi / 3),
                   WINDARROW[1] + WINDRADIUS * sin(VARIABLEDICT['windAngle'] - pi / 3)),
                  (WINDARROW[0] + WINDRADIUS * cos(VARIABLEDICT['windAngle'] + pi / 3),
                   WINDARROW[1] + WINDRADIUS * sin(VARIABLEDICT['windAngle'] + pi / 3)),
                  (WINDARROW[0] - WINDRADIUS * cos(VARIABLEDICT['windAngle']),
                   WINDARROW[1] - WINDRADIUS * sin(VARIABLEDICT['windAngle']))]
        
        # Draw arrow parts
        pg.draw.circle(DISPLAYSURF, WINDCOLOR, WINDARROW, WINDRADIUS, 1)
        pg.draw.polygon(DISPLAYSURF, WINDCOLOR, points)
        pg.draw.line(DISPLAYSURF, WINDCOLOR, points[0],
                     (WINDARROW[0] - WINDRADIUS * cos(VARIABLEDICT['windAngle']
                                                      - pi),
                       WINDARROW[1] - WINDRADIUS * sin(VARIABLEDICT['windAngle']
                                                       - pi)), 3)

        # Initialize information to print
        winds = FONTDICT['default'].render('Wind: {0:.1f} cm/s'.format(VARIABLEDICT['windSpeed']),
                            1, DEFAULTFONTCOLOR)
        winda = FONTDICT['default'].render('Angle: {0:.1f} deg'.format(VARIABLEDICT['windAngle'] * (180 / pi)),
                            1, DEFAULTFONTCOLOR)
        windsRect = winds.get_rect()
        windaRect = winda.get_rect()
        windsRect.bottomright = (WINDARROW[0] - WINDRADIUS, WINDARROW[1])
        windaRect.topright = windsRect.bottomright
    else:

        points = [(WINDARROW2[0] - WINDRADIUS * cos(VARIABLEDICT['windAngle']),
                   WINDARROW2[1] - WINDRADIUS * sin(VARIABLEDICT['windAngle'])),
                  (WINDARROW2[0] + WINDRADIUS * cos(VARIABLEDICT['windAngle'] - pi / 3),
                   WINDARROW2[1] + WINDRADIUS * sin(VARIABLEDICT['windAngle'] - pi / 3)),
                  (WINDARROW2[0] + WINDRADIUS * cos(VARIABLEDICT['windAngle'] + pi / 3),
                   WINDARROW2[1] + WINDRADIUS * sin(VARIABLEDICT['windAngle'] + pi / 3)),
                  (WINDARROW2[0] - WINDRADIUS * cos(VARIABLEDICT['windAngle']),
                   WINDARROW2[1] - WINDRADIUS * sin(VARIABLEDICT['windAngle']))]
        
        pg.draw.circle(DISPLAYSURF, WINDCOLOR, WINDARROW2, WINDRADIUS, 1)
        pg.draw.polygon(DISPLAYSURF, WINDCOLOR, points)
        pg.draw.line(DISPLAYSURF, WINDCOLOR, points[0],
                     (WINDARROW2[0] - WINDRADIUS * cos(VARIABLEDICT['windAngle']
                                                      - pi),
                       WINDARROW2[1] - WINDRADIUS * sin(VARIABLEDICT['windAngle']
                                                       - pi)), 3)

        winds = FONTDICT['default'].render('Wind: {0:.1f} cm/s'.format(VARIABLEDICT['windSpeed']),
                            1, DEFAULTFONTCOLOR)
        winda = FONTDICT['default'].render('Angle: {0:.1f} deg'.format(VARIABLEDICT['windAngle'] * (180 / pi)),
                            1, DEFAULTFONTCOLOR)
        windsRect = winds.get_rect()
        windaRect = winda.get_rect()
        windsRect.bottomleft = (WINDARROW2[0] + WINDRADIUS, WINDARROW2[1])
        windaRect.topleft = windsRect.bottomleft

    # Display wind information (speed and angle)
    DISPLAYSURF.blit(winds, windsRect)
    DISPLAYSURF.blit(winda, windaRect)
    return

if __name__ == '__main__':
    initialize()
