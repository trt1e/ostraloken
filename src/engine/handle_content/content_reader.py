import os
import re
from pathlib import Path

# import scripts
from engine import config
from engine import utils

# Parse a content file and extract its content
def file_parser(file: str) -> list:
    # find where diffrent parts are in the document
    return re.findall(r">>(\w+): (.*?)(?=>>|\/\~|$)", file, re.S)
    # Here we look for anything that starts with >>, then we get what is between >> and :, then we get the rest after ": "
    # This then stops if we find ">>", "/~" or the end of the document

# Format the content right
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


# Read the normal articles
def read_articles(): # !!! This one is treated diffrantly !!! To get the files and their content from all normal articals 
    output_sum = [] # all the output
    for utgava in Path(config.articles_path).iterdir(): # go thrpguth every folder to get all the upplagor
        article_output_sum = []
        formated_utgava_info = {}
        for file_path in Path(utgava).iterdir(): # Go througth every file in the list and extract the content
            file_name = Path(file_path.name).stem
            if not file_name.startswith("IMG-") and Path(file_path.name).suffix not in config.img_extentions: # If the file name does not start with "IMG-"
                # read the file
                with open(file_path, "tr", encoding="utf-8") as file:  
                    whole_text = file.read() # read it
                
                if file_name != "utgava_info": # If the file isnt the utgava info file
                    parsed_file = file_parser(whole_text)
                    formated_file = make_regex_list_to_dict(parsed_file)
                    article_output_sum.append(formated_file)
                else:
                    # find where diffrent parts are in the document
                    # REMEMBER: This is loaded 1, 10, 11, 12... 2, 20, 21, 22... 3, 30, 31, 32...
                    parsed_utgava_info = file_parser(whole_text)
                    formated_utgava_info = make_regex_list_to_dict(parsed_utgava_info)
                    
        output = dict(formated_utgava_info[0]) | {"Content": article_output_sum}
        output_sum.append(output)
        
    output_sum.sort(key=lambda x: int(x["Editionsnummer"])) # sort all articles based on edition number so it orders correct
    return output_sum

# Read any other txt files
def read_txt(txt_path):
    content_path = config.base_path / Path("content") / Path(txt_path)
    with open(content_path, "tr", encoding="utf-8") as file:  
        whole_text = file.read() # read it
    
    parsed_file = file_parser(whole_text)
    formated_file = make_regex_list_to_dict(parsed_file)
    return formated_file

if __name__ == "__main__":
    read_articles()