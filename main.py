import random
import sys  # We use sys.exit to exit the program
import pygame
from pygame.locals import *

# Global variables for the game
FPS = 32
SCREENWIDTH = 850
SCREENHEIGHT = 650
SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
GROUND = SCREENHEIGHT
GAME_SPRITES = {}
GAME_SOUNDS = {}
PLAYER = 'gallery/sprites/bird.png'
BACKGROUND = 'gallery/sprites/background.png'
PIPE = 'gallery/sprites/pipe1.png'
HIGHSCORE = 0
pygame.init()
font = pygame.font.Font('freesansbold.ttf', 32)
white = (255,255,255)


def welcomeScreen(SCORE):
    plx = int(SCREENWIDTH - GAME_SPRITES['player'].get_width())/2
    ply = int(SCREENHEIGHT - GAME_SPRITES['player'].get_height())/2
    msgx = int(SCREENWIDTH - GAME_SPRITES['message'].get_width())/2
    msgy = int(SCREENHEIGHT - GAME_SPRITES['message'].get_height())/2 - 30
    basex = -1
    hstext = font.render(f"High Score : {HIGHSCORE}", True, white)
    stext = font.render(f"You Scored {SCORE}", True, white)
    scr_x = int(SCREENWIDTH - stext.get_width())/2
    scr_y = GROUND+100
    while 1:
        SCREEN.blit(GAME_SPRITES['background'], (0,0))
        SCREEN.blit(GAME_SPRITES['base'], (basex,GROUND))
        if SCORE != -1:
            SCREEN.blit(stext, (scr_x,scr_y))
        SCREEN.blit(hstext, (3,3))
        SCREEN.blit(GAME_SPRITES['message'], (msgx,msgy))
        SCREEN.blit(GAME_SPRITES['player'], (plx,ply))
        pygame.display.update()
        FPSCLOCK.tick(FPS)
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            
            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                return
                

def getRandomPipe():
    '''
    generate position of two pipes(one bottom straight & one top rotated) for blitting on the screen
    '''
    # Minimum distance b/w 2 pipes
    offset = SCREENHEIGHT/5
    
    # Distance from top to the base
    h = SCREENHEIGHT - GAME_SPRITES['base'].get_height()

    # Lower end of upper pipe
    y1 = random.randrange(int(SCREENHEIGHT/8),int(h - offset-5))
    
    # UPPER end of lower pipe
    y2 = y1 + offset    # This is the maximum height of the lower pipe
    y2 += random.randrange(h- y2-5)

    # Converting y1 into its upper length
    y1 -= GAME_SPRITES['pipe'][0].get_height()

    pipex = float(SCREENWIDTH + 5)
    pipe = [
        {'x': pipex, 'y' : y1},#upper pipe
        {'x': pipex, 'y': y2}#lower pipe
    ]
    return pipe


# Checks if the player collided or not
def iscollide(plx,ply,ups,lps):
    pipeheight = GAME_SPRITES['pipe'][0].get_height()
    for pipe in ups:
        if ply < pipeheight + pipe['y'] and pipe['x'] - GAME_SPRITES['player'].get_width()/1.2 < plx < pipe['x'] + GAME_SPRITES['pipe'][0].get_width():
            GAME_SOUNDS['hit'].play()
            return True

    for pipe in lps:
        if ply + GAME_SPRITES['player'].get_height() > pipe['y'] and pipe['x'] - GAME_SPRITES['player'].get_width()/1.2 < plx < pipe['x'] + GAME_SPRITES['pipe'][0].get_width():
            GAME_SOUNDS['hit'].play()
            return True
    return False


