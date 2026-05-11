import os
import re
from PIL import Image
import math

is_linux = False

base_path = os.getcwd()

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

    if open_content == None:
        print("WARNING, NO UTF WORKING ON: " + content)

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
        print(f"WARNING, amount of < ({amount_of_start}) not same as > ({amount_of_end}) in {string}")
    
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
        not_closed_html_elements = []
        for element in list_of_html_elements:
            if element == "br" or element == "img": # br and img both do not have </ to close, so they are not relevant
                list_of_html_elements.remove(element)
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
    for number_of_articles in range(whole_text.count("### ")): # repeat for how many hear me outs there are in the txt
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


# FIX ARTICLES NAMES
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


# GENERATE SITES
lone_article_template_path = work_path(r"\ostraloken\frontend\template\lone_article.html")

index_template_path = work_path(r"\ostraloken\frontend\template\index.html")
index_generated_path = work_path(r"\ostraloken\frontend\webbpage\index.html")

article_template_path = work_path(r"\ostraloken\frontend\template\articles_pages.html")
generated_articles_path = work_path(r"\ostraloken\frontend\webbpage\a" + "\\")

hear_me_outs_template_path = work_path(r"\ostraloken\frontend\template\hear_me_outs.html")
lone_hear_me_out_template_path = work_path(r"\ostraloken\frontend\template\lone_hear_me_out.html")
hear_me_outs_generated_path = work_path(r"\ostraloken\frontend\webbpage\hear_me_outs\index.html")

short_storys_template_path = work_path(r"\ostraloken\frontend\template\notiser.html")
lone_short_story_template_path = work_path(r"\ostraloken\frontend\template\lone_notis.html")
short_storys_generated_path = work_path(r"\ostraloken\frontend\webbpage\notiser\index.html")

# images
def copy_over_images(article_title, upplaga_nmr, base_url):
    all_img_title = "IMG-" + strip_string(article_title, 100)
    old_img_path_no_extention = normal_story_path + handel_path_slash("\\") + f"upplaga_{upplaga_nmr}" + handel_path_slash("\\") + all_img_title
    new_img_url_with_extention = generated_articles_path + handel_path_slash("images\\") + all_img_title + ".webp"
    extentions = ["jpg", "JPG", "jpeg", "JPEG", "png", "PNG", "webp"]
    for ext in extentions:
        if os.path.isfile(f"{old_img_path_no_extention}.{ext}") is True:
            old_img_path_with_extention = f"{old_img_path_no_extention}.{ext}"
            break
    else:
        old_img_path_with_extention = "NO_IMG" # article does not have image
        
    if old_img_path_with_extention != "NO_IMG":
        if os.path.isfile(new_img_url_with_extention) is False:
            image = Image.open(old_img_path_with_extention)
            img_width, img_height = image.size
            new_width = 1000
            new_height = int((new_width / img_width) * img_height)
            new_image = image.resize((new_width, new_height))
            new_image.save(new_img_url_with_extention, quality=80)
            print(f"copied image: {all_img_title}")
        return base_url + all_img_title + ".webp"
    else:
        return ""

