import os
import sys
import glob
import re
import time
import shutil
from modules.tinytag import TinyTag


def main():
    args = get_arguments()
    confirm = input("Is the destination empty (required for FAT sorting) [y/n]?")
    if confirm == 'y':
        copy_full_directory(args['source'], args['destination'], args['source'])

def copy_full_directory(source, destination, source_directory):
    child_directories = get_all_subdirectories(source_directory)
    print('child_directories: ', child_directories)
    # Recursively copy child directories
    for child_directory in child_directories:
        # Concatenate directory names to form one flat directory for this folder
        destination_flat_dir = child_directory.replace(source_directory, '').replace(os.path.sep, ' - ')
        # Copy the music to the drive
        copy_fat_directory(child_directory, destination + destination_flat_dir)
    
def recursively_copy_directory_and_children(source, destination, source_directory):
    copy_fat_directory(source_directory, source_directory.replace(source, destination))
    # TODO: Option to convert nested directories into one flat level of directories & concatenate artist + album
    # 
    child_directories = get_all_subdirectories(source_directory)
    # Recursively copy child directories
    for child_directory in child_directories:
        print('Recursively copying: ', child_directory)
        recursively_copy_directory_and_children(source, destination, child_directory)

def get_arguments():
    args = {}
    source = sys.argv[1]
    destination = sys.argv[2]
    if os.path.exists(source) and os.path.exists(destination):
        args['source'] = source
        args['destination'] = destination
    return args

def get_all_subdirectories(path):
    directories = []
    for cur_path, subdirs, files in os.walk(path):
        directories.append(cur_path)
    return natural_sort(directories)

def get_immediate_subdirectories(path):
    directories = [f.path for f in os.scandir(path) if f.is_dir()]
    return natural_sort(directories)

def get_files(path):
    files = []
    globs = glob.glob(path + "/[!\.]*")
    for path in globs:
        if os.path.isfile(path):
            files.append(path)
    return files

def copy_fat_directory(source, destination):
    print('source: ', source)
    print('destination: ', destination)
    source_files = get_files(source)
    # print('source_files: ', source_files)
    # TODO: Option to primary sort by track number meta data, secondary by file name
    for source_file in source_files:
        tag = TinyTag.get(source_file)
        print(source_file, tag.track)
    sorted_source_files = natural_sort(source_files)
    for source_file_path in sorted_source_files:
        # Define destination file path
        destination_file_path = source_file_path.replace(source, destination)
        # Create directory if doesn't exist
        os.makedirs(os.path.dirname(destination_file_path), exist_ok=True)
        # Copy file
        print('Copying: ', source_file_path)
        shutil.copy(source_file_path, destination_file_path)
        # Iterate files with a 2.1s pause
        time.sleep(2.1)

def natural_track_sort(l):
    # TODO: 
    pass

def natural_sort(l): 
    convert = lambda text: int(text) if text.isdigit() else text.lower() 
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    return sorted(l, key = alphanum_key)
            
main()
