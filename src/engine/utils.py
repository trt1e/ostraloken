import re
from pathlib import Path

# import scripts
from engine import config
from engine.handle_content import content_reader


def file_parser(file):
    # find where diffrent parts are in the document
    return re.findall(r">>(\w+): (.*?)(?=>>|\/\~|$)", file, re.S)
    # Here we look for anything that starts with >>, then we get what is between >> and :, then we get the rest after ": "
    # This then stops if we find ">>", "/~" or the end of the document

def make_regex_list_to_dict(list) -> list:
    output_sum = []
    currant_bundle = {}
    number_of_articles = 0
    last_element = list[-1][0]
    for package in list: # go throught all the packages
        section_title = package[0].replace("\n", "")
        section_text = package[1].replace("\n", "")
        currant_bundle[section_title] = section_text # Ex: currant_bundle["Title"] = "What is the meaning of life?"
        
        if package[0] == last_element: # Then we have looped
            output_sum.append(currant_bundle)
            currant_bundle = {}
            number_of_articles += 1
            
    return output_sum

def strip_string(string, max):
    if max == -1 or max == "" or max is None:
        return re.sub(r"[^a-zA-Z0-9 åäöÅÄÖ]", "", string).replace(" ", "_")
    else:
        return re.sub(r"[^a-zA-Z0-9 åäöÅÄÖ]", "", string).replace(" ", "_")[:max]

def remove_html_elements(string):
    new_string = string
    last_pos = 0
    amount_of_start = string.count("<")
    amount_of_end = string.count(">")
    if amount_of_start != amount_of_end:
        print(f"WARNING WHEN REMOVING HTML FROM ELEMENT: amount of < ({amount_of_start}) not same as > ({amount_of_end}) in {string}")
    
    for _ in range(amount_of_start):
        start_pos = string.find("<", last_pos)
        end_pos = string.find(">", last_pos) + 1
        last_pos = end_pos
        new_string = new_string.replace(str(string[start_pos:end_pos]), "")
        
    return new_string

def fix_cut_of_html_elements(text):
    # closes html element if it was left open
    extra_at_end = ""
    if text.count("<") > text.count("</") and text.count("<") != 0 and text.count("<") != text.count("<br>"):
        # find what html element is missing
        list_of_html_elements = re.findall(r"<(.*?)>", text) # find all things between < and > and set it in a list (not including < and > in that element)
        remove_list = []
        not_closed_html_elements = []
        for element in list_of_html_elements:
            if element == "br" or element == "img": # br and img both do not have </ to close, so they are not relevant
                remove_list.append(element)
            else:
                element = re.split(" ", element)[0]
                if element in not_closed_html_elements:
                    not_closed_html_elements.remove(element)
                elif str("/" + element) in not_closed_html_elements:
                    not_closed_html_elements.remove("/" + element)
                elif element[1:] in not_closed_html_elements:
                    not_closed_html_elements.remove(element[1:])
                else:
                    not_closed_html_elements.append(element)
                    
        for element in remove_list:
            list_of_html_elements.remove(element)
                
        # paragraphs are closed automaticly, no need to do it here
        if "p" in not_closed_html_elements:
            not_closed_html_elements.remove("p")
        elif "/p" in not_closed_html_elements:
            not_closed_html_elements.remove("/p")
                
        for html_element in not_closed_html_elements: 
            # reverse the html element: if it is for example <span>, we need to make it </span> and vice versa
            if "/" in html_element:
                opposite_html_element = html_element[1:]
            else:
                opposite_html_element = "/" + html_element
            extra_at_end += f"<{opposite_html_element}>"
           
    # this returns what should be added at the end of the text given 
    return extra_at_end

def remove_åäö(string):
    replace_letters = {"å": "a", "Å": "A", "ä": "a", "Ä": "A", "ö": "o", "Ö": "O"}
    for letter in replace_letters:
        if letter in string:
            string = string.replace(letter, replace_letters[letter])
    return string

def get_curant_utgava_number():
    highest_utgava_number = 1
    for utgava in reversed(content_reader.read_articles()):
        if utgava["utgava"] > highest_utgava_number:
            highest_utgava_number = utgava["utgava"]
    return highest_utgava_number

def make_article_id(article_title, utgava_number):
    id_article = remove_åäö(article_title)
    id_article = strip_string(remove_html_elements(id_article), 100)
    id_utgava = "-U" + str(utgava_number)
    return id_article + id_utgava

def make_short_story_id(article_title, article_content):
    id_article = remove_åäö(article_title)
    id_article = remove_åäö(article_content)
    
    id_article = strip_string(remove_html_elements(str(article_title)), 60)
    id_content = strip_string(remove_html_elements(str(article_content)), 120)

    return id_article + "+" + id_content

def make_image_id(article_title):
    return "IMG-" + strip_string(remove_html_elements(article_title), 100)

def find_img(article_title, utgava_nmr, base_url):
    old_img_title = make_image_id(article_title)
    new_img_title = remove_åäö(make_image_id(article_title))
    old_img_path_no_extention = config.articles_path / f"utgava_{utgava_nmr}" / old_img_title
    for ext in config.img_extentions:
        if Path(f"{old_img_path_no_extention}.{ext}").is_file():
            old_img_path_with_extention = f"{old_img_path_no_extention}.{ext}"
            break
    else:
        old_img_path_with_extention = "NO_IMG" # article does not have image
        
    if old_img_path_with_extention != "NO_IMG":
        return base_url + new_img_title + ".webp"
    else:
        return ""

def get_head_writers():
    # Get head writers
    head_writers = [] # list Löken head writers
    # These are the names that if they wrote a article will redirect on click to the omoss page!
    with open(config.base_path / "content/static/staff.txt", "tr", encoding="utf-8") as file:  
        staff_file_content = file.read() # read it
    formated_staff_file_content = make_regex_list_to_dict(file_parser(staff_file_content))
    for person in formated_staff_file_content:
        head_writers.append(person["Namn"])
    # Get head writers
    head_writers = [] # list Löken head writers
    # These are the names that if they wrote a article will redirect on click to the omoss page!
    with open(config.base_path / "content/static/staff.txt", "tr", encoding="utf-8") as file:  
        staff_file_content = file.read() # read it
    formated_staff_file_content = make_regex_list_to_dict(file_parser(staff_file_content))
    for person in formated_staff_file_content:
        head_writers.append(person["Namn"])
    return head_writers