# articles
def generate_lone_article(redirect_src, img_src, title, content, type, author, article_nmr):
    # if you dont want a ancor redirecting to be generated, set redirect_src to "SHOULD_NOT_REDIRECT"
    if redirect_src is None or redirect_src == "":
        redirect_src = "./" # hide image
    if img_src is None or img_src == "" or img_src == "NO_IMAGE_AVAILABLE":
        no_img_class = "no_img"
        img_src += f'" alt="NO IMAGE HERE' # add the alt text
    else:
        no_img_class = ""
        img_src += f'" alt="{strip_string(title, -1).replace("_", " ")}" ' # add the alt text
        if article_nmr != 0: # this is so the first image dosn't have loading lazy so it dosnt pop in
            img_src += 'loading="lazy'
        else:
            img_src += 'fetchpriority="high'
    if title is None or title == "":
        title = "Null"
    if content is None or content == "":
        content = "Null"
        
    template = try_opening(lone_article_template_path, "")
    

    # Find where you put the redirect src
    article_redirect_href_pos = template.find('a href="') + 8 # dependent on the html layout
    # Find where you put the article id
    article_id_pos = template.find('id="') + 4 # only works if there is just one id, wich there should only be
    # Find where you put if there is no image
    no_img_class_pos = template.find('class="article ') + 15 # dependent on the html layout
    # Find where you put the img src
    article_img_src_pos = template.find('img src="') + 9 # dependent on the html layout
    
    # Find where it says <!-- [+title+] -->
    article_title_pos = template.find("<!-- [+title+] -->") + 18 
    # Find where it says <!-- [+type+] -->
    article_type_pos = template.find("<!-- [+type+] -->") + 17
    # Find where it says <!-- [+content+] -->
    article_content_pos = template.find("<!-- [+content+] -->") + 20 
    # Find where it says <!-- [+author+] -->
    article_author_pos = template.find("<!-- [+author+] -->") + 19

    # generate the article id
    article_id = (strip_string(remove_html_elements(title), -1) + "-" + strip_string(author, 20) + "-" + strip_string(type, -1))[:100] 
    # We strip the title of any unwanted caracters and replace spaces with _. Then we do the same to the author but only the first 15 caracters and last we add type if there is any caracters left since it then cuts of so its only combinend 100 caracters
    
    # get the core part that is in both versions
    core_article_part = article_id + template[article_id_pos:no_img_class_pos] + no_img_class + template[no_img_class_pos:article_type_pos] + type + template[article_type_pos:article_img_src_pos] + img_src + template[article_img_src_pos:article_title_pos] + title + template[article_title_pos:article_content_pos] + content + template[article_content_pos:article_author_pos] + author
    
    # act diffrently if it should redirect or not
    if redirect_src != "SHOULD_NOT_REDIRECT":
        final_article = template[:article_redirect_href_pos] + redirect_src + template[article_redirect_href_pos:article_id_pos] + core_article_part + template[article_author_pos:]
    else: # make article not ancor
        first_a_pos = template.find("<a") + 1
        second_a_pos = template.find("</a", first_a_pos) + 2
        final_article = template[:first_a_pos] + "div" + template[(first_a_pos + 1):article_id_pos] + core_article_part + template[article_author_pos:second_a_pos] + "div" + template[(second_a_pos + 1):]
        
    return final_article

