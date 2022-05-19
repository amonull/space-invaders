#!/usr/bin/env python
# ^-- uses this for python env instead of {#!/usr/bin/python} so it is more versitile and can be ran from CLI using a venv with correct modules (i.e. pygame)

import pygame # imported for the game itself
import numpy as np # imported for bunkers to use a matrix
import random # imported to calculate probability
import sys # imported to correctly exit game
from images import image_handler
from sounds import sound_handler
from fonts import font_handler

# __init__() are the properties set for the objects
# def <name> are the methods which can be called in the class or by the object outside the class
# classes are created to create objects

class Charachter:
    """this class makes charachters adds hitboxes and draws them on the screen"""
    # the {-> None} is an annotation to tell others this function returns a NoneType does nothing for the code
    def __init__(self, WIDTH, HEIGHT, X_axis, Y_axis, window) -> None:
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.X_axis = X_axis
        self.Y_axis = Y_axis
        self.window = window
    def hitbox(self): return pygame.Rect(self.X_axis, self.Y_axis, self.WIDTH, self.HEIGHT)
    """creates a hitbox for objects"""
    def draw_charachter(self, hitbox, IMAGE): return self.window.blit(image_handler.output(IMAGE, self.WIDTH, self.HEIGHT), (hitbox.x, hitbox.y))
    """draws objects on to the screen based on their hitboxs"""

class bunker(Charachter):
    """class to handle with the bunkers"""
    def __init__(self, WIDTH, HEIGHT, X_axis, Y_axis, IMAGE, window) -> None:
        # inheriting __init__ from charachter
        super().__init__(WIDTH, HEIGHT, X_axis, Y_axis, IMAGE, window)

    def generate_matrix(self):
        pass

class enemy(Charachter):
    """class to deal with enemies"""

    # enemy is in a dict not a matrix so i can use its key to allocate an image automatically
    enemies = {'ENEMY_1': [],
                'ENEMY_2': [],
                'ENEMY_3': []}

    def __init__(self, WIDTH, HEIGHT, window, direction, moving_blocks, enemy_speed) -> None:
        # no super.__init__() used since i cannot use x and y axis on this in single object values
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.window = window
        self.direction = direction # IMPORTANT: direction var must be kept here if handled by {def enemy_move()} it will constantly loop over it resetting its value to whatever was set originally
        self.moving_blocks = moving_blocks
        self.enemy_speed = enemy_speed
        self.ENEMY_X = 80
        self.ENEMY1_Y = 220 # the large increase is to consider that enemey_2 will have 2 rows which will collide with enemy_1 if large gap is not there
        self.ENEMY2_Y = 100
        self.ENEMY3_Y = 40
        self.timer = pygame.time.get_ticks() # timer starts when object is created

    def generator(self, enemy_list, spacing, X_axis, Y_axis, row, col=1):
        """spawns in charachters, inherits from Charachter class to make hitboxes and draw them on screen also adds them to a list"""
        # the _ is a temp value and has no relevance or use
        for _ in range(col):
            for enemy in range(row):
                # creating object by using inherited class and creates hitboxes for the objects
                enemy = Charachter(self.WIDTH, self.HEIGHT, X_axis, Y_axis, self.window).hitbox()
                enemy_list.append(enemy)
                X_axis += spacing
            Y_axis += 60 # resets to default values so next row can be placed correctly
            X_axis = self.ENEMY_X
    def draw_generator(self, charachter):
        """places enemies in the list on to the screen"""
        def choose_image(var_image):
            """used to choose the correct image for the enemy"""
            # due to match case statement only works in python 3.10 and above
            match var_image: # using match case statement as in this case it is easier to use than if and elif
                case "ENEMY_1":
                    return image_handler.ENEMY_1
                case "ENEMY_2":
                    return image_handler.ENEMY_2
                case "ENEMY_3":
                    return image_handler.ENEMY_3

        # uses 2 loop comprehensions to make it easier to read and shorter to write (loops through first dict (to find keys) and then the lists that are found from the looped keys)
        # dict.items() gets the key and the items while dict.values() gets only the items
        return [[charachter.draw_charachter(enemy, choose_image(key)) for enemy in enemy_lists] for key, enemy_lists in self.enemies.items()]

    def seperator(self) -> None:
        """seperates enemies into classes"""
        # enemies are created here
        self.generator(self.enemies['ENEMY_1'], 55, self.ENEMY_X, self.ENEMY1_Y, 12, 2)
        self.generator(self.enemies['ENEMY_2'], 55, self.ENEMY_X, self.ENEMY2_Y, 12, 2)
        self.generator(self.enemies['ENEMY_3'], 55, self.ENEMY_X, self.ENEMY3_Y, 12)

    def enemy_move(self, window_width, DEFAULT_WIDTH, current_time) -> list:
        """deals with enemy movement from left to right and below"""
        # enemies are merged in a very simple way since it works, is easy to do and theres not many of it
        merged_list = self.enemies['ENEMY_1'] + self.enemies['ENEMY_2'] + self.enemies['ENEMY_3']
        max_enemy_x = max(sorted(merged_list)).x + DEFAULT_WIDTH
        min_enemy_x = min(sorted(merged_list)).x

        if (current_time-self.timer) > self.enemy_speed: # the timer function is from https://github.com/leerob/space-invaders/blob/master/spaceinvaders.py
        # iterates through dict (gets the list)
            for catagory in self.enemies.values():
                # iterates through lists
                for enemy in catagory:
                    if max_enemy_x >= window_width: #checks if highest enemy x num reacher to end of screen
                        enemy.y += 20
                        self.direction = "left"
                    elif min_enemy_x <= 0: #checks if lowest enemy x reached end of screen
                        enemy.y += 20
                        self.direction = "right"
                    # ***IMPORTANT:*** the if statemt above must stay above the if statement below changing the order will cause the first enemy on the list to be one tic faster than the rest in all lists

                    # this if statement kickstarts enemy movement and handles their direction
                    if self.direction == "right":
                        enemy.x += self.moving_blocks
                    elif self.direction == "left":
                        enemy.x -= self.moving_blocks

            self.timer += self.enemy_speed
                
        return merged_list

