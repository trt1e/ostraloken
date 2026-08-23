import os
import math
from pathlib import Path
from PIL import Image, ImageOps, ImageDraw, ImageFont # To handle the images copyd and instagram images
import qrcode # To create qr-codes
from qrcode.image.pil import PilImage # To create qr-codes
from pdf2image import convert_from_path # To extract the pdfs to images

# import scripts
from engine import config
from engine import utils
from engine.handle_content import content_reader

# images
def copy_over_images(gen_type):
    instagram_article_image_template_path = config.base_path / Path("generated/social_media_imgs/templates/Normal_article.png")
    instagram_upplaga_image_template_1_path = config.base_path / Path("generated/social_media_imgs/templates/Upplaga_1.png")
    instagram_upplaga_image_template_2_path = config.base_path / Path("generated/social_media_imgs/templates/Upplaga_2.png")
    
    generated_images_path = config.base_path / Path("generated/webb/ostraloken.se/webbsite/a/images")
    generated_upplaga_images_path = config.base_path / Path("generated/webb/ostraloken.se/webbsite/pdfer/pdf_images")
    
    generated_social_media_imgs_path = config.base_path / Path("generated/social_media_imgs/output")
    
    all_articles = content_reader.read_articles()
    
    # go throught every upplaga
    for upplaga in all_articles:
        # go throught every article in the upplaga
        upplaga_number = upplaga["Upplaga"]
        image_number = 0
        for article in upplaga["Content"]:
            if article: # somethimes article is empty, this prevents that
                article_title = str(article[0]["Rubrik"])
                old_img_title = utils.make_image_id(article_title)
                new_img_title = utils.remove_åäö(utils.make_image_id(article_title)) + ".webp"
                new_img_title_insta = f"{image_number + 1}-" + utils.remove_åäö(utils.make_image_id(article_title))[4:].split(".")[0] + ".png"
                old_img_path_no_extention = content_reader.articles_path / f"upplaga_{upplaga_number}" / old_img_title
                for ext in config.img_extentions:
                    if Path(f"{old_img_path_no_extention}.{ext}").is_file():
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
                    instagram_destination_folder = generated_social_media_imgs_path / f"Upplaga_{upplaga_number}"
                    instagram_image_destination_dir = instagram_destination_folder / new_img_title_insta
                    if gen_type != "new" or Path(instagram_image_destination_dir).is_file() is False: # either gen_typ isn't new, or if it is, we still let it pass if there is no file
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
                            text_to_place = utils.remove_html_elements(article_title)
                            textarea_width = 950 # px
                            draw_insta_image = ImageDraw.Draw(insta_image)
                            # Import impact
                            impact_font = config.base_path / Path("generated/social_media_imgs/templates/impact.ttf")
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
                            upplaga_qr.add_data(f"https://ostraloken.se/a/{utils.make_article_id(article_title, upplaga_number)}")
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
                            print(f"Created social media image: {new_img_title_insta}")
                            
                            # create a upplaga image
                            if image_number == 1: # if its the first article, so it only does this once per upplaga
                                upplaga_first_page_dir = generated_upplaga_images_path / f"Upplaga_{upplaga_number}" / "page_1.webp"
                                instagram_image_upplaga_destination_dir = instagram_destination_folder / f"Read_upplaga_{upplaga_number}-1.png"

                                if upplaga_first_page_dir.is_file():
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
                                    print(f"Created social media upplaga image 1 for upplaga {upplaga_number}")
                                    
                                    # Create the second instagram image
                                    instagram_image_upplaga_destination_dir = instagram_destination_folder / f"Read_upplaga_{upplaga_number}-2.png"
                                    
                                    # Have the image (1000x1000px)
                                    insta_upplaga_image = Image.open(instagram_upplaga_image_template_2_path)
                                    draw_insta_upplaga_image = ImageDraw.Draw(insta_upplaga_image)
                                    
                                    # Import impact
                                    impact_font = config.base_path / Path("generated/social_media_imgs/templates/impact.ttf")
                                    insta_font = ImageFont.truetype(impact_font, 48)
                                    
                                    # Add some articles
                                    currant_y = 140
                                    constant_x = 70
                                    for new_upplaga in all_articles:
                                        if upplaga_number == new_upplaga["Upplaga"]:
                                            for new_article_number, new_article in enumerate(new_upplaga["Content"]):
                                                if new_article: # somethimes article is empty, this prevents that
                                                    # this now we get all article titles from the currant upplaga
                                                    new_article_title = "● " + str(utils.remove_html_elements(new_article[0]["Rubrik"]))
                                                    
                                                    # check so it fits, if it doesnt, we cut it down and add ... at the end
                                                    if insta_font.getlength(new_article_title) >= (1000 - (constant_x * 1.5)): # we check if the articles titles length is smaller than half constant_x to the right
                                                        # article title doesnt fit :(
                                                        dont_use_letters_amount = len(new_article_title) # we keep a list of how many of the letters we disgard
                                                        for _ in reversed(str(new_article_title)): # we go through every letter to find how many we need to remove!
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
                                    print(f"Created social media upplaga image 2 for upplaga {upplaga_number}")
                                else:
                                    print(f"No pdf generated for upplaga {upplaga_number} so no social media posts could be created!")
                                
                    
                    # Copy over image to destination in /a/images/
                    # if all and no file: YES
                    # if all and file: YES
                    # if new and no file: YES
                    # if new and file: NO
                    new_img_url_with_extention = generated_images_path / new_img_title
                    if gen_type != "new" or Path(new_img_url_with_extention).is_file() is False: # either gen_typ isn't new, or if it is, we still let it pass if there is no file
                        create_image_switch = False
                        if "specific" in gen_type:
                            desired_upplaga_nmr = gen_type.split(": ")[1]
                            if int(upplaga_number) == int(desired_upplaga_nmr):
                                create_image_switch = True
                        else:
                            create_image_switch = True

                        if create_image_switch:
                            os.makedirs(Path(old_img_path_with_extention).parent, exist_ok=True) # generate the folder / make sure it exists
                            image = Image.open(old_img_path_with_extention)
                            img_width, img_height = image.size
                            new_width = 1000
                            new_height = int((new_width / img_width) * img_height)
                            new_image = image.resize((new_width, new_height))
                            new_image.save(new_img_url_with_extention, quality=80)
                            print(f"Copied image: {new_img_title}")
                    else: # gen type == "new" and Path(new_img_url_with_extention).is_file():
                        pass
    else:
        print("No images left to copy")
