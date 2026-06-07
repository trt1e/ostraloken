import os
import re
import random
from PIL import Image
import progressbar

is_linux = False

global base_path
base_path = os.getcwd()
img_extentions = ["jpg", "JPG", "jpeg", "JPEG", "png", "PNG", "webp"]

# BASE COMMANDS
def strip_string(string, max):
    if max == -1 or max == "" or max is None:
        return re.sub(r"[^a-zA-Z0-9 åäöÅÄÖ]", "", string).replace(" ", "_")
    else:
        return re.sub(r"[^a-zA-Z0-9 åäöÅÄÖ]", "", string).replace(" ", "_")[:max]

def handel_path_slash(string): # needs to be own function cause some parts just require one or two slashes
    if is_linux == True:
        return string.replace("\\", "/")
    else:
        return string

def work_path(path): # input a path that works on windows and it then works in linux if needed
    if is_linux == True:
        new_path = handel_path_slash(path)
        new_path_start = new_path.find("/", 1)
        return base_path + new_path[new_path_start:]
    else:
        return base_path + path

def try_opening(content, extra): # extra is like "tr" or something like that
    list_of_utf = ["utf-8", "utf-8-sig", "utf-16", "utf-16le", "utf-16be", "utf-32"]
    open_content = None

    for utf in list_of_utf:
        try:
            if extra != "":
                open_content = open(content, extra, encoding=utf) # like se if it exists almost
            else:
                open_content = open(content, encoding=utf)
            text_output = open_content.read() # read it
            open_content.close() # at the end
            return text_output
        except:
            pass
    else: # this is only so py doesn't give an error
        if extra != "":
            open_content = open(content, extra, encoding="utf-8") # like se if it exists almost
        else:
            open_content = open(content, encoding="utf-8")
        text_output = open_content.read() # read it
        open_content.close() # at the end
        return text_output

def find_between(input, find_start, find_end, start_pos):
    pos1 = input.find(find_start, start_pos) + len(find_start)
    pos2 = input.find(find_end, pos1)
    return input[pos1:pos2]

def remove_html_elements(string):
    new_string = string
    last_pos = 0
    amount_of_start = string.count("<")
    amount_of_end = string.count(">")
    if amount_of_start != amount_of_end:
        print(f"WARNING WHEN REMOVING HTML FROM ELEMENT: amount of < ({amount_of_start}) not same as > ({amount_of_end}) in {string}")
    
    for i in range(amount_of_start):
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

def get_curant_upplaga_number():
    highest_upplaga_number = 1
    for upplaga in reversed(read_normal_storys()):
        if upplaga["Upplaga"] > highest_upplaga_number:
            highest_upplaga_number = upplaga["Upplaga"]
    return highest_upplaga_number

# READ TEXT
normal_story_path = work_path(r"\ostraloken\backend\content\normal_storys_and_other")
short_story_path = work_path(r"\ostraloken\backend\content\short_storys.txt")
hear_me_outs_path = work_path(r"\ostraloken\backend\content\hear_me_outs.txt")

def read_normal_storys(): # To get the files and their content from all normal articals 
    upplaga_list = os.listdir(normal_story_path) # list all folders in dir
    output_sum = [] # all the output
    for upplaga in upplaga_list: # go thrpguth every folder to get all the upplagor
        # list all files in dir  
        file_list = os.listdir(normal_story_path + handel_path_slash("\\") + upplaga)
        article_output_sum = []
        upplaga_number = 1
        upplaga_date = ""
        upplaga_extra_info = ""
        for file in file_list: # Go througth every file in the list and extract the content
            if file[:4] != "IMG-":
                # extract
                whole_text = try_opening(normal_story_path + handel_path_slash("\\") + upplaga + handel_path_slash("\\") + file, "tr")
                if file != "upplaga_info.txt":
                    # find where diffrent parts are in the document
                    title = find_between(whole_text, "### ", " ##", 0)
                    type = find_between(whole_text, "¤¤¤ ", " ¤¤", 0)
                    writer = find_between(whole_text, "@@@ ", " @@", 0)
                    article = whole_text[(whole_text.find(" @@") + 4):] # article is found after the writer aka after " @@"
                    
                    article_output = ({"Title": title, "Type": type, "Writer": writer, "Article": article})
                    article_output_sum.append(article_output)
                else:
                    # find where diffrent parts are in the document
                    # REMEMBER: This is loaded 1, 10, 11, 12... 2, 20, 21, 22... 3, 30, 31, 32...
                    upplaga_number = find_between(whole_text, "=== ", " ==", 0)
                    upplaga_date = find_between(whole_text, "$$$ ", " $$", 0)
                    upplaga_extra_info = find_between(whole_text, "*** ", " **", 0)
        output = ({"Upplaga": int(upplaga_number), "Release_date": upplaga_date, "Extra_upplaga_info": upplaga_extra_info, "Content": article_output_sum})
        output_sum.append(output)
        
    output_sum.sort(key=lambda x: int(x["Upplaga"])) # sort all articles based on upplaga_number so it orders correct
    return output_sum

def read_short_storys(): # To get the files and their content from all short articals
    whole_text = try_opening(short_story_path, "tr") # read it
    last_final_pos = whole_text.find("### ") # start at the first title aka the first "### "  
    output_sum = []
    for number_of_articles in range(whole_text.count("### ")): # repeat for how many short storys there are in the txt
        # find where diffrent parts are in the document
        title = find_between(whole_text, "### ", " ##", last_final_pos)
        article = find_between(whole_text, "+++ ", " ++", last_final_pos)
        last_final_pos = whole_text.find(" ++", last_final_pos) + 3
        
        output = ({"Number": number_of_articles, "Content": {"Title": title, "Article": article}})
        output_sum.append(output)
        
    return output_sum

