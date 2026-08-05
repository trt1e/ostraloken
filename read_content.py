import os
from pathlib import Path

# import scripts
import base_commands

base_path = Path(__file__).resolve().parent

# List the storys paths
normal_story_path = base_path / Path("content/normal_storys_and_other")
# Path(main.base_path) / Path(path)
short_story_path = base_path / Path("content/short_storys.txt")
short_story_selection = {"Title": {"start": "### ", "end": " ##"}, "Article": {"start": "+++ ", "end": " ++"}}

hear_me_outs_path = base_path / Path("content/hear_me_outs.txt")
hear_me_outs_selection = {"Hear_me_out": {"start": "### ", "end": " ##"}, "Description": {"start": "+++ ", "end": " ++"}}

staff_info_path = base_path / Path("content/static/staff.txt")
staff_info_selection = {"Name": {"start": "### ", "end": " ##"}, "Description": {"start": "+++ ", "end": " ++"}, "Title": {"start": '""" ', "end": ' ""'}, "Email": {"start": "@@@ ", "end": " @@"}, "Image_src": {"start": "§§§ ", "end": " §§"}}

static_articles_path = base_path / Path("content/static/articles.txt")
static_articles_selection = {"Title": {"start": "### ", "end": " ##"}, "Article": {"start": "+++ ", "end": " ++"}, "Image_src": {"start": "§§§ ", "end": " §§"}}

external_links_content_path = base_path / Path("content/static/external_links.txt")
external_links_content_selection = {"Title": {"start": "### ", "end": " ##"}, "Link": {"start": "@@@ ", "end": " @@"}, "Image_src": {"start": "§§§ ", "end": " §§"}, "Important": {"start": "!!! ", "end": " !!"}}

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
def read_txt(txt_path, dictionary_of_selection):
    # example of dictionary_of_selection = {"title": {"start": "### ", "end": " ##"}, "article": {"start": "+++ ", "end": " ++"}}
    # extract dictionary_of_selection
    selection_abs_start = list(dictionary_of_selection.values())[0]["start"] # the start of the whole element
    selection_abs_end = list(dictionary_of_selection.values())[-1]["end"] # the end if the whole element
    
    whole_text = base_commands.try_opening(txt_path, "tr") # read it
    last_final_pos = whole_text.find(selection_abs_start) # start at the first title aka the first selection_start
    output_sum = []
    for number_of_articles in range(whole_text.count(selection_abs_start)): # repeat for how many short storys there are in the txt
        # find where diffrent parts are in the document
        content_output = {}
        for element_number, element_name in enumerate(dictionary_of_selection): # go through dictionary_of_selection to find this elements start and end selectors, then extract whats in between
            start_selector = list(dictionary_of_selection.values())[element_number]["start"] # find start selector (ex "### ")
            end_selector = list(dictionary_of_selection.values())[element_number]["end"] # find end selector (ex " ##")
            in_between_selectors = base_commands.find_between(whole_text, start_selector, end_selector, last_final_pos) # find what is in between these selectors
            content_output[element_name] = in_between_selectors # add this to content_output
        last_final_pos = whole_text.find(selection_abs_end, last_final_pos) + 3
        
        output = ({"Number": number_of_articles, "Content": content_output})
        output_sum.append(output)
        
    return output_sum
