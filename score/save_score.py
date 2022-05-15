#!/usr/bin/env python
# ^-- uses this for python env instead of {#!/usr/bin/python} so it is more versitile and can be ran from CLI using a venv with correct modules (i.e. pygame)

import pathlib # imported to find parent folder

# grabs the current path this directory is on
file_path = pathlib.Path(__file__).parent.absolute()

# all_scores initially must be kept as empty string otherwise keeping it as list makes it split each charachter and keeping it as int gives ValueError
all_scores = str()

def add_scores(score):
    # opens file in append mode (w=overwrites x=creates file r=reades)
    with open(f'{file_path}/all_scores.txt', 'a') as file:
        # appends the score to file
        file.write(f"{score}\n")
        file.close()

def read_scores(): #returns the highest value in the scores file
    try:
        # attempts to open file in read mode
        with open(f'{file_path}/all_scores.txt', 'r') as file:
            # split is used to have all values in list without splitting them charachter by charachter or by the \n
            all_scores = file.read().split()
            # all values inside the list are converted into int()
            all_scores = [int(score) for score in all_scores]
            # sorts all items from the list
            all_scores.sort()
            file.close()
        try: 
            # gets the largest value in the list
            return str(all_scores[-1])
            # always returns as str() so pygame can use the value as string to place it on screen
        except IndexError:
            # issue happens when no value is inside the list which happens when the file is empty so value 0 is returned instead as a place holder. file is populated after player wins or looses
            return str(0)
            # returned as string for the same issue as before
    except FileNotFoundError:
        print("no file found... creating one...")
        # couldnt find file in path so creates one
        with open(f'{file_path}/all_scores.txt', 'x') as file:
            file.close()
