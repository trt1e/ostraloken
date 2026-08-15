import os
import re

# import scripts
from engine import config
from engine import utils
from engine.handle_content import content_reader


############### ADD CHECKING STATIC AND PDFS HERE!!! #################

def inspect_normal_storys(): # looks throught all files to se if something is wrong but doesnt change nothing
    print("↓ ARTICLES ↓")
    upplaga_list = os.listdir(content_reader.articles_path) # list all folders in dir
    for upplaga in upplaga_list: # go thrpguth every folder to get all the upplagor
        printed_something = False
        exists_upplaga_info_file = False
        images_list = []
        titles_list = []
        # list all files in dir
        file_list = os.listdir(content_reader.articles_path / upplaga)
        for file in file_list: # Go througth every file in the list
            if file[:4] != "IMG-":
                # check if there are img files that do not start with IMG-
                # OLD: if file[-3:] in config.img_extentions or file[-4:] in config.img_extentions:
                if file.endswith(tuple(config.img_extentions)):
                    print(f'WARNING: {file} is image but does not start with "IMG-" as it should')
                    printed_something = True
                else:
                    try:
                        whole_text = utils.try_opening(content_reader.articles_path / upplaga / file, "tr")
                        if re.search(r"[“”]", whole_text): # if “ or ” in file, should be "
                            print(f'NOTE: {file} contains “ and/or ”. Instead you should use "')
                            printed_something = True
                            
                        if whole_text.count("<") != whole_text.count(">"):
                            print(f'NOTE: {file} has a uneven amount of "<" and ">"')
                            printed_something = True
                            
                        if file != "upplaga_info.txt":
                            if whole_text.find("### ") == -1:
                                print(f'WARNING: {file} does not have a "### " as it should')
                                printed_something = True
                            if whole_text.find(" ##") == -1:
                                print(f'WARNING: {file} does not have a " ##" as it should')
                                printed_something = True
                            if whole_text.find("¤¤¤ ") == -1:
                                print(f'WARNING: {file} does not have a "¤¤¤ " as it should')
                                printed_something = True
                            if whole_text.find(" ¤¤") == -1:
                                print(f'WARNING: {file} does not have a " ¤¤" as it should')
                                printed_something = True
                            if whole_text.find("@@@ ") == -1:
                                print(f'WARNING: {file} does not have a "@@@ " as it should')
                                printed_something = True
                            if whole_text.find(" @@") == -1:
                                print(f'WARNING: {file} does not have a " @@" as it should')
                                printed_something = True

                            if whole_text.find("### ") != -1 and whole_text.find(" ##") != -1:
                                title = utils.find_between(whole_text, "### ", " ##", 0)
                                if title == "":
                                    print(f'WARNING: {file} title is empty')
                                if title == "RUBRIK":
                                    print(f'WARNING: {file} title is still template')
                                    
                                titles_list.append(utils.strip_string(utils.remove_html_elements(title), 100))
                                
                                if str("_".join(file.split(" ")[1:])).split(".")[0] != utils.strip_string(utils.remove_html_elements(title), 100):
                                    print(f'WARNING: {file} (fixed: {str("_".join(file.split(" ")[1:])).split(".")[0]}) does not have same name as title: {title} (fixed: {utils.strip_string(utils.remove_html_elements(title), 100)})')
                                    printed_something = True
                                
                            if whole_text.find("¤¤¤ ") != -1 and whole_text.find(" ¤¤") != -1:
                                type = utils.find_between(whole_text, "¤¤¤ ", " ¤¤", 0)
                                if type == "":
                                    print(f'WARNING: {file} type is empty')
                                if type == "ARTIKEL_TYP":
                                    print(f'WARNING: {file} type is still template')
                                
                            if whole_text.find("@@@ ") != -1 and whole_text.find(" @@") != -1:
                                writer = utils.find_between(whole_text, "@@@ ", " @@", 0)
                                if writer == "":
                                    print(f'WARNING: {file} writer is empty')
                                if writer == "SKRIBENT":
                                    print(f'WARNING: {file} writer is still template')
                                
                            article = whole_text[(whole_text.find(" @@") + 4):] # article is found after the writer aka after " @@"
                            if article == "":
                                print(f'WARNING: {file} does not have content after " @@"')
                                printed_something = True
                        else:
                            exists_upplaga_info_file = True
                            upplaga_number = utils.find_between(whole_text, "=== ", " ==", 0)
                            upplaga_date = utils.find_between(whole_text, "$$$ ", " $$", 0)
                            
                            if not re.search(r"^[0-9]+$", upplaga_number):
                                print(f'WARNING: {file} upplaga number is not number')
                                printed_something = True
                            if not re.search(r"^[0-9 \-]+$", upplaga_date):
                                print(f'WARNING: {file} upplaga date are not numbers')
                                printed_something = True
                            if upplaga_date == "DD/MM/ÅÅÅÅ":
                                print(f'WARNING: {file} upplaga date is still the template')
                                printed_something = True
                            
                            for image in images_list:
                                image_title = str(image[4:]).split(".")[0]
                                if image_title not in titles_list:
                                    print(f"WARNING: {image} does not have a article it is linked to")
                                    printed_something = True
                            
                            if printed_something is True:
                                print(f"↑ Upplaga number: {upplaga_number} ↑\n")
                    except Exception as e:
                        print(f"ERROR: {e}")
                        printed_something = True
            else: # starts with IMG-
                images_list.append(file) # add the file to a list so we can check if it has article by same name
            
        if exists_upplaga_info_file is False:
            print(f'WARNING: {upplaga} does not have a upplaga_info.txt file')