def read_hear_me_outs(): # To get the contents from all hear me outs
    whole_text = try_opening(hear_me_outs_path, "tr")
    last_final_pos = whole_text.find("### ") # start at the first title aka the first "### "
    output_sum = []
    for number_of_hear_me_outs in range(whole_text.count("### ")): # repeat for how many hear me outs there are in the txt

        # find where diffrent parts are in the document
        hear_me_out = find_between(whole_text, "### ", " ##", last_final_pos)
        desc = find_between(whole_text, "+++ ", " ++", last_final_pos)
        last_final_pos = whole_text.find(" ++", last_final_pos) + 3
        
        output = ({"Number": int(number_of_hear_me_outs), "Content": {"Hear_me_out": hear_me_out, "Description": desc}})
        output_sum.append(output)
        
    return output_sum


# FIX ARTICLES
def inspect_normal_storys(): # looks throught all files to se if something is wrong but doesnt change nothing
    print("↓ ARTICLES ↓")
    upplaga_list = os.listdir(normal_story_path) # list all folders in dir
    for upplaga in upplaga_list: # go thrpguth every folder to get all the upplagor
        printed_something = False
        exists_upplaga_info_file = False
        images_list = []
        titles_list = []
        # list all files in dir
        file_list = os.listdir(normal_story_path + handel_path_slash("\\") + upplaga)
        for file in file_list: # Go througth every file in the list
            if file[:4] != "IMG-":
                # check if there are img files that do not start with IMG-
                if file[-3:] in img_extentions or file[-4:] in img_extentions:
                    print(f'WARNING: {file} is image but does not start with "IMG-" as it should')
                    printed_something = True
                else:
                    try:
                        whole_text = try_opening(normal_story_path + handel_path_slash("\\") + upplaga + handel_path_slash("\\") + file, "tr")
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
                                title = find_between(whole_text, "### ", " ##", 0)
                                if title == "":
                                    print(f'WARNING: {file} title is empty')
                                if title == "RUBRIK":
                                    print(f'WARNING: {file} title is still template')
                                    
                                titles_list.append(strip_string(remove_html_elements(title), 100))
                                
                                if str("_".join(file.split(" ")[1:])).split(".")[0] != strip_string(remove_html_elements(title), 100):
                                    print(f'WARNING: {file} (fixed: {str("_".join(file.split(" ")[1:])).split(".")[0]}) does not have same name as title: {title} (fixed: {strip_string(remove_html_elements(title), 100)})')
                                    printed_something = True
                                
                            if whole_text.find("¤¤¤ ") != -1 and whole_text.find(" ¤¤") != -1:
                                type = find_between(whole_text, "¤¤¤ ", " ¤¤", 0)
                                if type == "":
                                    print(f'WARNING: {file} type is empty')
                                if type == "ARTIKEL_TYP":
                                    print(f'WARNING: {file} type is still template')
                                
                            if whole_text.find("@@@ ") != -1 and whole_text.find(" @@") != -1:
                                writer = find_between(whole_text, "@@@ ", " @@", 0)
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
                            upplaga_number = find_between(whole_text, "=== ", " ==", 0)
                            upplaga_date = find_between(whole_text, "$$$ ", " $$", 0)
                            
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
                            
                            if printed_something == True:
                                print(f"↑ Upplaga number: {upplaga_number} ↑\n")
                    except Exception as e:
                        print(f"ERROR: {e}")
                        printed_something = True
            else: # starts with IMG-
                images_list.append(file) # add the file to a list so we can check if it has article by same name
            
        if exists_upplaga_info_file == False:
            print(f'WARNING: {upplaga} does not have a upplaga_info.txt file')

