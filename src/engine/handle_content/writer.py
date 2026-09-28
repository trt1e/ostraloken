from pathlib import Path

# import scripts
from engine import config

def write_to_content(txt_path, writing_style, content):
    content_path = config.base_path / Path("content") / Path(txt_path)
    
    # create / find the file
    with open(content_path, writing_style, encoding="utf-8") as file:  
        file.write(content) # write to it