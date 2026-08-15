import os
from pathlib import Path

# import scripts
from engine import utils
from engine.handle_content import content_reader


def setup_new_upplaga_folder(day, month, year):
    next_upplaga_number = utils.get_curant_upplaga_number()
    next_upplaga_number += 1 # so highest_upplaga_number is one higher than what exists
    new_path = content_reader.articles_path / f"upplaga_{next_upplaga_number}" / "upplaga_info.txt"
    folder_path = content_reader.articles_path / f"upplaga_{next_upplaga_number}"
    os.makedirs(folder_path, exist_ok=True) # generate the folder

    content = f"""Upplaga: === {next_upplaga_number} ==
Datum: $$$ {day}-{month}-{year} $$
Extra info: ***  **"""
    # create / find the file
    with open(new_path, "x", encoding="utf-8") as file:
        file.write(content) # write to it
    
def setup_new_upplaga_articles(count_articles):
    next_upplaga_number = utils.get_curant_upplaga_number()
    # all new articles
    for article_number in range(int(count_articles)):
        article_path = content_reader.articles_path / f"upplaga_{next_upplaga_number}" / f"{article_number + 1} ARTICLE_NAME.txt"
        
        content = f"""### RUBRIK ##
¤¤¤ ARTIKEL_TYP ¤¤
@@@ SKRIBENT @@
BRÖDTEXT"""
        # create / find the file
        with open(article_path, "x", encoding="utf-8") as file:
            file.write(content) # write to it
    
def setup_new_notiser(count_notiser, day, month, year):
    next_upplaga_number = utils.get_curant_upplaga_number()
    for upplaga in reversed(content_reader.read_articles()):
        if upplaga["Upplaga"] > next_upplaga_number:
            highest_upplaga_number = upplaga["Upplaga"]
    
    content = f"""


Upplaga {next_upplaga_number} ({day}/{month}/{year}):"""
    if int(count_notiser) == 0:
        content = "" # make so it doesnt say "Upplaga {highest_upplaga_number} ({day}/{month}/{year}):" if there are no notiser
    lone_content = f"""

### RUBRIK ##
+++ BRÖDTEXT ++"""
    # add right amount of notiser to new upplaga
    for _ in range(int(count_notiser)):
        content += lone_content
    
    # create / find the file
    with open(content_reader.short_story_path, "a", encoding="utf-8") as file:
        file.write(content) # write to it

    print(f"Generated template for upplaga {next_upplaga_number}")
    
def setup_new_hear_me_outs(count_hear_me_outs):
    content = ""
    lone_content = f"""

### HEAR_ME_OUT ##
+++ BESKRIVNING ++"""
    # add right amount of notiser to new upplaga
    for _ in range(int(count_hear_me_outs)):
        content += lone_content
    
    # create / find the file
    with open(content_reader.hear_me_outs_path, "a", encoding="utf-8") as file:
        file.write(content) # write to it
    
    print(f"Generated template hear me outs")
