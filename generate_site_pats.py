import os
import re
import random
import math
from pathlib import Path
from dotenv import load_dotenv # For reading secrets
import datetime # To set the date of last update
from PIL import Image, ImageOps, ImageDraw, ImageFont # To handle the images copyd and instagram images
import shutil # To copy files (pdfs)
import qrcode # To create qr-codes
from qrcode.image.pil import PilImage # To create qr-codes
import progressbar # To show a progressbar in the backend terminal
from pdf2image import convert_from_path # To extract the pdfs to images
from pypdf import PdfReader # To get how many pages

# import scripts
import main
import base_commands
import read_content

base_path = Path(__file__).resolve().parent


# images
def find_img(article_title, upplaga_nmr, base_url):
    old_img_title = base_commands.make_image_id(article_title)
    new_img_title = base_commands.remove_åäö(base_commands.make_image_id(article_title))
    old_img_path_no_extention = read_content.normal_story_path / f"upplaga_{upplaga_nmr}" / old_img_title
    for ext in main.img_extentions:
        if os.path.isfile(f"{old_img_path_no_extention}.{ext}") is True:
            old_img_path_with_extention = f"{old_img_path_no_extention}.{ext}"
            break
    else:
        old_img_path_with_extention = "NO_IMG" # article does not have image
        
    if old_img_path_with_extention != "NO_IMG":
        return base_url + new_img_title + ".webp"
    else:
        return ""

