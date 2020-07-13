# importing required modules
import subprocess
import sys,os
import urllib.request
def connect(host='http://google.com'):
    try:
        urllib.request.urlopen(host)
        return True
    except:
        return False
def install(package):
    if connect():
        print("Active Internet")
        if (input("Want to install pygame(Enter yes):")).lower() == "yes":
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    else:
        print("No internet!")
try:
    import pygame
except ModuleNotFoundError:
    install("pygame")
import random
pygame.mixer.init()
pygame.init()
#Setting up GameWindow
screen_width=900
screen_height=600
gameWindow = pygame.display.set_mode((screen_width, screen_height))
gameIcon = pygame.image.load('pyicon.jpg')
pygame.display.set_icon(gameIcon)
pygame.display.set_caption("SnakeGame")
pygame.display.update()
bgimg = pygame.image.load("snake.png")
gmimg = pygame.image.load("snwall.jpg")
# bgimg=pygame.transform.scale(bgimg, (screen_width, screen_height)).convert_alpha()
#colors
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
BLACK = (0,0,0)
AQUA = (0,255,255)
PURPLE = (128,0,128)
FUCHSIA = (255,0,255)
#clock and fonts
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 55)
if not os.path.exists("HIghScore.txt"):
    with open("HighScore.txt","w") as f:
        f.write("0")
        high_score = f.read()
        temp = int(high_score)
else:
    with open("HighScore.txt","r") as f:
        high_score = f.read()
        temp = int(high_score)
def welcome():
    exit_game = False
    while not exit_game:
        gameWindow.fill(AQUA)
        gameWindow.blit(bgimg,(0,0))
        text_screen("Welcome to Snakes", BLACK, 260, 250)
        text_screen("Press SPACE_BAR to play", PURPLE, 210, 300)
        text_screen("Press Esc to quit", FUCHSIA, 260, 350)
        for event in pygame.event.get():
            pygame.mixer.music.load("snake.mp3")
            pygame.mixer.music.play(10)
            if event.type == pygame.QUIT:
                exit_game = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pygame.mixer.music.pause()
                    gameloop()
                if event.key == pygame.K_ESCAPE:
                    exit_game = True
            pygame.display.update()
            clock.tick(60)
def text_screen(text, color, x, y):
    screen_text = font.render(text, True, color)
    gameWindow.blit(screen_text, (x,y))
def plot_snake(gameWindow, color, snk_list, snake_size):
    for x,y in snk_list:
        pygame.draw.rect(gameWindow, color, [x, y, snake_size, snake_size])
#Main GameLoops
def gameloop():
    #Game Variables
    game_over = False
    exit_game = False
    snake_x = 100
    snake_y = 100
    snake_size = 10
    init_vel = 5
    velocity_x = 0
    velocity_y = 0
    fps = 30
    food_x = random.randint(20, screen_width -100)
    food_y = random.randint(200, screen_height -100)
    food_size = 10
    score = 0
    snk_list = list()
    snk_len = 1
    # Main Loop
    while not exit_game:
        global high_score
        if game_over:
            gameWindow.fill(WHITE)
            gameWindow.blit(bgimg, (0,0))
            if score >temp:
                text_screen("New High Score=" + str(high_score), PURPLE, screen_width // 3, screen_height // 3 + 100)
                text_screen("Old High Score=" + str(temp), PURPLE, screen_width // 3, screen_height // 3 + 150)
                text_screen("Well Played", AQUA, screen_width // 3, screen_height // 3)
                with open("HighScore.txt", "w") as f:
                    f.write(str(score))
            else:
                text_screen("High Score=" + str(high_score), PURPLE, screen_width // 3, screen_height // 3 + 100)
                text_screen("Try Again", AQUA, screen_width // 3, screen_height // 3)
            text_screen("Game Over !", RED,  screen_width//4, screen_height//4)
            text_screen("Your Score="+str(score), GREEN, screen_width//3, screen_height//3+50)
            text_screen( "Press Enter to play Again", RED, screen_width//3, screen_height-200)
            text_screen("Press Esc to Exit  Game", BLUE, screen_width // 3, screen_height -100)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        gameloop()
                    if event.key == pygame.K_ESCAPE:
                        exit_game = True
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game=True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                       velocity_x = init_vel
                       velocity_y = 0
                    if event.key == pygame.K_LEFT:
                       velocity_x = -init_vel
                       velocity_y = 0
                    if event.key == pygame.K_DOWN:
                        velocity_y = init_vel
                        velocity_x = 0
                    if event.key == pygame.K_UP:
                        velocity_y = -init_vel
                        velocity_x = 0
            snake_x = snake_x + velocity_x
            snake_y = snake_y + velocity_y
            if abs(snake_x - food_x)<6 and abs(snake_y - food_y)<6:
                pygame.mixer.music.load("sn_jizz.mp3")
                pygame.mixer.music.play()
                score +=1
                food_x = random.randint(20, screen_width / 2)
                food_y = random.randint(20, screen_height / 2)
                snk_len += 1
                if score > int(high_score):
                    high_score = score
            gameWindow.fill(WHITE)
            gameWindow.blit(gmimg, (0,0))
            text_screen("SCORE:" + str(score)+"   High Score:"+str(high_score), BLACK, 5, 5)
            pygame.draw.rect(gameWindow, GREEN, [food_x, food_y, food_size, food_size])
            head=list()
            head.append(snake_x)
            head.append(snake_y)
            snk_list.append(head)
            if len(snk_list)>snk_len:
                del snk_list[0]
            if snake_x < 0 or snake_x > screen_width or snake_y < 0 or snake_y > screen_height:
                pygame.mixer.music.load("gameover.mp3")
                pygame.mixer.music.play()
                game_over=True
            if head in snk_list[:-1]:
                pygame.mixer.music.load("gameover.mp3")
                pygame.mixer.music.play()
                game_over = True
            plot_snake(gameWindow, RED, snk_list, snake_size)
        pygame.display.update()
        clock.tick(fps)
    pygame.quit()
    sys.exit()
if __name__ == '__main__':
    welcome()
