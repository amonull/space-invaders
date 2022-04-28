#!/usr/bin/python3

import pygame
from pygame import mixer
import pathlib

file_path = pathlib.Path(__file__).parent.absolute()

mixer.init()

ship_shoot = pygame.mixer.Sound(f'{file_path}/shoot.wav')
enemy_shoot = pygame.mixer.Sound(f'{file_path}/shoot2.wav')
