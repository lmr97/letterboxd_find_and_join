# This script updates the watched.csv file from Letterboxd with genre tags

import pandas as pd
import math
import letterboxdfinders as lbf

load_bar_width_total = 50

def print_centered_msg(msg):
    print()
    print(math.ceil(2+(load_bar_width_total-len(msg))/2) * "-", 
          msg, 
          math.ceil(2+(load_bar_width_total-len(msg))/2) * "-")


# load data
print_centered_msg("Loading data...")
watched = pd.read_csv("./letterboxd-dialectica972/watched.csv")
num_rows = len(watched.index)

# test_subset = watched.head(13).copy()
# num_rows = len(test_subset.index)
# print_centered_msg("Main Genre column writing started...")
# test_subset.loc[:, "Main Genre"] = test_subset.groupby(test_subset.index).apply(
#     lambda x: get_nth_genre(x, n=0))
# print_centered_msg("Main Genre column added!")
# test_subset.to_csv("./letterboxd-dialectica972/watched_with_genres_test.csv")
# exit()


# add columns
print_centered_msg("Main Genre column writing started...")
watched.loc[:, "Main Genre"] = watched.groupby(watched.index).apply(
    lambda x: lbf.get_nth_genre(x, n=0, 
                            bar_width=load_bar_width_total, 
                            total_rows=num_rows))
print_centered_msg("Main Genre column added!")

print_centered_msg("Secondary Genre column writing started...")
watched.loc[:, "Secondary Genre"] = watched.groupby(watched.index).apply(
    lambda x: lbf.get_nth_genre(x, n=1, 
                            bar_width=load_bar_width_total, 
                            total_rows=num_rows))
print_centered_msg("Secondary Genre column added!")

print_centered_msg("Tertiary Genre column writing started...")
watched.loc[:, "Tertiary Genre"] = watched.groupby(watched.index).apply(
    lambda x: lbf.get_nth_genre(x, n=2, 
                            bar_width=load_bar_width_total, 
                            total_rows=num_rows))
print_centered_msg("Tertiary Genre column added!")

# export data
print_centered_msg("All genre columns added. Exporting to csv file...")
watched.to_csv("./letterboxd-dialectica972/watched_with_genres.csv")
print_centered_msg("File updated. Program complete!")
print()
