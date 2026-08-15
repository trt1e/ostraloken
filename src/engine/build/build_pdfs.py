import os
import re
from pathlib import Path
import shutil # To copy files (pdfs)
from pdf2image import convert_from_path # To extract the pdfs to images
from pypdf import PdfReader # To get how many pages

# import scripts
from engine import config
from engine import utils
from engine.handle_content import content_reader

# Copy pdf:s
def copy_over_pdfs(gen_type):
    pdf_start_path = config.base_path / Path("content/upplagor_pdfs")
    pdf_file_end_path = config.base_path / Path("generated/webb/ostraloken.se/webbpage/pdfer/pdf_files")
    pdf_images_end_path = config.base_path / Path("generated/webb/ostraloken.se/webbpage/pdfer/pdf_images")
    
    amount_of_pdfs = 0
    all_amount_pages = {}
    pdfs_list = os.listdir(pdf_start_path)
    
    for file_dir in pdfs_list:
        full_start_file_dir = pdf_start_path / file_dir
        
        amount_of_pdfs += 1
        upplaga_number = file_dir.split("Östra_Löken_upplaga_")[1].split(".pdf")[0]
        
        pdf_reader = PdfReader(open(full_start_file_dir, "rb"))
        amount_of_pages = len(pdf_reader.pages)
        all_amount_pages[upplaga_number] = (amount_of_pages)
        
        full_pdf_file_end_path = pdf_file_end_path / utils.remove_åäö(file_dir)
        copy_file_switch = False
        
        if gen_type != "new" or Path(full_pdf_file_end_path).is_file() is False:
            if "specific" in gen_type:
                desired_upplaga_nmr = gen_type.split(": ")[1]
                if int(upplaga_number) == int(desired_upplaga_nmr):
                    copy_file_switch = True
            else:
                copy_file_switch = True

        # Copy the file
        if copy_file_switch:
            shutil.copyfile(full_start_file_dir, full_pdf_file_end_path)
            
            print(f"Copied pdf file {file_dir}")

        pdf_image_folder_path = pdf_images_end_path / f"Upplaga_{upplaga_number}"
        create_images_switch = False
        
        if gen_type != "new" or Path(pdf_image_folder_path).is_file() is False: # if gen_type = "specific" we check if the folder for that pdf exists, not if it has image files inside
            if "specific" in gen_type:
                desired_upplaga_nmr = gen_type.split(": ")[1]
                if int(upplaga_number) == int(desired_upplaga_nmr):
                    create_images_switch = True
            else:
                create_images_switch = True

        # Create the images from pdf
        if create_images_switch:
            os.makedirs(pdf_image_folder_path, exist_ok=True) # generate the folder
            
            created_pdf_images = convert_from_path(full_start_file_dir)
            for image_nr in range(len(created_pdf_images)):
                created_pdf_images[image_nr].save(pdf_image_folder_path / f"page_{str(image_nr + 1)}.webp", "WEBP")
            
            print(f"Created pdf images for upplaga {upplaga_number}")
    else:
        print("No pdf:s left to copy")
        
    # change the PDFjs_reader.js in the /pdfer/js/ folder so that it has the correct amount of pdfs listed
    pdf_js_program_path = config.base_path / Path("generated/webb/ostraloken.se/webbpage/pdfer/js/PDF_reader.js")
    
    # get the content
    with open(pdf_js_program_path, "tr", encoding="utf-8") as file:  
        js_file_content = file.read() # read it
    
    # Sort amount all pages
    all_amount_pages_sorted = dict(sorted(all_amount_pages.items(), key=lambda item: int(item[0])))
    
    # change the number of amount of pdfs
    js_changed_content = re.sub(r"const amoutPDfs = \d+", f"const amoutPDFs = {amount_of_pdfs}", js_file_content)
    # change how many are max pages
    js_changed_content = re.sub(r"const maxPages = \d+", f"const maxPages = {max(list(all_amount_pages_sorted.values()))}", js_changed_content) 
    # change how many are max pages
    js_changed_content = re.sub(r"const pagesPerPDF = \[.*?\]", f"const pagesPerPDF = {list(all_amount_pages_sorted.values())}", js_changed_content)
    
    # create / find the file
    with open(pdf_js_program_path, "w", encoding="utf-8") as file:
        file.write(js_changed_content) # write to it
    
    print("Uppdated amoutPDFs, maxPages and pagesPerPDF in PDF_reader.js")
    
    # Copy over Om_krisen_kriget_eller_Ulf_Kristersson_kommer
    pdf_start_path = config.base_path / Path("content/extra/Om_krisen_kriget_eller_Ulf_Kristersson_kommer.pdf")
    pdf_file_end_path = config.base_path / Path("generated/webb/ostraloken.se/webbpage/Om_krisen_kriget_eller_Ulf_Kristersson_kommer/pdf_files/Om_krisen_kriget_eller_Ulf_Kristersson_kommer.pdf")
    
    os.makedirs(Path(pdf_file_end_path).parent, exist_ok=True) # generate the folder
    shutil.copyfile(pdf_start_path, pdf_file_end_path)
    
    print(f"Copied pdf file {str(pdf_start_path).split("\\")[-1]}")