def copy_over_images(gen_type):
    instagram_article_image_template_path = base_path / Path("instagram_images/templates/Normal_article.png")
    instagram_upplaga_image_template_1_path = base_path / Path("instagram_images/templates/Upplaga_1.png")
    instagram_upplaga_image_template_2_path = base_path / Path("instagram_images/templates/Upplaga_2.png")
    
    generated_images_path = base_path / Path("webb/ostraloken.se/webbpage/a/images")
    generated_upplaga_images_path = base_path / Path("webb/ostraloken.se/webbpage/pdfer/pdf_images")
    
    generated_instagram_images_path = base_path / Path("instagram_images/final_images")
    
    all_articles = read_content.read_normal_storys()
    
    # go throught every upplaga
    for upplaga in all_articles:
        # go throught every article in the upplaga
        upplaga_number = upplaga["Upplaga"]
        image_number = 0
        for article in upplaga["Content"]:
            if article: # somethimes article is empty, this prevents that
                article_title = str(article["Title"])
                old_img_title = base_commands.make_image_id(article_title)
                new_img_title = base_commands.remove_åäö(base_commands.make_image_id(article_title)) + ".webp"
                new_img_title_insta = f"{image_number + 1}-" + base_commands.remove_åäö(base_commands.make_image_id(article_title))[4:].split(".")[0] + ".png"
                old_img_path_no_extention = read_content.normal_story_path / f"upplaga_{upplaga_number}" / old_img_title
                for ext in main.img_extentions:
                    if os.path.isfile(f"{old_img_path_no_extention}.{ext}") is True:
                        old_img_path_with_extention = f"{old_img_path_no_extention}.{ext}"
                        image_number += 1
                        break
                else:
                    old_img_path_with_extention = "NO_IMG" # article does not have image
                
                if old_img_path_with_extention != "NO_IMG": # Create insta image
                    # if all and no file: YES
                    # if all and file: YES
                    # if new and no file: YES
                    # if new and file: NO                        
                    instagram_destination_folder = generated_instagram_images_path / f"Upplaga_{upplaga_number}"
                    instagram_image_destination_dir = instagram_destination_folder / new_img_title_insta
                    if gen_type != "new" or os.path.isfile(instagram_image_destination_dir) is False: # either gen_typ isn't new, or if it is, we still let it pass if there is no file
                        create_image_switch = False
                        if "specific" in gen_type:
                            desired_upplaga_nmr = gen_type.split(": ")[1]
                            if int(upplaga_number) == int(desired_upplaga_nmr):
                                create_image_switch = True
                        else:
                            create_image_switch = True

                        # Instagram image
                        if create_image_switch: 
                            os.makedirs(instagram_destination_folder, exist_ok=True) # generate the folder / make sure it exists
                            
                            # Copy over image to instagram format
                            old_insta_image = Image.open(old_img_path_with_extention)
                            insta_overlay = Image.open(instagram_article_image_template_path)
                            
                            # create a blac slate of orange 1000x1000px
                            insta_image = Image.new("RGB", (1000, 1000), color=(238, 115, 34)) # Have full canvas that is just orange
                            
                            # Add text
                            text_to_place = base_commands.remove_html_elements(article_title)
                            textarea_width = 950 # px
                            draw_insta_image = ImageDraw.Draw(insta_image)
                            # Import impact
                            impact_font = base_path / Path("instagram_images/templates/impact.ttf")
                            insta_font = ImageFont.truetype(impact_font, 64)
                            # Split up the son-to-be-drawn-text
                            currant_x_length = 0
                            words_on_row = ""
                            how_many_rows = math.ceil(insta_font.getlength(text_to_place) / textarea_width)
                            currant_y = 1000 - ((70 * how_many_rows) + 20)
                            org_y = currant_y
                            length_of_blank = insta_font.getlength(" ")
                            for word_number, word in enumerate(text_to_place.split(" "), 1):
                                word_length = insta_font.getlength(word + " ") # get the pixel length of the word
                                if word_length + currant_x_length >= textarea_width or word_number == len(text_to_place.split(" ")):
                                    # if its the last word, make sure its counted in
                                    last_word_and_too_long = False
                                    if word_number == len(text_to_place.split(" ")):
                                        if not word_length + currant_x_length >= textarea_width: # only if the new word doesnt make the row too long
                                            words_on_row += word + " "
                                            currant_x_length += word_length
                                        else:
                                            last_word_and_too_long = True # This makes so later the last word is added on a new row

                                    # Print the currant row
                                    # calculate the x
                                    currant_x = 500 - ((currant_x_length - length_of_blank) / 2)
                                    # Draw the row
                                    draw_insta_image.text((currant_x, currant_y), words_on_row[0:-1], (255, 255, 255), font=insta_font)
                                    
                                    # In the case that this last word makes the row too long
                                    # Then we go through and add the last word on a new row!
                                    if last_word_and_too_long:
                                        # calculate the x
                                        currant_extra_x = 500 - (word_length / 2)
                                        currant_extra_y = currant_y + 70
                                        # Draw the row
                                        draw_insta_image.text((currant_extra_x, currant_extra_y), word, (255, 255, 255), font=insta_font)
                                    
                                    # go to the next row
                                    currant_x_length = 0
                                    currant_y += 70
                                    words_on_row = ""
                                    
                                # Add word to word row and to row length
                                words_on_row += word + " "
                                currant_x_length += word_length
                            
                            
                            # Zoom in the image to a 1000x1000 aspect ratio
                            height_of_undersection = (org_y - 20) # px (old: 217px)
                            old_insta_image = ImageOps.fit(old_insta_image, (1000, height_of_undersection), method=0, bleed=0.0, centering=(0.5, 0.5))
                            insta_image.paste(old_insta_image, (0, 0)) # Paste the old
                            insta_image.paste(insta_overlay, (0, 0), mask = insta_overlay) # Add the template for a normal article as overlay
                            
                            # Add a qr-code to the image
                            upplaga_qr = qrcode.QRCode(
                                box_size=50,
                                border=1.5
                            )
                            upplaga_qr.add_data(f"https://ostraloken.se/a/{base_commands.make_article_id(article_title, upplaga_number)}")
                            upplaga_qr.make(fit=True)
                            upplaga_img_qr = upplaga_qr.make_image(
                                fill_color="white",
                                back_color="#EE7322", 
                                image_factory=PilImage
                            ).convert("RGB")
                            length = 250
                            upplaga_img_qr = upplaga_img_qr.resize((length, length))
                            insta_image.paste(upplaga_img_qr, ((1000 - length), (height_of_undersection - length))) # Add the qr code to the article
                            
                            insta_image.save(instagram_image_destination_dir, quality=100)
                            print(f"Created Instagram image: {new_img_title_insta}")
                            
                            # create a upplaga image
                            if image_number == 1: # if its the first article, so it only does this once per upplaga
                                upplaga_first_page_dir = generated_upplaga_images_path / f"Upplaga_{upplaga_number}" / "page_1.webp"
                                instagram_image_upplaga_destination_dir = instagram_destination_folder / f"Read_upplaga_{upplaga_number}-1.png"
                                
                                # Have the image (1000x1000px)
                                insta_upplaga_image = Image.open(instagram_upplaga_image_template_1_path)
                                
                                # add first page
                                insta_upplaga_first_page = Image.open(upplaga_first_page_dir)
                                width, height = insta_upplaga_first_page.size
                                new_width = 800
                                new_height = int(height * (new_width / width))
                                insta_upplaga_first_page = insta_upplaga_first_page.resize((new_width, new_height))
                                # insta_upplaga_first_page = insta_upplaga_first_page.rotate(-30)
                                insta_upplaga_image.paste(insta_upplaga_first_page, (100, 150)) # Add the upplagas first page
                                
                                # Add a qr-code to the image
                                upplaga_qr = qrcode.QRCode(
                                    box_size=50,
                                    border=1.5
                                )
                                upplaga_qr.add_data(f"https://ostraloken.se/pdfer/?upplaga={upplaga_number}")
                                upplaga_qr.make(fit=True)
                                upplaga_img_qr = upplaga_qr.make_image(
                                    fill_color="white", 
                                    back_color="#E97C26", 
                                    image_factory=PilImage
                                ).convert("RGB")
                                length = 325
                                upplaga_img_qr = upplaga_img_qr.resize((length, length))
                                insta_upplaga_image.paste(upplaga_img_qr, ((1000 - length), (1000 - length))) # Add the upplagas first page
                                
                                insta_upplaga_image.save(instagram_image_upplaga_destination_dir, quality=100)
                                print(f"Created Instagram upplaga image 1 for upplaga {upplaga_number}")
                                
                                # Create the second instagram image
                                instagram_image_upplaga_destination_dir = instagram_destination_folder / f"Read_upplaga_{upplaga_number}-2.png"
                                
                                # Have the image (1000x1000px)
                                insta_upplaga_image = Image.open(instagram_upplaga_image_template_2_path)
                                draw_insta_upplaga_image = ImageDraw.Draw(insta_upplaga_image)
                                
                                # Import impact
                                impact_font = base_path / Path("instagram_images/templates/impact.ttf")
                                insta_font = ImageFont.truetype(impact_font, 48)
                                
                                # Add some articles
                                currant_y = 140
                                constant_x = 70
                                for new_upplaga in all_articles:
                                    if upplaga_number == new_upplaga["Upplaga"]:
                                        for new_article_number, new_article in enumerate(new_upplaga["Content"]):
                                            if new_article: # somethimes article is empty, this prevents that
                                                # this now we get all article titles from the currant upplaga
                                                new_article_title = "● " + str(base_commands.remove_html_elements(new_article["Title"]))
                                                
                                                # check so it fits, if it doesnt, we cut it down and add ... at the end
                                                if insta_font.getlength(new_article_title) >= (1000 - (constant_x * 1.5)): # we check if the articles titles length is smaller than half constant_x to the right
                                                    # article title doesnt fit :(
                                                    dont_use_letters_amount = len(new_article_title) # we keep a list of how many of the letters we disgard
                                                    for letter in reversed(str(new_article_title)): # we go through every letter to find how many we need to remove!
                                                        if insta_font.getlength(new_article_title[:dont_use_letters_amount] + "...") < (1000 - (constant_x * 1.5)):
                                                            # Ok, it was enought, now we just remove the dont use letters and add ... at the end!
                                                            new_article_title = new_article_title[:dont_use_letters_amount] + "..."
                                                            break
                                                        else: # not enought, to the next letter
                                                            dont_use_letters_amount -= 1
                                                
                                                # Draw the article title as text
                                                draw_insta_upplaga_image.text((constant_x, currant_y), new_article_title, (255, 255, 255), font=insta_font)

                                                currant_y += 90
                                                
                                                if new_article_number >= 6: # on the fith run
                                                    break
                                                
                                draw_insta_upplaga_image.text((70, currant_y), "● Och mycket mer!", (255, 255, 255), font=insta_font)

                                
                                insta_upplaga_image.save(instagram_image_upplaga_destination_dir, quality=100)
                                print(f"Created Instagram upplaga image 2 for upplaga {upplaga_number}")
                                
                    
                    # Copy over image to destination in /a/images/
                    # if all and no file: YES
                    # if all and file: YES
                    # if new and no file: YES
                    # if new and file: NO
                    new_img_url_with_extention = generated_images_path / new_img_title
                    if gen_type != "new" or os.path.isfile(new_img_url_with_extention) is False: # either gen_typ isn't new, or if it is, we still let it pass if there is no file
                        create_image_switch = False
                        if "specific" in gen_type:
                            desired_upplaga_nmr = gen_type.split(": ")[1]
                            if int(upplaga_number) == int(desired_upplaga_nmr):
                                create_image_switch = True
                        else:
                            create_image_switch = True

                        if create_image_switch:
                            image = Image.open(old_img_path_with_extention)
                            img_width, img_height = image.size
                            new_width = 1000
                            new_height = int((new_width / img_width) * img_height)
                            new_image = image.resize((new_width, new_height))
                            new_image.save(new_img_url_with_extention, quality=80)
                            print(f"Copied image: {new_img_title}")
                    else: # gen type == "new" and os.path.isfile(new_img_url_with_extention) is True
                        pass
    else:
        print("No images left to copy")

