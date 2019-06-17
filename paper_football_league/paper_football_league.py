# Paper Football League
# Beta Version 1.0
# By Josh Klipstein
# May, 31, 2019

import pygame as pg
import sys
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

#              R    G    B
GREY =       (128, 128, 128)
BLUE =       (  0,   0, 255)
WHITE =      (255, 255, 255)
BLACK =      (  0,   0,   0)
RED =        (192,   0,   0)
GREEN =      (  0, 255,   0)
BROWN =      ( 64,  64,   0)

# Color Constants
DEFAULTFONTCOLOR = BLACK
TITLEONECOLOR = RED
TITLETWOCOLOR = GREEN
DEFAULTBACKCOLOR = WHITE
BUTTONTEXTCOLOR = GREEN
BUTTONCOLOR = BROWN
ARROWCOLOR = RED
WINDCOLOR = BLUE

# Physics Constants
WINDRADIUS = 20
WINDARROW = (int(WINWIDTH - 1.25 * WINDRADIUS), WINHEIGHT - WINDRADIUS)
GRAVITY = 9.8
FRICTION = 0.5

# Initialization function
def initialize():

    global DISPLAYSURF, VARIABLEDICT, IMGDICT, FONTDICT, RECTDICT, FPSCLOCK
    
    # Initialize pygame and declare fonts
    pg.init()
    DISPLAYSURF = pg.display.set_mode((WINWIDTH, WINHEIGHT))
    pg.display.set_caption("Paper Football League Beta -- Josh Klipstein")
    FPSCLOCK = pg.time.Clock()
    TITLEFONT = pg.font.SysFont('arialblack', 40)
    DEFAULTFONT = pg.font.SysFont('calibri', 15)
    BUTTONFONT = pg.font.SysFont('impact', 20)
    WINDFONT = pg.font.Font('freesansbold.ttf', 15)

    # Initialize all game objects
    BACKGROUND = pg.image.load('images/pfootback.tif')
    BACKGROUND = pg.transform.smoothscale(BACKGROUND, (WINWIDTH, WINHEIGHT))
    BACKGROUNDRECT = BACKGROUND.get_rect()
    BACKGROUNDRECT.center = (HALFWIDTH, HALFHEIGHT)
    PAPERFOOTBALL = pg.Rect(0, 0, 120, 120)
    PAPERFOOTBALL.midbottom = (HALFWIDTH + QUARTERWIDTH,
                               WINHEIGHT)
    WINDARROW = (WINWIDTH - WINDRADIUS, WINHEIGHT - WINDRADIUS)
    PAPERFOOTBALLIMG = []
    for i in range(1, 25):
        PAPERFOOTBALLIMG.append(pg.image.load('images/pfb{0}.png'.format(i)))
    GOALIMG = pg.image.load('images/gp.png')
    GOALPOST = GOALIMG.get_rect()
    GOALPOST.midbottom = (QUARTERWIDTH, WINHEIGHT + 50)
    GOALAREA = pg.Rect((GOALPOST.left + 133, GOALPOST.top + 47),
                       (int(GOALPOST.width * 0.08), int(GOALPOST.height * 0.32)))
    POSTAREA = pg.Rect((GOALAREA.left, GOALAREA.bottom),
                       (int(GOALPOST.width * 0.09), int(GOALPOST.height * 0.41)))
    POSTAREA2 = pg.Rect(GOALPOST.left + 48, POSTAREA.bottom,
                        int(GOALPOST.width * 0.82), int(GOALPOST.height * 0.14))

    # End game buttons
    # Quit
    quitButton = BUTTONFONT.render('Quit', 1, BUTTONTEXTCOLOR,
                                           BUTTONCOLOR)
    quitButtonRect = quitButton.get_rect()
    quitButtonRect.center = (HALFWIDTH + QUARTERWIDTH // 2,
                             HALFHEIGHT + QUARTERHEIGHT)
    DISPLAYSURF.blit(quitButton, quitButtonRect)

    # Restart game
    restartButton = BUTTONFONT.render('Restart', 1, BUTTONTEXTCOLOR,
                                      BUTTONCOLOR)
    restartButtonRect = restartButton.get_rect()
    restartButtonRect.center = (HALFWIDTH - QUARTERWIDTH // 2,
                                HALFHEIGHT + QUARTERHEIGHT)
    DISPLAYSURF.blit(restartButton, restartButtonRect)

    # Initialize variable dictionary
    VARIABLEDICT = {'mousePos': (0, 0),
                    'draggingArrow': False,
                    'power': 50,
                    'launchAngle': 0,
                    'scoreOne': 0,
                    'scoreTwo': 0,
                    'hiScore': 0,
                    'gameTime': 60,
                    'windSpeed': 0,
                    'windAngle': 0,
                    'ballSpeed': 0,
                    'message': 0,
                    'rotation': 6,
                    'radius': 60,
                    'gameOver': False,
                    'showHelp': True}

    # Initialize Rect dictionary
    RECTDICT = {'football': PAPERFOOTBALL,
                'goal': GOALPOST,
                'goalArea': GOALAREA,
                'brickAreaOne': POSTAREA,
                'brickAreaTwo': POSTAREA2,
                'background': BACKGROUNDRECT,
                'message': (0, 0, 0, 0),
                'quit': quitButtonRect,
                'restart': restartButtonRect}

    # Initialize image dictionary
    IMGDICT = {'football': PAPERFOOTBALLIMG,
               'goal': GOALIMG,
               'background': BACKGROUND,
               'message': DEFAULTFONT.render("", 1, DEFAULTFONTCOLOR),
               'quit': quitButton,
               'restart': restartButton}

    # Initialize font dictionary
    FONTDICT = {'default': DEFAULTFONT,
                'titleOne': TITLEFONT,
                'titleTwo': TITLEFONT,
                'button': BUTTONFONT,
                'wind': WINDFONT}

    # Go to main function
    main(VARIABLEDICT, RECTDICT, IMGDICT, FONTDICT)
    
