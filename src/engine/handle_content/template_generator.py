import os
from pathlib import Path

# import scripts
from engine import config
from engine import utils
from engine.handle_content import content_reader
from engine.handle_content import content_writer


def setup_new_utgava_folder(utgava_number, day, month, year):
    new_path = config.articles_path / f"utgava_{utgava_number}" / "utgava_info.txt"
    folder_path = config.articles_path / f"utgava_{utgava_number}"
    os.makedirs(folder_path, exist_ok=True) # generate the folder

    content = f""">>Editionsnummer: {utgava_number}
>>Utgivningsdatum: {day}-{month}-{year}
>>Extra_information: """
    # create / find the file
    with open(new_path, "x", encoding="utf-8") as file:
        file.write(content) # write to it
    
def setup_new_utgava_articles(utgava_number, count_articles):
    # all new articles
    for article_number in range(int(count_articles)):
        content = f""">>Rubrik: RUBRIK
>>Texttyp: ARTIKEL_TYP
>>Skribent: SKRIBENT
>>Artikel: 
BRÖDTEXT"""
        content_writer.write_to_content(f"articles/utgava_{utgava_number}/{article_number + 1}-ARTICLE_NAME.txt", "x", content)
        print(f"Generated {article_number + 1}-ARTICLE_NAME.txt")
    
def setup_new_notiser(utgava_number, count_notiser, day, month, year):
    content = f"""


/~utgava {utgava_number} ({day}/{month}/{year}):"""
    if int(count_notiser) == 0:
        content = "" # make so it doesnt say "utgava {highest_utgava_number} ({day}/{month}/{year}):" if there are no notiser
    lone_content = f"""

>>Rubrik: RUBRIK
>>Artikel: BRÖDTEXT"""
    # add right amount of notiser to new utgava
    for _ in range(int(count_notiser)):
        content += lone_content
    
    content_writer.write_to_content("notiser.txt", "a", content)

    print(f"Generated notis template for utgava {utgava_number}")
    
def setup_new_hear_me_outs(utgava_number, count_hear_me_outs):
    content = ""
    lone_content = f"""

>>Hear_me_out: HEAR_ME_OUT
>>Beskrivning: BESKRIVNING"""
    # add right amount of notiser to new utgava
    for _ in range(int(count_hear_me_outs)):
        content += lone_content
    
    content_writer.write_to_content("hear_me_outs.txt", "a", content)
    
    print(f"Generated hear me outs template for utgava {utgava_number}")
