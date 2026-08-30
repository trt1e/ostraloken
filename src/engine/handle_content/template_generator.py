import os
from pathlib import Path

# import scripts
from engine import config
from engine import utils
from engine.handle_content import content_reader
from engine.handle_content import content_writer


def setup_new_utgava_folder(day, month, year):
    next_utgava_number = len(content_reader.read_articles()) + 1
    
    new_path = config.articles_path / f"utgava_{next_utgava_number}" / "utgava_info.txt"
    folder_path = config.articles_path / f"utgava_{next_utgava_number}"
    os.makedirs(folder_path, exist_ok=True) # generate the folder

    content = f""">>Editionsnummer: {next_utgava_number}
>>Utgivningsdatum: {day}-{month}-{year}
>>Extra information: """
    # create / find the file
    with open(new_path, "x", encoding="utf-8") as file:
        file.write(content) # write to it
    
def setup_new_utgava_articles(count_articles):
    next_utgava_number = len(content_reader.read_articles()) + 1
    
    # all new articles
    for article_number in range(int(count_articles)):
        content = f""">>Rubrik: RUBRIK
>>Texttyp: ARTIKEL_TYP
>>Skribent: SKRIBENT
>>Artikel: 
BRÖDTEXT"""
        content_writer.write_to_content(f"articles/utgava_{next_utgava_number}/{article_number + 1}-ARTICLE_NAME.txt", "x", content)
    
def setup_new_notiser(count_notiser, day, month, year):
    next_utgava_number = len(content_reader.read_articles()) + 1
    
    content = f"""


/~utgava {next_utgava_number} ({day}/{month}/{year}):"""
    if int(count_notiser) == 0:
        content = "" # make so it doesnt say "utgava {highest_utgava_number} ({day}/{month}/{year}):" if there are no notiser
    lone_content = f"""

>>Rubrik: RUBRIK
>>Artikel: BRÖDTEXT"""
    # add right amount of notiser to new utgava
    for _ in range(int(count_notiser)):
        content += lone_content
    
    content_writer.write_to_content("notiser.txt", "a", content)

    print(f"Generated template for utgava {next_utgava_number}")
    
def setup_new_hear_me_outs(count_hear_me_outs):
    content = ""
    lone_content = f"""

>>Hear_me_out: HEAR_ME_OUT
>>Beskrivning: BESKRIVNING"""
    # add right amount of notiser to new utgava
    for _ in range(int(count_hear_me_outs)):
        content += lone_content
    
    content_writer.write_to_content("hear_me_outs.txt", "a", content)
    
    print(f"Generated template hear me outs")
