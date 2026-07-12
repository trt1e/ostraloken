import os
import re
import random
from PIL import Image
import shutil
import progressbar

is_linux = False

global base_path
base_path = os.getcwd()
img_extentions = ["jpg", "JPG", "jpeg", "JPEG", "png", "PNG", "webp"]

# ---------------------------------
# BASE COMMANDS
# ---------------------------------

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

def make_article_id(article_title, upplaga_number):
    id_article = strip_string(remove_html_elements(article_title), 100)
    replace_letters = {"å": "a", "Å": "A", "ä": "a", "Ä": "A", "ö": "o", "Ö": "O"}
    for letter in replace_letters:
        if letter in id_article:
            id_article = id_article.replace(letter, replace_letters[letter])
    id_upplaga = "-U" + str(upplaga_number)
    return id_article + id_upplaga

def make_short_story_id(article_title, article_content):
    replace_letters = {"å": "a", "Å": "A", "ä": "a", "Ä": "A", "ö": "o", "Ö": "O"}
    
    id_article = strip_string(remove_html_elements(article_title), 60)
    id_content = strip_string(remove_html_elements(article_content), 120)
    for letter in replace_letters:
        if letter in id_article:
            id_article = id_article.replace(letter, replace_letters[letter])
        if letter in id_content:
            id_content = id_content.replace(letter, replace_letters[letter])

    return id_article + "+" + id_content

def make_image_id(article_title, remove_åäö):
    id = "IMG-" + strip_string(remove_html_elements(article_title), 100)
    if remove_åäö:
        replace_letters = {"å": "a", "Å": "A", "ä": "a", "Ä": "A", "ö": "o", "Ö": "O"}
        for letter in replace_letters:
            if letter in id:
                id = id.replace(letter, replace_letters[letter])
    return id


# ---------------------------------
# READ TEXT
# ---------------------------------

normal_story_path = work_path(r"\ostraloken\backend\content\normal_storys_and_other")
short_story_path = work_path(r"\ostraloken\backend\content\short_storys.txt")
hear_me_outs_path = work_path(r"\ostraloken\backend\content\hear_me_outs.txt")

staff_info_path = work_path(r"\ostraloken\backend\content\static\staff.txt")
static_articles_path = work_path(r"\ostraloken\backend\content\static\articles.txt")
external_links_content_path = work_path(r"\ostraloken\backend\content\static\external_links.txt")

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

def read_staff_info_content(): # To get the staff info
    whole_text = try_opening(staff_info_path, "tr") # read it
    last_final_pos = whole_text.find("### ") # start at the first title aka the first "### "  
    output_sum = []
    for number_of_articles in range(whole_text.count("### ")): # repeat for how many bits of content there are in the txt
        # find where diffrent parts are in the document
        name = find_between(whole_text, "### ", " ##", last_final_pos)
        desc = find_between(whole_text, "+++ ", " ++", last_final_pos)
        title = find_between(whole_text, '""" ', ' ""', last_final_pos)
        email = find_between(whole_text, "@@@ ", " @@", last_final_pos)
        image_src = find_between(whole_text, "§§§ ", " §§", last_final_pos)
        last_final_pos = whole_text.find(" §§", last_final_pos) + 3
        
        output = {"Name": name, "Description": desc, "Title": title, "Email": email, "Image_src": image_src}
        output_sum.append(output)
        
    return output_sum

def read_static_content(): # To get the content of the the static informational text to be placed in
    whole_text = try_opening(static_articles_path, "tr") # read it
    last_final_pos = whole_text.find("### ") # start at the first title aka the first "### "  
    output_sum = []
    for number_of_articles in range(whole_text.count("### ")): # repeat for how many bits of content there are in the txt
        # find where diffrent parts are in the document
        title = find_between(whole_text, "### ", " ##", last_final_pos)
        article = find_between(whole_text, "+++ ", " ++", last_final_pos)
        image_src = find_between(whole_text, "§§§ ", " §§", last_final_pos)
        last_final_pos = whole_text.find(" §§", last_final_pos) + 3
        
        output = {"Title": title, "Article": article, "Image_src": image_src}
        output_sum.append(output)
        
    return output_sum

