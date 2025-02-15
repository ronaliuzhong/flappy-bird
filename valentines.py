# importing modules
import random
import sys
import pygame
from pygame.locals import *



# global variables for the game
window_width = 600
window_height = 500

# set height and width of window
window = pygame.display.set_mode((window_width, window_height))
elevation = window_height * 0.8
game_images = {}
framepersecond = 32
pipeimage = "C:\\Users\\yimin\\PycharmProjects\\pythonProject\\rainbowImages\\pipe.png"
rainbowBackground = "C:\\Users\\yimin\\PycharmProjects\\pythonProject\\rainbowImages\\rainbowBackground.jpg"
mufasaImage = "C:\\Users\\yimin\\PycharmProjects\\pythonProject\\rainbowImages\\mufasa.png"
sealevel_image = "C:\\Users\\yimin\\PycharmProjects\\pythonProject\\rainbowImages\\base.jfif"

your_score = 0

def flappygame():
    global your_score
    your_score = 0
    horizontal = int(window_width/5)
    vertical = int(window_width/2)
    ground = 0
    mytempheight = 100

    # generating two pipes
    first_pipe = createPipe()
    second_pipe = createPipe()

    # list containing lower pipes
    down_pipes = [
        {'x': window_width + 300 - mytempheight,
         'y': first_pipe[1]['y']},
        {'x': window_width+300-mytempheight+(window_width/2),
         'y': second_pipe[1]['y']}
    ]

    # list containing upper pipes
    up_pipes = [
        {'x': window_width + 300 - mytempheight,
         'y': first_pipe[0]['y']},
        {'x': window_width + 200 - mytempheight + (window_width/2),
         'y': second_pipe[0]['y']},
    ]

    # pipe velocity along x
    pipeVelX = -4

    bird_velocity_y = -9
    bird_Max_Vel_Y = 10
    bird_Min_Vel_Y = -8
    birdAccY = 1

    # velocity while flapping
    bird_flap_velocity = -8


    # only true when bird flapping
    bird_flapped = False
    while True:

        # handling the key events
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.type == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if vertical > 0:
                    bird_velocity_y = bird_flap_velocity
                    bird_flapped = True

        # this function will return true if the flappybird is crashed
        game_over = isGameOver(horizontal, vertical, up_pipes, down_pipes)
        if game_over:
            return

        if gameWin(your_score):
            gameWinScreen()

        # check for score
        playerMidPos = horizontal + game_images['character'].get_width() / 2
        for pipe in up_pipes:
            pipeMidPos = pipe['x'] + game_images['pipeimage'][0].get_width() / 2
            if pipeMidPos <= playerMidPos < pipeMidPos + 4:
                your_score += 1
                print(f'Your score is {your_score}')

        if bird_velocity_y < bird_Max_Vel_Y and not bird_flapped:
            bird_velocity_y += birdAccY

        if bird_flapped:
            bird_flapped = False
        playerHeight = game_images['character'].get_height()
        vertical = vertical + min(bird_velocity_y, elevation - vertical - playerHeight)

        # move pipes to the left
        for upperPipe, lowerPipe in zip(up_pipes, down_pipes):
            upperPipe['x'] += pipeVelX
            lowerPipe['x'] += pipeVelX

        # Add a new pipe when the first is about to cross the leftmost part of the screen
        if 0 < up_pipes[0]['x'] < 5:
            newpipe = createPipe()
            up_pipes.append(newpipe[0])
            down_pipes.append(newpipe[1])

        # if the pipe is out of the screen, remove it
        if up_pipes[0]['x'] < -game_images['pipeimage'][0].get_width():
            up_pipes.pop(0)
            down_pipes.pop(0)

        # lets blit our game images now
        window.blit(game_images['background'], (0, 0))
        for upperPipe, lowerPipe in zip(up_pipes, down_pipes):
            window.blit(game_images['pipeimage'][0],
                        (upperPipe['x'], upperPipe['y']))
            window.blit(game_images['pipeimage'][1],
                        (lowerPipe['x'], lowerPipe['y']))

        window.blit(game_images['sea_level'], (ground, elevation))
        window.blit(game_images['character'], (horizontal, vertical))

        # fetching the digits of score
        numbers = [int(x) for x in list(str(your_score))]
        width = 0

        # finding the width of score images from numbers
        for num in numbers:
            width += game_images['scoreimages'][num].get_width()
        Xoffset = (window_width - width)/1.1

        # blitting the images on the window
        for num in numbers:
                window.blit(game_images['scoreimages'][num], (Xoffset, window_width*0.02))
                Xoffset += game_images['scoreimages'][num].get_width()

        # refreshing the game window and displaying the score
        pygame.display.update()

        # set the framepersecond
        framepersecond_clock.tick(framepersecond)


