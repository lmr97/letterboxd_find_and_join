# this driver adds Director and Genre columns to a given Letterboxd list.

import math
import csv
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
    

# requires attribute_name to be lower case and have hyphens for spaces, 
# e.g. "Assistant Director" should be "assistant-director"
# TODO: make catalogue of strings for certain film attributes for documentation
def add_tab_content_columns(file_path, attribute_name):
    
    updated_file_loc = file_path.replace(".csv", "_with_" + attribute_name + "s.csv")

    print_centered_msg(attribute_name + " column writing started...")

    with open(file_path, "r") as lbfile_reader:
        lb_csv_read = lbfile_reader.readlines()
        num_lines = sum(1 for row in lb_csv_read)

    with open(updated_file_loc, "w") as lbfile_writer:
        
        # determine where the actual column labels begin. If the file is a Letterboxd list,
        # then there will be a row at the top that starts with "Letterboxd list export" 
        # with a version number afterwards, 2 more rows of list info, then a blank line
        header_line = 0 # default
        if (lb_csv_read[0].find("Le") == 0): 
            header_line = 4

        col_count = len(lb_csv_read[header_line].split(","))  # length of columns in header at the start
        # we'll need to know how many the max of each is in order to make the header
        max_attribute_count = 0 
        
        for i, line in enumerate(lb_csv_read):
            print_loading_bar(i, num_lines)
            
            # take out newline character, if there is one at the end of the line
            if (line.find("\n") > 0): line = line[0:-1]
            parsed_line = line.split(",")

            # we need to know what the highest attribute counts are
            # before we can do the header,
            # so we'll look for it while we're looping through the rows
            # thus, if we're on the header, don't do anything to it
            if (i == 2):  # line 2 is the last line of list info, doesn't need newline
                whole_line = ",".join(parsed_line)  
            elif (i <= header_line):
                whole_line = ",".join(parsed_line)+"\n"
            else:
                line_url = parsed_line[3]  # URL is always in the 4th column
                attribute_content = lbf.get_tabbed_attribute(line_url, attribute_name)

                # add extra commas for null values under each column 
                # from previous added columns with nulls
                if (col_count > len(parsed_line)): parsed_line.append((col_count - len(parsed_line)-1)*",") 

                parsed_line += attribute_content # only then add attribute list

                if (len(attribute_content) > max_attribute_count): 
                    max_attribute_count = len(attribute_content)

                whole_line = ",".join(parsed_line) + "\n"
            
            lb_csv_read[i] = whole_line
        
        # now that we know how long the longest line is, we know how many genre lines to add
        
        # get header and replace newline character with comma at the end
        header = lb_csv_read[header_line]
        header = header[0:-1]  
        header += ","

        # add director columns then genre columns
        attribute_pretty = attribute_name.replace("-", " ")
        attribute_pretty = attribute_pretty.capitalize()
        for number in range(max_attribute_count):
            header = header + attribute_pretty + " " + str(number+1) + ","
        
        # replace terminal comma with newline character
        header = header[0:-1] 
        header += "\n"

        lb_csv_read[header_line] = header
        lbfile_writer.writelines(lb_csv_read)

    print_centered_msg(attribute_name + " column(s) added!")

    return updated_file_loc



def main():
    
    # get location of file to add data to
    file_loc = input("\nPath to Letterboxd CSV: ")
    
    director_file = add_tab_content_columns(file_loc, "director")
    genre_director_file = add_tab_content_columns(director_file, "genre")
    finished_file = add_tab_content_columns(genre_director_file, "actor")

    print_centered_msg("All columns added!")
    print("\nYour file with all added info is at:\n", finished_file, "\n")


if (__name__ == "__main__"):
    main()