def inspect_short_storys():
    whole_text = try_opening(short_story_path, "tr") # read it
    print("\n↓ NOTISER ↓")
    if re.search(r"[“”]", whole_text): # if “ or ” in file, should be "
        print(f'NOTE: Notiser contains “ and/or ”. Instead you should use "')
        
    if whole_text.count("<") != whole_text.count(">"):
        print(f'NOTE: Notiser has a uneven amount of "<" and ">"')
    
    last_final_pos = whole_text.find("### ") # start at the first title aka the first "### "  
    for number_of_articles in range(whole_text.count("### ")): # repeat for how many hear me outs there are in the txt
        # find where diffrent parts are in the document
        title = find_between(whole_text, "### ", " ##", last_final_pos)
        if "++" in title:
            print(f'WARNING: {title} contains "++" in title which it should not have')
        if "##" in title:
            print(f'WARNING: {title} contains "##" in title which it should not have')
        if title == "":
            print(f'WARNING: {title} is empty')
        if title == "RUBRIK":
            print(f'WARNING: {title} is still template')
        article = find_between(whole_text, "+++ ", " ++", last_final_pos)
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
    whole_text = try_opening(hear_me_outs_path, "tr") # read it
    print("\n↓ HEAR ME OUTS ↓")
    if re.search(r"[“”]", whole_text): # if “ or ” in file, should be "
        print(f'NOTE: Hear me outs contains “ and/or ”. Instead you should use "')
        
    if whole_text.count("<") != whole_text.count(">"):
        print(f'NOTE: Hear me outs has a uneven amount of "<" and ">"')
    
    last_final_pos = whole_text.find("### ") # start at the first title aka the first "### "  
    for number_of_articles in range(whole_text.count("### ")): # repeat for how many hear me outs there are in the txt
        # find where diffrent parts are in the document
        hear_me_out = find_between(whole_text, "### ", " ##", last_final_pos)
        if "++" in hear_me_out:
            print(f'WARNING: {hear_me_out} contains "++" in hear me out which it should not have')
        if "##" in hear_me_out:
            print(f'WARNING: {hear_me_out} contains "##" in hear me out which it should not have')
        if hear_me_out == "":
            print(f'WARNING: {hear_me_out} is empty')
        if hear_me_out == "HEAR_ME_OUT":
            print(f'WARNING: {hear_me_out} is still template')
        desc = find_between(whole_text, "+++ ", " ++", last_final_pos)
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
    upplaga_list = os.listdir(normal_story_path) # list all folders in dir
    for upplaga in upplaga_list: # go thrpguth every folder to get all the upplagor
        # list all files in dir
        file_list = os.listdir(normal_story_path + handel_path_slash("\\") + upplaga)
        for file in file_list: # Go througth every file in the list
            if file[:4] != "IMG-":
                whole_text = try_opening(normal_story_path + handel_path_slash("\\") + upplaga + handel_path_slash("\\") + file, "tr")
                if re.search(r"[“”]", whole_text): # if “ or ” in file, should be "
                    new_text = whole_text.replace("“", '"')
                    new_text = new_text.replace("”", '"')
                    open_content = open(normal_story_path + handel_path_slash("\\") + upplaga + handel_path_slash("\\") + file, "w", encoding="utf-8")
                    open_content.write(new_text) # write to it
                    open_content.close()
                    
                    fixed_something = True
                    print(f"Fixed citationmark(s) in {file}")
                    
    if fixed_something == False:
        print("No citationmarks to fix in articles")

    # short storys
    fixed_something = False
    whole_text = try_opening(short_story_path, "tr") # read it
    if re.search(r"[“”]", whole_text): # if “ or ” in file, should be "
        new_text = whole_text.replace("“", '"')
        new_text = new_text.replace("”", '"')
        open_content = open(short_story_path, "w", encoding="utf-8")
        open_content.write(new_text) # write to it
        open_content.close()
        
        fixed_something = True
        print(f"Fixed citationmark(s) in notiser")
        
    if fixed_something == False:
        print("No citationmarks to fix in notiser")

    # hear me outs
    fixed_something = False
    whole_text = try_opening(hear_me_outs_path, "tr") # read it
    if re.search(r"[“”]", whole_text): # if “ or ” in file, should be "
        new_text = whole_text.replace("“", '"')
        new_text = new_text.replace("”", '"')
        open_content = open(hear_me_outs_path, "w", encoding="utf-8")
        open_content.write(new_text) # write to it
        open_content.close()
        
        fixed_something = True
        print(f"Fixed citationmark(s) in hear me outs")
        
    if fixed_something == False:
        print("No citationmarks to fix in hear me outs")

def fix_all_backend_articles_names(): # Make the names in articles more consistant
    upplaga_list = os.listdir(normal_story_path) # list all folders in dir
    for upplaga in upplaga_list: # go thrpguth every folder to get all the upplagor
        # list all files in dir 
        file_list = os.listdir(normal_story_path + handel_path_slash("\\") + upplaga)
        for file_number, file in enumerate(file_list, 1): # Go througth every file in the list and extract the content
            if file != "upplaga_info.txt" and file[:4] != "IMG-":
                # extract
                whole_text = try_opening(normal_story_path + handel_path_slash("\\") + upplaga + handel_path_slash("\\") + file, "tr")
                # find where title is in the document
                title = find_between(whole_text, "### ", " ##", 0)
                basic_title = remove_html_elements(title)
                
                new_file_name = str(file_number) + " " + strip_string(basic_title, 100) + ".txt"
                
                os.rename((normal_story_path + handel_path_slash("\\") + upplaga + handel_path_slash("\\") + file), (normal_story_path + handel_path_slash("\\") + upplaga + handel_path_slash("\\") + new_file_name))

    print("Article names successfully fixed!")

# SETUP TEMPLATES
def setup_new_upplaga_folder(day, month, year):
    next_upplaga_number = get_curant_upplaga_number()
    next_upplaga_number += 1 # so highest_upplaga_number is one higher than what exists
    new_path = normal_story_path + handel_path_slash("\\") + f"upplaga_{next_upplaga_number}" + handel_path_slash("\\") + "upplaga_info.txt"
    folder_path = normal_story_path + handel_path_slash("\\") + f"upplaga_{next_upplaga_number}"
    os.makedirs(folder_path, exist_ok=True) # generate the folder
    generated_file = open(new_path, "x", encoding="utf-8") # create / find the file
    content = f"""Upplaga: === {next_upplaga_number} ==
Datum: $$$ {day}-{month}-{year} $$
Extra info: ***  **"""
    generated_file.write(content) #write to it
    generated_file.close()
    
def setup_new_upplaga_articles(count_articles):
    next_upplaga_number = get_curant_upplaga_number()
    # all new articles
    for article_number in range(int(count_articles)):
        article_path = normal_story_path + handel_path_slash("\\") + f"upplaga_{next_upplaga_number}" + handel_path_slash("\\") + f"{article_number + 1} ARTICLE_NAME.txt"
        generated_file = open(article_path, "x", encoding="utf-8") # create / find the file
        content = f"""### RUBRIK ##
¤¤¤ ARTIKEL_TYP ¤¤
@@@ SKRIBENT @@
BRÖDTEXT"""
        generated_file.write(content) #write to it
        generated_file.close()
    