def inspect_short_storys():
    whole_text = utils.try_opening(content_reader.short_story_path, "tr") # read it
    print("\n↓ NOTISER ↓")
    if re.search(r"[“”]", whole_text): # if “ or ” in file, should be "
        print(f'NOTE: Notiser contains “ and/or ”. Instead you should use "')
        
    if whole_text.count("<") != whole_text.count(">"):
        print(f'NOTE: Notiser has a uneven amount of "<" and ">"')
    
    last_final_pos = whole_text.find("### ") # start at the first title aka the first "### "  
    for _ in range(whole_text.count("### ")): # repeat for how many hear me outs there are in the txt
        # find where diffrent parts are in the document
        title = utils.find_between(whole_text, "### ", " ##", last_final_pos)
        if "++" in title:
            print(f'WARNING: {title} contains "++" in title which it should not have')
        if "##" in title:
            print(f'WARNING: {title} contains "##" in title which it should not have')
        if title == "":
            print(f'WARNING: {title} is empty')
        if title == "RUBRIK":
            print(f'WARNING: {title} is still template')
        article = utils.find_between(whole_text, "+++ ", " ++", last_final_pos)
        if "++" in article:
            print(f'WARNING: {title} contains "++" in article which it should not have')
        if "##" in article:
            print(f'WARNING: {title} contains "##" in article which it should not have')
        if article == "":
            print(f'WARNING: {title} text is empty')
        if article == "BRÖDTEXT":
            print(f'WARNING: {title} text is still template')
        last_final_pos = whole_text.find(" ++", last_final_pos) + 3
        