def mainGame():
    score = 0
    plx = int(SCREENWIDTH)/5
    ply = int(SCREENHEIGHT)/2
    basex = 0

    # Create two pipes for blitting on screen
    newp1 = getRandomPipe()
    newp2 = getRandomPipe()

    # My list of upper pipes
    ups = [
        {'x' : float(SCREENWIDTH + 5), 'y' : newp1[0]['y']},
        {'x' : float(SCREENWIDTH + 5 + (SCREENWIDTH/2)), 'y' : newp2[0]['y']} 
    ]

    # My list of lower pipes
    lps = [
        {'x' : float(SCREENWIDTH + 5), 'y' : newp1[1]['y']},
        {'x' : float(SCREENWIDTH + 5 + (SCREENWIDTH/2)), 'y' : newp2[1]['y']}
    ]


    # Defining some variables for the movement
    pipvelX = float(-5 )    # Pipe veclocity
    plyVelY = -9    # Player Velocity  
    plymaxvelY = 10 # Player max velocity
    plyAccY = 1     # Player acceleration while falling

    flpngV = -8    # velocity while flapping
    plyFlped = False    #True while flapping

    while 1:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if ply > 0:
                    plyVelY = flpngV
                    plyFlped = True
                    GAME_SOUNDS['wing'].play()

        
        crashTest = iscollide(plx,ply,ups,lps)
        if crashTest:
            return score

        #Checking score
        plymid = plx + GAME_SPRITES['player'].get_width()/2
        for pipe in ups:
            pipmid = pipe['x'] + GAME_SPRITES['pipe'][0].get_width()/2
            if pipmid <= plymid < pipmid-pipvelX:
                score+=1
                print(f"SCORE : {score}")
                GAME_SOUNDS['point'].play()

        if plyVelY < plymaxvelY and not plyFlped:
            plyVelY += plyAccY
        
        plyFlped = False
        
        playerheight = GAME_SPRITES['player'].get_height()
        ply += min(plyVelY, GROUND - ply - playerheight)

        #Moves pipes to the left
        for up, lp in zip(ups,lps):
            up['x'] += pipvelX
            lp['x'] += pipvelX


        #Add a new pipe
        if 0 < ups[0]['x'] < 6:
            newpipe = getRandomPipe()
            ups.append(newpipe[0])
            lps.append(newpipe[1])

        # removing pipe if it is out of the screen
        if ups[0]['x'] <= -GAME_SPRITES['pipe'][0].get_width():
            ups.pop(0)
            lps.pop(0)

        #Blitting the pipe
        SCREEN.blit(GAME_SPRITES['background'], (0,0))
        SCREEN.blit(GAME_SPRITES['player'], (plx, ply))
        for up,lp in zip(ups,lps):
            SCREEN.blit(GAME_SPRITES['pipe'][0], (up['x'], up['y']))
            SCREEN.blit(GAME_SPRITES['pipe'][1], (lp['x'], lp['y']))
        SCREEN.blit(GAME_SPRITES['base'], (basex, GROUND))
        
        mydigits = [int(x) for x in list(str(score))]
        width = 0
        for digits in mydigits:
            width += GAME_SPRITES['number'][digits].get_width()
        
        xoffset = (SCREENWIDTH - width)/2
        for digit in mydigits:
            SCREEN.blit(GAME_SPRITES['number'][digit], (xoffset, SCREENHEIGHT*0.12))
            xoffset += GAME_SPRITES['number'][digit].get_width()

        pygame.display.update()
        FPSCLOCK.tick(FPS)


if __name__ == '__main__':
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption("Flappy Bird by Rocko")
    GAME_SPRITES['number']= (
        pygame.image.load('gallery/sprites/0-Number-PNG.png').convert_alpha(),
        pygame.image.load('gallery/sprites/1-Number-PNG.png').convert_alpha(),
        pygame.image.load('gallery/sprites/2-Number-PNG.png').convert_alpha(),
        pygame.image.load('gallery/sprites/3-Number-PNG.png').convert_alpha(),
        pygame.image.load('gallery/sprites/4-Number-PNG.png').convert_alpha(),
        pygame.image.load('gallery/sprites/5-Number-PNG.png').convert_alpha(),
        pygame.image.load('gallery/sprites/6-Number-PNG.png').convert_alpha(),
        pygame.image.load('gallery/sprites/7-Number-PNG.png').convert_alpha(),
        pygame.image.load('gallery/sprites/8-Number-PNG.png').convert_alpha(),
        pygame.image.load('gallery/sprites/9-Number-PNG.png').convert_alpha(),
    )
    #Game Sprites
    GAME_SPRITES['message'] = pygame.image.load('gallery/sprites/message.png').convert_alpha()
    GAME_SPRITES['base'] = pygame.image.load('gallery/sprites/base.png').convert_alpha()
    GAME_SPRITES['background'] = pygame.image.load(BACKGROUND).convert()
    GAME_SPRITES['player'] = pygame.image.load(PLAYER).convert_alpha()
    
    GAME_SPRITES['pipe'] =(
        pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(), 180),
        pygame.image.load(PIPE).convert_alpha()
    )
    # global GROUND
    GROUND -= GAME_SPRITES['base'].get_height()

    #Game Sounds
    GAME_SOUNDS['die'] = pygame.mixer.Sound('gallery/audio/die.wav')
    GAME_SOUNDS['hit'] = pygame.mixer.Sound('gallery/audio/hit.wav')
    GAME_SOUNDS['wing'] = pygame.mixer.Sound('gallery/audio/wing.wav')
    GAME_SOUNDS['point'] = pygame.mixer.Sound('gallery/audio/point.wav')
    GAME_SOUNDS['swoosh'] = pygame.mixer.Sound('gallery/audio/swoosh.wav')
    try:
        with open("HIGHSCORE.txt",'r') as f:
            HIGHSCORE = int(f.read())

    except:
        with open("HIGHSCORE.txt","w") as f:
            f.write("0")

    welcomeScreen(-1)
    while 1:
        SCORE = mainGame()
        if SCORE > HIGHSCORE:
            HIGHSCORE = SCORE
            with open("HIGHSCORE.txt","w") as f:
                f.write(str(SCORE))
        welcomeScreen(SCORE)
