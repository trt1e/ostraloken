import os
import re
from pathlib import Path

# import scripts
from engine import config
from engine import utils

# List the storys paths
articles_path = config.base_path / Path("content/articles")

# Read the normal articles
def read_articles(): # !!! This one is treated diffrantly !!! To get the files and their content from all normal articals 
    upplaga_list = os.listdir(articles_path) # list all folders in dir
    output_sum = [] # all the output
    for upplaga in upplaga_list: # go thrpguth every folder to get all the upplagor
        article_output_sum = []
        upplaga_number = 1
        upplaga_date = ""
        upplaga_extra_info = ""
        for file_path in Path(articles_path / upplaga).iterdir(): # Go througth every file in the list and extract the content
            file_name = Path(file_path.name).stem
            if file_name[:4] != "IMG-": # If the file name does not start with "IMG-"
                # read the file
                with open(file_path, "tr", encoding="utf-8") as file:  
                    whole_text = file.read() # read it
                
                if file_name != "upplaga_info": # If the file isnt the upplaga info file
                    parsed_file = utils.file_parser(whole_text)
                    formated_file = utils.make_regex_list_to_dict(parsed_file)
                    article_output_sum.append(formated_file)
                else:
                    # find where diffrent parts are in the document
                    # REMEMBER: This is loaded 1, 10, 11, 12... 2, 20, 21, 22... 3, 30, 31, 32...
                    upplaga_number = re.findall(r">>Editionsnummer: (.*)", whole_text)[0]
                    upplaga_date = re.findall(r">>Utgivningsdatum: (.*)", whole_text)[0]
                    upplaga_extra_info = re.findall(r">>Extra information: (.*?)$", whole_text, re.S)[0].replace("\n", "")
                    
        output = ({"Upplaga": int(upplaga_number), "Release_date": upplaga_date, "Extra_upplaga_info": upplaga_extra_info.replace("\n", ""), "Content": article_output_sum})
        output_sum.append(output)
        
    output_sum.sort(key=lambda x: int(x["Upplaga"])) # sort all articles based on upplaga_number so it orders correct
    return output_sum

# Read any other txt files
def read_txt(txt_path):
    content_path = config.base_path / Path("content") / Path(txt_path)
    with open(content_path, "tr", encoding="utf-8") as file:  
        whole_text = file.read() # read it
    
    parsed_file = utils.file_parser(whole_text)
    formated_file = utils.make_regex_list_to_dict(parsed_file)
    return formated_file

if __name__ == "__main__":
    read_articles()