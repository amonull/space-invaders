#!/usr/bin/python3

import pathlib

# grabs the current path this directory is on
file_path = pathlib.Path(__file__).parent.absolute()

def add_scores(score):
    # opens file in append mode (w=overwrites x=creates file r=reades)
    with open(f'{file_path}/all_scores.txt', 'a') as file:
        # appends the score to file
        file.write(score)
        file.close()

def read_scores(): #returns the highest value in the scores file
    try:
        # attempts to open file in read mode
        with open(f'{file_path}/all_scores.txt', 'r') as file:
            all_scores = list(file.read())
            file.close()
        # sorts all items from the list
        all_scores.sort()
        try: 
            # gets the largest value in the list
            return all_scores[-1]
        except IndexError:
            print("no scores found in file... populating...")
            # no scores found to sort so populates file with value 0 to not interfere
            with open(f'{file_path}/all_scores.txt', 'w') as file:
                file.write('0')
                file.close()
    except FileNotFoundError:
        print("no file found... creating one...")
        # couldnt find file in path so creates one
        with open(f'{file_path}/all_scores.txt', 'x') as file:
            file.close()
