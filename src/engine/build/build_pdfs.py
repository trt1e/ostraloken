import os
import re
from pathlib import Path
from PIL import Image
import shutil # To copy files (pdfs)
import pymupdf # To extract the pdfs to images

# import scripts
from engine import config
from engine import utils

# Copy pdf:s
def copy_over_pdfs(gen_type):
    pdf_start_path = config.base_path / Path("content/utgavor_pdfs")
    pdf_file_end_path = config.base_path / Path("generated/webb/ostraloken.se/webbsite/pdfer/pdf_files")
    pdf_images_end_path = config.base_path / Path("generated/webb/ostraloken.se/webbsite/pdfer/pdf_images")
    
    amount_of_pdfs = 0
    all_amount_pages = {}
    
    desired_utgava_nmr = None
    if "specific" in gen_type:
        desired_utgava_nmr = re.findall(r"specific: (\d+)", gen_type)[0] # Find what desired utgava number we are searching for
    
    for file_dir in Path(pdf_start_path).iterdir():
        amount_of_pdfs += 1
        utgava_number = re.findall(r"Ostra_Loken_utgava-(\d+)", file_dir.stem)[0]

        # Get the document
        pdf_document = pymupdf.open(file_dir)

        # Get amount of pages
        amount_of_pages = len(pdf_document)
        all_amount_pages[utgava_number] = amount_of_pages
        
        full_pdf_file_end_path = pdf_file_end_path / utils.remove_åäö(file_dir.name)
        copy_file_switch = False
        
        if gen_type != "new" or Path(full_pdf_file_end_path).is_file() is False:
            if desired_utgava_nmr:
                if int(utgava_number) == int(desired_utgava_nmr):
                    copy_file_switch = True
            else:
                copy_file_switch = True

        # Copy the file
        if copy_file_switch:
            shutil.copyfile(file_dir, full_pdf_file_end_path)
            
            print(f"Copied pdf file {file_dir.name}")

        pdf_image_folder_path = pdf_images_end_path / f"utgava_{utgava_number}"
        create_images_switch = False
        
        if gen_type != "new" or Path(pdf_image_folder_path).is_dir() is False: # if gen_type = "specific" we check if the folder for that pdf exists, not if it has image files inside
            if desired_utgava_nmr:
                if int(utgava_number) == int(desired_utgava_nmr):
                    create_images_switch = True
            else:
                create_images_switch = True

        # Create the images from pdf
        if create_images_switch:
            os.makedirs(pdf_image_folder_path, exist_ok=True) # generate the folder

            # Save the pages as images
            for image_nr in range(amount_of_pages):
                pdf_page = pdf_document[image_nr]
                pdf_pixmap = pdf_page.get_pixmap(dpi=300)
                created_pdf_image = Image.frombytes("RGB", (pdf_pixmap.width, pdf_pixmap.height), pdf_pixmap.samples)
                created_pdf_image.save(pdf_image_folder_path / f"page_{str(image_nr + 1)}.webp", "WEBP")
            
            print(f"Created pdf images for utgava {utgava_number}")
    else:
        print("No pdf:s left to copy")
        
    # change the PDFjs_reader.js in the /pdfer/js/ folder so that it has the correct amount of pdfs listed
    pdf_js_program_path = config.base_path / Path("generated/webb/ostraloken.se/webbsite/pdfer/js/PDF_reader.js")
    
    
    # Sort amount all pages
    all_amount_pages_sorted = dict(sorted(all_amount_pages.items(), key=lambda item: int(item[0])))
    
    # get the content
    with open(pdf_js_program_path, "tr", encoding="utf-8") as file:  
        js_file_content = file.read() # read it
    # change how many are max pages
    js_changed_content = re.sub(r"const maxPages = \d+", f"const maxPages = {max(list(all_amount_pages_sorted.values()))}", js_file_content) 
    # change how many are max pages
    js_changed_content = re.sub(r"const pagesPerPDF = \[.*?\]", f"const pagesPerPDF = {list(all_amount_pages_sorted.values())}", js_changed_content)
    
    # create / find the file
    with open(pdf_js_program_path, "w", encoding="utf-8") as file:
        file.write(js_changed_content) # write to it
    
    print("Uppdated amoutPDFs, maxPages and pagesPerPDF in PDF_reader.js")
    
    # Copy over Om_krisen_kriget_eller_Ulf_Kristersson_kommer
    pdf_start_path = config.base_path / Path("content/extra/Om_krisen_kriget_eller_Ulf_Kristersson_kommer.pdf")
    pdf_file_end_path = config.base_path / Path("generated/webb/ostraloken.se/webbsite/Om_krisen_kriget_eller_Ulf_Kristersson_kommer/pdf_files/Om_krisen_kriget_eller_Ulf_Kristersson_kommer.pdf")
    
    os.makedirs(Path(pdf_file_end_path).parent, exist_ok=True) # generate the folder
    shutil.copyfile(pdf_start_path, pdf_file_end_path)
    
    print(f"Copied pdf file {str(pdf_start_path).split("\\")[-1]}")