def read_external_links_content(): # To get the external liks in länk nav
    whole_text = try_opening(external_links_content_path, "tr") # read it
    last_final_pos = whole_text.find("### ") # start at the first title aka the first "### "  
    output_sum = []
    for number_of_articles in range(whole_text.count("### ")): # repeat for how many bits of content there are in the txt
        # find where diffrent parts are in the document
        title = find_between(whole_text, "### ", " ##", last_final_pos)
        link = find_between(whole_text, "@@@ ", " @@", last_final_pos)
        image_src = find_between(whole_text, "§§§ ", " §§", last_final_pos)
        important_statment = find_between(whole_text, "!!! ", " !!", last_final_pos)
        last_final_pos = whole_text.find(" !!", last_final_pos) + 3
        
        output = {"Title": title, "Link": link, "Image_src": image_src, "Important": important_statment}
        output_sum.append(output)
        
    return output_sum

# ---------------------------------
# FIX ARTICLES
# ---------------------------------

############### ADD CHECKING STATIC AND PDFS HERE!!! #################

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


# ---------------------------------
# SETUP TEMPLATES
# ---------------------------------

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


# ---------------------------------
# GENERATE SITES
# ---------------------------------

# images
def find_img(article_title, upplaga_nmr, base_url):
    old_img_title = make_image_id(article_title, False)
    new_img_title = make_image_id(article_title, True)
    old_img_path_no_extention = normal_story_path + handel_path_slash("\\") + f"upplaga_{upplaga_nmr}" + handel_path_slash("\\") + old_img_title
    for ext in img_extentions:
        if os.path.isfile(f"{old_img_path_no_extention}.{ext}") is True:
            old_img_path_with_extention = f"{old_img_path_no_extention}.{ext}"
            break
    else:
        old_img_path_with_extention = "NO_IMG" # article does not have image
        
    if old_img_path_with_extention != "NO_IMG":
        return base_url + new_img_title + ".webp"
    else:
        return ""

def copy_over_images(gen_type):
    generated_images_path = work_path(r"\ostraloken\ostraloken.se\webbpage\a\images" + "\\")
    
    # go throught every upplaga
    for upplaga in read_normal_storys():
        # go throught every article in the upplaga
        upplaga_number = upplaga["Upplaga"]
        for article in upplaga["Content"]:
            if article: # somethimes article is empty, this prevents that
                article_title = str(article["Title"])
                old_img_title = make_image_id(article_title, False)
                new_img_title = make_image_id(article_title, True)
                old_img_path_no_extention = normal_story_path + handel_path_slash("\\") + f"upplaga_{upplaga_number}" + handel_path_slash("\\") + old_img_title
                new_img_url_with_extention = generated_images_path + new_img_title + ".webp"
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
                            print(f"copied image: {new_img_title}")
                    else: # gen type == "new" and os.path.isfile(new_img_url_with_extention) is True
                        pass
    else:
        print("No images left to copy")