# Main function
def main(VARIABLEDICT, RECTDICT, IMGDICT, FONTDICT):

    # Run game function
    run_game(VARIABLEDICT, FONTDICT, IMGDICT, RECTDICT)
        
    if VARIABLEDICT['gameOver']:
        # Call function to write game over message on screen
        VARIABLEDICT['message'] = 10
        write_message(VARIABLEDICT, FONTDICT, RECTDICT, IMGDICT)
        if VARIABLEDICT['scoreOne'] > VARIABLEDICT['hiScore']:
            VARIABLEDICT['hiScore'] = VARIABLEDICT['scoreOne']
        
    while VARIABLEDICT['gameOver']:

        # Check event loop if player clicks button
        for event in pg.event.get():
            if event.type == QUIT or event.type == KEYUP and event.key == K_ESCAPE:
                pg.quit()
                sys.exit()
            if event.type == MOUSEMOTION:
                VARIABLEDICT['mousePos'] = event.pos
            if event.type == MOUSEBUTTONDOWN:
                if RECTDICT['quit'].collidepoint(VARIABLEDICT['mousePos']):
                    pg.quit()
                    sys.exit()
                elif RECTDICT['restart'].collidepoint(VARIABLEDICT['mousePos']):
                    VARIABLEDICT['gameOver'] = False
                    VARIABLEDICT['scoreOne'] = 0
                    VARIABLEDICT['gameTime'] = 60
                    VARIABLEDICT['windSpeed'] = 0
                    VARIABLEDICT['windAngle'] = 0
                    run_game(VARIABLEDICT, FONTDICT, IMGDICT, RECTDICT)
                    VARIABLEDICT['message'] = 10
                    write_message(VARIABLEDICT, FONTDICT, RECTDICT, IMGDICT)

        redraw_window(VARIABLEDICT, RECTDICT, IMGDICT)

# Game function
def run_game(VARIABLEDICT, FONTDICT, IMGDICT, RECTDICT):
    
    # Call writing messages function to tell player to get ready
    VARIABLEDICT['message'] = 1
    write_message(VARIABLEDICT, FONTDICT, RECTDICT, IMGDICT)

    # Tell player to start playing
    VARIABLEDICT['message'] = 2
    write_message(VARIABLEDICT, FONTDICT, RECTDICT, IMGDICT)

    # Main loop
    while True:

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
                launch_ball(VARIABLEDICT, RECTDICT, IMGDICT)
                VARIABLEDICT['power'] = 50
                VARIABLEDICT['launchAngle'] = 0

        # Show instructions to play for first time in game
        if VARIABLEDICT['showHelp']:
            VARIABLEDICT['message'] = 9
            write_message(VARIABLEDICT, FONTDICT, RECTDICT, IMGDICT)
        else:
            VARIABLEDICT['message'] = 0

            # Randomize wind speed and angle
            if randint(1, 100) == 50:
                VARIABLEDICT['windAngle'] = random() * 2 * pi
                VARIABLEDICT['windSpeed'] = random() * 30

            VARIABLEDICT['gameTime'] -= .1 # decrease time as you go
            
            # Check if time runs out
            if VARIABLEDICT['gameTime'] < 0:
                VARIABLEDICT['gameTime'] = 0
                VARIABLEDICT['gameOver'] = True

            # Return to main if game is over
            if VARIABLEDICT['gameOver']:
                return

            # Reset center
            RECTDICT['football'].midbottom = (HALFWIDTH + QUARTERWIDTH,
                                              WINHEIGHT)
            VARIABLEDICT['rotation'] = 6
            redraw_window(VARIABLEDICT, RECTDICT, IMGDICT) # redraw window