# Copy pdf:s
def copy_over_pdfs(gen_type):
    pdf_start_path = base_path / Path("content/pdfs")
    pdf_file_end_path = base_path / Path("webb/ostraloken.se/webbpage/pdfer/pdf_files")
    pdf_images_end_path = base_path / Path("webb/ostraloken.se/webbpage/pdfer/pdf_images")
    
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
        
        full_pdf_file_end_path = pdf_file_end_path / base_commands.remove_åäö(file_dir)
        copy_file_switch = False
        
        if gen_type != "new" or os.path.isfile(full_pdf_file_end_path) is False:
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
        
        if gen_type != "new" or os.path.isdir(pdf_image_folder_path) is False: # if gen_type = "specific" we check if the folder for that pdf exists, not if it has image files inside
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
    pdf_js_program_path = base_path / Path("webb/ostraloken.se/webbpage/pdfer/js/PDF_reader.js")
    
    # get the content
    js_file_content = base_commands.try_opening(pdf_js_program_path, "tr") # read it
    
    # Sort amount all pages
    all_amount_pages_sorted = dict(sorted(all_amount_pages.items(), key=lambda item: int(item[0])))
    
    # change the number of amount of pdfs
    js_changed_content = re.sub(r"const amoutPDfs = \d+", f"const amoutPDFs = {amount_of_pdfs}", js_file_content)
    # change how many are max pages
    js_changed_content = re.sub(r"const maxPages = \d+", f"const maxPages = {max(list(all_amount_pages_sorted.values()))}", js_changed_content) 
    # change how many are max pages
    list_there_alredy = base_commands.find_between(js_changed_content, "const pagesPerPDF = [", "] // ID=pagesPerPDF", 0)
    js_changed_content = js_changed_content.replace(f"const pagesPerPDF = [{str(list_there_alredy)}]", f"const pagesPerPDF = {list(all_amount_pages_sorted.values())}")
    
    changed_js_file = open(pdf_js_program_path, "w", encoding="utf-8") # create / find the file
    changed_js_file.write(js_changed_content) # write to it
    changed_js_file.close()
    
    print("Uppdated amoutPDFs, maxPages and pagesPerPDF in PDF_reader.js ")

