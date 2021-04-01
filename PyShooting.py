import pygame
import sys
import random
from time import sleep

BLACK = (0,0,0)
padWidth = 480      # screen width
padHeight = 640     # schreen height
rockImage = ['./img/rock01.png', './img/rock02.png', './img/rock03.png', './img/rock04.png', './img/rock05.png',\
             './img/rock06.png', './img/rock07.png', './img/rock08.png', './img/rock09.png', './img/rock10.png',\
             './img/rock11.png', './img/rock12.png', './img/rock13.png', './img/rock14.png', './img/rock15.png',\
             './img/rock16.png', './img/rock17.png', './img/rock18.png', './img/rock19.png', './img/rock20.png',\
             './img/rock21.png', './img/rock22.png', './img/rock23.png', './img/rock24.png', './img/rock25.png',\
             './img/rock26.png', './img/rock27.png', './img/rock28.png', './img/rock29.png', './img/rock30.png']
explosionSound = ['./sound/explosion01.wav', './sound/explosion02.wav', './sound/explosion03.wav','./sound/explosion04.wav']

# destroyed rock count
def writeScore(count):
    global gamePad
    font = pygame.font.Font('./font/NanumGothic.ttf', 20)
    text = font.render('destroyed rock:' + str(count), True, (255, 255, 255))
    gamePad.blit(text, (10, 0))

# attack earth count
def writePassed(count):
    global gamePad
    font = pygame.font.Font('./font/NanumGothic.ttf', 20)
    text = font.render('passed rock:' + str(count), True, (255, 0, 0))
    gamePad.blit(text, (345, 0))

def writeMessage(text):
    global gamePad, gameOverSound
    textfont = pygame.font.Font('./font/NanumGothic.ttf', 80)
    text = textfont.render(text, True,(255,0,0))
    textpos = text.get_rect()
    textpos.center = (padWidth/2, padHeight/2)
    gamePad.blit(text, textpos)
    pygame.display.update()
    pygame.mixer.music.stop()   # pause background sound
    gameOverSound.play()        # play gameover sound
    sleep(2)
    pygame.mixer.music.play(-1) # play background sound
    runGame()

def crash():
    global gamePad
    writeMessage("FLIGHT DESTORYED!")

def gameOver():
    global gamePad
    writeMessage("GAME OVER :(")

def drawObject(obj, x, y):
    global gamePad
    gamePad.blit(obj, (x, y))


def initGame():
    global gamePad, clock, background, fighter, missile, explosion, missileSound, gameOverSound
    pygame.init()
    gamePad = pygame.display.set_mode((padWidth, padHeight)) # screen size set
    pygame.display.set_caption('PyShooting')                 # name of game
    background = pygame.image.load('./img/background.png')         # background image
    fighter = pygame.image.load('./img/fighter.png')               # fighter image
    missile = pygame.image.load('./img/missile.png')               # missile image
    explosion = pygame.image.load('./img/explosion.png')           # explosion image
    pygame.mixer.music.load('./sound/music.wav')                     # background sound
    pygame.mixer.music.play(-1)                              # play background sound
    missileSound = pygame.mixer.Sound('./sound/missile.wav')         # missile sound
    gameOverSound = pygame.mixer.Sound('./sound/gameover.wav')       # game over sound
    clock = pygame.time.Clock()

def runGame():
    global gamePad, clock, background, fighter, missile, explosion, missileSound, gameOverSound
    # size of fighter
    fighterSize = fighter.get_rect().size
    fighterWidth = fighterSize[0]
    fighterHeight = fighterSize[1]

    # init pos of fighter (x,y)
    x = padWidth * 0.45
    y = padHeight * 0.9
    fighterX = 0

    # missile pos list
    missileXY = [];

    # get rock random
    rock = pygame.image.load(random.choice(rockImage))
    rockSize = rock.get_rect().size             # rock size
    rockWidth = rockSize[0]
    rockHeight = rockSize[1]
    destroyedSound = pygame.mixer.Sound(random.choice(explosionSound))

    # init pos of rock
    rockX = random.randrange(0, padWidth - rockWidth)
    rockY = 0
    rockSpeed = 2

    # when rock hit by fighter missile
    isShot = False
    shotCount = 0
    rockPassed = 0
    
    onGame = False
    while not onGame:
        for event in pygame.event.get():
            if event.type in [pygame.QUIT]:     # quit game prog
                pygame.quit()
                sys.exit()

            if event.type in [pygame.KEYDOWN]:      # press key
                if event.key == pygame.K_LEFT:      # move fighter left
                    fighterX -= 5;
                elif event.key == pygame.K_RIGHT:   # move fighter right
                    fighterX += 5;
                elif event.key == pygame.K_SPACE:   # shooting missile
                    missileSound.play()             # missile sound
                    missileX = x + fighterWidth/2
                    missileY = y - fighterHeight/2
                    missileXY.append([missileX, missileY])

            if event.type in [pygame.KEYUP]:    # not press key stop
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    fighterX = 0
                

        drawObject(background, 0, 0)    # draw background

        # reposition fighter position
        x += fighterX
        if x < 0:
            x = 0
        elif x > padWidth - fighterWidth:
            x = padWidth - fighterWidth

        # check fighter hit with rock
        if y < rockY + rockHeight:
            if (rockX > x and rockX < x + fighterWidth) or \
               (rockX + rockWidth > x and rockX + rockWidth < x + fighterWidth):
                crash()
        
        
        drawObject(fighter, x, y)       # draw fifghter at (x,y)
        
        
        # draw missile
        if len(missileXY) != 0:
            for i, bxy in enumerate(missileXY):
                bxy[1] -= 10        # move missile up 10 (y -= 10)
                missileXY[i][1] = bxy[1]

                # when rock hits missile
                if bxy[1] < rockY:
                    if bxy[0] > rockX and bxy[0] < rockX + rockWidth:
                        missileXY.remove(bxy)
                        isShot = True
                        shotCount += 1
                        
                if bxy[1] <= 0:     # missile is out of screen
                    try:
                        missileXY.remove(bxy)
                    except:
                        pass
            if len(missileXY) != 0:
                for bx, by in missileXY:
                    drawObject(missile, bx, by)

        # destroyed rock count
        
        writeScore(shotCount)
        
        rockY += rockSpeed          # rock is moving down

        # When the rock falldown to earth
        if rockY > padHeight:
            # create new rock(random)
            rock = pygame.image.load(random.choice(rockImage))
            rockSize = rock.get_rect().size
            rockHeight = rockSize[1]
            rockX = random.randrange(0, padWidth - rockWidth)
            rockY = 0
            rockPassed += 1

        if rockPassed == 3:
            gameOver()
                    
        # missed number of rock
        writePassed(rockPassed);
        
        if isShot:
            # explosion rock
            drawObject(explosion, rockX, rockY)
            destroyedSound.play()
            # create new rock(random)
            rock = pygame.image.load(random.choice(rockImage))
            rockSize = rock.get_rect().size
            rockHeight = rockSize[1]
            rockX = random.randrange(0, padWidth - rockWidth)
            rockY = 0
            destroyedSound = pygame.mixer.Sound(random.choice(explosionSound))
            isShot = False
            rockSpeed += 0.2
            if rockSpeed >= 10:
                rockSpeed = 10;
        

        drawObject(rock, rockX, rockY)  # draw rock
        
        pygame.display.update()         # redraw game screen

        clock.tick(60)                  # frame number per sec = 60

    pygame.quit()   # quit pygame

initGame()
runGame()
