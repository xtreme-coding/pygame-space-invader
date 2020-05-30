import pygame
import random
import math
from pygame import mixer

# initialize py game
pygame.init()

# create a screen
screen = pygame.display.set_mode((800, 600))

# background
background = pygame.image.load("background.png")

# background sound
mixer.music.load("background.wav")
mixer.music.play(-1)

# title and icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("ufo.png")
pygame.display.set_icon(icon)

# score
score = 0
score_font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

# game over text
over_font = pygame.font.Font('freesansbold.ttf', 64)

# player
playerImage = pygame.image.load("player.png")
playerX = 370
playerY = 525
playerX_change = 0

# enemy
enemyImage = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
numOfEnemy = 5
for i in range(numOfEnemy):
    enemyImage.append(pygame.image.load("enemy.png"))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(25, 200))
    enemyX_change.append(5)
    enemyY_change.append(40)

# bullet
# ready state - cant see bullet on screen
# fire - bullet currently moving
bulletImage = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"


def show_score(x, y):
    score_val = score_font.render("Score : " + str(score), True, (255, 255, 255))
    screen.blit(score_val, (x, y))


def gameOver_text():
    over_text = over_font.render("GAME OVER", True, (0, 255, 0))
    screen.blit(over_text, (200, 250))


def player(x, y):
    screen.blit(playerImage, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImage[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImage, (x + 16, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 30:
        return True
    else:
        return False


# game loop
running = True
while running:

    # background color of screen
    screen.fill((0, 0, 0))

    # background image adding
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # check keystroke is left or right
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -6

            if event.key == pygame.K_RIGHT:
                playerX_change = 6

            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound("laser.wav")
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # boundary of spaceship
    playerX += playerX_change

    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # boundary of enemy
    # enemy movement
    for i in range(numOfEnemy):

        # game over
        if enemyY[i] > 450:
            for j in range(numOfEnemy):
                enemyY[j] = 2000
            gameOver_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 5
            enemyY[i] += enemyY_change[i]

        elif enemyX[i] >= 736:
            enemyX_change[i] = -5
            enemyY[i] += enemyY_change[i]

        # collision

        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound("explosion.wav")
            explosion_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(25, 200)

        enemy(enemyX[i], enemyY[i], i)

    # bullet movement

    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()

pygame.quit()
