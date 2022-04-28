#!/usr/bin/python3
# check main.py to see the problems with using this path

import pygame
import random
from images import image_handler
from sounds import sound_handler

# __init__() are the properties set for the objects
# def <name> are the methods which can be called in the class or by the object outside the class

class Charachter:
    """this class makes charachters adds hitboxes and draws them on the screen"""
    def __init__(self, WIDTH, HEIGHT, X_axis, Y_axis, IMAGE, window):
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.X_axis = X_axis
        self.Y_axis = Y_axis
        self.IMAGE = IMAGE
        self.window = window
    def hitbox(self): return pygame.Rect(self.X_axis, self.Y_axis, self.WIDTH, self.HEIGHT)
    def draw_charachter(self, hitbox): return self.window.blit(image_handler.output(self.IMAGE), (hitbox.x, hitbox.y))

class barrier(Charachter):
    """class to handle with the bases/barriers"""
    def __init__(self, WIDTH, HEIGHT, X_axis, Y_axis, IMAGE, window):
        # inheriting __init__ from charachter
        super().__init__(WIDTH, HEIGHT, X_axis, Y_axis, IMAGE, window)

class enemy(Charachter):
    """class to deal with enemies"""
    def __init__(self, enemy_list, WIDTH, HEIGHT, X_axis, Y_axis, IMAGE, window, speed, direction) -> None: #DETERMINE ENEMY TYPE IN MAIN
        # inheriting __init__ from charachter
        super().__init__(WIDTH, HEIGHT, X_axis, Y_axis, IMAGE, window)
        self.enemy_list = enemy_list
        self.speed = speed
        self.direction = direction
        # IMPORTANT: direction var must be kept here if handled by {def enemy_move()} it will constantly loop over it resetting its value to whatever was set originally

    def generator(self, amount, spacing):
        """spawns in charachters, inherits from Charachter class to make hitboxes and draw them on screen also adds them to a list"""
        for enemy in range(amount):
            # creating object by using inherited class and creates hitboxes for the objects
            enemy = Charachter(self.WIDTH, self.HEIGHT, self.X_axis, self.Y_axis, self.IMAGE, self.window).hitbox()
            self.enemy_list.append(enemy)
            self.X_axis += spacing
    def draw_generator(self, charachter):
        """places enemies in the list on to the screen"""
        return [charachter.draw_charachter(enemy) for enemy in self.enemy_list]

    def enemy_move(self, window_width, **other_enemy_lists):
        """deals with enemy movement from left to right and below"""
        for enemy in self.enemy_list:
            max_enemy_x = max(sorted(self.enemy_list)).x + self.WIDTH #moves enemy when it touches side of screen (max has WIDHT beacuse enemy x starts from its top left corner so min doesnt need it)
            min_enemy_x = min(sorted(self.enemy_list)).x

            # this if statement kickstarts enemy movement and handles their direction
            if self.direction == "right":
                enemy.x += self.speed
            elif self.direction == "left":
                enemy.x -= self.speed

            if max_enemy_x == window_width: #checks if highest enemy x num reacher to end of screen
                enemy.y += 10
                self.direction = "left"
            elif min_enemy_x == 0: #checks if lowest enemy x reached end of screen
                enemy.y += 10
                self.direction = "right"

    def probability(self):
        """probability counter to determine if ship laser can destroy enemy laser"""
        if self.enemy_laser['normal_laser']: #always returns true
            return True
        elif self.enemy_laser['fast_laser']: #1/2 chance to return true 
            chance = random.randint(0,2)
            if chance == 0:
                return True
        elif self.enemy_laser['wiglly_laser']: #1/3 chance to return true
            chance = random.randint(0,3)
            if chance == 0:
                return True
        else: #if laser is none of the above returns an error and stops the code
            raise Exception("wrong laser type entered")
    def enemy_laser(self):
        """handles enemy laser shooting"""
        pass

class projectile(enemy):
    """deals with projectiles"""
    lasers_list = []

    def __init__(self, ship, window, score, *lists, **enemy_lasers) -> None:
        self.window = window
        self.ship = ship
        self.score = score
        self.enemy_lasers = enemy_lasers
        self.lists = lists

    def handle_lasers(self, LASER_SPEED):
        """adds laser to screen, deals with its movement, and removes from list when an event occurs"""
        # the [:] before calling lists allows for chaning the lists more accurately
        for laser in self.lasers_list[:]:
            for laser in self.lasers_list: self.window.blit(image_handler.LASER, (laser)) #draws laser
            laser.y -= LASER_SPEED #moves laser
            if laser.y < 0: #destroy laser if it goes over the screen
                self.lasers_list.remove(laser)
            
            # if laser hits enemy or barrier destroy laser, kill enemy and ad appropriate score to player score
            for enemy in self.lists[0][:]:
                if laser.colliderect(enemy):
                    # removes hit enemy from list "killing" it
                    self.lists[0].remove(enemy)
                    # adds score
                    self.score += 10
                    # removes laser from list to make it usuable again
                    self.lasers_list.remove(laser)
                    # draws the explosion on enemy hitbox as an after death effect
                    Charachter(enemy.width, enemy.height, enemy.x, enemy.y, image_handler.EXPLOSION_PURPLE, self.window).draw_charachter(enemy)
            for enemy in self.lists[1][:]:
                if laser.colliderect(enemy):
                    self.lists[1].remove(enemy)
                    self.score += 10
                    self.lasers_list.remove(laser)
                    Charachter(enemy.width, enemy.height, enemy.x, enemy.y, image_handler.EXPLOSION_GREEN, self.window).draw_charachter(enemy)
            for enemy in self.lists[2][:]:
                if laser.colliderect(enemy):
                    self.lists[2].remove(enemy)
                    self.score += 10
                    self.lasers_list.remove(laser)
                    Charachter(enemy.width, enemy.height, enemy.x, enemy.y, image_handler.EXPLOSION_BLUE, self.window).draw_charachter(enemy)

    def shoot_lasers(self): #dependent on button press cant work at the same place with handle lasers
        """creates laser hitbox and adds it to a list"""
        if not self.lasers_list: #checks if the list is empty
            laser = pygame.Rect(self.ship.x + self.ship.width//2, self.ship.y + self.ship.height//2 - 7, 5, 15) # last numbedlers are width and height (theres a -7 to make bullet placement more accurate and so it doesnt show)
            self.lasers_list.append(laser)