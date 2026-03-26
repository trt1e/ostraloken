import os

base_path = os.getcwd()
lead_story_path = base_path + r"\ostraloken\backend\content\articles\lead_storys"
normal_story_path = base_path + r"\ostraloken\backend\content\articles\normal_storys"
short_story_path = base_path + r"\ostraloken\backend\content\articles\short_storys"
debates_path = base_path + r"\ostraloken\backend\content\sent_ins\debates"
sent_letters_path = base_path + r"\ostraloken\backend\content\sent_ins\debates"
hear_me_outs_path = base_path + r"\ostraloken\backend\content\sent_ins\hear_me_outs.md"

"""
base_path = r"content/articles/lead_storys"
file_list = os.listdir(base_path)
"""

def read_lead_story():
    file_list = os.listdir(lead_story_path)
    for storys in file_list:
        file = file_list[0]
        print(lead_story_path + file)
        content = open(os.path.dirname(lead_story_path + file))
        print(content)
    
read_lead_story()