# Copy pdf:s
def copy_over_pdfs(gen_type):
    pdf_start_path = work_path(r"\ostraloken\backend\content\pdfs" + "\\")
    pdf_end_path = work_path(r"\ostraloken\ostraloken.se\webbpage\pdfer\pdfs" + "\\")
    
    amount_of_pdfs = 0
    pdfs_list = os.listdir(pdf_start_path)
    
    for file_dir in pdfs_list:
        amount_of_pdfs += 1
        
        full_start_file_dir = pdf_start_path + file_dir
        full_end_file_dir = pdf_end_path + file_dir
        
        copy_file_switch = False
        
        if gen_type != "new" or os.path.isfile(full_end_file_dir) is False:
            if "specific" in gen_type:
                desired_upplaga_nmr = gen_type.split(": ")[1]
                upplaga_number = file_dir.split("Östra_Löken_upplaga_")[1].split(".pdf")[0]
                if int(upplaga_number) == int(desired_upplaga_nmr):
                    copy_file_switch = True
            else:
                copy_file_switch = True

        if copy_file_switch:
            shutil.copyfile(full_start_file_dir, full_end_file_dir)
            
            print(f"copied pdf {file_dir}")
    else:
        print("No pdf:s left to copy")
        
    # change the PDFjs_reader.js in the /pdfer/js/ folder so that it has the correct amount of pdfs listed
    pdf_js_program_path = work_path(r"\ostraloken\ostraloken.se\webbpage\pdfer\js\PDFjs_reader.js")
    
    # get the content
    js_file_content = try_opening(pdf_js_program_path, "tr") # read it
    
    # change the number
    js_changed_content = re.sub(r"const amoutPDfs = \d+", f"const amoutPDfs = {amount_of_pdfs}", js_file_content)
    
    changed_js_file = open(pdf_js_program_path, "w", encoding="utf-8") # create / find the file
    changed_js_file.write(js_changed_content) # write to it
    changed_js_file.close()
    

# basic for all generated text files
def generate_site(template_path, generated_path, dictionary_of_replacment, file_type): # the sites that dont realy need to be generated    
    template = try_opening(template_path, "")
    
    final_file = template
    for item in dictionary_of_replacment:
        final_file = final_file.replace(str(item), str(dictionary_of_replacment[item]))
    
    # add something to notify the user that it is editing in the generated file instead of templates
    row_endings = []
    start_warning = ""
    end_warning = ""
    if file_type == "html":
        row_endings = ["<head>", "</head>", "<body>", "</body>", "<header>", "</header>", "<main>", "</main>", "<footer>", "</footer>"]
        start_warning = "<!--"
        end_warning = "-->"
    elif file_type == "css" or file_type == "js":
        row_endings = ["{"]
        start_warning = "/*"
        end_warning = "*/"
    
    for ending in row_endings:
        final_file = final_file.replace(str(ending), f"{ending} {start_warning}ATTENTION: YOU ARE RIGHT NOW IN A GENERATED FILE!{end_warning}")
    
    # add header
    header_read = get_header()
    final_file = final_file.replace("[+header+]", header_read) # add header
    final_file = final_file.replace("[+index_header+]", header_read.replace("../", "./")) # add header for specificly index
    
    # add footer
    final_file = final_file.replace("[+footer+]", get_footer()) # add footer
    
    # add general scripts
    scripts_read = get_general_scripts()
    final_file = final_file.replace("[+general_scripts+]", scripts_read)
    final_file = final_file.replace("[+index_general_scripts+]", scripts_read.replace("../", "./")) # add scripts for specificly index
    
    generated_file = open(generated_path, "w", encoding="utf-8") # create / find the file
    generated_file.write(final_file) # write to it
    generated_file.close()

# static articles
def generate_static_section(title, content, image_src):
    if title is None or title == "":
        title = "Null"
    if content is None or content == "":
        content = "Null"
    if image_src is None or image_src == "":
        image_context = "<!-- NO IMAGE HERE -->"
    else:
        image_context = f'<img src="{image_src}" alt="{image_src}" width="800" height="600">'
    
    final_article = f"""
<article class="article" id="{title.replace(" ", "_")}">
    {image_context}
    <h2>{title}</h2>
    <p class="main_article_text">{content}</p>
</article>
"""
        
    return final_article

def get_all_static_articles_replacments(image_switch):
    replacment = {}
    
    for content in read_static_content():
        section_title = content["Title"]
        section_article = content["Article"]
        if image_switch:
            section_image_src = content["Image_src"]
        else:
            section_image_src = ""
        generated_section = generate_static_section(section_title, section_article, section_image_src)
        replacment[f"[+{section_title.replace(" ", "_")}+]"] = generated_section
    
    return replacment