def generate_index(): # PS images are copyd here
    how_many_articles_generated = 0
    template = try_opening(index_template_path, "")
    
    # Find where it says <!-- [+articles+] -->
    article_container_pos = template.find("<!-- [+articles+] -->") + 22
    
    generated_articles = ""
    
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
                            title_end_pos = article_title[30:].find(">")
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
                article_main_text_last_caracter = re.search(r"\.|\?|\!|\:|\;", article_main_text[200:]) # this finds a . ? ! : or ; in the last 200-400 characters
                if article_main_text_last_caracter:
                    article_main_text_last_caracter_pos = article_main_text.find(article_main_text_last_caracter.group(0), 200)
                    # print(article_main_text[article_main_text_last_caracter_pos])
                    
                    # se if its closed by a <br> before the . ? ! : or ;
                    if article_main_text[:article_main_text_last_caracter_pos].find("<br>") != -1: # if <br> exists
                        character_before_break_pos = article_main_text.find("<br>") - 1
                        if article_main_text[character_before_break_pos] == ">": # so if for example something ends with </i>, the i isnt cut of
                            # find how long the html element before the break is
                            length_of_html_element_before_break = 4 # have 4 (the length of, for example, <\i>) as a backup just in case
                            for element_length, character in enumerate(article_main_text[:character_before_break_pos]):
                                if character == "<":
                                    length_of_html_element_before_break = character_before_break_pos - element_length + 1
                            article_main_text_last_caracter_pos = character_before_break_pos - length_of_html_element_before_break
                            extra_at_end += article_main_text[(article_main_text.find("<br>") - length_of_html_element_before_break):(article_main_text.find("<br>"))]
                        else:
                            article_main_text_last_caracter_pos = character_before_break_pos
                else:
                    if article_main_text.find("<br>") != -1: # if <br> exists
                        character_before_break_pos = article_main_text.find("<br>") - 1
                        if character_before_break_pos <= 400:
                            if article_main_text[character_before_break_pos] == ">": # so if for example something ends with </i>, the i isnt cut of
                                # find how long the html element before the break is
                                length_of_html_element_before_break = 4 # have 4 (the length of, for example, <\i>) as a backup just in case
                                for element_length, character in enumerate(article_main_text[:character_before_break_pos]):
                                    if character == "<":
                                        length_of_html_element_before_break = character_before_break_pos - element_length + 1
                                article_main_text_last_caracter_pos = character_before_break_pos - length_of_html_element_before_break
                                extra_at_end += article_main_text[(article_main_text.find("<br>") - length_of_html_element_before_break):(article_main_text.find("<br>"))]
                            else:
                                article_main_text_last_caracter_pos = character_before_break_pos
                        else:
                            article_main_text = article_main_text.replace("<br>", "")
                
                # the text cut of at the right place
                shorted_main_text = article_main_text[:article_main_text_last_caracter_pos]
                            
                # add back any cut of html elements
                extra_at_end = fix_cut_of_html_elements(shorted_main_text)
                                    
                article_type = article["Type"]
                article_author = article["Writer"]
                
                # copy over images and get the url to the right image
                html_url = copy_over_images(basic_article_title, upplaga_number, "./a/images/")
    
                generated_articles += generate_lone_article(("./a/" + strip_string(org_article_title, 100) + ".html"), html_url, article_title, (shorted_main_text + extra_at_end + "..."), article_type, article_author, how_many_articles_generated)
                how_many_articles_generated += 1
                
    generated_file = open(index_generated_path, "w", encoding="utf-8") # create / find the file
    generated_file.write(template[:article_container_pos] + generated_articles + template[article_container_pos:]) #write to it
    
    print("Index successfully generated!")

def generate_all_articles(): # PS images are also copyd here
    template = try_opening(article_template_path, "")
    
    # Find where it says <!-- [+article+] -->
    article_pos = template.find("<!-- [+article+] -->") + 20 + 1
    # Find where it says <!-- [+upplaga_number+] -->
    upplaga_number_pos = template.find("<!-- [+upplaga_number+] -->") + 27
    # Find where it says <!-- [+date+] -->
    date_pos = template.find("<!-- [+date+] -->") + 17
    
    # go throught every upplaga
    for upplaga in read_normal_storys():
        # go throught every article in the upplaga
        upplaga_number = upplaga["Upplaga"]
        upplaga_date = upplaga["Release_date"]
        for article in upplaga["Content"]:
            if article: # somethimes article is empty, this prevents that
                generated_articles = "" # where we put the article
                
                article_title = str(article["Title"])
                basic_article_title = remove_html_elements(article_title)
                article_main_text = str(article["Article"])
                article_type = str(article["Type"])
                article_author = str(article["Writer"])
                # copy over images and get the url to the right image
                article_img_src = copy_over_images(basic_article_title, upplaga_number, "./images/")
                generated_articles += generate_lone_article("SHOULD_NOT_REDIRECT", article_img_src, article_title, article_main_text, article_type, article_author, 0)
            
                # generate the home url
                article_home_url_pos = template.find('<a id="return" href="') + 21 
                home_place_id = (strip_string(basic_article_title, -1) + "-" + strip_string(article_author, 20) + "-" + strip_string(article_type, -1))[:100]
                article_home_url_finale = "../#" + home_place_id

                generated_file = open((generated_articles_path + strip_string(basic_article_title, 100) + ".html"), "w", encoding="utf-8") # create / find the file
                generated_file.write(template[:article_home_url_pos] + article_home_url_finale + template[article_home_url_pos:article_pos] + generated_articles + template[article_pos:upplaga_number_pos] + str(upplaga_number) + template[upplaga_number_pos:date_pos] + upplaga_date + template[date_pos:]) # write to it
        
    print("All articles successfully generated!")

