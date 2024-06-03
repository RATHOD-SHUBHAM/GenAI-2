import os
import shutil
import re

HOME = os.getcwd()


def deleteDirectory():
    # Specify the directory where you want to delete the folders
    directory = f'{HOME}/runs/detect'

    # Define a regex pattern to match folder names like predict, predict1, predict2, etc.
    pattern = re.compile(r'^predict\d*$')

    # Iterate over the items in the specified directory
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        # Check if the item is a directory and matches the pattern
        if os.path.isdir(item_path) and pattern.match(item):
            print(f'Deleting folder: {item_path}')
            # Remove the directory and its contents
            shutil.rmtree(item_path)

    print('Deletion complete.')