# header & footer
def get_header():
    header_path = work_path(r"\ostraloken\ostraloken.se\templates\base\header.html")
    header_content = open(header_path, "r", encoding="utf-8") # get its content
    header_final = header_content.read()
    header_content.close()
    
    for replacment in replacment_for_all:
        header_final = header_final.replace(replacment, replacment_for_all[replacment])
    
    return header_final

def get_footer():
    footer_path = work_path(r"\ostraloken\ostraloken.se\templates\base\footer.html")
    footer_content = open(footer_path, "r", encoding="utf-8") # get its content
    footer_final = footer_content.read()
    footer_content.close()
    
    for replacment in replacment_for_all:
        footer_final = footer_final.replace(replacment, replacment_for_all[replacment])
    
    return footer_final

def get_general_scripts():
    scripts_path = work_path(r"\ostraloken\ostraloken.se\templates\base\general_scripts.html")
    scripts_content = open(scripts_path, "r", encoding="utf-8") # get its content
    scripts_final = scripts_content.read()
    scripts_content.close()
    
    for replacment in replacment_for_all:
        scripts_final = scripts_final.replace(replacment, replacment_for_all[replacment])
    
    return scripts_final

# articles
def generate_lone_article(redirect_src, img_src, title, content, type, author, article_nmr, upplaga_nmr):
    # if you dont want a ancor redirecting to be generated, set redirect_src to "SHOULD_NOT_REDIRECT"
    if redirect_src is None or redirect_src == "":
        redirect_src = "./" # no redirect
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
    article_id = make_article_id(title, upplaga_nmr)
    # We strip the title of any unwanted caracters and replace spaces with _. Then we do the same to the author but only the first 15 caracters and last we add type if there is any caracters left since it then cuts of so its only combinend 100 caracters
    
    if redirect_src == "SHOULD_NOT_REDIRECT": # Not anchor
        author_context = f'<p class="author_text"><b>{author}</b></p>'
        
        # list Löken head writers
        head_writers = ["Vilhelm Grill", "Joar Stange", "John Ericson", "Magne Nordström", "Elliot Sandström"]
        # if author is one of head Löken writers: point their name to their part of kontaktinfo 
        if author in head_writers:
            author_context = f'<p class="author_text"><a href="https://ostraloken.se/kontakt/#{author.replace(" ", "_")}"><b>{author}</b></a></p>'
        
        final_article = f"""
<article id="{article_id}" class="article {no_img_class}"> <!--Add the "no_img" class to article if it has no image-->
    {type_context}
    {image_context}
    <h1>{title}</h1> <!-- This is the h1 since nothing else is on this page -->
    <p>{content}</p>
    {author_context}
</article>
"""
    else: # make article anchor
        final_article = f"""
<a href="{redirect_src}" id="{article_id}" class="article {no_img_class}"> <!--Add the "no_img" class to article if it has no image-->
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

def generate_preview_article(base_redirect_html_url, get_what_articles):
    how_many_articles_generated = 0
    generated_articles = [] # for get_what_articles == "All"
    generated_articles_based_on_type = {} # for get_what_articles == "Similar"
    generated_list = [] # for get_what_articles == "List"
    
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
                article_id = make_article_id(article_title, upplaga_number) # what is used to identefy the article

                if get_what_articles == "All":
                    img_url = find_img(org_article_title, upplaga_number, f"{base_redirect_html_url}images/") # get the url to the img as a html link
                    generated_articles.append(generate_lone_article((base_redirect_html_url + article_id + ".html"), img_url, article_title, (shorted_main_text + extra_at_end + "..."), article_type, article_author, how_many_articles_generated, upplaga_number))
                    how_many_articles_generated += 1
                elif get_what_articles == "Similar":
                    if article_type not in generated_articles_based_on_type:
                        generated_articles_based_on_type[article_type] = {} # initialize generated_articles_based_on_type[article_type]
                    generated_articles_based_on_type[article_type].update({article_id: generate_lone_article(("./" + article_id + ".html"), None, article_title, (shorted_main_text + extra_at_end + "..."), None, article_author, -1, upplaga_number)})
                    how_many_articles_generated += 1
                else: # get_what_articles == "List"
                    generated_list.append(article)
                    
    if get_what_articles == "All":
        return generated_articles
    elif get_what_articles == "Similar":
        return generated_articles_based_on_type
    else: # get_what_articles == "List"
        return generated_list

def generate_all_articles():
    article_template_path = work_path(r"\ostraloken\ostraloken.se\templates\a\articles_pages.html")
    generated_articles_path = work_path(r"\ostraloken\ostraloken.se\webbpage\a" + "\\")
    
    list_of_articles_with_similer_type = generate_preview_article("./a/", "Similar")
    
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
                article_id = make_article_id(article_title, upplaga_number)

                if article_type == "Insändare" and has_extra_info == False: # this is "else if" so that it cant both have extra upplaga info and a write-a-insändare prompt
                    has_extra_info = True
                    # add prompt to write insändare if it is a insändare
                    generated_article += """