# Redraw window
def redraw_window(VARIABLEDICT, RECTDICT, IMGDICT):
    
    DISPLAYSURF.blit(IMGDICT['background'], RECTDICT['background'])
    draw_wind(VARIABLEDICT, FONTDICT)
    write_info(VARIABLEDICT, FONTDICT)
    DISPLAYSURF.blit(IMGDICT['football'][VARIABLEDICT['rotation']],
                                         RECTDICT['football'])
    DISPLAYSURF.blit(IMGDICT['goal'], RECTDICT['goal'])
    if VARIABLEDICT['message'] > 0:
        DISPLAYSURF.blit(IMGDICT['message'], RECTDICT['message'])
    if VARIABLEDICT['gameOver']:
        DISPLAYSURF.blit(IMGDICT['quit'], RECTDICT['quit'])
        DISPLAYSURF.blit(IMGDICT['restart'], RECTDICT['restart'])
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
        
    # Temporary for Beta Version
    elif VARIABLEDICT['message'] == 10:
        IMGDICT['message'] = FONTDICT['titleTwo'].render('Game Over!', 1,
                                                         TITLETWOCOLOR)
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
    timeWrite = FONTDICT['default'].render('Time: {0:.1f}'.format(VARIABLEDICT['gameTime']),
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

    # GIVE ME A BREAK
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
    points = [(centerx - power * cos(angle),
              centery - power * sin(angle)),
              (centerx - power * cos(angle - pi / 4),
              centery - power * sin(angle - pi / 4)),
             (centerx - power * cos(angle + pi / 4),
              centery - power * sin(angle + pi / 4))]

    # Check if arrow exceeds power limit    
    if hypot(mousex - centerx,
             mousey - centery) > power:

        # Set a max x and y
        maxx = centerx - power * cos(angle)
        maxy = centery - power * sin(angle)

        points2 = [RECTDICT['football'].center, (maxx, maxy)]

    else:
        # Arrow does not exceed power limit        

        points2 = [RECTDICT['football'].center, (mousex, mousey)]
        
    # Draw arrowhead
    pg.draw.polygon(DISPLAYSURF, ARROWCOLOR, points)

    # Draw arrow shaft
    pg.draw.polygon(DISPLAYSURF, ARROWCOLOR, points2, 20)

    # Write power level next to arrow
    powerLvl = FONTDICT['default'].render(str(int(power)),
                                          1, DEFAULTFONTCOLOR)
    DISPLAYSURF.blit(powerLvl, (mousex - 50, mousey))

    pg.display.update()
    FPSCLOCK.tick(FPS)
    return

# Calculate ball trajectory and speed
def launch_ball(VARIABLEDICT, RECTDICT, IMGDICT):

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
            VARIABLEDICT['scoreOne'] += 10

        # Stem of goal post
        if center[0] <= RECTDICT['brickAreaOne'].right + radius:
            if center[1] < RECTDICT['brickAreaTwo'].top - radius\
               and center[1] >= RECTDICT['brickAreaOne'].top - radius:
                center = (RECTDICT['brickAreaOne'].right + radius, center[1])
                negative = -negative * FRICTION
                negative3 = -negative3
            elif center[1] >= RECTDICT['brickAreaTwo'].top - radius:
                # Ball collides with stem and base of goal post
                center = (RECTDICT['brickAreaOne'].right + radius,
                          RECTDICT['brickAreaOne'].top - radius)
                negative = -negative * FRICTION
                negative2 = -negative2 * FRICTION
                negative3 = -negative3
                
        # Right of base of goal post
        if center[0] <= RECTDICT['brickAreaTwo'].right + radius:
            if center[1] >= RECTDICT['brickAreaTwo'].top:
                center = (RECTDICT['brickAreaTwo'].right + radius, center[1])
                negative = -negative * FRICTION
                negative3 = -negative3
            if center[1] >= RECTDICT['brickAreaTwo'].top - radius:
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
        
    return

# Find center of object
def find_center(center, velocity, time):
    
    return (int(center[0] - velocity[0] * time),
            int(center[1] - velocity[1] * time))

# Draw wind arrow
def draw_wind(VARIABLEDICT, FONTDICT):

    # Initialize point of arrow
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

    # Display wind information (speed and angle)
    DISPLAYSURF.blit(winds, windsRect)
    DISPLAYSURF.blit(winda, windaRect)
    return

if __name__ == '__main__':
    initialize()