def inspect_hear_me_outs():
    whole_text = utils.try_opening(content_reader.hear_me_outs_path, "tr") # read it
    print("\n↓ HEAR ME OUTS ↓")
    if re.search(r"[“”]", whole_text): # if “ or ” in file, should be "
        print(f'NOTE: Hear me outs contains “ and/or ”. Instead you should use "')
        
    if whole_text.count("<") != whole_text.count(">"):
        print(f'NOTE: Hear me outs has a uneven amount of "<" and ">"')
    
    last_final_pos = whole_text.find("### ") # start at the first title aka the first "### "  
    for _ in range(whole_text.count("### ")): # repeat for how many hear me outs there are in the txt
        # find where diffrent parts are in the document
        hear_me_out = utils.find_between(whole_text, "### ", " ##", last_final_pos)
        if "++" in hear_me_out:
            print(f'WARNING: {hear_me_out} contains "++" in hear me out which it should not have')
        if "##" in hear_me_out:
            print(f'WARNING: {hear_me_out} contains "##" in hear me out which it should not have')
        if hear_me_out == "":
            print(f'WARNING: {hear_me_out} is empty')
        if hear_me_out == "HEAR_ME_OUT":
            print(f'WARNING: {hear_me_out} is still template')
        desc = utils.find_between(whole_text, "+++ ", " ++", last_final_pos)
        if "++" in desc:
            print(f'WARNING: {hear_me_out} contains "++" in description which it should not have')
        if "##" in desc:
            print(f'WARNING: {hear_me_out} contains "##" in description which it should not have')
        if hear_me_out == "BESKRIVNING":
            print(f'WARNING: {hear_me_out} description is still template')
        last_final_pos = whole_text.find(" ++", last_final_pos) + 3

def fix_citationmarks():
    # normal storys
    fixed_something = False
    upplaga_list = os.listdir(content_reader.articles_path) # list all folders in dir
    for upplaga in upplaga_list: # go thrpguth every folder to get all the upplagor
        # list all files in dir
        file_list = os.listdir(content_reader.articles_path / upplaga)
        for file in file_list: # Go througth every file in the list
            if file[:4] != "IMG-":
                whole_text = utils.try_opening(content_reader.articles_path / upplaga / file, "tr")
                if re.search(r"[“”]", whole_text): # if “ or ” in file, should be "
                    new_text = whole_text.replace("“", '"')
                    new_text = new_text.replace("”", '"')
                    
                    with open(content_reader.articles_path / upplaga / file, "w", encoding="utf-8") as file:
                        file.write(new_text) # write to it
                    
                    fixed_something = True
                    print(f"Fixed citationmark(s) in {file}")
                    
    if fixed_something is False:
        print("No citationmarks to fix in articles")

    # short storys
    fixed_something = False
    whole_text = utils.try_opening(content_reader.short_story_path, "tr") # read it
    if re.search(r"[“”]", whole_text): # if “ or ” in file, should be "
        new_text = whole_text.replace("“", '"')
        new_text = new_text.replace("”", '"')
        with open(content_reader.short_story_path, "w", encoding="utf-8") as file:
            file.write(new_text) # write to it
        
        fixed_something = True
        print(f"Fixed citationmark(s) in notiser")
        
    if fixed_something is False:
        print("No citationmarks to fix in notiser")

    # hear me outs
    fixed_something = False
    whole_text = utils.try_opening(content_reader.hear_me_outs_path, "tr") # read it
    if re.search(r"[“”]", whole_text): # if “ or ” in file, should be "
        new_text = whole_text.replace("“", '"')
        new_text = new_text.replace("”", '"')
        with open(content_reader.hear_me_outs_path, "w", encoding="utf-8") as file:
            file.write(new_text) # write to it
        
        fixed_something = True
        print(f"Fixed citationmark(s) in hear me outs")
        
    if fixed_something is False:
        print("No citationmarks to fix in hear me outs")

def fix_all_backend_articles_names(): # Make the names in articles more consistant
    upplaga_list = os.listdir(content_reader.articles_path) # list all folders in dir
    for upplaga in upplaga_list: # go thrpguth every folder to get all the upplagor
        # list all files in dir 
        file_list = os.listdir(content_reader.articles_path / upplaga)
        for file_number, file in enumerate(file_list, 1): # Go througth every file in the list and extract the content
            if file != "upplaga_info.txt" and file[:4] != "IMG-":
                # extract
                whole_text = utils.try_opening(content_reader.articles_path / upplaga / file, "tr")
                # find where title is in the document
                title = utils.find_between(whole_text, "### ", " ##", 0)
                basic_title = utils.remove_html_elements(title)
                
                new_file_name = str(file_number) + " " + utils.strip_string(basic_title, 100) + ".txt"
                
                os.rename((content_reader.articles_path / upplaga / file), (content_reader.articles_path / upplaga / new_file_name))

    print("Article names successfully fixed!")