<a class="article extra_info user_prompt" href="https://forms.gle/bBiEhDSCFijSFoHk9" target="_blank">
    <h2>Skicka in en insändare!</h2>
    <p>Vill du också skicka en insändare till Östra Löken? Fyll bara i denna korta enkät!</p>
</a>
"""

                # add scrolling news feed
                all_short_storys = read_short_storys()
                random_short_story = all_short_storys[random.randint(0, len(all_short_storys) - 1)]["Content"]
                final_random_short_story = f"<b>{random_short_story["Title"]}</b> • {random_short_story["Article"]}"
                short_story_id = make_short_story_id(random_short_story["Title"], random_short_story["Article"])
                feed_element = f"""
<div id="scrolling_news_feed">
    <a href="../notiser/#{short_story_id}">{final_random_short_story}</a>
</div>
"""

                replacment = {
                    "[+description+]": remove_html_elements(article_main_text)[:200].replace('"', "&quot;") + "...",
                    "[+url+]": f"https://ostraloken.se/a/{article_id}.html",
                    "[+home_url+]": f"../#{article_id}",
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
                    "[+thumb_image_url+]": "https://ostraloken.se/images/meta/Östra_Löken_webbsida_cover_image.png", # basic backup image
                    "[+scrolling_news_feed+]": feed_element # add news feed
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
                
                generate_site(article_template_path, (generated_articles_path + article_id + ".html"), replacment, "html")
    
    progressbar_item.finish()
    print("All articles successfully generated!")

def get_all_articles_previews():
    list_of_generated_articles = generate_preview_article("./a/", "All")
    all_generated_articles = ""
    for generated_articles in list_of_generated_articles:
        all_generated_articles += str(generated_articles)
    return all_generated_articles

def get_all_articles_full():
    whole_content_articles = ""
    for upplaga in reversed(read_normal_storys()):
        # go throught every article in the upplaga
        upplaga_number = upplaga["Upplaga"]
        for article in upplaga["Content"]:
            if article: # somethimes article is empty, this prevents that
                article_title = str(article["Title"])
                basic_article_title = remove_html_elements(article_title)
                article_main_text = str(article["Article"])
                article_type = str(article["Type"])
                article_author = str(article["Writer"])
                # copy over images and get the url to the right image
                article_img_src = find_img(basic_article_title, upplaga_number, "https://ostraloken.se/a/images/")
                whole_content_articles += generate_lone_article("SHOULD_NOT_REDIRECT", article_img_src, article_title, article_main_text, article_type, article_author, 0, upplaga_number)
    return whole_content_articles

# short storys
def generate_lone_short_storys(title, content):
    if title is None or title == "":
        title = "Null"
    if content is None or content == "":
        content = "Null"
    
    short_story_id = make_short_story_id(title, content)
        
    final_article = f"""
