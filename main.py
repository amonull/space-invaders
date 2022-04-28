#!/usr/bin/python3
# this environemt path changes depending on where python path is on venv or on system

# THE x AND y AXIS ARE HARD CODED
# ^-- to change the space inbetween enemy to enemy or barrier to barrier the new x axis must be calculated
#to add more barrier more barrier_health variables must be added

import pygame
from images import image_handler
from sounds import sound_handler
from scores import save_score
import charachters

pygame.init() # safely initilizing all pygame modules

# [GENERAL] consts/vars
score = 0
hi_score = save_score.read_scores()

# [WINDOW]
width, height = 800, 600
WINDOW = pygame.display.set_mode((width, height))
pygame.display.set_caption("Space Invaders Game Project")

# [COLOURS]
BLACK = pygame.Color(0, 0, 0)
WHITE = pygame.Color(255, 255, 255)
RED = pygame.Color(255, 0, 0)
GREEN = pygame.Color(0, 255, 0)
BLUE = pygame.Color(0, 0, 255)

# defining how many frames per second the game updates at
FPS = 60

# objects/sprites and object attributes
# images/sounds/fonts gotten from https://github.com/leerob/space-invaders

# generating empty list for enemies
enemy1, enemy2, enemy3 = [], [], []
# keep barrirs in lists an attempt to change that to dict would result in unmutable barriers
barriers = []

# constants for overall functionality
ship_speed = 3
enemy_speed = 1
laser_speed = 5
DEFAULT_WIDTH, DEFAULT_HEIGHT = 50, 50
SHIP_X, SHIP_Y = 375, 520
BARRIER_X, BARRIER_Y = 175, 455
ENEMY1_X, ENEMY1_Y = 35, 375
ENEMY2_X, ENEMY2_Y = 35, 300
ENEMY3_X, ENEMY3_Y = 35, 225
direction = "right"


def change_window(**hit_box):
    """adds sprites to screen"""
    WINDOW.blit(image_handler.BG_IMG,(0,0)) #always keep on top so images added later on are not behind background image
    hit_box['SHIP'].draw_charachter(hit_box['SHIP_HITBOX']) #adds ship to screen
    hit_box['LASERS'].handle_lasers(laser_speed) #creates and handles lasers movement
    hit_box['ENEMY1'].draw_generator(hit_box['ENEMY1']) #***IMPORTANT*** enemy dying animation too quick try to add here and destroy when a func is run
    hit_box['ENEMY2'].draw_generator(hit_box['ENEMY2'])
    hit_box['ENEMY3'].draw_generator(hit_box['ENEMY3'])
    pygame.display.update()

def endgame_screen():
    """sceen to come up when the player wins or looses"""
    pass

def main(**sprites):
    """main function that runs the program"""
    SHIP_HITBOX = sprites['SHIP'].hitbox()
    LASERS = charachters.projectile(SHIP_HITBOX, WINDOW, score, enemy1, enemy2, enemy3, barriers, normal_laser=0, fast_laser=0, wiglly_laser=0) #might not work because of the way hitbox is made (doesnt return anything dontknow whether it can access x, y and width, height)

    clock = pygame.time.Clock()
    run = True

    # pygame runs on a forever loop untill the loop is false
    while run:
        clock.tick(FPS) # controls the speed of while loop
        for event in pygame.event.get():

            # [QUIT]
            run = False if event.type == pygame.QUIT else True # sets run to False which kills the while loop ending the game

            # [SHOOT]
            if event.type == pygame.KEYDOWN: #shoots ships bullets
                if event.key == pygame.K_SPACE:
                    LASERS.shoot_lasers()
                elif event.key == pygame.K_RCTRL: #added in so you can move and shoot with one hand
                    LASERS.shoot_lasers()

        # [MOVEMENT]
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and SHIP_HITBOX.x - ship_speed > 0: # [LEFT] checks to make sure charachter hitbox wont go off screen
            SHIP_HITBOX.x -= ship_speed
        elif keys[pygame.K_RIGHT] and SHIP_HITBOX.x + ship_speed + DEFAULT_WIDTH < width: # [RIGHT]
            SHIP_HITBOX.x += ship_speed
        
        # [ENEMY MOVEMENT]
        sprites['ENEMY1'].enemy_move(width)
        sprites['ENEMY2'].enemy_move(width)
        sprites['ENEMY3'].enemy_move(width)

        change_window(LASERS=LASERS, SHIP=sprites['SHIP'], SHIP_HITBOX=SHIP_HITBOX, ENEMY1=sprites['ENEMY1'], ENEMY2=sprites['ENEMY2'], ENEMY3=sprites['ENEMY3'])
    pygame.quit() # cant quit by pressing red X without this line or the if statement above

# start point of the program
if __name__ == "__main__":
    # [OBJECTS]
    SHIP = charachters.Charachter(DEFAULT_WIDTH, DEFAULT_HEIGHT, SHIP_X, SHIP_Y, image_handler.SHIP, WINDOW)
    #BARRIER = charachters.multiple_charachters(barriers, DEFAULT_WIDTH, DEFAULT_HEIGHT, BARRIER_X, BARRIER_Y, image_handler.BARRIER, WINDOW)

    ENEMY1 = charachters.enemy(enemy1, DEFAULT_WIDTH, DEFAULT_HEIGHT, ENEMY1_X, ENEMY1_Y, image_handler.ENEMY_1, WINDOW, enemy_speed, direction)
    ENEMY1.generator(11, 65) 
    ENEMY2 = charachters.enemy(enemy2, DEFAULT_WIDTH, DEFAULT_HEIGHT, ENEMY2_X, ENEMY2_Y, image_handler.ENEMY_2, WINDOW, enemy_speed, direction)
    ENEMY2.generator(11, 65)
    ENEMY3 = charachters.enemy(enemy3, DEFAULT_WIDTH, DEFAULT_HEIGHT, ENEMY3_X, ENEMY3_Y, image_handler.ENEMY_3, WINDOW, enemy_speed, direction)
    ENEMY3.generator(11, 65)

    main(SHIP=SHIP, ENEMY1=ENEMY1, ENEMY2=ENEMY2, ENEMY3=ENEMY3, MYSTERY='')
