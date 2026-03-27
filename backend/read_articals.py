import os

base_path = os.getcwd()
normal_story_path = base_path + r"\ostraloken\backend\content\normal_storys_and_other"
short_story_path = base_path + r"\ostraloken\backend\content\short_storys"
hear_me_outs_path = base_path + r"\ostraloken\backend\content\hear_me_outs.txt"

"""
base_path = r"content/articles/lead_storys"
file_list = os.listdir(base_path)
"""

def read_normal_storys(): # To get the files and their content from all normal articals 
    file_list = os.listdir(normal_story_path) # list all files in dir
    for file in file_list: # Go througth every file in the list and extract the content
        content = open(normal_story_path + "\\" + file, "tr", encoding="utf-8") # extract
        whole_text = content.read() # read it
        
        # find the positions of difrent key parts
        title_pos1 = whole_text.find("## ") + 3
        title_pos2 = whole_text.find(" ##")
        type_pos1 = whole_text.find("¤¤ ") + 3
        type_pos2 = whole_text.find(" ¤¤")
        writer_pos1 = whole_text.find("@@ ") + 3
        writer_pos2 = whole_text.find(" @@")
        
        # Sum up into the title, type, writer and article
        title = whole_text[title_pos1:title_pos2]
        type = whole_text[type_pos1:type_pos2]
        writer = whole_text[writer_pos1:writer_pos2]
        article = whole_text[(writer_pos2 + 4):]
        
        print("Title:", title)
        print("Type:", type)
        print("Writer:", writer)
        print("Article:", article)
        
        content.close() # at the end

def read_short_storys(): # To get the files and their content from all short articals 
    file_list = os.listdir(short_story_path) # list all files in dir
    for file in file_list: # Go througth every file in the list and extract the content
        content = open(short_story_path + "\\" + file, "tr", encoding="utf-8") # extract
        whole_text = content.read() # read it
        
        # find the positions of difrent key parts
        title_pos1 = whole_text.find("## ") + 3
        title_pos2 = whole_text.find(" ##")
        
        # Sum up into the title, type, writer and article
        title = whole_text[title_pos1:title_pos2]
        article = whole_text[(title_pos2 + 4):]
        
        print("Title:", title)
        print("Article:", article)
        
        content.close() # at the end

def read_hear_me_outs(): # To get the contents from all hear me outs
    content = open(hear_me_outs_path, "tr", encoding="utf-8") # extract
    whole_text = content.read() # read it
    last_final_pos = 0
    
    for number_of_HMOs in range(whole_text.count("## ")): # repeat for how many hear me outs there are in the txt
        # find the positions of difrent key parts
        hear_me_out_pos1 = whole_text.find("## ", last_final_pos) + 3
        hear_me_out_pos2 = whole_text.find(" ##", last_final_pos)
        desc_pos1 = whole_text.find("++ ", last_final_pos) + 3
        desc_pos2 = whole_text.find(" ++", last_final_pos)
        last_final_pos = desc_pos2 + 3
        
        # Sum up into the title, type, writer and article
        hear_me_out = whole_text[hear_me_out_pos1:hear_me_out_pos2]
        desc = whole_text[desc_pos1:desc_pos2]
        
        print("Hear_me_out:", hear_me_out)
        print("Description:", desc)
    
    content.close() # at the end
    
# read_normal_storys()
# read_short_storys()
# read_hear_me_outs()