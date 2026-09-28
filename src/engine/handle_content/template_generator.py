import os
from pathlib import Path

# import scripts
from engine import config
from engine import utils
from engine.handle_content import reader
from engine.handle_content import writer


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
        writer.write_to_content(f"articles/utgava_{utgava_number}/{article_number + 1}-ARTICLE_NAME.txt", "x", content)
        print(f"Generated {article_number + 1}-ARTICLE_NAME.txt")


def setup_new_txt(utgava_number, count_list, day, month, year):
    base_content_path = Path(config.base_path / "content")
    for file_dir in base_content_path.iterdir():
        if file_dir.is_file() and file_dir.suffix == ".txt":
            content = f"""


/~utgava {utgava_number} ({day}/{month}/{year}):"""
            lone_content = f"""

>>Rubrik: RUBRIK
>>Artikel: BRÖDTEXT"""
            # add right amount of notiser to new utgava
            if count_list is None or count_list == "" or str(count_list) == "0":
                content += "\n/~INGENTING HÄR"
            else:
                content += str(lone_content) * int(count_list)
            
            writer.write_to_content("notiser.txt", "a", content)

            print(f"Generated notis template for utgava {utgava_number}")

            

def setup_new_notiser(utgava_number, count_notiser, day, month, year):
    content = f"""


/~utgava {utgava_number} ({day}/{month}/{year}):"""
    lone_content = f"""

>>Rubrik: RUBRIK
>>Artikel: BRÖDTEXT"""
    # add right amount of notiser to new utgava
    if count_notiser == None or count_notiser == "" or str(count_notiser) == "0":
        content += "\n/~INGENTING HÄR"
    else:
        content += str(lone_content) * int(count_notiser)
    
    writer.write_to_content("notiser.txt", "a", content)

    print(f"Generated notis template for utgava {utgava_number}")
    
def setup_new_hear_me_outs(utgava_number, count_hear_me_outs):
    lone_content = f"""

>>Hear_me_out: HEAR_ME_OUT
>>Beskrivning: BESKRIVNING"""
    # add right amount of hear me out to new utgava
    content = str(lone_content) * int(count_hear_me_outs)
    
    writer.write_to_content("hear_me_outs.txt", "a", content)
    
    print(f"Generated hear me outs template for utgava {utgava_number}")

def setup_new_rod_flagga(utgava_number, count_roda_flaggor):
    lone_content = f"""

>>Rod_flagga: ROD_FLAGGA
>>Beskrivning: BESKRIVNING"""
    # add right amount of rod flagga to new utgava
    content = str(lone_content) * int(count_roda_flaggor)
    
    writer.write_to_content("roda_flaggor.txt", "a", content)
    
    print(f"Generated roda flaggors template for utgava {utgava_number}")