# basic for all generated text files
def generate_site(template_path, generated_path, dictionary_of_replacment, file_type): # the sites that dont realy need to be generated    
    template = base_commands.try_opening(template_path, "")
    
    final_file = template
    for item in dictionary_of_replacment:
        final_file = final_file.replace(str(item), str(dictionary_of_replacment[item]))
    
    # add something to notify the user that it is editing in the generated file instead of templates
    row_endings = []
    start_warning = ""
    end_warning = ""
    if file_type == "html":
        row_endings = ["<head>", "</head>", "<body>", "</body>", "<header>", "</header>", "<main>", "</main>", "<footer>", "</footer>"]
        start_warning = "<!--"
        end_warning = "-->"
    elif file_type == "css" or file_type == "js":
        row_endings = ["{"]
        start_warning = "/*"
        end_warning = "*/"
    
    for ending in row_endings:
        final_file = final_file.replace(str(ending), f"{ending} {start_warning}ATTENTION: YOU ARE RIGHT NOW IN A GENERATED FILE!{end_warning}")
    
    # add header
    header_read = get_base("webb/ostraloken.se/templates/base/header.html")
    final_file = final_file.replace("[+header+]", header_read) # add header
    final_file = final_file.replace("[+index_header+]", header_read.replace("../", "./")) # add header for specificly index
    
    # add footer
    footer_read = get_base("webb/ostraloken.se/templates/base/footer.html")
    final_file = final_file.replace("[+footer+]", footer_read) # add footer
    
    # add general scripts
    scripts_read = get_base("webb/ostraloken.se/templates/base/general_scripts.html")
    final_file = final_file.replace("[+general_scripts+]", scripts_read)
    final_file = final_file.replace("[+index_general_scripts+]", scripts_read.replace("../", "./")) # add scripts for specificly index
    
    generated_file = open(generated_path, "w", encoding="utf-8") # create / find the file
    generated_file.write(final_file) # write to it
    generated_file.close()

# static articles
def generate_static_section(title, content, image_src):
    if title is None or title == "":
        title = "Null"
    if content is None or content == "":
        content = "Null"
    if image_src is None or image_src == "":
        image_context = "<!-- NO IMAGE HERE -->"
    else:
        image_context = f'<img src="{image_src}" alt="{image_src}" width="800" height="600">'
    
    final_article = f"""
<article class="article" id="{title.replace(" ", "_")}">
    {image_context}
    <h2>{title}</h2>
    <p class="main_article_text">{content}</p>
</article>
"""
        
    return final_article

# base elements (like header and footer)
def get_base(path):
    worked_path = base_path / Path(path)
    content = open(worked_path, "r", encoding="utf-8") # get its content
    final = content.read()
    content.close()
    
    for replacment in replacment_for_all:
        final = final.replace(replacment, replacment_for_all[replacment])
    
    return final

# articles
def generate_lone_article(redirect_src, img_src, title, content, type, author, article_nmr, upplaga_nmr):
    # if you dont want a ancor redirecting to be generated, set redirect_src to "SHOULD_NOT_REDIRECT"
    if redirect_src is None or redirect_src == "":
        redirect_src = "./" # no redirect
    if img_src is None or img_src == "" or img_src == "NO_IMAGE_AVAILABLE":
        no_img_class = "no_img"
        image_context = "<!-- NO IMAGE HERE -->"
    else:
        no_img_class = ""
        image_extra = f'alt="{base_commands.strip_string(title, -1).replace("_", " ")}"' # add the alt text
        if article_nmr != 0: # this is so the first image dosn't have loading lazy so it dosnt pop in
            image_extra += ' loading="lazy"'
        else:
            image_extra += ' fetchpriority="high"'
            
        image_context = f'<img src="{img_src}" {image_extra} width="800" height="600">'
    if title is None or title == "":
        title = "Null"
    if content is None or content == "":
        content = "Null"
    if type is None or type == "":
        type_context = "<!-- NO TYPE HERE -->"
    else:
        type_context = f'<p class="type_text">{type}</p>'
        
    # generate the article id
    article_id = base_commands.make_article_id(title, upplaga_nmr)
    # We strip the title of any unwanted caracters and replace spaces with _. Then we do the same to the author but only the first 15 caracters and last we add type if there is any caracters left since it then cuts of so its only combinend 100 caracters
    
    if redirect_src == "SHOULD_NOT_REDIRECT": # Not anchor
        author_context = f'<p class="author_text"><b>{author}</b></p>'
        
        # list Löken head writers
        head_writers = ["Vilhelm Grill", "Joar Stange", "John Ericson", "Magne Nordström", "Elliot Sandström"]
        # if author is one of head Löken writers: point their name to their part of kontaktinfo 
        if author in head_writers:
            author_context = f'<p class="author_text"><a href="https://ostraloken.se/om_oss/#{author.replace(" ", "_")}"><b>{author}</b></a></p>'
        
        final_article = f"""
<article id="{article_id}" class="article {no_img_class}"> <!--Add the "no_img" class to article if it has no image-->
    {type_context}
    {image_context}
    <h1>{title}</h1> <!-- This is the h1 since nothing else is on this page -->
    <p>{content}</p>
    {author_context}
</article>
"""
    else: # make article anchor
        final_article = f"""
<a href="{redirect_src}" id="{article_id}" class="article {no_img_class}"> <!--Add the "no_img" class to article if it has no image-->
    <article>
        {type_context}
        {image_context}
        <h2>{title}</h2>
        <p>{content}</p>
        <p class="author_text"><b>{author}</b></p>
    </article>
</a>
"""

    return final_article

