import os
import re
from pathlib import Path

# import scripts
from engine import config
from engine import utils


def inspect_all():
    base_content_path = Path(config.base_path / "content")
    
    # This is what is get looked throguh and will be updated when the script finds more folders
    look_index = [base_content_path] # Start with just the content folder
    
    found_something = False
    
    for path in look_index:
        currant_folder = Path(str(path).replace(str(base_content_path), ""))
        for file_dir in path.iterdir():
            if file_dir.is_file() and file_dir.suffix == ".txt":
                file_name = currant_folder / file_dir.name
                # read the file
                with open(file_dir, "tr", encoding="utf-8") as file:  
                    whole_text = file.read() # read it
                
                if re.search(r"[“”]", whole_text): # if “ or ” in file, should be "
                    print(f'NOTE: {file_name} contains “ and/or ”. Instead you should use "')
                    found_something = True
                    
                if re.search(r"[‘’]", whole_text): # if ‘ or ’ in file, should be '
                    print(f"NOTE: {file_name} contains ‘ and/or ’. Instead you should use '")
                    found_something = True
                    
                parsed_file = utils.file_parser(whole_text)
                formated_file = utils.make_regex_list_to_dict(parsed_file)
                
                if formated_file == "" or formated_file == [] or formated_file == [""]:
                    print(f'WARNING: {file_name} is empty when formated')
                    found_something = True
                
                for file in formated_file:
                    file_keys = list(file.keys())
                    for key in file_keys:
                        # Check so there is no unwanted space
                        if " " in key:
                            print(f'WARNING: {file_name} contains a space in "{key[:30]}..." which it should not have')
                            found_something = True
                            
                        # Check so there is no unwanted >>
                        if ">>" in key:
                            print(f'WARNING: {file_name} contains ">>" in "{key[:30]}..." which it should not have')
                            found_something = True
                    
                    
                    file_values = list(file.values())
                    for value in file_values:
                        # Check if it has a uneven amount of < and >
                        if value.count("<") != value.count(">"):
                            print(f'NOTE: {file_name} has a uneven amount of "<" and ">" (in the content). This could mean that there is a non closed html <tag>')
                            found_something = True
                        
                        # Check so there is no unwanted >>
                        if ">>" in value:
                            print(f'WARNING: {file_name} contains ">>" in "{value[:30]}..." which it should not have')
                            found_something = True
                                
                        
            elif file_dir.is_dir():
                look_index.append(file_dir)

    if found_something is False:
        print("Nothing found")

def fix_citationmarks():
    base_content_path = Path(config.base_path / "content")
    
    # This is what is get looked throguh and will be updated when the script finds more folders
    look_index = [base_content_path] # Start with just the content folder
    
    fixed_something = False
    
    for path in look_index:
        currant_folder = Path(str(path).replace(str(base_content_path), ""))
        for file_dir in path.iterdir():
            if file_dir.is_file() and file_dir.suffix == ".txt":
                file_name = currant_folder / file_dir.name
                # read the file
                with open(file_dir, "tr", encoding="utf-8") as file:  
                    whole_text = file.read() # read it
                
                if re.search(r"[“”‘’]", whole_text): # if “, ”, ‘ or ’ in file
                    new_text = whole_text.replace('“', '"')
                    new_text = new_text.replace('”', '"')
                    new_text = new_text.replace("‘", "'")
                    new_text = new_text.replace("’", "'")
                    
                    with open(file_dir, "w", encoding="utf-8") as file:
                        file.write(new_text)
                                    
                    fixed_something = True
                    print(f"Fixed citationmark(s) in {file_name}")
                    
            elif file_dir.is_dir():
                look_index.append(file_dir)
    
    if fixed_something is False:
        print("No citationmarks to fix")

def fix_all_backend_articles_names(): # Make the names in articles more consistant
    utgava_list = os.listdir(config.articles_path) # list all folders in dir
    for utgava in utgava_list: # go thrpguth every folder to get all the upplagor
        # list all files in dir 
        file_list = os.listdir(config.articles_path / utgava)
        for file_number, file in enumerate(file_list, 1): # Go througth every file in the list and extract the content
            if file != "utgava_info.txt" and file[:4] != "IMG-":
                # extract
                with open(config.articles_path / utgava / file, "tr", encoding="utf-8") as file:  
                    whole_text = file.read() # read it
                # find where title is in the document
                parsed_file = utils.file_parser(whole_text)
                formated_file = utils.make_regex_list_to_dict(parsed_file)
                basic_title = utils.remove_html_elements(formated_file[0]["Rubrik"])
                
                new_file_name = str(file_number) + "-" + utils.strip_string(basic_title, 100) + ".txt"

                os.rename(file.name, (config.articles_path / utgava / new_file_name))

    print("Article names successfully fixed!")