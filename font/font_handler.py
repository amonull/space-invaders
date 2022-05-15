#!/usr/bin/env python
# ^-- uses this for python env instead of {#!/usr/bin/python} so it is more versitile and can be ran from CLI using a venv with correct modules (i.e. pygame)

import pygame
import pathlib # imported to find parent folder

pygame.font.init()

file_path = pathlib.Path(__file__).parent.absolute()

# gets font from fonts folder so it can be used ingame
SPACE_INVADERS_FONT = f"{file_path}/space_invaders.ttf"

choose_font = lambda FONT, SIZE: pygame.font.Font(FONT, SIZE)
"""enables fonts to be used and the size of the font to be changed"""

output = lambda FONT, SIZE, TEXT, COLOUR: choose_font(FONT, SIZE).render(str(TEXT), True, COLOUR)
"""places text on the screen with the required font"""