def setup_new_notiser(count_notiser, day, month, year):
    next_upplaga_number = get_curant_upplaga_number()
    for upplaga in reversed(read_normal_storys()):
        if upplaga["Upplaga"] > next_upplaga_number:
            highest_upplaga_number = upplaga["Upplaga"]
    edited_file = open(short_story_path, "a", encoding="utf-8") # create / find the file
    content = f"""


Upplaga {next_upplaga_number} ({day}/{month}/{year}):"""
    if int(count_notiser) == 0:
        content = "" # make so it doesnt say "Upplaga {highest_upplaga_number} ({day}/{month}/{year}):" if there are no notiser
    lone_content = f"""

### RUBRIK ##
+++ BRÖDTEXT ++"""
    # add right amount of notiser to new upplaga
    for notis_number in range(int(count_notiser)):
        content += lone_content
    
    edited_file.write(content) #write to it
    edited_file.close()

    print(f"Generated template for upplaga {next_upplaga_number}")
    
def setup_new_hear_me_outs(count_hear_me_outs):
    edited_file = open(hear_me_outs_path, "a", encoding="utf-8") # create / find the file
    content = ""
    lone_content = f"""

### HEAR_ME_OUT ##
+++ BESKRIVNING ++"""
    # add right amount of notiser to new upplaga
    for hear_me_out_number in range(int(count_hear_me_outs)):
        content += lone_content
    
    edited_file.write(content) #write to it
    edited_file.close()
    
    print(f"Generated template hear me outs")


# GENERATE SITES
index_template_path = work_path(r"\ostraloken\ostraloken.se\templates\index.html")
index_generated_path = work_path(r"\ostraloken\ostraloken.se\webbpage\index.html")

article_template_path = work_path(r"\ostraloken\ostraloken.se\templates\articles_pages.html")
generated_articles_path = work_path(r"\ostraloken\ostraloken.se\webbpage\a" + "\\")

short_storys_template_path = work_path(r"\ostraloken\ostraloken.se\templates\notiser.html")
short_storys_generated_path = work_path(r"\ostraloken\ostraloken.se\webbpage\notiser\index.html")

hear_me_outs_template_path = work_path(r"\ostraloken\ostraloken.se\templates\hear_me_outs.html")
hear_me_outs_generated_path = work_path(r"\ostraloken\ostraloken.se\webbpage\hear_me_outs\index.html")

pdfer_template_path = work_path(r"\ostraloken\ostraloken.se\templates\pdfer.html")
pdfer_generated_path = work_path(r"\ostraloken\ostraloken.se\webbpage\pdfer\index.html")
nav_template_path = work_path(r"\ostraloken\ostraloken.se\templates\nav.html")
nav_generated_path = work_path(r"\ostraloken\ostraloken.se\webbpage\nav\index.html")
omoss_template_path = work_path(r"\ostraloken\ostraloken.se\templates\omoss.html")
omoss_generated_path = work_path(r"\ostraloken\ostraloken.se\webbpage\omoss\index.html")
kontakt_template_path = work_path(r"\ostraloken\ostraloken.se\templates\kontakt.html")
kontakt_generated_path = work_path(r"\ostraloken\ostraloken.se\webbpage\kontakt\index.html")

utforska_template_path = work_path(r"\ostraloken\utforska.ostraloken.se\templates\index.html")
utforska_generated_path = work_path(r"\ostraloken\utforska.ostraloken.se\webbpage\index.html")

# images
def find_img(article_title, upplaga_nmr, base_url):
    all_img_title = "IMG-" + strip_string(article_title, 100)
    old_img_path_no_extention = normal_story_path + handel_path_slash("\\") + f"upplaga_{upplaga_nmr}" + handel_path_slash("\\") + all_img_title
    for ext in img_extentions:
        if os.path.isfile(f"{old_img_path_no_extention}.{ext}") is True:
            old_img_path_with_extention = f"{old_img_path_no_extention}.{ext}"
            break
    else:
        old_img_path_with_extention = "NO_IMG" # article does not have image
        
    if old_img_path_with_extention != "NO_IMG":
        return base_url + all_img_title + ".webp"
    else:
        return ""

def copy_over_images(gen_type):
    # go throught every upplaga
    for upplaga in read_normal_storys():
        # go throught every article in the upplaga
        upplaga_number = upplaga["Upplaga"]
        for article in upplaga["Content"]:
            if article: # somethimes article is empty, this prevents that
                article_title = str(article["Title"])
                all_img_title = "IMG-" + strip_string(remove_html_elements(article_title), 100)
                old_img_path_no_extention = normal_story_path + handel_path_slash("\\") + f"upplaga_{upplaga_number}" + handel_path_slash("\\") + all_img_title
                new_img_url_with_extention = generated_articles_path + handel_path_slash("images\\") + all_img_title + ".webp"
                for ext in img_extentions:
                    if os.path.isfile(f"{old_img_path_no_extention}.{ext}") is True:
                        old_img_path_with_extention = f"{old_img_path_no_extention}.{ext}"
                        break
                else:
                    old_img_path_with_extention = "NO_IMG" # article does not have image
                    
                if old_img_path_with_extention != "NO_IMG":
                    # if all and no file: YES
                    # if all and file: YES
                    # if new and no file: YES
                    # if new and file: NO
                    if gen_type != "new" or os.path.isfile(new_img_url_with_extention) is False: # either gen_typ isn't new, or if it is, we still let it pass if there is no file
                        create_image_switch = False
                        if "specific" in gen_type:
                            desired_upplaga_nmr = gen_type.split(": ")[1]
                            if int(upplaga_number) == int(desired_upplaga_nmr):
                                create_image_switch = True
                        else:
                            create_image_switch = True

                        if create_image_switch:
                            image = Image.open(old_img_path_with_extention)
                            img_width, img_height = image.size
                            new_width = 1000
                            new_height = int((new_width / img_width) * img_height)
                            new_image = image.resize((new_width, new_height))
                            new_image.save(new_img_url_with_extention, quality=80)
                            print(f"copied image: {all_img_title}")
                    else: # gen type == "new" and os.path.isfile(new_img_url_with_extention) is True
                        pass
    else:
        print("No images left to copy")

