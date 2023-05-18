import pandas as pd
import numpy as np
import sys
import os
from sys import argv
pd.options.mode.chained_assignment = None  # default='warn'

"""
First step in behaviour pipeline. Creates reference files with filenames mapped to key parameter settings.

"""

# Must be run from within behaviour
OUTPUT_DIRECTORY = argv[1]

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))

print(OUTPUT_DIRECTORY)

file_list = [file[0] for file in os.walk(OUTPUT_DIRECTORY)]

result_df = pd.DataFrame()

# Loop through all files and get a table of results
for file_index in range(len(file_list)):

    filename = file_list[file_index]
    print(filename)

    if filename != OUTPUT_DIRECTORY:

        if os.path.isfile(filename+'/initialconditions.txt'):

            try:

                # Get df of initial conditions
                initial_conditions = pd.read_csv(filename+'/initialconditions.txt',header=None,delimiter=r"\s+")
                initial_conditions.columns = ['Parameter','Value']

                if not len(initial_conditions) == 28:
                    print("Initial conditions incomplete")

                else:

                    # Extract relevant information about the run
                    leader_k = initial_conditions.loc[initial_conditions['Parameter']=='leader_k'].values[0][1]
                    leader_autonomousMag = initial_conditions.loc[initial_conditions['Parameter']=='leader_autonomousMag'].values[0][1]
                    leader_De = initial_conditions.loc[initial_conditions['Parameter']=='leader_De'].values[0][1]

                    follower_k = initial_conditions.loc[initial_conditions['Parameter']=='follower_k'].values[0][1]
                    follower_autonomousMag = initial_conditions.loc[initial_conditions['Parameter']=='follower_autonomousMag'].values[0][1]
                    follower_De = initial_conditions.loc[initial_conditions['Parameter']=='follower_De'].values[0][1]

                    middle_zone_height = initial_conditions.loc[initial_conditions['Parameter']=='middle_zone_height'].values[0][1]


                    experimentType = initial_conditions.loc[initial_conditions['Parameter']=='experimentType'].values[0][1]

                    #print(num_leader_overtakes)

                    data = {
                            'leader_k': round(leader_k, 8),
                            'leader_De': round(leader_De, 8),
                            'leader_a': round(leader_autonomousMag, 8),
                            'follower_k': round(follower_k, 8),
                            'follower_De': round(follower_De, 8),
                            'follower_autonomousMag': round(follower_autonomousMag, 8),
                            'middle_zone_height': round(middle_zone_height, 8),
                            'experimentType': experimentType,
                            'filename': filename
                            }

                    run_output = pd.DataFrame(data, index=[0])

                    # Add individual simulation output to dataframe
                    result_df = result_df.append(run_output, sort=True)

            except FileNotFoundError:
                print("File not found")
                print(filename)
            except pd.errors.EmptyDataError:
                print("EmptyDataError")
                print(filename)
            except IndexError:
                print("IndexError")
                print(filename)
            except TypeError:
                print("TypeError")
                print(filename)
            except KeyError:
                print("KeyError")
                print(filename)

result_df.to_csv(CURRENT_DIR + '/behavioural_data/result_00_file_name_param_combos.csv')
