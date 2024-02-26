import requests
from bs4 import BeautifulSoup
import math


def get_nth_genre(df, n, bar_width, total_rows):
    webpage = requests.get(df.iloc[0,3])
    soup = BeautifulSoup(webpage.text, features="lxml") # make page parseable

    genre_tab = soup.find(id="tab-genres")
    if(genre_tab): genre_elements = genre_tab.p.find_all("a")
    else: return None

    # loading bar
    bar_width_now = math.ceil(bar_width * (df.index[0]+1)/total_rows)
    print("| ", "█" * bar_width_now, 
          (bar_width - bar_width_now) * " ", "|", 
          f"{(df.index[0]+1)/total_rows:.0%}",
          end = "\r")

    if (len(genre_elements) > n): return genre_elements[n].contents[0]
    else: return None