def isGameOver(horizontal, vertical, up_pipes, down_pipes):

    # check if bird is above the sealevel
    if vertical > elevation - 25 or vertical < 0:
        return True

    # checking if bird hits the lower pipe or not
    for pipe in up_pipes:
        pipeHeight = game_images['pipeimage'][0].get_height()
        if (vertical < pipeHeight + pipe['y'] and abs(horizontal - pipe['x']) < game_images['pipeimage'][0].get_width()):
            return True

    # Checking if bird hits the lower pipe or not
    for pipe in down_pipes:
        if (vertical + game_images['character'].get_height() > pipe['y']) and abs(horizontal - pipe['x']) < game_images['pipeimage'][0].get_width():
            return True

    return False

def gameWin(your_score):
    return your_score >= 10

def gameWinScreen():
    valentineImage = pygame.image.load("C:\\Users\\yimin\\PycharmProjects\\pythonProject\\rainbowImages\\valentine.png").convert_alpha()
    background_image_size = (window_width, window_height)
    game_images['valentine'] = pygame.transform.scale(valentineImage, background_image_size)
    window.blit(game_images['valentine'], (0, 0))
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN:
                displayCelebration()

def displayCelebration():
    faceImage = pygame.image.load("C:\\Users\\yimin\\PycharmProjects\\pythonProject\\rainbowImages\\faces").convert_alpha()
    background_image_size = (window_width, window_height)
    game_images['beach'] = pygame.transform.scale(faceImage, background_image_size)
    game_images['beach'] = pygame.transform.rotate(game_images['beach'], 180)
    window.blit(game_images['beach'], (0, 0))

    font = pygame.font.Font('freesansbold.ttf', 32)
    text = font.render('YAYAYAYAYAAYAY', True, (255, 255, 255))
    textRect = text.get_rect()
    textRect.center = (window_width // 2, window_height // 2)
    window.blit(text, textRect)
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                return  # Exit screen when any key is pressed

def gameWin(score):
    return score >= 10

def createPipe():
    offset = window_height/3
    # so i think this is the top pipe
    pipeHeight = game_images['pipeimage'][0].get_height()

    # generating random height of pipes
    y2 = offset + random.randrange(
        0, int(window_height - game_images['sea_level'].get_height() - 1.2*offset))
    pipeX = window_width + 10
    y1 = pipeHeight - y2 + offset
    pipe = [
        # upper pipe
        {'x': pipeX, 'y': -y1},
        # lower pipe
        {'x': pipeX, 'y': y2}
    ]

    return pipe





# For initializing modules of pygame library
pygame.init()
framepersecond_clock = pygame.time.Clock()

# Load all the images which we will use in the game
# images for displaying score
# creates a dictionary where at key 'scoreimages' stores a tuple of images of scores
game_images['scoreimages'] = (
    pygame.image.load('C:\\Users\\yimin\\PycharmProjects\\pythonProject\\rainbowImages\\0.png').convert_alpha(),
    pygame.image.load("C:\\Users\\yimin\\PycharmProjects\\pythonProject\\rainbowImages\\1.png").convert_alpha(),
    pygame.image.load("C:\\Users\\yimin\\PycharmProjects\\pythonProject\\rainbowImages\\2.png").convert_alpha(),
    pygame.image.load("C:\\Users\\yimin\\PycharmProjects\\pythonProject\\rainbowImages\\3.png").convert_alpha(),
    pygame.image.load("C:\\Users\\yimin\\PycharmProjects\\pythonProject\\rainbowImages\\4.png").convert_alpha(),
    pygame.image.load("C:\\Users\\yimin\\PycharmProjects\\pythonProject\\rainbowImages\\5.png").convert_alpha(),
    pygame.image.load("C:\\Users\\yimin\\PycharmProjects\\pythonProject\\rainbowImages\\6.png").convert_alpha(),
    pygame.image.load("C:\\Users\\yimin\\PycharmProjects\\pythonProject\\rainbowImages\\7.png").convert_alpha(),
    pygame.image.load("C:\\Users\\yimin\\PycharmProjects\\pythonProject\\rainbowImages\\8.png").convert_alpha(),
    pygame.image.load("C:\\Users\\yimin\\PycharmProjects\\pythonProject\\rainbowImages\\9.png").convert_alpha()
)

# why did we initialize these images at the top? why couldn't we just initialize it here?
game_images['character'] = pygame.image.load(mufasaImage).convert_alpha()
game_images['sea_level'] = pygame.image.load(sealevel_image).convert_alpha()
game_images['background'] = pygame.image.load(rainbowBackground).convert_alpha()
# creates a tuple with a top pip and a bottom pipe
game_images['pipeimage'] = (pygame.transform.rotate(pygame.image.load(pipeimage).convert_alpha(), 180),
                            pygame.image.load(pipeimage).convert_alpha())

background_image_size = (window_width, window_height)
game_images['background'] = pygame.transform.scale(game_images['background'], background_image_size)
mufasa_image_size = (window_width // 7, window_height // 7)
game_images['character'] = pygame.transform.scale(game_images['character'], mufasa_image_size)

print('WELCOME TO THE FLAPPY BIRD GAME')
print('Press space to start the game')

# set height and width and title of window
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Rainbows!--get 10 to win")

# creating new icon
icon = pygame.image.load(
    "C:\\Users\\yimin\\PycharmProjects\\pythonProject\\rainbowImages\\rainbowheart.png").convert_alpha()
pygame.display.set_icon(icon)


def start_screen():
    window.fill((144, 238, 144))
    pygame.draw.rect(window, (255, 192, 203),  # rgb values
                     [window_width / 3, window_height / 3, window_width / 3, window_height / 5], 0)
    font = pygame.font.Font('freesansbold.ttf', 32)
    text = font.render('Press Space -- get 10 to win', True, (255, 255, 255))
    textRect = text.get_rect()
    textRect.center = (window_width // 2, window_height // 2)
    window.blit(text, textRect)
    pygame.display.update()


start_screen()
# idk the start screen doesn't work

# sets the coordinates of the flappy bird
horizontal = int(window_width/5)
vertical = int((window_height - (game_images['character'].get_height()))/2)

# for sealevel
ground = 0
while True:
    for event in pygame.event.get():

        # if user clicks on cross button or esc key, close the game
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            pygame.quit()

            # exit the program
            sys.exit()

        # If the user presses space or enter key, starts the game
        elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
            flappygame() # we will code the actual flappy game in a moment

        elif gameWin(your_score):
            gameWinScreen()

        # if user doesn't press any key, nothing happens
        else:
            # draws the surfaces
            window.blit(game_images['background'], (0,0))
            window.blit(game_images['character'], (horizontal, vertical))
            window.blit(game_images['sea_level'], (ground, elevation))

            # refreshes the screen
            pygame.display.update()

            # set the rate of frame per second
            # framepersecond_clock was the pygame.time.Clock() object that we created
            # we defined the framespersecond in a variable
            framepersecond_clock.tick(framepersecond)











