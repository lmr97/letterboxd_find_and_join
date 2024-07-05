import math
import numpy as np
import pandas as pd
import letterboxdfinders as lbf

OUTPUT_WIDTH = 50


def print_centered_msg(msg):
    print()
    print(math.ceil(2+(OUTPUT_WIDTH-len(msg))/2) * "-", 
          msg, 
          math.ceil(2+(OUTPUT_WIDTH-len(msg))/2) * "-")
    


def print_loading_bar(rows_now, total_rows):
    bar_width_now = math.ceil(OUTPUT_WIDTH * (rows_now+1)/total_rows)
    print("| ", "█" * bar_width_now, 
            (OUTPUT_WIDTH - bar_width_now) * " ", "|", 
            f"{(rows_now+1)/total_rows:.0%}",
            end = "\r")



def create_new_attr_cols(url_df, film_attribute):
    new_attr_cols = []  # using list at first for flexibility
    num_rows = url_df.size
    max_attr_length = 0

    print_centered_msg("Fetching data...")
    for i, url in enumerate(url_df):
        if (i == 0): continue
        
        print_loading_bar(i, num_rows)
        
        attr_for_row = lbf.get_tabbed_attribute(url, attribute=film_attribute)
        new_attr_cols.append(attr_for_row)

        # update maximum attribute length for dataframe building
        if (len(attr_for_row) > max_attr_length):
            max_attr_length = len(attr_for_row)

    print_centered_msg("Formatting data...")

    # make header
    header = []
    film_attribute = film_attribute.capitalize()
    for i in range(max_attr_length):
        header.append(film_attribute + " " + str(i+1))

    new_attr_cols = pd.DataFrame(new_attr_cols, columns=header)

    return new_attr_cols




def main():
    file_path = "/Users/martinreid/Desktop/Personal_Coding/Python/letterboxd-dialectica972/watched_test.csv"
    print_centered_msg("Loading file...")
    lb_df = pd.read_csv(file_path)

    genre_cols = create_new_attr_cols(lb_df['Letterboxd URI'], "genre")
    lb_df_with_genres = lb_df.join(genre_cols)

    print_centered_msg("Writing to file...")
    lb_df_with_genres.to_csv("/Users/martinreid/Desktop/Personal_Coding/Python/letterboxd-dialectica972/watched_test_w_genres.csv")
    print_centered_msg("Data added successfully!")

    


    
    
if (__name__ == "__main__"):
    main()