<a class="article notis" id="{short_story_id}">
    <article class="">
        <h2>{title}</h2>
        <p>{content}</p>
    </article>
</a>
"""
        
    return final_article

def get_short_story():
    generated_short_story = ""
    
    for short_story_bundle in reversed(read_short_storys()):
        content = short_story_bundle["Content"]
        if content:
            article_title = content["Title"]
            article_main_content = content["Article"]
            generated_short_story += generate_lone_short_storys(article_title, article_main_content)
            
    return generated_short_story

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
    
    final_article = f"""
<article class="article hear_me_out">
    <h2>{hear_me_out}</h2>
    <p>{description}</p>
    <div class="smash_pass_area">
        <button class="HMO_button smash_button"><i>SMASH</i></button>
        <button class="HMO_button pass_button"><i>PASS</i></button>
    </div>
</article>
"""
        
    return final_article

def get_hear_me_outs():
    generated_hear_me_out = ""
    
    for hear_me_out_bundle in reversed(read_hear_me_outs()):
        content = hear_me_out_bundle["Content"]
        if content:
            article_hear_me_out = content["Hear_me_out"]
            article_desc = content["Description"]
            generated_hear_me_out += generate_lone_hear_me_out(article_hear_me_out, article_desc)
            
    return generated_hear_me_out

# Nav page
def generate_lone_nav_element(title, link, image_src, important_status):
    if title is None or title == "":
        title = "Null"
    if link is None or link == "":
        link = "Null"
    if image_src is None or image_src == "":
        image_context = "<!-- NO IMAGE HERE -->"
    else:
        image_context = f'<img src="{image_src}" alt="{image_src}">'
        
    if important_status == "True":
        highlight_context = " highlight"
    else:
        highlight_context = ""
    
    final_article = f"""
<a class="article clickable_element nav_card{highlight_context}" target="_blank" href="{link}">
    <h2>{title}</h2>
    {image_context}
</a>
"""
        
    return final_article

def get_nav_element(img_switch, highlight_switch):
    generated_nav_element = ""
    
    for content in read_external_links_content():
        nav_element_important_status = content["Important"]
        if str(nav_element_important_status) == str(highlight_switch):
            nav_element_title = content["Title"]
            nav_element_link = content["Link"]
            if img_switch: # has image
                nav_element_image_src = content["Image_src"]
            else: # no image
                nav_element_image_src = ""
            generated_nav_element += generate_lone_nav_element(nav_element_title, nav_element_link, nav_element_image_src, nav_element_important_status)
        
    return generated_nav_element

# Kontakt page
def generate_kontakt_section(name, desc, title, email, image_src):
    if name is None or name == "":
        name = "Null"
    if title is None or title == "":
        title = "Null"
    if email is None or email == "":
        email = "Null"
    if image_src is None or image_src == "":
        image_context = "<!-- NO IMAGE HERE -->"
    else:
        image_context = f'<img src="{image_src}" alt="{name}">'
    
    final_article = f"""
<div class="article kontakt_card" id="{name.replace(" ", "_")}">
    <div class="kontakt_card_not_link_section">
        {image_context}
        <div class="kontakt_card_text_section">
            <h2>{title}: {name}</h2>
            <p>{desc}</p>
        </div>
    </div>
    <a class="article clickable_element highlight" href="mailto:{email}"><p><b>Skicka epost till {name}</b></p></a>
</div>
"""
    return final_article


# ---------------------------------
# MAKE GENERAL REPLACMENT
# ---------------------------------

def create_dictionary():
    replacment_dictionary = {}
    
    # Add go up button
    replacment_dictionary["[+go_up+]"] = """
