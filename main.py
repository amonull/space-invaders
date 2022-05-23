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

def change_window(**hit_box):
    """draw sprites to screen"""
    WINDOW.blit(image_handler.BG_IMG,(0,0)) #always keep on top so images added later on are not behind background image
    hit_box['SHIP'].draw_charachter(hit_box['SHIP_HITBOX'], image_handler.SHIP) #adds ship to screen
    hit_box['ENEMY'].draw_generator(hit_box['ENEMY']) # draws enemies on screen
    enemy_laser, laser_type = hit_box['ENEMY_LASER'].handle_enemy_lasers(height, hit_box['LASER_TYPE'], hit_box['ENEMY_LASER_OBJECT']) # handles the enemy laser (draws it on screen handles deleting it)
    hit_box['LASERS'].handle_lasers(laser_speed, enemy_laser, laser_type, enemy_laser_list) #creates and handles lasers movement
    pygame.display.update()

def main(**sprites):
    """main function that runs the program"""
    SHIP_HITBOX = sprites['SHIP'].hitbox() # ship.hitbox() is not called in __name__="__main__" since it is also needed in change_window to call draw_charachter
    LASERS = charachters.projectile(SHIP_HITBOX, WINDOW, score, 5, 15) # LASER is here and not in __name__="__main__" since it needs to use the hitbox of the ship

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
            win_or_loss = sprites['ENEMY'].enemy_move(width, DEFAULT_WIDTH, current_time) # runs the function and puts the returned value into a variable

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
        

        change_window(LASERS=LASERS, SHIP=sprites['SHIP'], SHIP_HITBOX=SHIP_HITBOX, ENEMY=sprites['ENEMY'], ENEMY_LASER=ENEMY_LASER, LASER_TYPE=LASER_TYPE, ENEMY_LASER_OBJECT=ENEMY_LASER_OBJECT)
    #save_score.add_scores(str(LASERS.score)) # only runs when pygame is quit by pressing x button i dont know if i shoul add this as it would save user score before the game is officially finished (saves when user quits)
    pygame.quit() # quits pygame when out of loop

# start point of the program
if __name__ == "__main__":
    # [OBJECTS]
    SHIP = charachters.Charachter(DEFAULT_WIDTH, DEFAULT_HEIGHT, SHIP_X, SHIP_Y, WINDOW)

    ENEMY = charachters.enemy(DEFAULT_WIDTH, DEFAULT_HEIGHT, WINDOW, direction, enemy_blocks, enemy_speed)
    ENEMY.seperator()

    menu_run = True
    BUTTON_COLOR=DARK_BLUE
    while menu_run: # start screen is made this way and not with class menus due to this window having to use main function that has parameters. the menus class cannot handle arguments on button functions as of right now
        # creats new background image to overwrite anything underneath
        WINDOW.blit(image_handler.BG_IMG,(0,0))

        menu_text = font_handler.output(font_handler.SPACE_INVADERS_FONT, 60, "PLAY THE GAME", WHITE) # large menu text
        # the self.x an self.y calculations are done to ensure text is in the middle of the screen
        # the {menu_text.get_rect(center = self.window.get_rect().center).x} is used to find the center (X axis wise) part of the screen
        WINDOW.blit(menu_text, (menu_text.get_rect(center = WINDOW.get_rect().center).x, 40)) # places it on screen

        win_or_loss_text = font_handler.output(font_handler.SPACE_INVADERS_FONT, 45, "PLAY", WHITE)
        WINDOW.blit(win_or_loss_text, (win_or_loss_text.get_rect(center = WINDOW.get_rect().center).x, 120))

        basic_button1 = charachters.buttons(200, 85, 300, 375, WINDOW, font_handler.SPACE_INVADERS_FONT, button_colour=BUTTON_COLOR, text_colour=WHITE)
        # button text has vauge naming so i can use it for any menu anywhere and still match the name to the button
        basic_button1.draw(text="PLAY", outline=(0,0,0)) # outlines (0,0,0) is the colour black

        basic_button2 = charachters.buttons(200, 85, 300, 475, WINDOW, font_handler.SPACE_INVADERS_FONT, button_colour=BUTTON_COLOR, text_colour=WHITE)
        basic_button2.draw(text="HELP", outline=(0,0,0))

        for event in pygame.event.get():

            menu_run = False if event.type == pygame.QUIT else True

            # [BUTTON ACTIONS]
            if event.type == pygame.MOUSEBUTTONDOWN: # checks for mouse button click action
                if basic_button1.isHover():
                    # runs main function
                    main(SHIP=SHIP, ENEMY=ENEMY, MYSTERY='')
                if basic_button2.isHover():
                    webbrowser.open(f'{parent_path}/help.html')
            
            if event.type == pygame.MOUSEMOTION: # checks for mouse button hover action
                if basic_button1.isHover():
                    BUTTON_COLOR = (25,16,43) # if hovering on top of the button changes the colour to a light purple
                else:
                    BUTTON_COLOR = DARK_BLUE # this format of changing the colours was choosen as it was the easiest (if not hover changes the colour back to dark purple)

                if basic_button2.isHover():
                    BUTTON_COLOR = (25,16,43)
                else:
                    BUTTON_COLOR = DARK_BLUE

        pygame.display.update()
    pygame.quit()
    sys.exit() # sys.exit() needed to avoid {pygame.error: display Surface quit} error
