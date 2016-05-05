"""Evaluates the location information from the state in order to determine the state of origin of tweet"""

import re
import json
import os
import glob
import pandas as pd
import numpy as np


csv_file = 'fips_codes.csv'
df = pd.read_csv(csv_file)
state_name = df['State Name'].str.lower()
state_abbr = df['State Abbreviation'].str.lower()
alt_abbr = df['Alternate Abbreviation'].str.lower()
gu_name = df['GU Name'].str.lower()
super_tues = df['Super Tuesday']

# Active Files:
# path = r'C:\Election_Scripts\location_filtered'
# save_path = r'C:\Election_Scripts\location_filtered'

# Test Files:
path = r'C:\TUYR2\Election_Scripts\location_\test_'
save_path = r'C:\TUYR2\Election_Scripts\location_\test_'


def files_to_update(path):
    file_list = []
    for filename in glob.glob(os.path.join(path, '*.txt')):
        file_list.append(filename)
    return file_list


def createlist(tweet):
    location = []
    field_headers = [
        # 'place',
        'location',
        # 'coordinates',
    ]
    for field in field_headers:
        if tweet[field]:
            location.append(tweet[field])
            return location
        else:
            location.append('none')
            return location


def delimitlist(location):
    delimiters = '; |, |: |\*|,|:|;'
    for item in location:
        newlocation = re.split(delimiters, item)
        location = newlocation
        return location


def state(location):
    for i in location:
        focii = df.loc[
            (
                (state_name == i.lower()) |
                (state_abbr == i.lower()) |
                (alt_abbr == i.lower())
            ), 'State Abbreviation'
        ].unique()
        if focii:
            relevant_state = df.loc[
                (state_abbr == focii[0].lower()), 'Super Tuesday'
            ].unique()
            if relevant_state:
                return focii, relevant_state.astype(np.int32)
            else:
                relevant_state = [0]
                return focii, relevant_state
    if not focii:
        focii = [None]
        relevant_state = [None]
        return focii, relevant_state

file_list = files_to_update(path)

for filename in file_list:
    basefile = os.path.splitext(filename)[0]
    print(basefile)
    with open(filename, 'r') as thefile:
        for line in thefile:
            tweet = json.loads(line)
            location = createlist(tweet)
            newlocation = delimitlist(location)
            state_abbrev, super_tuesday_state = state(newlocation)
            new_fields = {
                'State': state_abbrev[0],
                'Super_Tuesday': super_tuesday_state[0],
            }
            tweet.update(new_fields)

            # Output Type: Single File
            # if state_abbrev[0]:
            #     revised_filepath = os.path.join(
            #         basefile + 'state__' + '.txt'
            #     )
            #     with open(revised_filepath, 'a') as nf:
            #         json.dump(tweet, nf)
            #         nf.write('\n')

            # Output Type: Multple File, by state
            if state_abbrev[0]:
                revised_filepath = os.path.join(
                    basefile + state_abbrev[0] + '.txt'
                )
                with open(revised_filepath, 'a') as nf:
                    json.dump(tweet, nf)
                    nf.write('\n')