class mystery(Charachter):
    # inheriting __init__ from charachter
    def __init__(self, WIDTH, HEIGHT, X_axis, Y_axis, window, score) -> None:
        super().__init__(WIDTH, HEIGHT, X_axis, Y_axis, window)
        self.score = score
        self.timer = pygame.time.get_ticks()

    def spawn(self, current_time):
        # 25000 = 2 mins 5 secs
        if (current_time-self.timer) > 25000:
            pass
        # IMPORTATN: make sure you reset the timer so it can spawn again

    def score_porabability(self) -> int:
        """determines what score player can get"""
        probability = (0,4)
        # match-case statements are new in python added in 3.10
        match probability: # match-case statements were used since it is easier to write as i am only working with a single value
            case 0:
                return int(50)
            case 1:
                return int(100)
            case 2:
                return int(150)
            case 3:
                return int(200)
            case 4:
                return int(300)

    def __del__(self):
        """ran when object is destroyed"""
        # run using del {object}
        self.score += self.score_porabability()
        return self.score

# the ship laser is an object list since i had to make sure only one was on the screen at a time and had to check colisions repetedly and using a list for that was the easiest
# enemy is inherited so the dict enemies can be used and some of its function, inheriting enemy also inherits Charachter as enemy inherits Charachter
class projectile(enemy): # IMPORTANT: the ship laser is not created using Charachter class as it couldnt be called in 2 different functions without the hitbox but when created with the hitbox it couldnt call draw_charachter
    """deals with projectiles"""
    lasers_list = []

    def __init__(self, ship, window, score, laser_width, laser_height,) -> None:
        self.window = window
        self.ship = ship
        self.score = score
        self.laser_width = laser_width
        self.laser_height = laser_height

    def probability(self, enemy_laser) -> bool:
        """probability counter to determine if ship laser can destroy enemy laser"""

        match enemy_laser:
            case 'normal_laser': #always returns true
                return True
            case 'fast_laser': #1/2 chance to return true
                chance = random.randint(0,1)
                if not chance: # checks if value is 0
                    return True
            case 'wiggly_laser': #1/3 chance to return true
                chance = random.randint(0,2)
                if not chance: #checks if value is 0
                    return True

    def handle_lasers(self, LASER_SPEED, enemy_laser, laser_type, enemy_laser_list):
        """adds laser to screen, deals with its movement, and removes from list when an event occurs"""
        for laser in self.lasers_list:
            # [LASER OFF SCREEN]
            for laser in self.lasers_list: self.window.blit(image_handler.output(image_handler.LASER, self.laser_width, self.laser_height), (laser.x, laser.y)) #draws laser
            laser.y -= LASER_SPEED #moves laser
            if laser.y < 0: #destroy laser if it goes over the screen
                self.lasers_list.remove(laser)
            
            # [ENEMY COLLISON]
            for enemy_in_list in self.enemies['ENEMY_1']:
                if laser.colliderect(enemy_in_list):
                    # removes laser from list to make it usuable again
                    self.lasers_list.remove(laser) # IMPORTANT: sometimes a bug may occur where this command throws a value error (happens when laser hits 2 enemies at the same time) (avoided this issue by making gap between enemies larger) (can also be avoided by making the laser smaller or faster)
                    # adds score
                    self.score += 10
                    # draws the explosion on enemy hitbox as an after death effect
                    # it does it by calling inherited class to create an object again and only uses draw methods to use enemies hitbox to spawn it
                    Charachter(enemy_in_list.width, enemy_in_list.height, enemy_in_list.x, enemy_in_list.y, self.window).draw_charachter(enemy_in_list, image_handler.EXPLOSION_PURPLE)
                    sound_handler.output(sound_handler.INVADER_DEATH) #enemy death sound
                    # removes hit enemy from list "killing" it
                    self.enemies['ENEMY_1'].remove(enemy_in_list) # can access this list using self beacause of inheritance
            for enemy_in_list in self.enemies['ENEMY_2']:
                if laser.colliderect(enemy_in_list):
                    self.lasers_list.remove(laser)
                    self.score += 20
                    Charachter(enemy_in_list.width, enemy_in_list.height, enemy_in_list.x, enemy_in_list.y, self.window).draw_charachter(enemy_in_list, image_handler.EXPLOSION_BLUE)
                    sound_handler.output(sound_handler.INVADER_DEATH)
                    self.enemies['ENEMY_2'].remove(enemy_in_list)
            for enemy_in_list in self.enemies['ENEMY_3']:
                if laser.colliderect(enemy_in_list):
                    self.lasers_list.remove(laser)
                    self.score += 30
                    Charachter(enemy_in_list.width, enemy_in_list.height, enemy_in_list.x, enemy_in_list.y, self.window).draw_charachter(enemy_in_list, image_handler.EXPLOSION_GREEN)
                    sound_handler.output(sound_handler.INVADER_DEATH)
                    self.enemies['ENEMY_3'].remove(enemy_in_list)

            # [ENEMY LASER COLLISION]
            if laser.colliderect(enemy_laser): # checks if ship laser and enemy laser hit
                if self.probability(laser_type): # checks if return is True
                    enemy_laser_list.remove(enemy_laser) # removes enemy laser
                else:
                    try: # this error handling pass is very important it ensures that if both an enemy and a laser is hit at the same time with both returning to destroy ship laser it passes this one so enemy laser can continue but enemy is destroyed and no error comes up
                        self.lasers_list.remove(laser) # removes ship laser
                    except ValueError:
                        pass

            return laser

    def shoot_lasers(self): #dependent on button press cant work at the same place with handle lasers
        """creates laser hitbox and adds it to a list"""
        if not self.lasers_list: #checks if the list is empty
            laser = pygame.Rect(self.ship.x + self.ship.width//2, self.ship.y + self.ship.height//2 - 7, self.laser_width, self.laser_height) # last numbers are width and height (theres a -7 to make bullet placement more accurate and so it doesnt show)
            self.lasers_list.append(laser)
            sound_handler.output(sound_handler.SHIP_SHOOT) #shooting sound

class enemy_lasers(enemy): # the enemy laser is an object in a list and not a single object since it made interacting with the player and ship laser easier and didnt have to loop it to constantly create it in the main function in main.py
    """class to deal with enemy lasers"""

    def __init__(self, window, empty_list, width, height) -> None:
        self.window = window
        self.empty_list = empty_list
        self.width = width
        self.height = height

    def select_shooter(self) -> tuple:
        """selects the enemy to shoot and the laser type"""
        laser_types = ["normal_laser", "fast_laser", "wiggly_laser"]
        merged_list = enemy.enemies['ENEMY_1'] + enemy.enemies['ENEMY_2'] + enemy.enemies['ENEMY_3']
        return random.choice(merged_list), random.choice(laser_types) # chooses enemy and laser type on random

    def shoot(self) -> tuple:
        """creates the hitbox for the laser and makes it drawable"""
        enemy, laser_type = self.select_shooter() # chooses laser type and the enemy
        enemy_laser_object = Charachter(self.width, self.height, (enemy.x+(enemy.width/2)), enemy.y+(enemy.height), self.window) # creats laser object

        self.empty_list.append(enemy_laser_object.hitbox()) # places laser hitbox in list

        return laser_type, enemy_laser_object

    def handle_enemy_lasers(self, window_height, laser_type, enemy_laser_object) -> tuple:
        """handles everything to do with the laser"""
        def select_image(laser_type):
            """selects the correct image for laser"""
            match laser_type:
                case "normal_laser":
                    return image_handler.ENEMY_LASER
                case "fast_laser":
                    return image_handler.ENEMY_FAST_LASER
                case "wiggly_laser":
                    return image_handler.ENEMY_WIGLLY_LASER

        for laser in self.empty_list:
            laser.y += 2 # moves laser
            enemy_laser_object.draw_charachter(laser, select_image(laser_type)) # draws the laser
        # [ENEMY LASER off screen]
            if window_height < laser.y: # checks if laser is off screen
                self.empty_list.remove(laser) # removes laser
            return laser, laser_type

class buttons:
    """class to create buttons"""
    def __init__(self, width, height, X_axis, Y_axis, window, font, **colour) -> None:
        self.width = width
        self.height = height
        self.X_axis = X_axis
        self.Y_axis = Y_axis
        self.window = window
        self.font = font
        self.colour = colour
    # default values are used so the user doesn have to type in 0 or any value
    def draw(self, text=None, outline=None):
        """class to draw buttons on the screen"""
        if outline: #checks if outline should be enabled
            # outline value used as colour
            pygame.draw.rect(self.window, outline, (self.X_axis-2, self.Y_axis-2, self.width+4, self.height+4), 0) # creates another larger rectangle aroun button to function as an outline
        pygame.draw.rect(self.window, self.colour['button_colour'], (self.X_axis, self.Y_axis, self.width, self.height), 0)

        if text: # checks if theres a text to input
            button_text = font_handler.output(self.font, 15, text, self.colour['text_colour']) # text for button
            # places the text in the center of the button
            # using the center method i used in menu doesnt work as it misalignes text and button
            self.window.blit(button_text, (self.X_axis + (self.width/2 - button_text.get_width()/2), self.Y_axis + (self.height/2 - button_text.get_height()/2)))
    def isHover(self) -> bool:
        """checks if mouse is hovering over the button"""
        mouse_position_x, mouse_position_y = pygame.mouse.get_pos()
        if mouse_position_x > self.X_axis and mouse_position_x < self.X_axis + self.width:
            if mouse_position_y > self.Y_axis and mouse_position_y < self.Y_axis + self.height:
                return True
        return False

class menus(buttons):
    """class used to create menus/screens in the game to display things like winning screen or options"""
    def __init__(self, window, font, **colour) -> None:
        self.window = window
        self.font = font
        self.colour = colour

    def create_menu(self, func_button1, func_button2, **text):
        """function to create menus"""
        old_button_colour = self.colour['button1_colour']

        menu_run = True
        while menu_run:
            # creats new background image to overwrite anything underneath
            self.window.blit(image_handler.BG_IMG,(0,0))

            menu_text = font_handler.output(self.font, 60, text['main_text'], self.colour['text_colour']) # large menu text
            # the self.x an self.y calculations are done to ensure text is in the middle of the screen
            # the {menu_text.get_rect(center = self.window.get_rect().center).x} is used to find the center (X axis wise) part of the screen
            self.window.blit(menu_text, (menu_text.get_rect(center = self.window.get_rect().center).x, 40)) # places it on screen

            win_or_loss_text = font_handler.output(self.font, 45, text['win_or_loss'], self.colour['text_colour'])
            self.window.blit(win_or_loss_text, (win_or_loss_text.get_rect(center = self.window.get_rect().center).x, 120))

            basic_button1 = buttons(200, 85, 300, 375, self.window, self.font, button_colour=self.colour['button1_colour'], text_colour=self.colour['text_colour'])
            # button text has vauge naming so i can use it for any menu anywhere and still match the name to the button
            basic_button1.draw(text=text['button_text1'], outline=(0,0,0)) # outlines (0,0,0) is the colour black
    
            basic_button2 = buttons(200, 85, 300, 475, self.window, self.font, button_colour=self.colour['button2_colour'], text_colour=self.colour['text_colour'])
            basic_button2.draw(text=text['button_text2'], outline=(0,0,0))

            for event in pygame.event.get():

                menu_run = False if event.type == pygame.QUIT else True

                # [BUTTON ACTIONS]
                if event.type == pygame.MOUSEBUTTONDOWN: # checks for mouse button click action
                    if basic_button1.isHover():
                        func_button1()
                    if basic_button2.isHover():
                        func_button2()
                
                if event.type == pygame.MOUSEMOTION: # checks for mouse button hover action
                    if basic_button1.isHover():
                        self.colour['button1_colour'] = (25,16,43) # if hovering on top of the button changes the colour to a light purple
                    else:
                        self.colour['button1_colour'] = old_button_colour # this format of changing the colours was choosen as it was the easiest (if not hover changes the colour back to dark purple)

                    if basic_button2.isHover():
                        self.colour['button2_colour'] = (25,16,43)
                    else:
                        self.colour['button2_colour'] = old_button_colour

            pygame.display.update()
        pygame.quit()
        sys.exit() # sys.exit() needed to avoid {pygame.error: display Surface quit} error