def generate_preview_article(base_redirect_html_url, get_what_articles):
    how_many_articles_generated = 0
    generated_articles = [] # for get_what_articles == "All"
    generated_articles_based_on_type = {} # for get_what_articles == "Similar"
    generated_list = [] # for get_what_articles == "List"
    
    for upplaga in reversed(read_content.read_normal_storys()):
        upplaga_number = upplaga["Upplaga"]
        content = upplaga["Content"]
        if content: # if there is content, content is the text, title, type and author
            for article in content:
                extra_at_end = ""
                article_title = article["Title"]
                basic_article_title = base_commands.remove_html_elements(article_title)
                org_article_title = basic_article_title # so that even if title is shortend, it is still the same URL
                # shorten down article titles over 70 characters
                if len(basic_article_title) >= 70:
                    if ">" in article_title:
                        if article_title[30:].find(">") == -1: # if there is no ">" in the first 30 characters
                            title_end_pos = article_title.find(">")
                        else:
                            title_end_pos = int(article_title[30:].find(">")) + 30
                        basic_article_title = basic_article_title[:title_end_pos] + base_commands.fix_cut_of_html_elements(basic_article_title) + "..." # add back any cut of html elements
                    else:
                        basic_article_title = basic_article_title[:70] + base_commands.fix_cut_of_html_elements(basic_article_title) + "..."
                
                article_main_text = article["Article"][:400]
                # remove any bolding
                if "<b>" in article_main_text:
                    article_main_text = article_main_text.replace("<b>", "")
                    article_main_text = article_main_text.replace("</b>", "")
                    
                # find the last character
                article_main_text_last_caracter_pos = 400 # if no . ? ! : ; or <br> is found: this is used and we cut at the 400:th character
                article_main_text_last_caracter_match = re.search(r"\.|\?|\!|\:|\;", article_main_text[200:]) # this finds a . ? ! : or ; in the last 200-400 characters
                if article_main_text_last_caracter_match:
                    article_main_text_last_caracter_pos = article_main_text_last_caracter_match.start() + 200 # .start() gives position at cut, we add 200 since article_main_text was started on 200
                    
                    # se if its closed by a <br> before the . ? ! : or ;
                    if article_main_text[:article_main_text_last_caracter_pos].find("<br>") != -1: # if <br> exists
                        end_characters = [".", "?", "!", ":", ";"]
                        for character in end_characters: # so that it only removes the last character if it is one of . ? ! : or ;
                            if character == article_main_text[article_main_text.find("<br>") - 1]:
                                article_main_text_last_caracter_pos = article_main_text.find("<br>") - 1 # do -1 since we know that it only does it if there is a . ? ! : or ; before
                                break
                        else:
                            article_main_text_last_caracter_pos = article_main_text.find("<br>")
                else:
                    if article_main_text.find("<br>") != -1: # if <br> exists
                        break_pos = article_main_text.find("<br>")
                        article_main_text_last_caracter_pos = break_pos
                
                # the text cut of at the right place
                shorted_main_text = article_main_text[:article_main_text_last_caracter_pos]
                            
                # add back any cut of html elements
                extra_at_end = base_commands.fix_cut_of_html_elements(shorted_main_text)
                                    
                article_type = article["Type"]
                article_author = article["Writer"]
                
                # not basic_title since that has been shortend alredy
                article_id = base_commands.make_article_id(article_title, upplaga_number) # what is used to identefy the article

                if get_what_articles == "All":
                    img_url = find_img(org_article_title, upplaga_number, f"{base_redirect_html_url}images/") # get the url to the img as a html link
                    generated_articles.append(generate_lone_article((base_redirect_html_url + article_id + ".html"), img_url, article_title, (shorted_main_text + extra_at_end + "..."), article_type, article_author, how_many_articles_generated, upplaga_number))
                    how_many_articles_generated += 1
                elif get_what_articles == "Similar":
                    if article_type not in generated_articles_based_on_type:
                        generated_articles_based_on_type[article_type] = {} # initialize generated_articles_based_on_type[article_type]
                    generated_articles_based_on_type[article_type].update({article_id: generate_lone_article(("./" + article_id + ".html"), None, article_title, (shorted_main_text + extra_at_end + "..."), None, article_author, -1, upplaga_number)})
                    how_many_articles_generated += 1
                else: # get_what_articles == "List"
                    generated_list.append(article)
                    
    if get_what_articles == "All":
        return generated_articles
    elif get_what_articles == "Similar":
        return generated_articles_based_on_type
    else: # get_what_articles == "List"
        return generated_list