<button id="go_up">
    <svg width="100%" height="100%" viewBox="0 0 400 300" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" xml:space="preserve" xmlns:serif="http://www.serif.com/" style="fill-rule:evenodd;clip-rule:evenodd;stroke-linejoin:round;stroke-miterlimit:2;">
        <g transform="matrix(1,0,0,1,1.28586,-100)">
            <g transform="matrix(1.232315,-0.038988,0.083035,1.234494,-33.300057,-56.518675)">
                <path d="M128.273,321.058L117.364,330.939C111.936,325.411 106.658,319.737 101.229,314.21C93.175,306.009 85.046,297.882 76.916,289.755C66.327,279.169 55.662,268.658 45.073,258.072L62.896,241.928C72.386,253.511 81.793,265.161 91.283,276.743C98.567,285.635 105.852,294.527 113.218,303.351C118.183,309.299 123.308,315.111 128.273,321.058Z" style="fill:currentColor;"/>
            </g>
            <g transform="matrix(0.575378,-0.866878,0.635263,0.785159,-135.892841,100.50832)">
                <path d="M297.669,507.928L286.604,517.95C243.179,470.858 199.689,423.829 156.265,376.738C134.554,353.193 112.432,330.016 91.197,306.041C76.476,289.42 63.173,271.631 48.452,255.011L59.517,244.989C74.603,261.278 90.993,276.272 106.079,292.561C127.841,316.059 148.722,340.36 170.009,364.289C212.585,412.149 255.093,460.068 297.669,507.928Z" style="fill:currentColor;"/>
            </g>
            <g transform="matrix(-0.038151,0.057479,-0.042121,-0.05206,86.735403,259.912122)">
                <path d="M53.984,250C71.791,255.317 89.585,259.88 107.392,265.197C122.369,269.669 235.991,303.593 294.619,324.189C305.694,328.079 418.997,367.882 431.632,386.83C450.231,414.719 473.499,440.962 487.404,470.51C500.894,499.176 509.26,529.486 512.234,558.107C515.209,586.729 512.916,614.851 504.927,639.11C504.853,639.333 464.405,703.17 464.306,703.22C441.78,714.547 422.386,731.415 396.691,737.142C371.762,742.699 343.551,742.205 315.363,736.42C287.175,730.635 257.839,719.319 230.643,703.066C223.042,698.523 164.198,663.354 145.108,627.585C120.644,581.748 91.814,444.048 88.487,428.155C79.859,386.945 71.804,345.789 63.836,304.646C60.303,286.402 57.518,268.245 53.984,250Z" style="fill:currentColor;"/>
            </g>
            <g transform="matrix(-0.038988,-1.232315,1.234494,-0.083035,-252.534198,337.284534)">
                <path d="M128.273,321.058L117.364,330.939C111.936,325.411 106.658,319.737 101.229,314.21C93.175,306.009 85.046,297.882 76.916,289.755C66.327,279.169 55.662,268.658 45.073,258.072L62.896,241.928C72.386,253.511 81.793,265.161 91.283,276.743C98.567,285.635 105.852,294.527 113.218,303.351C118.183,309.299 123.308,315.111 128.273,321.058Z" style="fill:currentColor;"/>
            </g>
        </g>
    </svg>
