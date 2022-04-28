#!/usr/bin/python3

import pygame
import pathlib

file_path = pathlib.Path(__file__).parent.absolute()

SHIP = pygame.image.load(f"{file_path}/ship.png")
BARRIER = pygame.image.load(f"{file_path}/barrier.png")
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

output = lambda IMAGE: pygame.transform.scale(IMAGE, (50, 50))
