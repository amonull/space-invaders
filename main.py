#!/usr/bin/env python3.10
# ^-- uses this for python env instead of {#!/usr/bin/python} so it is more versitile and can be ran from CLI using a venv with correct modules (i.e. pygame)

# THE x AND y AXIS ARE HARD CODED
# ^-- to change the space inbetween enemy to enemy or barrier to barrier the new x axis must be calculated

import webbrowser #to open help guide
import pathlib
import pygame
import sys
from images import image_handler
from scores import save_score
from fonts import font_handler
import charachters

# gets the path of the parent directory
parent_path = pathlib.Path(__file__).parent.absolute()

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
DARK_BLUE = pygame.Color(10,0,21)

# defining how many frames per second the game updates at
FPS = 30

# constants and variables for overall functionality
ship_speed = 10
laser_speed = 30
enemy_blocks = 10
enemy_speed = 400
direction = "right" # attempted to do it by using 1 and 0 but it wouldnt work
DEFAULT_WIDTH, DEFAULT_HEIGHT = 40, 40
SHIP_X, SHIP_Y = 375, 520
BARRIER_X, BARRIER_Y = 175, 455

enemy_laser_list = []

# the {: str} is a function annotation it is intended to be look at by other to undertand this value is a string
# the {: str} doesnt actually do anything for python
def winning(score: str): # the charachters.menus is the screen while the nested functions are buttons
    """screen to come up when player wins"""
    #IMPORTANT: the next 2 functions cannot have any arguments as they cannot be passed through so it had to be duplicated (to losing) for it to be used without any difficulties
    def quit_with_save():
        save_score.add_scores(score)
        pygame.quit() # quits pygame
        sys.exit() # sys.exit must be added after pygame.quit if still inside the while loop in main.py to have a graceful and error free exit ({pygame.error: display Surface quit} error comes up otherwise)
    # pygame.quit() quits pygame while sys.exit() quits the program after pygame quits"""
    def quit_without_save():
        pygame.quit()
        sys.exit()
    charachters.menus(WINDOW, font_handler.SPACE_INVADERS_FONT, text_colour= WHITE, button1_colour=DARK_BLUE, button2_colour=DARK_BLUE).create_menu(quit_with_save, quit_without_save, main_text="Game Over", win_or_loss="You Won!", button_text1="Quit With Saving", button_text2="Quit Without Saving")
def losing(score: str):
    """screen to come up when the player looses"""
    def quit_with_save():
        save_score.add_scores(score)
        pygame.quit()
        sys.exit()
    def quit_without_save():
        pygame.quit()
        sys.exit()
    charachters.menus(score, WINDOW, font_handler.SPACE_INVADERS_FONT, text_colour= WHITE, button1_colour=DARK_BLUE, button2_colour=DARK_BLUE).create_menu(quit_with_save, quit_without_save, main_text="Game Over", win_or_loss="You Lost!", button_text1="Quit With Saving", button_text2="Quit Without Saving")

# used for a button so needs to be function
def open_html(): webbrowser.open(f'{parent_path}/help.html')

def change_window(**hit_box):
    """draw sprites to screen"""
    WINDOW.blit(image_handler.BG_IMG,(0,0)) #always keep on top so images added later on are not behind background image
    hit_box['SHIP'].draw_charachter(hit_box['SHIP_HITBOX'], image_handler.SHIP) #adds ship to screen
    hit_box['ENEMY'].draw_generator(hit_box['ENEMY']) # draws enemies on screen
    enemy_laser, laser_type = hit_box['ENEMY_LASER'].handle_enemy_lasers(height, hit_box['LASER_TYPE'], hit_box['ENEMY_LASER_OBJECT']) # handles the enemy laser (draws it on screen handles deleting it)
    hit_box['LASERS'].handle_lasers(laser_speed, enemy_laser, laser_type, enemy_laser_list) #creates and handles lasers movement
    pygame.display.update()

def main():
    """main function that runs the program"""
    # [OBJECTS]
    SHIP = charachters.Charachter(DEFAULT_WIDTH, DEFAULT_HEIGHT, SHIP_X, SHIP_Y, WINDOW)
    SHIP_HITBOX = SHIP.hitbox() # ship.hitbox() is not called in __name__="__main__" since it is also needed in change_window to call draw_charachter
    LASERS = charachters.projectile(SHIP_HITBOX, WINDOW, score, 5, 15) # LASER is here and not in __name__="__main__" since it needs to use the hitbox of the ship
    ENEMY = charachters.enemy(DEFAULT_WIDTH, DEFAULT_HEIGHT, WINDOW, direction, enemy_blocks, enemy_speed)
    ENEMY.seperator()

    clock = pygame.time.Clock()
    run = True

    # pygame runs on a forever loop untill the loop is false
    while run:
        current_time = pygame.time.get_ticks() # gets the current time (in ms) of the game
        clock.tick(FPS) # controls the speed of while loop
        for event in pygame.event.get():

            # [QUIT]
            run = False if event.type == pygame.QUIT else True # used to quit the game when x button is crossed

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
        
        # [ENEMY MOVEMENT AND WINNING AND LOSING DECISION]
        # moves enemy
        try:
            # the ValueError occurs at max_enemy_x variable on enemy_move i would perfer to handle it there just with the affected variables however then i would have a to find another way to find if the user won or not instead of just checking if the lists are empty and if they return an error when they are
            # not the optimal way to handle an error like this however this way of handling it instead of handling it enemy_move() function makes saving user score easier
            win_or_loss = ENEMY.enemy_move(width, DEFAULT_WIDTH, current_time) # runs the function and puts the returned value into a variable

            if max(sorted(win_or_loss)).y + DEFAULT_HEIGHT >= height: # check if player lost
                losing(LASERS.score)

        except ValueError: # occurs when player wins
            run = False
            # IMPORTANT: error occurs on {class: enemy} {function: enemy_move} {variable: max_enemy_x & min_enemy_x}
            # IMPORTANT: this gives value error when merged_list is empty (so when all enemies are dead) so use this try and expect to call a function to handle winnings
            winning(str(LASERS.score))

        # [ENEMY LASER SHOOT]
        if not enemy_laser_list:
            ENEMY_LASER = charachters.enemy_lasers(WINDOW, enemy_laser_list, 10, 15) # creates enemy laser object
            LASER_TYPE, ENEMY_LASER_OBJECT = ENEMY_LASER.shoot() # shoots the enemy laser when enemy laser list is empty
        

        change_window(LASERS=LASERS, SHIP=SHIP, SHIP_HITBOX=SHIP_HITBOX, ENEMY=ENEMY, ENEMY_LASER=ENEMY_LASER, LASER_TYPE=LASER_TYPE, ENEMY_LASER_OBJECT=ENEMY_LASER_OBJECT)
    #save_score.add_scores(str(LASERS.score)) # only runs when pygame is quit by pressing x button i dont know if i shoul add this as it would save user score before the game is officially finished (saves when user quits)
    pygame.quit() # quits pygame when out of loop

# start point of the program
if __name__ == "__main__":
    charachters.menus(WINDOW, font_handler.SPACE_INVADERS_FONT, text_colour= WHITE, button1_colour=DARK_BLUE, button2_colour=DARK_BLUE).create_menu(main, open_html, main_text="Spac Invaders", win_or_loss="Start Game", button_text1="Start", button_text2="Help")