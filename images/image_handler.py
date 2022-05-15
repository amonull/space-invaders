#!/usr/bin/env python
# ^-- uses this for python env instead of {#!/usr/bin/python} so it is more versitile and can be ran from CLI using a venv with correct modules (i.e. pygame)

import pygame
import pathlib # imported to find parent folder

# path of file which this file is on
file_path = pathlib.Path(__file__).parent.absolute()

# gets images from path and loads them for pygame to use
SHIP = pygame.image.load(f"{file_path}/ship.png")
LASER = pygame.image.load(f"{file_path}/laser.png")
ENEMY_1 = pygame.image.load(f"{file_path}/enemy1_1.png")
ENEMY_2 = pygame.image.load(f"{file_path}/enemy2_1.png")
ENEMY_3 = pygame.image.load(f"{file_path}/enemy3_1.png")
MYSTERY_SHIP = pygame.image.load(f"{file_path}/mystery.png")
ENEMY_LASER = pygame.image.load(f"{file_path}/enemylaser.png")
ENEMY_WIGLLY_LASER = pygame.image.load(f"{file_path}/wigllylaser.png")
ENEMY_FAST_LASER = pygame.image.load(f"{file_path}/fastlaser.png")
EXPLOSION_BLUE = pygame.image.load(f"{file_path}/explosionblue.png")
EXPLOSION_GREEN = pygame.image.load(f"{file_path}/explosiongreen.png")
EXPLOSION_PURPLE = pygame.image.load(f"{file_path}/explosionpurple.png")
BG_IMG = pygame.image.load(f"{file_path}/background.jpg")

output = lambda IMAGE, WIDTH, HEIGHT: pygame.transform.scale(IMAGE, (WIDTH, HEIGHT))
"""takes the image and adjusts scale to make it fit the screen"""