</button>
"""
    
    # All normal articles preview that you can click and it brings you to that article page
    replacment_dictionary["[+all_preview_articles+]"] = get_all_articles_previews()
    
    # All normal articles fully printed
    replacment_dictionary["[+all_articles+]"] = get_all_articles_full()
    
    # All short storys
    replacment_dictionary["[+all_short_storys+]"] = get_short_story()
    
    # All hear me outs
    replacment_dictionary["[+all_hear_me_outs+]"] = get_hear_me_outs()
    
    # Dynamicly add all static articles
    for content in read_static_content():
        section_title = content["Title"]
        section_article = content["Article"]
        section_image_src = content["Image_src"]
        
        # generate article
        generated_section = generate_static_section(section_title, section_article, section_image_src)
        replacment_dictionary[f"[+{section_title.replace(" ", "_")}+]"] = generated_section
        
        # generate without image
        generated_section = generate_static_section(section_title, section_article, "")
        replacment_dictionary[f"[+no_img_{section_title.replace(" ", "_")}+]"] = generated_section
        
        # add just the article
        replacment_dictionary[f"[+{section_title.replace(" ", "_")}_article+]"] = section_article
    
    # Add content from staff
    generated_sections = ""
    staff_list = ""
    for content in read_staff_info_content():
        person_name = content["Name"]
        person_desc = content["Description"]
        person_title = content["Title"]
        person_email = content["Email"]
        person_image_src = content["Image_src"]
        generated_sections += generate_kontakt_section(person_name, person_desc, person_title, person_email, person_image_src)
        staff_list += f'<a href="https://ostraloken.se/omoss/#{person_name.replace(" ", "_")}">{person_name}</a>'
    # List of staff as html button elements which lead to their email
    replacment_dictionary["[+staff_email_buttons+]"] = generated_sections
    # List of staff as links to their kontaktinfo page
    replacment_dictionary["[+staff_link_list+]"] = staff_list
    
    # The latest story
    most_recent_story = generate_preview_article("../a/", "All")[0]
    replacment_dictionary["[+latest_article+]"] = most_recent_story
    # The latest story title
    most_recent_story_list = generate_preview_article("../a/", "List")[0]
    replacment_dictionary["[+latest_title+]"] = remove_html_elements(most_recent_story_list["Title"]).replace('"', "&quot;")
    
    # Get the nav cards
    replacment_dictionary["[+nav_highlight_cards+]"] = get_nav_element(True, True)
    replacment_dictionary["[+no_img_nav_highlight_cards+]"] = get_nav_element(False, True)
    replacment_dictionary["[+nav_normal_cards+]"] = get_nav_element(True, False)
    replacment_dictionary["[+no_img_nav_normal_cards+]"] = get_nav_element(False, False)
    
    print("Dictionary created")
    
    return replacment_dictionary

replacment_for_all = create_dictionary()

def generate_all_normal_pages(): # go throught every file in templates
    template_base_path = work_path(r"\ostraloken\ostraloken.se\templates" + "\\")
    basic_template_files_list = os.listdir(template_base_path) # list all folders in dir
    for file_dir in basic_template_files_list:
        if "." in file_dir: # If it is not a folder
            whole_file_dir = template_base_path + file_dir
            whole_file = try_opening(whole_file_dir, "tr")
            destination_dir = find_between(whole_file, "<!--@( ", " )@-->", 0)
            whole_destination_dir = work_path(destination_dir)
            generate_site(whole_file_dir, whole_destination_dir, replacment_for_all, file_dir.split(".")[-1])
            print(f"Generated {file_dir}")


# ---------------------------------
# BACKEND TERMINAL
# ---------------------------------

# UI for backend user
def handle_backend_UI():
    global base_path
    global replacment_for_all
    
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

    COPY IMAGES
    $ copy images new --> Copy over only the new images
    $ copy images all --> Copy over all images, even if they alredy exists
    $ copy images specific --> Copy over all images in a specific upplaga
    
    COPY PDF:S
    $ copy pdf new --> Copy over only the new pdf:s
    $ copy pdf all --> Copy over all pdf:s, even if they alredy exists
    $ copy pdf specific --> Copy over a specific upplagas pdf 
    
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
                replacment_for_all = create_dictionary()
                generate_all_normal_pages()
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
                    
            # pdfs
            elif answer == "copy pdf new":
                copy_over_pdfs("new")
            elif answer == "copy pdf all":
                copy_over_pdfs("all")
            elif answer == "copy pdf specific":
                upplaga_to_copy = input("Copy over pdf upplaga: ")
                if re.search(r"[0-9]", upplaga_to_copy):
                    copy_over_pdfs(f"specific: {upplaga_to_copy}")
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
- gör tinder av hear me outs
- lägg till en custome scrollbar

Att fixa senare:
- Alla artiklar innan upplaga 11-5 ska dubbelkollas om artikeln är samma i pdf som text
"""