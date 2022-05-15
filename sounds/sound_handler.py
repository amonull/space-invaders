#!/usr/bin/env python
# ^-- uses this for python env instead of {#!/usr/bin/python} so it is more versitile and can be ran from CLI using a venv with correct modules (i.e. pygame)

import pygame
import pathlib # imported to find parent folder

file_path = pathlib.Path(__file__).parent.absolute()

pygame.mixer.init()
"""
ENEMY_MOVE1 = pygame.mixer.Sound(f'{file_path}/0.wav')
ENEMY_MOVE2 = pygame.mixer.Sound(f'{file_path}/1.wav') SOUND FOR ENEMY MOVEMENT NOT ADDED SINCE VOLUME CANNOT BE CONTROLED WITH THE WAY PYGAME HANDLES IT
ENEMY_MOVE3 = pygame.mixer.Sound(f'{file_path}/2.wav')
ENEMY_MOVE4 = pygame.mixer.Sound(f'{file_path}/3.wav')
"""
INVADER_DEATH = pygame.mixer.Sound(f'{file_path}/invaderkilled.wav')

MYSTERY_ENTER = pygame.mixer.Sound(f'{file_path}/mysteryentered.wav')
MYSTERY_KILL = pygame.mixer.Sound(f'{file_path}/mysterykilled.wav')

SHIP_EXPLOSION = pygame.mixer.Sound(f'{file_path}/shipexplosion.wav')

SHIP_SHOOT = pygame.mixer.Sound(f'{file_path}/shoot.wav')

# using default value so i only change it when i need to
output = lambda SOUND, VOLUME=0.5: SOUND.play().set_volume(VOLUME)
"""sets the volume for sounds and plays them"""