def generate_all_articles():
    article_template_path = base_path / Path("webb/ostraloken.se/templates/a/articles_pages.html")
    generated_articles_path = base_path / Path("webb/ostraloken.se/webbpage/a")
    
    list_of_articles_with_similer_type = generate_preview_article("./a/", "Similar")
    all_short_storys = read_content.read_txt(read_content.short_story_path, read_content.short_story_selection)
    
    random.seed(hash(str(all_short_storys) + str(list_of_articles_with_similer_type)))
    
    print("Generating all articles:")
    progressbar_item = progressbar.ProgressBar(maxval=int(len(read_content.read_normal_storys())))
    progressbar_item.start()
    
    # go throught every upplaga
    for progressbar_ticker, upplaga in enumerate(read_content.read_normal_storys()):
        # go throught every article in the upplaga
        upplaga_number = upplaga["Upplaga"]
        upplaga_date = upplaga["Release_date"]
        upplaga_extra_info = upplaga["Extra_upplaga_info"]
        progressbar_item.update(progressbar_ticker + 1)
        for article in upplaga["Content"]:
            if article: # somethimes article is empty, this prevents that       
                generated_article = "" # where we put the article
                has_extra_info = False
                
                # this is done early so it is over the article itself
                if upplaga_extra_info != "" and upplaga_extra_info != None and has_extra_info == False:
                    has_extra_info = True
                    # add the extra content
                    generated_article += f"""
<div class="article extra_info attention">
    <p><b>Notera:</b> {upplaga_extra_info}</p>
</div>  
"""        
                article_title = str(article["Title"])
                basic_article_title = base_commands.remove_html_elements(article_title)
                article_main_text = str(article["Article"])
                article_type = str(article["Type"])
                article_author = str(article["Writer"])
                # copy over images and get the url to the right image
                article_img_src = find_img(basic_article_title, upplaga_number, "./images/")
                generated_article += generate_lone_article("SHOULD_NOT_REDIRECT", article_img_src, article_title, article_main_text, article_type, article_author, 0, upplaga_number)

                # generate the article id
                article_id = base_commands.make_article_id(article_title, upplaga_number)

                if article_type == "Insändare" and has_extra_info == False: # this is "else if" so that it cant both have extra upplaga info and a write-a-insändare prompt
                    has_extra_info = True
                    # add prompt to write insändare if it is a insändare
                    generated_article += """
<a class="article extra_info user_prompt" href="https://forms.gle/bBiEhDSCFijSFoHk9" target="_blank">
    <h2>Skicka in en insändare!</h2>
    <p>Vill du också skicka en insändare till Östra Löken? Fyll bara i denna korta enkät!</p>
</a>
"""

                # add scrolling news feed
                random_short_story = all_short_storys[random.randint(0, len(all_short_storys) - 1)]["Content"]
                final_random_short_story = f"<b>{random_short_story["Title"]}</b> • {random_short_story["Article"]}"
                short_story_id = base_commands.make_short_story_id(random_short_story["Title"], random_short_story["Article"])
                feed_element = f"""
<div id="scrolling_news_feed">
    <a href="../notiser/#{short_story_id}">{final_random_short_story}</a>
</div>
"""

                replacment = {
                    "[+description+]": base_commands.remove_html_elements(article_main_text)[:200].replace('"', "&quot;") + "...",
                    "[+url+]": f"https://ostraloken.se/a/{article_id}",
                    "[+home_url+]": f"../#{article_id}",
                    "[+title+]": article_title.replace('"', "&quot;"),
                    "[+title_basic+]": base_commands.remove_html_elements(article_title).replace('"', "&quot;"),
                    "[+article_type+]": article_type,
                    "[+article_type_basic+]": base_commands.remove_html_elements(article_type),
                    "[+article_author+]": article_author,
                    "[+article_author_basic+]": base_commands.remove_html_elements(article_author),
                    "[+upplaga_date_ISO_8601+]": f"{upplaga_date.split("-")[2]}-{upplaga_date.split("-")[1].zfill(2)}-{upplaga_date.split("-")[0].zfill(2)}",
                    "[+article+]": generated_article,
                    "[+upplaga_number+]": str(upplaga_number),
                    "[+upplaga_date+]": upplaga_date,
                    "[+h3_text_to_intorduce_section+]": "<h3>Läs liknande artiklar:</h3>", # so it can be removed
                    "[+thumb_image_url+]": "https://ostraloken.se/images/meta/Östra_Löken_webbsida_cover_image.png", # basic backup image
                    "[+scrolling_news_feed+]": feed_element # add news feed
                } # what gets replaced and with what
                
                if article_img_src is not None and article_img_src != "": # make image in preview to the article image if one exists
                    replacment["[+thumb_image_url+]"] = f"https://ostraloken.se/a/images/IMG-{article_id}.webp"
                
                # generate extra articles
                dict_of_similar_articles = dict(list_of_articles_with_similer_type)[article_type]
                dict_of_similar_articles_copy = dict_of_similar_articles.copy() # we do this so we can edit it without changing the original
                dict_of_similar_articles_copy.pop(article_id) # remove the article (the one you are adding "read also" too) from the dict
                new_list_of_similar_articles = list(dict_of_similar_articles_copy.values())
                if new_list_of_similar_articles != []:
                    random.seed(hash(str(new_list_of_similar_articles) + "1")) # we set the seed so that if we are to make a small change and push it it doesnt change everything, only when we add, remove or change articles of that type does this change
                    chosen_article = new_list_of_similar_articles[random.randint(0, len(new_list_of_similar_articles) - 1)] # this random function is determaistic so if we enter the same seed and same command it will give the same result which we want!
                    replacment[f"[+extra_article_link_1+]"] = chosen_article
                    new_list_of_similar_articles.remove(chosen_article) # we remove it so it isn't listed again
                    
                    if new_list_of_similar_articles != []:
                        random.seed(hash(str(new_list_of_similar_articles) + "2"))
                        chosen_article = new_list_of_similar_articles[random.randint(0, len(new_list_of_similar_articles) - 1)]
                        replacment[f"[+extra_article_link_2+]"] = chosen_article
                        new_list_of_similar_articles.remove(chosen_article)
                        
                        if new_list_of_similar_articles != []:
                            random.seed(hash(str(new_list_of_similar_articles) + "3"))
                            chosen_article = new_list_of_similar_articles[random.randint(0, len(new_list_of_similar_articles) - 1)]
                            replacment[f"[+extra_article_link_3+]"] = chosen_article
                        else:
                            replacment[f"[+extra_article_link_3+]"] = ""
                    else:
                        replacment[f"[+extra_article_link_2+]"] = ""
                        replacment[f"[+extra_article_link_3+]"] = ""
                else:
                    replacment["[+h3_text_to_intorduce_section+]"] = "" # make so there is no h3 text if there are no extra links
                    replacment[f"[+extra_article_link_1+]"] = ""
                    replacment[f"[+extra_article_link_2+]"] = ""
                    replacment[f"[+extra_article_link_3+]"] = ""
                
                generate_site(article_template_path, (generated_articles_path / (article_id + ".html")), replacment, "html")
    
    random.seed()
    progressbar_item.finish()
    print("All articles successfully generated!")

