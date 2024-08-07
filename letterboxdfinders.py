import requests
from selectolax.parser import HTMLParser

# getting any set of information from the tabs 
# in the center of the page on Letterboxd,
# except for Releases; the logic there is different

# attribute is a string, and can be any element you see in the tabs.
# if there are multiple words in the attribute, it must have a hyphen (-)
# between them. For example, 'assistant director' should be 'assistant-director'.
def get_tabbed_attribute(url, attribute):
    webpage = requests.get(url)
    tree = HTMLParser(webpage.text)

    # find HTML elements whose href contains 'attibute'
    tabbed_elements = tree.css("a[href*='/" + attribute + "/']")

    # extract text from found HTML elements
    attribute_list = []
    for element in tabbed_elements:
        attribute_list.append(element.text())
    
    # return only distinct values, but still as a list
    return set(attribute_list)


def get_avg_rating(film_url):
    webpage = requests.get(film_url)
    tree = HTMLParser(webpage.text)
    rating_element = tree.css("meta[name='twitter:data2']")   # returns list, albeit with 1 element
    
    avg_rating = None
    if (len(rating_element) > 0):
        rating_element_content = rating_element[0].attributes['content']
        rating_element_title_parsed = rating_element_content.split(" ")
        avg_rating = float(rating_element_title_parsed[0])

    return avg_rating