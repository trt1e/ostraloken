import os
import re
from pathlib import Path
import importlib
import pkgutil

# import scripts
from engine import config
from engine.build import build_articles
from engine.build import replacments


# Create the dictionary where all articles (exept /a/ articles) are run through to see and replace using the dict generated here
def create_dictionary():
    replacment_dictionary = {}
        
    # Import the replacment components in the replacment dictionary
    # The files in /replacments/ output a dict which is named "output"
    for module_bundle in pkgutil.iter_modules(replacments.__path__):
        module = importlib.import_module(f"{replacments.__name__}.{module_bundle.name}")
        replacment_dictionary = replacment_dictionary | module.output # Merge the dicts
    
    print("Dictionary created")
    
    return replacment_dictionary

replacment_for_all = create_dictionary()

# Go throught and generate all non /a/ articles
def generate_webbsite(webb_path, template_path):
    # Go throught all the folders in template dir
    for file_dir in Path(template_path).iterdir():
        if Path(file_dir).is_file(): # If it is not a folder
            with open(file_dir, "tr", encoding="utf-8") as file:  
                whole_file = file.read() # read it
            file_type = Path(file_dir).suffix
            if file_type == ".html":
                destination_dir = re.findall(r"<!--@\( (.*?) \)@-->", whole_file)[0]
            elif file_type == ".css" or file_type == ".js":
                destination_dir = re.findall(r"\/\*@\( (.*?) \)@\*\/", whole_file)[0]
            else:
                print(f"WARNING: {file_dir} does not have a destination dir! Please add one. This file is skiped.")
                continue
            full_destination_dir = webb_path / "webbsite" / Path(str(destination_dir)) 
            os.makedirs(full_destination_dir.parent, exist_ok=True) # make sure the folder exists, else: generate the folder
            build_articles.generate_site(file_dir, full_destination_dir, replacment_for_all)
            generated_site_name = (str(template_path).replace(str(config.base_path), "")).split("\\")[3]
            print(f"Generated {generated_site_name}: {file_dir.stem}{file_dir.suffix}")

# First find all the webb- and template paths
def generate_all_normal_pages(): # go throught every file in templates
    for webb_path in config.base_webb_paths:
        template_path = webb_path / "templates"
        extra_template_path = webb_path / "templates/extra"
        if extra_template_path.is_dir(): # If there is a extra/ folder in templates
            generate_webbsite(webb_path, extra_template_path)
            
        generate_webbsite(webb_path, template_path)
