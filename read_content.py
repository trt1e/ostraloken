import os
import re
from pathlib import Path

# import scripts
import base_commands

base_path = Path(__file__).resolve().parent


# List the storys paths
normal_story_path = base_path / Path("content/normal_storys_and_other")

# Read the normal storys
def read_normal_storys(): # !!! This one is treated diffrantly !!! To get the files and their content from all normal articals 
    upplaga_list = os.listdir(normal_story_path) # list all folders in dir
    output_sum = [] # all the output
    for upplaga in upplaga_list: # go thrpguth every folder to get all the upplagor
        # list all files in dir  
        file_list = os.listdir(normal_story_path / upplaga)
        article_output_sum = []
        upplaga_number = 1
        upplaga_date = ""
        upplaga_extra_info = ""
        for file in file_list: # Go througth every file in the list and extract the content
            if file[:4] != "IMG-":
                # extract
                whole_text = base_commands.try_opening(normal_story_path / upplaga / file, "tr")
                if file != "upplaga_info.txt":
                    # find where diffrent parts are in the document
                    title = base_commands.find_between(whole_text, "### ", " ##", 0)
                    type = base_commands.find_between(whole_text, "¤¤¤ ", " ¤¤", 0)
                    writer = base_commands.find_between(whole_text, "@@@ ", " @@", 0)
                    article = whole_text[(whole_text.find(" @@") + 4):] # article is found after the writer aka after " @@"
                    
                    article_output = ({"Title": title, "Type": type, "Writer": writer, "Article": article})
                    article_output_sum.append(article_output)
                else:
                    # find where diffrent parts are in the document
                    # REMEMBER: This is loaded 1, 10, 11, 12... 2, 20, 21, 22... 3, 30, 31, 32...
                    upplaga_number = base_commands.find_between(whole_text, "=== ", " ==", 0)
                    upplaga_date = base_commands.find_between(whole_text, "$$$ ", " $$", 0)
                    upplaga_extra_info = base_commands.find_between(whole_text, "*** ", " **", 0)
        output = ({"Upplaga": int(upplaga_number), "Release_date": upplaga_date, "Extra_upplaga_info": upplaga_extra_info, "Content": article_output_sum})
        output_sum.append(output)
        
    output_sum.sort(key=lambda x: int(x["Upplaga"])) # sort all articles based on upplaga_number so it orders correct
    return output_sum


# Read any other story
def read_txt(txt_path):
    content_path = base_path / Path("content") / Path(txt_path)
    whole_text = base_commands.try_opening(content_path, "tr") # read it
    
    all_packages = re.findall(r">>(\w+): (.*?)(?=>>|END OF TXT)", whole_text, re.S)
    # Here we look for anything that starts with >>, then we get what is between >> and :, then we get the rest after ": "
    # This then stops if we find >> or END OF TXT
    
    output_sum = []
    currant_bundle = {}
    number_of_articles = 0
    last_element = all_packages[-1][0]
    for package in all_packages: # go throught all the packages
        section_title = package[0].replace("\n", "")
        section_text = package[1].replace("\n", "")
        currant_bundle[section_title] = section_text # Ex: currant_bundle["Title"] = "What is the meaning of life?"
        
        if package[0] == last_element: # Then we have looped
            output_sum.append(currant_bundle)
            currant_bundle = {}
            number_of_articles += 1
    
    return output_sum
