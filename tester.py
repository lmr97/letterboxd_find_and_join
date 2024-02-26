# This script allows for testing on a small subset of the data,
# without commenting out code

import pandas as pd
import math
import letterboxdfinders as lbf

OUTPUT_WIDTH = 50

def print_centered_msg(msg):
    print()
    print(math.ceil(2+(OUTPUT_WIDTH-len(msg))/2) * "-", 
          msg, 
          math.ceil(2+(OUTPUT_WIDTH-len(msg))/2) * "-")


def main():
    
    print_centered_msg("Loading data...")
    file_loc = "./letterboxd-dialectica972/watched.csv" # hard-coding for easy testing
    watched = pd.read_csv(file_loc)
    num_rows = len(watched.index)
    
    test_subset = watched.head(13).copy()
    num_rows = len(test_subset.index)
    print_centered_msg("Main Genre column writing started...")
    test_subset.loc[:, "Main Genre"] = test_subset.groupby(test_subset.index).apply(
        lambda x: lbf.get_nth_genre(x, n=0, bar_width=OUTPUT_WIDTH))
    print_centered_msg("Main Genre column added!")
    
    
    test_subset.to_csv("./letterboxd-dialectica972/watched_with_genres_test.csv")


if __name__ == "__main__":
    main()