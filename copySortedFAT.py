import os
import sys
import glob
import re
import time
import shutil
import functools
from modules.tinytag import TinyTag


def main():
    args = get_arguments()
    confirm = input("Is the destination empty (required for FAT sorting) [y/n]?")
    if confirm == 'y':
        copy_full_directory(args['source'], args['destination'], args['source'])

def copy_full_directory(source, destination, source_directory):
    child_directories = get_all_subdirectories(source_directory)
    # Recursively copy child directories
    for child_directory in child_directories:
        # Concatenate directory names to form one flat directory for this folder
        destination_flat_dir = child_directory.replace(source_directory, '').replace(os.path.sep, ' - ')
        # Copy the music to the drive
        copy_fat_directory(child_directory, destination + destination_flat_dir)
    
def recursively_copy_directory_and_children(source, destination, source_directory):
    copy_fat_directory(source_directory, source_directory.replace(source, destination))
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

def compare_by_track_natural(item1, item2):
    # Primary sort by track number meta data
    try:
        if TinyTag.get(item1).track is None and TinyTag.get(item2).track is not None:
            return 1
        elif TinyTag.get(item1).track is not None and TinyTag.get(item2).track is None:
            return -1
        elif TinyTag.get(item1).track is not None and TinyTag.get(item2).track is not None:
            if int(TinyTag.get(item1).track) > int(TinyTag.get(item2).track):
                return 1
            elif int(TinyTag.get(item1).track) < int(TinyTag.get(item2).track):
                return -1
            else:
                return 0
        else:
            # Secondary sort by file name (natural sort)
            sorted_list = natural_sort([item1, item2])
            if sorted_list[0] == item1:
                return -1
            else:
                return 1
    except:
        return -1

def sort_by_track_and_filename(source_files):
    return sorted(source_files, key=functools.cmp_to_key(compare_by_track_natural))

def copy_fat_directory(source, destination):
    print('copy_fat_directory: ', source, destination)
    source_files = get_files(source)
    if len(source_files) <= 0:
        return
    sorted_source_files = sort_by_track_and_filename(source_files)
    # exit()
    for source_file_path in sorted_source_files:
        # Define destination file path and use original file name
        destination_file_path = source_file_path.replace(source, destination)
        # Remove track number from file name
        try:
            if TinyTag.get(source_file_path).track is not None:
                track_characters = len(str(TinyTag.get(source_file_path).track))
                if (
                    os.path.basename(destination_file_path)[:track_characters + 1] == str(TinyTag.get(source_file_path).track) + ' '
                    or os.path.basename(destination_file_path)[:track_characters + 2] == '0' + str(TinyTag.get(source_file_path).track) + ' '
                ):
                    destination_file_path = os.path.dirname(destination_file_path) + os.path.sep + re.sub('^[0-9]+\s(\-\s)?', '', os.path.basename(destination_file_path))
        except:
            pass
        # Create directory if doesn't exist
        os.makedirs(os.path.dirname(destination_file_path), exist_ok=True)
        if not os.path.exists(destination_file_path):
            # Copy file
            print('Copying to: ', destination_file_path)
            shutil.copy(source_file_path, destination_file_path)
            # Iterate files with a 2.1s pause
            time.sleep(2.1)

def natural_sort(l): 
    convert = lambda text: int(text) if text.isdigit() else text.lower() 
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    return sorted(l, key = alphanum_key)
            
main()