# basic for all generated text files
def generate_site(template_path, generated_path, dictionary_of_replacment): # the sites that dont realy need to be generated
    # pdf:er
    template = try_opening(template_path, "")
    
    final_file = template
    for item in dictionary_of_replacment:
        final_file = final_file.replace(str(item), str(dictionary_of_replacment[item]))
    
    # add something to notify the user that it is editing in the generated file instead of templates
    row_endings = ["<head>", "</head>", "<body>", "</body>", "<header>", "</header>", "<main>", "</main>", "<footer>", "</footer>"]
    for ending in row_endings:
        final_file = final_file.replace(str(ending), f"{ending} <!--ATTENTION: YOU ARE RIGHT NOW IN THE GENERATED FILE!-->")
    
    generated_file = open(generated_path, "w", encoding="utf-8") # create / find the file
    generated_file.write(final_file) # write to it
    generated_file.close()

# articles
def generate_lone_article(redirect_src, img_src, title, content, type, author, article_nmr, upplaga_nmr):
    # if you dont want a ancor redirecting to be generated, set redirect_src to "SHOULD_NOT_REDIRECT"
    if redirect_src is None or redirect_src == "":
        redirect_src = "./" # hide image
    if img_src is None or img_src == "" or img_src == "NO_IMAGE_AVAILABLE":
        no_img_class = "no_img"
        image_context = "<!-- NO IMAGE HERE -->"
    else:
        no_img_class = ""
        image_extra = f'alt="{strip_string(title, -1).replace("_", " ")}"' # add the alt text
        if article_nmr != 0: # this is so the first image dosn't have loading lazy so it dosnt pop in
            image_extra += ' loading="lazy"'
        else:
            image_extra += ' fetchpriority="high"'
            
        image_context = f'<img src="{img_src}" {image_extra} width="800" height="600">'
    if title is None or title == "":
        title = "Null"
    if content is None or content == "":
        content = "Null"
    if type is None or type == "":
        type_context = "<!-- NO TYPE HERE -->"
    else:
        type_context = f'<p class="type_text">{type}</p>'
        
    # generate the article id
    article_id = strip_string(remove_html_elements(title), -1)[:100] + "-U" + str(upplaga_nmr)
    # We strip the title of any unwanted caracters and replace spaces with _. Then we do the same to the author but only the first 15 caracters and last we add type if there is any caracters left since it then cuts of so its only combinend 100 caracters
    
    if redirect_src == "SHOULD_NOT_REDIRECT": # Not anchor
        author_context = f'<p class="author_text"><b>{author}</b></p>'
        
        # list Löken head writers
        head_writers = ["Vilhelm Grill", "Joar Stange", "John Ericson", "Magne Nordström", "Elliot Sandström"]
        # if author is one of head Löken writers: point their name to their part of kontaktinfo 
        if author in head_writers:
            author_context = f'<p class="author_text"><a href="https://ostraloken.se/kontakt/#{author.replace(" ", "_")}"><b>{author}</b></a></p>'
        
        final_article = f"""<article id="{article_id}" class="article {no_img_class}"> <!--Add the "no_img" class to article if it has no image-->
            {type_context}
            {image_context}
            <h1>{title}</h1> <!-- This is the h1 since nothing else is on this page -->
            <p>{content}</p>
            {author_context}
        </article>
        """
    else: # make article not anchor
        final_article = f"""<a href="{redirect_src}" id="{article_id}" class="article {no_img_class}"> <!--Add the "no_img" class to article if it has no image-->
                <article>
                    {type_context}
                    {image_context}
                    <h2>{title}</h2>
                    <p>{content}</p>
                    <p class="author_text"><b>{author}</b></p>
                </article>
            </a>
            """

    return final_article

