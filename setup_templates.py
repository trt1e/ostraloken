import os
from pathlib import Path

# import scripts
import base_commands
import read_content


def setup_new_upplaga_folder(day, month, year):
    next_upplaga_number = base_commands.get_curant_upplaga_number()
    next_upplaga_number += 1 # so highest_upplaga_number is one higher than what exists
    new_path = read_content.normal_story_path / f"upplaga_{next_upplaga_number}" / "upplaga_info.txt"
    folder_path = read_content.normal_story_path / f"upplaga_{next_upplaga_number}"
    os.makedirs(folder_path, exist_ok=True) # generate the folder
    generated_file = open(new_path, "x", encoding="utf-8") # create / find the file
    content = f"""Upplaga: === {next_upplaga_number} ==
Datum: $$$ {day}-{month}-{year} $$
Extra info: ***  **"""
    generated_file.write(content) #write to it
    generated_file.close()
    
def setup_new_upplaga_articles(count_articles):
    next_upplaga_number = base_commands.get_curant_upplaga_number()
    # all new articles
    for article_number in range(int(count_articles)):
        article_path = read_content.normal_story_path / f"upplaga_{next_upplaga_number}" / f"{article_number + 1} ARTICLE_NAME.txt"
        generated_file = open(article_path, "x", encoding="utf-8") # create / find the file
        content = f"""### RUBRIK ##
¤¤¤ ARTIKEL_TYP ¤¤
@@@ SKRIBENT @@
BRÖDTEXT"""
        generated_file.write(content) #write to it
        generated_file.close()
    
def setup_new_notiser(count_notiser, day, month, year):
    next_upplaga_number = base_commands.get_curant_upplaga_number()
    for upplaga in reversed(read_content.read_normal_storys()):
        if upplaga["Upplaga"] > next_upplaga_number:
            highest_upplaga_number = upplaga["Upplaga"]
    edited_file = open(read_content.short_story_path, "a", encoding="utf-8") # create / find the file
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
    edited_file = open(read_content.hear_me_outs_path, "a", encoding="utf-8") # create / find the file
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