# short storys
def generate_lone_short_storys(title, content):
    if title is None or title == "":
        title = "Null"
    if content is None or content == "":
        content = "Null"
        
    template = try_opening(lone_short_story_template_path, "")
    

    # Find where it says <!-- [+title+] -->
    article_title_pos = template.find("<!-- [+title+] -->") + 18
    # Find where it says <!-- [+content+] -->
    article_content_pos = template.find("<!-- [+content+] -->") + 20
    
    final_article = template[:article_title_pos] + title + template[article_title_pos:article_content_pos] + content + template[article_content_pos:]
        
    return final_article

def generate_short_storys():
    template = try_opening(short_storys_template_path, "")
    
    # Find where it says <!-- [+short_storys+] -->
    short_story_container_pos = template.find("<!-- [+short_storys+] -->") + 26
    
    generated_short_story = ""
    
    for short_story_bundle in reversed(read_short_storys()):
        content = short_story_bundle["Content"]
        if content:
            article_title = content["Title"]
            article_main_content = content["Article"]
            generated_short_story += generate_lone_short_storys(article_title, article_main_content)
    
    generated_file = open(short_storys_generated_path, "w", encoding="utf-8") # create / find the file
    generated_file.write(template[:short_story_container_pos] + generated_short_story + template[short_story_container_pos:]) #write to it
    
    print("Short storys successfully generated!")

# hear me outs
def generate_lone_hear_me_out(hear_me_out, description):
    if hear_me_out is None or hear_me_out == "":
        hear_me_out = "Null"
    if description is None:
        description = "Null"
    if description != "":
        description = "<b>Förklaring:</b> " + description
        
    template = try_opening(lone_hear_me_out_template_path, "")
    

    # Find where it says <!-- [+hear_me_out+] -->
    article_hear_me_out_pos = template.find("<!-- [+hear_me_out+] -->") + 24
    # Find where it says <!-- [+desc+] -->
    article_desc_pos = template.find("<!-- [+desc+] -->") + 17
    
    if len(hear_me_out) > 70:
        hear_me_out = hear_me_out[:70] + "..."
        
    if len(description) > 500:
        description = description[:500] + "..."
    
    final_article = template[:article_hear_me_out_pos] + hear_me_out + template[article_hear_me_out_pos:article_desc_pos] + description + template[article_desc_pos:]
        
    return final_article

def generate_hear_me_outs():
    template = try_opening(hear_me_outs_template_path, "")
    
    # Find where it says <!-- [+hear_me_outs+] -->
    hear_me_out_container_pos = template.find("<!-- [+hear_me_outs+] -->") + 26
    
    generated_hear_me_out = ""
    
    for hear_me_out_bundle in reversed(read_hear_me_outs()):
        content = hear_me_out_bundle["Content"]
        if content:
            article_hear_me_out = content["Hear_me_out"]
            article_desc = content["Description"]
            generated_hear_me_out += generate_lone_hear_me_out(article_hear_me_out, article_desc)
    
    generated_file = open(hear_me_outs_generated_path, "w", encoding="utf-8") # create / find the file
    generated_file.write(template[:hear_me_out_container_pos] + generated_hear_me_out + template[hear_me_out_container_pos:]) #write to it
    
    print("Hear me outs successfully generated!")


generate_index()
generate_hear_me_outs()
generate_short_storys()
generate_all_articles()
fix_all_backend_articles_names()

"""
Saker att lägga till
- sökfunktion

Att fixa senare:
- Alla artiklar innan upplaga 11-5 ska dubbelkollas om artikeln är samma i pdf som text
- dubbelkolla allas type

SE TILL ATT LIGHTHOUSE OCH VALIDATOR FUNGERAR!!!

Mindre viktigt:
 - skriv vidare på vår historia mm
"""