def generate_preview_article(find_similar_articles_switch):
    how_many_articles_generated = 0
    generated_articles = [] # for find_similar_articles == False
    generated_articles_based_on_type = {} # for find_similar_articles == True
    
    for upplaga in reversed(read_normal_storys()):
        upplaga_number = upplaga["Upplaga"]
        content = upplaga["Content"]
        if content: # if there is content, content is the text, title, type and author
            for article in content:
                extra_at_end = ""
                article_title = article["Title"]
                basic_article_title = remove_html_elements(article_title)
                org_article_title = basic_article_title # so that even if title is shortend, it is still the same URL
                # shorten down article titles over 70 characters
                if len(basic_article_title) >= 70:
                    if ">" in article_title:
                        if article_title[30:].find(">") == -1: # if there is no ">" in the first 30 characters
                            title_end_pos = article_title.find(">")
                        else:
                            title_end_pos = int(article_title[30:].find(">")) + 30
                        basic_article_title = basic_article_title[:title_end_pos] + fix_cut_of_html_elements(basic_article_title) + "..." # add back any cut of html elements
                    else:
                        basic_article_title = basic_article_title[:70] + fix_cut_of_html_elements(basic_article_title) + "..."
                
                article_main_text = article["Article"][:400]
                # remove any bolding
                if "<b>" in article_main_text:
                    article_main_text = article_main_text.replace("<b>", "")
                    article_main_text = article_main_text.replace("</b>", "")
                    
                # find the last character
                article_main_text_last_caracter_pos = 400 # if no . ? ! : ; or <br> is found: this is used and we cut at the 400:th character
                article_main_text_last_caracter_match = re.search(r"\.|\?|\!|\:|\;", article_main_text[200:]) # this finds a . ? ! : or ; in the last 200-400 characters
                if article_main_text_last_caracter_match:
                    article_main_text_last_caracter_pos = article_main_text_last_caracter_match.start() + 200 # .start() gives position at cut, we add 200 since article_main_text was started on 200
                    
                    # se if its closed by a <br> before the . ? ! : or ;
                    if article_main_text[:article_main_text_last_caracter_pos].find("<br>") != -1: # if <br> exists
                        end_characters = [".", "?", "!", ":", ";"]
                        for character in end_characters: # so that it only removes the last character if it is one of . ? ! : or ;
                            if character == article_main_text[article_main_text.find("<br>") - 1]:
                                article_main_text_last_caracter_pos = article_main_text.find("<br>") - 1 # do -1 since we know that it only does it if there is a . ? ! : or ; before
                                break
                        else:
                            article_main_text_last_caracter_pos = article_main_text.find("<br>")
                else:
                    if article_main_text.find("<br>") != -1: # if <br> exists
                        break_pos = article_main_text.find("<br>")
                        article_main_text_last_caracter_pos = break_pos
                
                # the text cut of at the right place
                shorted_main_text = article_main_text[:article_main_text_last_caracter_pos]
                            
                # add back any cut of html elements
                extra_at_end = fix_cut_of_html_elements(shorted_main_text)
                                    
                article_type = article["Type"]
                article_author = article["Writer"]
                
                # not basic_title since that has been shortend alredy
                article_id = strip_string(org_article_title, -1)[:100] + "-U" + str(upplaga_number) # what is used to identefy the article

                if find_similar_articles_switch is False:
                    img_url = find_img(org_article_title, upplaga_number, "./a/images/") # get the url to the img as a html link
                    generated_articles.append(generate_lone_article(("./a/" + article_id + ".html"), img_url, article_title, (shorted_main_text + extra_at_end + "..."), article_type, article_author, how_many_articles_generated, upplaga_number))
                    how_many_articles_generated += 1
                else:
                    # img_url = find_img(org_article_title, upplaga_number, "./images/") # get the url to the img as a html link
                    if article_type not in generated_articles_based_on_type:
                        generated_articles_based_on_type[article_type] = {} # initialize generated_articles_based_on_type[article_type]
                    generated_articles_based_on_type[article_type].update({article_id: generate_lone_article(("./" + article_id + ".html"), None, article_title, (shorted_main_text + extra_at_end + "..."), None, article_author, -1, upplaga_number)})
                    how_many_articles_generated += 1
    if find_similar_articles_switch is False:
        return generated_articles
    else:
        return generated_articles_based_on_type

def generate_index(): # PS images are copyd here
    list_of_generated_articles = generate_preview_article(False)
    all_generated_articles = ""
    for generated_articles in list_of_generated_articles:
        all_generated_articles += str(generated_articles)

    # get the top story
    latest_title = ""
    for upplaga in read_normal_storys():
        content = upplaga["Content"]
        if content: # if there is content, content is the text, title, type and author
            for order_number, article in enumerate(content):
                if order_number == 0:
                    latest_title = remove_html_elements(article["Title"])
    
    replacment = {"[+articles+]": all_generated_articles, "[+latest_title+]": latest_title.replace('"', "&quot;")} # what gets replaced and with what
    generate_site(index_template_path, index_generated_path, replacment)
    
    print("Index successfully generated!")