# Nav page
def get_nav_element(img_switch, highlight_switch):
    generated_nav_element = ""
    
    for links_bundle in read_content.read_txt(read_content.external_links_content_path, read_content.external_links_content_selection):
        content = links_bundle["Content"]
        if content:
            nav_element_important_status = content["Important"]
            if str(nav_element_important_status) == str(highlight_switch):
                nav_element_image_src = content["Image_src"]
                if img_switch and not (nav_element_image_src is None or nav_element_image_src == ""):
                    image_context = f'<img src="{nav_element_image_src}" alt="{nav_element_image_src}">'
                else:
                    image_context = "<!-- NO IMAGE HERE -->"
                    
                if nav_element_important_status == "True":
                    highlight_context = " highlight"
                else:
                    highlight_context = ""
                
                generated_nav_element += f"""
<a class="article clickable_element nav_card{highlight_context}" target="_blank" href="{content["Link"]}">
    <h2>{content["Title"]}</h2>
    {image_context}
</a>
"""

    return generated_nav_element


# Create the dictionary where all articles (exept /a/ articles) are run through to see and replace using the dict generated here
def create_dictionary():
    replacment_dictionary = {}
    
    # Add go up button
    replacment_dictionary["[+go_up+]"] = """
<button id="go_up">
    <svg width="100%" height="100%" viewBox="0 0 400 300" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" xml:space="preserve" xmlns:serif="http://www.serif.com/" style="fill-rule:evenodd;clip-rule:evenodd;stroke-linejoin:round;stroke-miterlimit:2;">
        <g transform="matrix(1,0,0,1,1.28586,-100)">
            <g transform="matrix(1.232315,-0.038988,0.083035,1.234494,-33.300057,-56.518675)">
                <path d="M128.273,321.058L117.364,330.939C111.936,325.411 106.658,319.737 101.229,314.21C93.175,306.009 85.046,297.882 76.916,289.755C66.327,279.169 55.662,268.658 45.073,258.072L62.896,241.928C72.386,253.511 81.793,265.161 91.283,276.743C98.567,285.635 105.852,294.527 113.218,303.351C118.183,309.299 123.308,315.111 128.273,321.058Z" style="fill:currentColor;"/>
            </g>
            <g transform="matrix(0.575378,-0.866878,0.635263,0.785159,-135.892841,100.50832)">
                <path d="M297.669,507.928L286.604,517.95C243.179,470.858 199.689,423.829 156.265,376.738C134.554,353.193 112.432,330.016 91.197,306.041C76.476,289.42 63.173,271.631 48.452,255.011L59.517,244.989C74.603,261.278 90.993,276.272 106.079,292.561C127.841,316.059 148.722,340.36 170.009,364.289C212.585,412.149 255.093,460.068 297.669,507.928Z" style="fill:currentColor;"/>
            </g>
            <g transform="matrix(-0.038151,0.057479,-0.042121,-0.05206,86.735403,259.912122)">
                <path d="M53.984,250C71.791,255.317 89.585,259.88 107.392,265.197C122.369,269.669 235.991,303.593 294.619,324.189C305.694,328.079 418.997,367.882 431.632,386.83C450.231,414.719 473.499,440.962 487.404,470.51C500.894,499.176 509.26,529.486 512.234,558.107C515.209,586.729 512.916,614.851 504.927,639.11C504.853,639.333 464.405,703.17 464.306,703.22C441.78,714.547 422.386,731.415 396.691,737.142C371.762,742.699 343.551,742.205 315.363,736.42C287.175,730.635 257.839,719.319 230.643,703.066C223.042,698.523 164.198,663.354 145.108,627.585C120.644,581.748 91.814,444.048 88.487,428.155C79.859,386.945 71.804,345.789 63.836,304.646C60.303,286.402 57.518,268.245 53.984,250Z" style="fill:currentColor;"/>
            </g>
            <g transform="matrix(-0.038988,-1.232315,1.234494,-0.083035,-252.534198,337.284534)">
                <path d="M128.273,321.058L117.364,330.939C111.936,325.411 106.658,319.737 101.229,314.21C93.175,306.009 85.046,297.882 76.916,289.755C66.327,279.169 55.662,268.658 45.073,258.072L62.896,241.928C72.386,253.511 81.793,265.161 91.283,276.743C98.567,285.635 105.852,294.527 113.218,303.351C118.183,309.299 123.308,315.111 128.273,321.058Z" style="fill:currentColor;"/>
            </g>
        </g>
    </svg>
</button>
"""
    
    # All normal articles preview that you can click and it brings you to that article page
    list_of_generated_articles = generate_preview_article("./a/", "All")
    all_generated_articles = ""
    for generated_articles in list_of_generated_articles:
        all_generated_articles += str(generated_articles)
    replacment_dictionary["[+all_preview_articles+]"] = all_generated_articles
    
    # All normal articles fully printed
    whole_content_articles = ""
    for upplaga in reversed(read_content.read_normal_storys()):
        # go throught every article in the upplaga
        upplaga_number = upplaga["Upplaga"]
        for article in upplaga["Content"]:
            if article: # somethimes article is empty, this prevents that
                article_img_src = find_img(base_commands.remove_html_elements(str(article["Title"])), upplaga_number, "https://ostraloken.se/a/images/") # get the url to the right image
                whole_content_articles += generate_lone_article("SHOULD_NOT_REDIRECT", article_img_src, str(article["Title"]), str(article["Article"]), str(article["Type"]), str(article["Writer"]), 0, upplaga_number)
    replacment_dictionary["[+all_articles+]"] = whole_content_articles
    
    # All short storys
    generated_short_storys = ""
    for short_story_bundle in reversed(read_content.read_txt(read_content.short_story_path, read_content.short_story_selection)):
        content = short_story_bundle["Content"]
        short_story_id = base_commands.make_short_story_id(content["Title"], content["Article"])
        generated_short_storys += f"""
<a class="article notis" id="{short_story_id}">
    <article class="">
        <h2>{content["Title"]}</h2>
        <p>{content["Article"]}</p>
    </article>
</a>
"""
    replacment_dictionary["[+all_short_storys+]"] = generated_short_storys
    
    # All hear me outs
    generated_hear_me_outs = ""
    for hear_me_out_bundle in reversed(read_content.read_txt(read_content.hear_me_outs_path, read_content.hear_me_outs_selection)):
        content = hear_me_out_bundle["Content"]
        article_hear_me_out = content["Hear_me_out"]
        article_desc = content["Description"]
        if article_desc != "":
            article_desc = "<b>Förklaring:</b> " + article_desc
        if len(article_hear_me_out) > 70:
            article_hear_me_out = article_hear_me_out[:70] + "..."
        if len(article_desc) > 500:
            article_desc = article_desc[:500] + "..."
        generated_hear_me_outs += f"""
<article class="article hear_me_out">
    <h2>{article_hear_me_out}</h2>
    <p>{article_desc}</p>
    <div class="smash_pass_area">
        <button class="HMO_button smash_button"><i>SMASH</i></button>
        <button class="HMO_button pass_button"><i>PASS</i></button>
    </div>
</article>
"""
    replacment_dictionary["[+all_hear_me_outs+]"] = generated_hear_me_outs
    
    # Dynamicly add all static articles
    for static_bundle in reversed(read_content.read_txt(read_content.static_articles_path, read_content.static_articles_selection)):
        content = static_bundle["Content"]
        replacment_name = content["Title"].replace(" ", "_")
        # generate article
        generated_section = generate_static_section(content["Title"], content["Article"], content["Image_src"])
        replacment_dictionary[f"[+{replacment_name}+]"] = generated_section # like ex "[+test+]"
        
        # generate without image
        generated_section = generate_static_section(content["Title"], content["Article"], "")
        replacment_dictionary[f"[+no_img_{replacment_name}+]"] = generated_section # like ex "[+no_img_test+]"
        
        # add just the article
        replacment_dictionary[f"[+{replacment_name}_article+]"] = content["Article"] # like ex "[+test_article+]"
    
    # Add content from staff
    generated_sections = ""
    staff_list = ""
    for staff_bundle in read_content.read_txt(read_content.staff_info_path, read_content.staff_info_selection):
        content = staff_bundle["Content"]
        staff_list += f'<p>{content["Name"]}</p>'
        
        name = content["Name"]
        image_src = content["Image_src"]
        if image_src is None or image_src == "":
            image_context = "<!-- NO IMAGE HERE -->"
        else:
            image_context = f'<img src="{image_src}" alt="{name}">'
        
        generated_sections += f"""
<div class="kontakt_card" id="{name.replace(" ", "_")}">
    <div class="kontakt_card_not_link_section">
        {image_context}
        <div class="kontakt_card_text_section">
            <h2>{content["Title"]}: {name}</h2>
            <p>{content["Description"]}</p>
        </div>
    </div>
    <!--
    <a class="article clickable_element highlight" href="mailto:{content["Email"]}"><p><b>Skicka epost till {name}</b></p></a>
    -->
</div>
"""
        
        
    # List of staff as html button elements which lead to their email
    replacment_dictionary["[+staff_email_buttons+]"] = generated_sections
    # List of staff as links to their kontaktinfo page
    replacment_dictionary["[+staff_list+]"] = staff_list
    
    # The latest story
    replacment_dictionary["[+latest_article+]"] = generate_preview_article("../a/", "All")[0]
    # The latest story title
    most_recent_story_list = generate_preview_article("../a/", "List")[0]
    replacment_dictionary["[+latest_title+]"] = base_commands.remove_html_elements(most_recent_story_list["Title"]).replace('"', "&quot;")
    
    # Get the nav cards
    replacment_dictionary["[+nav_highlight_cards+]"] = get_nav_element(True, True) # image and highlight
    replacment_dictionary["[+no_img_nav_highlight_cards+]"] = get_nav_element(False, True) # no image but highlight
    replacment_dictionary["[+nav_normal_cards+]"] = get_nav_element(True, False) # image but not highlight
    replacment_dictionary["[+no_img_nav_normal_cards+]"] = get_nav_element(False, False) # no image or highlight
    
    # Last uppdated aka the currant date at which you run this
    date_today = datetime.datetime.now()
    replacment_dictionary["[+last_updated+]"] = f"{date_today.strftime(r"%d")}-{date_today.strftime(r"%m")}-{date_today.strftime(r"%Y")} {date_today.strftime(r"%H")}:{date_today.strftime(r"%M")}"
    
    print("Dictionary created")
    
    return replacment_dictionary

replacment_for_all = create_dictionary()

# Go throught and generate all non /a/ articles
def generate_all_normal_pages(): # go throught every file in templates
    template_base_paths = [
        base_path / Path("webb/nyhetsflode.ostraloken.se/templates"),
        base_path / Path("webb/ostraloken.se/templates")
    ]
    for template_path in template_base_paths:
        basic_template_files_list = os.listdir(template_path) # list all folders in dir
        for file_dir in basic_template_files_list:
            if "." in file_dir: # If it is not a folder
                whole_file_dir = template_path / file_dir
                whole_file = base_commands.try_opening(whole_file_dir, "tr")
                destination_dir = base_commands.find_between(whole_file, "<!--@( ", " )@-->", 0)
                whole_destination_dir = base_path / Path(destination_dir)
                generate_site(whole_file_dir, whole_destination_dir, replacment_for_all, file_dir.split(".")[-1])
                print(f"Generated {str(template_path).split("\\")[-2]}: {file_dir}")
