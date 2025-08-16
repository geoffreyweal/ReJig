"""
print_settings.py, Geoffrey Weal, 2/5/24

This method will print the current settings of ths `ReJig submit` module.
"""
import os

def print_settings(path_to_settings_txt_file):
    """
    This method will print the current settings of ths `ReJig submit` module.

    This works by printing the contents of the path_to_settings_txt_file file
    """
    print(f'No arguments have been passed through to the ReJig submit_jobs_to_slurm settings.')
    print(f'---------------------------------------------------------------------------------')
    print(f'Here are the current settings given in the file: {path_to_settings_txt_file}')
    print()
    with open(path_to_settings_txt_file, 'r') as FILE:
        for line in FILE:
            print(line.rstrip())
    print(f'---------------------------------------------------------------------------------')