def generate_all_articles(): # PS images are also copyd here
    list_of_articles_with_similer_type = generate_preview_article(True)
    
    print("Generating all articles:")
    progressbar_item = progressbar.ProgressBar(maxval=int(len(read_normal_storys())))
    progressbar_item.start()
    
    # go throught every upplaga
    for progressbar_ticker, upplaga in enumerate(read_normal_storys()):
        # go throught every article in the upplaga
        upplaga_number = upplaga["Upplaga"]
        upplaga_date = upplaga["Release_date"]
        upplaga_extra_info = upplaga["Extra_upplaga_info"]
        progressbar_item.update(progressbar_ticker + 1)
        for article in upplaga["Content"]:
            if article: # somethimes article is empty, this prevents that
                generated_article = "" # where we put the article
                has_extra_info = False
                
                # this is done early so it is over the article itself
                if upplaga_extra_info != "" and upplaga_extra_info != None and has_extra_info == False:
                    has_extra_info = True
                    # add the extra content
                    generated_article += f""" 
        <div class="article extra_info attention">
            <p><b>Notera:</b> {upplaga_extra_info}</p>
        </div>
        
        """        
                article_title = str(article["Title"])
                basic_article_title = remove_html_elements(article_title)
                article_main_text = str(article["Article"])
                article_type = str(article["Type"])
                article_author = str(article["Writer"])
                # copy over images and get the url to the right image
                article_img_src = find_img(basic_article_title, upplaga_number, "./images/")
                generated_article += generate_lone_article("SHOULD_NOT_REDIRECT", article_img_src, article_title, article_main_text, article_type, article_author, 0, upplaga_number)
            
                # generate the article id
                article_id = strip_string(remove_html_elements(article_title), -1)[:100] + "-U" + str(upplaga_number)
            
                if article_type == "Insändare" and has_extra_info == False: # this is "else if" so that it cant both have extra upplaga info and a write-a-insändare prompt
                    has_extra_info = True
                    # add prompt to write insändare if it is a insändare
                    generated_article += """ 
        <a class="article extra_info user_prompt" href="https://forms.gle/bBiEhDSCFijSFoHk9" target="_blank">
            <h2>Skicka in en insändare!</h2>
            <p>Vill du också skicka en insändare till Östra Löken? Fyll bara i denna korta enkät!</p>
        </a>
        """
                
                replacment = {
                    "[+description+]": remove_html_elements(article_main_text)[:200].replace('"', "&quot;") + "...",
                    "[+url+]": f"https://ostraloken.se/a/{article_id}.html",
                    "[+home_url+]": "../#" + article_id,
                    "[+title+]": article_title.replace('"', "&quot;"),
                    "[+title_basic+]": remove_html_elements(article_title).replace('"', "&quot;"),
                    "[+article_type+]": article_type,
                    "[+article_type_basic+]": remove_html_elements(article_type),
                    "[+article_author+]": article_author,
                    "[+article_author_basic+]": remove_html_elements(article_author),
                    "[+upplaga_date_ISO_8601+]": f"{upplaga_date.split("-")[2]}-{upplaga_date.split("-")[1].zfill(2)}-{upplaga_date.split("-")[0].zfill(2)}",
                    "[+article+]": generated_article,
                    "[+upplaga_number+]": str(upplaga_number),
                    "[+upplaga_date+]": upplaga_date,
                    "[+h3_text_to_intorduce_section+]": "<h3>Läs liknande artiklar:</h3>", # so it can be removed
                    "[+thumb_image_url+]": "https://ostraloken.se/images/meta/Östra_Löken_webbsida_cover_image.png" # basic backup image
                } # what gets replaced and with what
                
                if article_img_src is not None and article_img_src != "": # make image in preview to the article image if one exists
                    replacment["[+thumb_image_url+]"] = f"https://ostraloken.se/a/images/IMG-{article_id}.webp"
                
                # generate extra articles
                dict_of_similar_articles = dict(list_of_articles_with_similer_type)[article_type]
                dict_of_similar_articles_copy = dict_of_similar_articles.copy() # we do this so we can edit it without changing the original
                dict_of_similar_articles_copy.pop(article_id) # remove the article (the one you are adding "read also" too) from the dict
                new_list_of_similar_articles = list(dict_of_similar_articles_copy.values())
                if new_list_of_similar_articles != []:
                    random.seed(str(new_list_of_similar_articles) + "1") # we set the seed so that if we are to make a small change and push it it doesnt change everything, only when we add, remove or change articles of that type does this change
                    chosen_article = new_list_of_similar_articles[random.randint(0, len(new_list_of_similar_articles) - 1)] # this random function is determaistic so if we enter the same seed and same command it will give the same result which we want!
                    replacment[f"[+extra_article_link_1+]"] = chosen_article
                    new_list_of_similar_articles.remove(chosen_article) # we remove it so it isn't listed again
                    
                    if new_list_of_similar_articles != []:
                        random.seed(str(new_list_of_similar_articles) + "2")
                        chosen_article = new_list_of_similar_articles[random.randint(0, len(new_list_of_similar_articles) - 1)]
                        replacment[f"[+extra_article_link_2+]"] = chosen_article
                        new_list_of_similar_articles.remove(chosen_article)
                        
                        if new_list_of_similar_articles != []:
                            random.seed(str(new_list_of_similar_articles) + "3")
                            chosen_article = new_list_of_similar_articles[random.randint(0, len(new_list_of_similar_articles) - 1)]
                            replacment[f"[+extra_article_link_3+]"] = chosen_article
                            random.seed()
                        else:
                            replacment[f"[+extra_article_link_3+]"] = ""
                    else:
                        replacment[f"[+extra_article_link_2+]"] = ""
                        replacment[f"[+extra_article_link_3+]"] = ""
                else:
                    replacment["[+h3_text_to_intorduce_section+]"] = "" # make so there is no h3 text if there are no extra links
                    replacment[f"[+extra_article_link_1+]"] = ""
                    replacment[f"[+extra_article_link_2+]"] = ""
                    replacment[f"[+extra_article_link_3+]"] = ""
                
                generate_site(article_template_path, (generated_articles_path + article_id + ".html"), replacment)
    
    progressbar_item.finish()
    print("All articles successfully generated!")

# short storys
def generate_lone_short_storys(title, content):
    if title is None or title == "":
        title = "Null"
    if content is None or content == "":
        content = "Null"
        
    final_article = f"""<article class="article">
                <h2>{title}</h2>
                <p>{content}</p>
            </article>
            """
        
    return final_article

def generate_short_storys():
    generated_short_story = ""
    
    for short_story_bundle in reversed(read_short_storys()):
        content = short_story_bundle["Content"]
        if content:
            article_title = content["Title"]
            article_main_content = content["Article"]
            generated_short_story += generate_lone_short_storys(article_title, article_main_content)
    
    replacment = {"[+short_storys+]": generated_short_story} # what gets replaced and with what
    generate_site(short_storys_template_path, short_storys_generated_path, replacment)
    
    print("Short storys successfully generated!")

# hear me outs
def generate_lone_hear_me_out(hear_me_out, description):
    if hear_me_out is None or hear_me_out == "":
        hear_me_out = "Null"
    if description is None:
        description = "Null"
    if description != "":
        description = "<b>Förklaring:</b> " + description
    
    if len(hear_me_out) > 70:
        hear_me_out = hear_me_out[:70] + "..."
        
    if len(description) > 500:
        description = description[:500] + "..."
    
    final_article = f"""<article class="article">
            <h2>{hear_me_out}</h2>
            <p>{description}</p>
            <div class="smash_pass_area">
                <button class="smash_button"><i>SMASH</i></button>
                <button class="pass_button"><i>PASS</i></button>
            </div>
        </article>
        """
        
    return final_article

