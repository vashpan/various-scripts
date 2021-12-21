#!/bin/bash

# Renames and pushes a tag, removing old one.
#
# 1. After rename, you have to tell your colegues (or in your different repo copy) to run:
# 
# $ git pull --prune --tags
# 
# To avoid situation that old tags will be "re-pushed" again
# 
# 2. This script can be used in conjunction with some tags list to rename multiple tags together.
# 
# First, pipe tags to a text file (you can edit it to customize the list)
# 
# $ git tag > tags-to-rename.txt
#
# Then you can run script like that to process them:
# 
# !/usr/bin/fish
# for old_tag in (cat old-tags.txt)
#     set new_tag "release/$old_tag"
#     git_rename_tag.sh $old_tag $new_tag
# end
#

# check arguments
if [ "$#" -ne 2 ]; then
    echo "Illegal number of parameters."
    echo "Usage: git_rename_tag <old_tag_name> <new_tag_name>"
    exit 2
fi

# perform rename on current repo
TAG_OLD=$1
TAG_NEW=$2

echo "Renaming tag: ${TAG_OLD} to ${TAG_NEW}"

git tag ${TAG_NEW} ${TAG_OLD}
git tag -d ${TAG_OLD}
git push origin ${TAG_NEW} :${TAG_OLD}
