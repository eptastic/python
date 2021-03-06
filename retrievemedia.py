#!/usr/bin/env python3
"""
Media retrieval tool for my media server
"""
import os
import sys
import argparse

parser = argparse.ArgumentParser(
    description="Copies Movie and TV_Shows directories to shared network drive")
parser.add_argument('-d', '--test', action='store_true',
                    dest='testmode', help='use rsync dryrun')

group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('-M', '--4k', action='store_const', const='/thufir/plex_media/4k/',
                   dest='path', help='use 4k movie directory')

group.add_argument('-m', '--movies', action='store_const', const='/thufir/plex_media/movies/',
                   dest='path', help='use movie directory')


group.add_argument('-t', '--tv', action='store_const', const='/thufir/plex_media/tv_shows/',
                   dest='path', help='use tv shows directory')

arguments = parser.parse_args(sys.argv[1:])

source_dir = arguments.path

dest_dir = "/share/sietchtabr/"

# Get user input for media title
search_query = input("Media Title: ")

# Gets names of file in given path (source_dir)
directories = os.scandir(source_dir)

# A list to save the search result (search_query)
search_result = list()

# Checks through directories, if entry name contains search query, it is saved to search result (list)
# Search query and entry name is converted to lowercase to remove captalisation problems
for entry in directories:
    if search_query.lower() in entry.name.lower():
        search_result.append(entry)

# Prints readable list for user starting from 1 (because alex is fussy with indexing) and "-"
for index, title in enumerate(search_result):
    print(index+1, "-", title.name)

# Converted string user input (etc 1,2,3) into a number TO select media name
usr_select = int(input("Choose Number: "))-1

# Pulls selected media from list and splits file path based on "/"
result = search_result[usr_select].path.split("/")

# add "'" before and after last list item (media name)
result[-1] = result[-1].replace("'", "\\'").replace("(",
                                                    "\(").replace(")", "\)").replace(" ", "\ ")

# convert list into a file path with /
result = "/".join(result)

# define rsync command
if arguments.testmode:
    rsync_cmd = "sudo rsync -av --dry-run {} {}".format(result, dest_dir)
else:
    rsync_cmd = "sudo rsync -aP {} {}".format(result, dest_dir)

print("rsync_cmd: {}".format(rsync_cmd))

# Input rsync_cmd into system
os.system(rsync_cmd)