def generate_hear_me_outs():
    generated_hear_me_out = ""
    
    for hear_me_out_bundle in reversed(read_hear_me_outs()):
        content = hear_me_out_bundle["Content"]
        if content:
            article_hear_me_out = content["Hear_me_out"]
            article_desc = content["Description"]
            generated_hear_me_out += generate_lone_hear_me_out(article_hear_me_out, article_desc)
    
    replacment = {"[+hear_me_outs+]": generated_hear_me_out} # what gets replaced and with what
    generate_site(hear_me_outs_template_path, hear_me_outs_generated_path, replacment)
    
    print("Hear me outs successfully generated!")

# the rest in main webbpage
def copy_non_changing_sites():
    replacment_all = {}
    
    # PDF:er
    generate_site(pdfer_template_path, pdfer_generated_path, replacment_all)
    print("PDF:s successfully copy:d!")
    
    # Nav
    generate_site(nav_template_path, nav_generated_path, replacment_all)
    print("Nav successfully copy:d!")

    # Om oss
    generate_site(omoss_template_path, omoss_generated_path, replacment_all)
    print("Om oss successfully copy:d!")
    
    # Kontakt
    generate_site(kontakt_template_path, kontakt_generated_path, replacment_all)
    print("Kontakt successfully copy:d!")

# utforska
def generate_utforska():

    
    print("Utforska successfully generated!")


# UI for backend user
def handle_backend_UI():
    global base_path
    
    print("Welcome to the backend terminal!")
    print('(Print "help" for commands)')
    while True:
        answer = input("$ ")
        try:
            if answer == "help":
                print("""
    $ help --> Lists all commands
    $ close --> Terminate script
    
    TEMPLATES
    $ new upplaga template --> Generates a new upplaga template with articles, notiser and hear me outs
    
    GENERATE TEXT FILES
    $ gen all --> Generate all webbpage files that are generated
    
    $ gen index --> Generate just the index file
    $ gen hear me outs --> Generate just the hear me outs file
    $ gen notiser --> Generate just the notiser file
    $ gen articles --> Generate just all the article files
    $ gen not changing --> Generate just the non-changing files
    
    COPY IMAGES
    $ copy images new --> Copy over only the new images
    $ copy images all --> Copy over all images, even if they alredy exists
    $ copy images specific --> Copy over all images in a specific upplaga
    
    FIX CONTENT
    $ inspect --> Looks through content so everything is as it should be, if not: it is reported   
    $ fix citationmarks --> Replace all “ and ” with ", as they should be
    $ fix article names --> Rename normal storys to their title (keeping them in the same order)
 
    OTHER
    $ get dir --> Print the currant base dir
    $ set dir --> Set the base dir
                    """)
            elif answer == "close":
                break
            
            # new content
            elif answer == "new upplaga template":
                amount_of_articles = input("Amount articles: ")
                if amount_of_articles is None or amount_of_articles == "" or not re.search(r"[0-9]", amount_of_articles):
                    amount_of_articles = 0
                amount_of_notiser = input("Amount notiser: ")
                if amount_of_notiser is None or amount_of_notiser == "" or not re.search(r"[0-9]", amount_of_notiser):
                    amount_of_notiser = 0
                amount_of_hear_me_outs = input("Amount hear me outs: ")
                if amount_of_hear_me_outs is None or amount_of_hear_me_outs == "" or not re.search(r"[0-9]", amount_of_hear_me_outs):
                    amount_of_hear_me_outs = 0
                    
                day = input("Day of release: ")
                if day is None or day == "" or not re.search(r"[0-9]", day):
                    day = "DD"
                month = input("Month of release: ")
                if month is None or month == "" or not re.search(r"[0-9]", month):
                    month = "MM"
                year = input("Year of release: ")
                if year is None or year == "" or not re.search(r"[0-9]", year):
                    year = "ÅÅÅÅ"
                    
                setup_new_upplaga_folder(day, month, year)
                setup_new_upplaga_articles(amount_of_articles)
                setup_new_notiser(amount_of_notiser, day, month, year)
                setup_new_hear_me_outs(amount_of_hear_me_outs)
            
            # generate text files
            elif answer == "gen all":
                generate_index()
                generate_hear_me_outs()
                generate_short_storys()
                generate_all_articles()
                copy_non_changing_sites()
            elif answer == "gen index":
                generate_index()
            elif answer == "gen hear me outs":
                generate_hear_me_outs()
            elif answer == "gen notiser":
                generate_short_storys()
            elif answer == "gen articles":
                generate_all_articles()
            elif answer == "gen not changing":
                generate_all_articles()
                
            # images
            elif answer == "copy images new":
                copy_over_images("new")
            elif answer == "copy images all":
                copy_over_images("all")
            elif answer == "copy images specific":
                upplaga_to_copy = input("Copy over images in upplaga: ")
                if re.search(r"[0-9]", upplaga_to_copy):
                    copy_over_images(f"specific: {upplaga_to_copy}")
                else:
                    print(f"{upplaga_to_copy} not a number")
                    
            # fix content
            elif answer == "inspect":
                inspect_normal_storys()
                inspect_short_storys()
                inspect_hear_me_outs()
            elif answer == "fix citationmarks":
                fix_citationmarks()
            elif answer == "fix article names":
                fix_all_backend_articles_names()
                
            # other
            elif answer == "get dir":
                print(base_path)
            elif answer == "set dir":
                base_path = input("New dir: ")
                
            else:
                if answer != "":
                    print(f'"{answer}" is not a command')
        except Exception as e:
            print(f"ERROR: {e}")

handle_backend_UI()

r"""
Saker att lägga till
- sökfunktion
- gör tinder av hear me outs

Att fixa senare:
- Alla artiklar innan upplaga 11-5 ska dubbelkollas om artikeln är samma i pdf som text
"""