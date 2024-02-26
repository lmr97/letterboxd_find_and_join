# This script updates the watched.csv file from Letterboxd with genre tags

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
    
    # get location of file to add data to
    folder_loc = input("\nLocation of Letterboxd data folder: ")
    file_name = input("Name of file (without .csv extension): ")
    
    # load data
    print_centered_msg("Loading data...")
    watched = pd.read_csv(folder_loc+"/"+file_name+".csv")
    num_rows = len(watched.index)


    # add columns
    print_centered_msg("Main Genre column writing started...")
    watched.loc[:, "Main Genre"] = watched.groupby(watched.index).apply(
        lambda x: lbf.get_nth_genre(x, n=0, 
                                bar_width=OUTPUT_WIDTH, 
                                total_rows=num_rows))
    print_centered_msg("Main Genre column added!")

    print_centered_msg("Secondary Genre column writing started...")
    watched.loc[:, "Secondary Genre"] = watched.groupby(watched.index).apply(
        lambda x: lbf.get_nth_genre(x, n=1, 
                                bar_width=OUTPUT_WIDTH, 
                                total_rows=num_rows))
    print_centered_msg("Secondary Genre column added!")

    print_centered_msg("Tertiary Genre column writing started...")
    watched.loc[:, "Tertiary Genre"] = watched.groupby(watched.index).apply(
        lambda x: lbf.get_nth_genre(x, n=2, 
                                bar_width=OUTPUT_WIDTH, 
                                total_rows=num_rows))
    print_centered_msg("Tertiary Genre column added!")


    # export data
    print_centered_msg("All genre columns added. Exporting to csv file...")
    watched.to_csv(folder_loc+file_name+"_with_genres.csv")
    print_centered_msg("File updated. Program complete!")
    print()


if (__name__ == "__main__"):
    main()