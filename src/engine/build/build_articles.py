import re
import random
from pathlib import Path
import progressbar # To show a progressbar in the backend terminal

# import scripts
from engine import config
from engine import utils
from engine.handle_content import content_reader
from engine.build import gen_replacment_dict


# ---------------------------------------------
# CORE BUILDING
# ---------------------------------------------

# base elements (like header or footer)
def get_base(path):
    # get its content
    with open(Path(path), "tr", encoding="utf-8") as file:
        content = file.read() # read the content
    
    for replacment in gen_replacment_dict.replacment_for_all:
        content = content.replace(replacment, gen_replacment_dict.replacment_for_all[replacment])
    
    return content

# basic for all generated text files
def generate_site(template_path, generated_path, dictionary_of_replacment): # the sites that dont realy need to be generated    
    with open(template_path, "tr", encoding="utf-8") as file:  
        template = file.read() # read it
    
    final_file = template
    for item in dictionary_of_replacment:
        final_file = final_file.replace(str(item), str(dictionary_of_replacment[item]))
    
    # add something to notify the user that it is editing in the generated file instead of templates
    row_endings = []
    start_warning = ""
    end_warning = ""
    file_type = Path(generated_path).suffix
    if file_type == ".html":
        row_endings = ["<head>", "</head>", "<body>", "</body>", "<header>", "</header>", "<main>", "</main>", "<footer>", "</footer>", "</p>"]
        start_warning = "<!--"
        end_warning = "-->"
    elif file_type == ".css" or file_type == ".js":
        row_endings = ["}"]
        start_warning = "/*"
        end_warning = "*/"
    
    for ending in row_endings:
        final_file = final_file.replace(str(ending), f"{ending} {start_warning}ATTENTION: YOU ARE RIGHT NOW IN A GENERATED FILE!{end_warning}")
    
    # Add the base elements
    base_dir_path = config.base_path / Path("generated/webb/ostraloken.se/templates/base/")
    for file in Path(base_dir_path).iterdir():
        data_read = get_base(base_dir_path / file.name)
        final_file = final_file.replace(f"[+{file.stem}+]", data_read) # add data to final file
        final_file = final_file.replace(f"[+{file.stem}:index_version+]", data_read.replace("../", "./")) # add index version of data to final file (for index.html)
    
    # create / find the file
    with open(generated_path, "w", encoding="utf-8") as file:
        file.write(final_file) # write to it


# ---------------------------------------------
# STATIC ARTICLES
# ---------------------------------------------

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


# ---------------------------------------------
# ARTICLES
# ---------------------------------------------

# create the article for preview or /a/ articles
def generate_lone_article(redirect_src, img_src, title, content, type, author, article_nmr, upplaga_nmr): # upplaga_nmr should be -1 if its the only/primary article
    # if you dont want a ancor redirecting to be generated, set redirect_src to "SHOULD_NOT_REDIRECT"
    if redirect_src is None or redirect_src == "":
        redirect_src = "./" # no redirect
    if img_src is None or img_src == "" or img_src == "NO_IMAGE_AVAILABLE":
        no_img_class = "no_img"
        image_context = "<!-- NO IMAGE HERE -->"
    else:
        no_img_class = ""
        image_extra = f'alt="{utils.strip_string(title, -1).replace("_", " ")}"' # add the alt text
        if article_nmr != 0 and article_nmr != -1: # this is so the first image dosn't have loading lazy so it dosnt pop in
            image_extra += ' loading="lazy"'
            
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
    article_id = utils.make_article_id(title, upplaga_nmr)
    # We strip the title of any unwanted caracters and replace spaces with _. Then we do the same to the author but only the first 15 caracters and last we add type if there is any caracters left since it then cuts of so its only combinend 100 caracters
    
    if redirect_src == "SHOULD_NOT_REDIRECT": # Not anchor
        author_context = f'<p class="author_text"><b>{author}</b></p>'
        # if author is one of head Löken writers: point their name to their part of kontaktinfo 
        if author in utils.head_writers:
            author_context = f'<p class="author_text"><a href="https://ostraloken.se/om_oss/#{author.replace(" ", "_")}"><b>{author}</b></a></p>'
        
        h_tag = "h2"
        if article_nmr == -1:
            h_tag = "h1"
        
        final_article = f"""
<article id="{article_id}" class="article {no_img_class}"> <!--Add the "no_img" class to article if it has no image-->
    {type_context}
    {image_context}
    <{h_tag}>{title}</{h_tag}> <!-- This is the h1 since nothing else is on this page -->
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

# Generate the preview articles in index and sok
def get_all_articles(base_redirect_html_url, get_what_articles):
    how_many_articles_generated = 0
    generated_articles = [] # for get_what_articles == "All"
    generated_articles_based_on_type = {} # for get_what_articles == "Similar"
    generated_list = [] # for get_what_articles == "List"
    
    for upplaga in reversed(content_reader.read_articles()):
        upplaga_number = upplaga["Upplaga"]
        content = upplaga["Content"]
        if content: # if there is content, content is the text, title, type and author
            for article_bundle in content:
                article = article_bundle[0]
                extra_at_end = ""
                article_title = article["Rubrik"]
                basic_article_title = utils.remove_html_elements(article_title)
                org_article_title = basic_article_title # so that even if title is shortend, it is still the same URL
                # shorten down article titles over 70 characters
                if len(basic_article_title) >= 70:
                    if ">" in article_title:
                        if article_title[30:].find(">") == -1: # if there is no ">" in the first 30 characters
                            title_end_pos = article_title.find(">")
                        else:
                            title_end_pos = int(article_title[30:].find(">")) + 30
                        basic_article_title = basic_article_title[:title_end_pos] + utils.fix_cut_of_html_elements(basic_article_title) + "..." # add back any cut of html elements
                    else:
                        basic_article_title = basic_article_title[:70] + utils.fix_cut_of_html_elements(basic_article_title) + "..."
                
                article_main_text = article["Artikel"][:400]
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
                extra_at_end = utils.fix_cut_of_html_elements(shorted_main_text)
                                    
                article_type = article["Texttyp"]
                article_author = article["Skribent"]
                
                # not basic_title since that has been shortend alredy
                article_id = utils.make_article_id(article_title, upplaga_number) # what is used to identefy the article

                if get_what_articles == "All":
                    img_url = utils.find_img(org_article_title, upplaga_number, f"{base_redirect_html_url}images/") # get the url to the img as a html link
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

# Generate all the article files in /a/
def generate_all_articles():
    article_template_path = config.base_path / Path("generated/webb/ostraloken.se/templates/a/articles_pages.html")
    generated_articles_path = config.base_path / Path("generated/webb/ostraloken.se/webbsite/a")
    
    list_of_articles_with_similer_type = get_all_articles("./a/", "Similar")
    all_short_storys = content_reader.read_txt("notiser.txt")
    
    random.seed(hash(str(all_short_storys) + str(list_of_articles_with_similer_type)))
    
    print("Generating all articles:")
    progressbar_item = progressbar.ProgressBar(maxval=int(len(content_reader.read_articles())))
    progressbar_item.start()
    
    # go throught every upplaga
    for progressbar_ticker, upplaga in enumerate(content_reader.read_articles()):
        # go throught every article in the upplaga
        upplaga_number = upplaga["Upplaga"]
        upplaga_date = upplaga["Release_date"]
        upplaga_extra_info = upplaga["Extra_upplaga_info"]
        progressbar_item.update(progressbar_ticker + 1)
        for article_bundle in upplaga["Content"]:
            article = article_bundle[0]
            if article: # somethimes article is empty, this prevents that       
                generated_article = "" # where we put the article
                has_extra_info = False
                
                # this is done early so it is over the article itself
                if upplaga_extra_info != "" and upplaga_extra_info is not None and has_extra_info is False:
                    has_extra_info = True
                    # add the extra content
                    generated_article += f"""
<div class="article extra_info attention">
    <p><b>Notera:</b> {upplaga_extra_info}</p>
</div>  
"""
                article_title = article["Rubrik"]
                basic_article_title = utils.remove_html_elements(article_title)
                article_main_text = article["Artikel"]
                article_type = article["Texttyp"]
                article_author = article["Skribent"]
                # copy over images and get the url to the right image
                article_img_src = utils.find_img(basic_article_title, upplaga_number, "./images/")
                generated_article += generate_lone_article("SHOULD_NOT_REDIRECT", article_img_src, article_title, article_main_text, article_type, article_author, -1, upplaga_number)

                # generate the article id
                article_id = utils.make_article_id(article_title, upplaga_number)

                if article_type == "Insändare" and has_extra_info is False: # this is "else if" so that it cant both have extra upplaga info and a write-a-insändare prompt
                    has_extra_info = True
                    # add prompt to write insändare if it is a insändare
                    generated_article += """
<a class="article extra_info user_prompt" href="https://forms.gle/bBiEhDSCFijSFoHk9" target="_blank">
    <h2>Skicka in en insändare!</h2>
    <p>Vill du också skicka en insändare till Östra Löken? Fyll bara i denna korta enkät!</p>
</a>
"""

                # add scrolling news feed
                random_short_story = all_short_storys[random.randint(0, len(all_short_storys) - 1)]
                final_random_short_story = f"<b>{random_short_story["Rubrik"]}</b> • {random_short_story["Artikel"]}"
                short_story_id = utils.make_short_story_id(random_short_story["Rubrik"], random_short_story["Artikel"])
                feed_element = f"""
<div id="scrolling_news_feed">
    <a href="../notiser/#{short_story_id}">{final_random_short_story}</a>
</div>
"""

                replacment = {
                    "[+description+]": utils.remove_html_elements(article_main_text)[:200].replace('"', "&quot;") + "...",
                    "[+url+]": f"https://ostraloken.se/a/{article_id}",
                    "[+home_url+]": f"../#{article_id}",
                    "[+title+]": article_title.replace('"', "&quot;"),
                    "[+title_basic+]": utils.remove_html_elements(article_title).replace('"', "&quot;"),
                    "[+article_type+]": article_type,
                    "[+article_type_basic+]": utils.remove_html_elements(article_type),
                    "[+article_author+]": article_author,
                    "[+article_author_basic+]": utils.remove_html_elements(article_author),
                    "[+upplaga_date_ISO_8601+]": f"{upplaga_date.split("-")[2]}-{upplaga_date.split("-")[1].zfill(2)}-{upplaga_date.split("-")[0].zfill(2)}",
                    "[+article+]": generated_article,
                    "[+upplaga_number+]": str(upplaga_number),
                    "[+upplaga_date+]": upplaga_date,
                    "[+text_to_intorduce_section+]": '<h2 id="read_similar">Läs liknande artiklar:</h2>', # so it can be removed
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
                    replacment["[+extra_article_link_1+]"] = chosen_article
                    new_list_of_similar_articles.remove(chosen_article) # we remove it so it isn't listed again
                    
                    if new_list_of_similar_articles != []:
                        random.seed(hash(str(new_list_of_similar_articles) + "2"))
                        chosen_article = new_list_of_similar_articles[random.randint(0, len(new_list_of_similar_articles) - 1)]
                        replacment["[+extra_article_link_2+]"] = chosen_article
                        new_list_of_similar_articles.remove(chosen_article)
                        
                        if new_list_of_similar_articles != []:
                            random.seed(hash(str(new_list_of_similar_articles) + "3"))
                            chosen_article = new_list_of_similar_articles[random.randint(0, len(new_list_of_similar_articles) - 1)]
                            replacment["[+extra_article_link_3+]"] = chosen_article
                        else:
                            replacment["[+extra_article_link_3+]"] = ""
                    else:
                        replacment["[+extra_article_link_2+]"] = ""
                        replacment["[+extra_article_link_3+]"] = ""
                else:
                    replacment["[+text_to_intorduce_section+]"] = "" # make so there is no h3 text if there are no extra links
                    replacment["[+extra_article_link_1+]"] = ""
                    replacment["[+extra_article_link_2+]"] = ""
                    replacment["[+extra_article_link_3+]"] = ""
                
                generate_site(article_template_path, (generated_articles_path / (article_id + ".html")), replacment)
    
    random.seed()
    progressbar_item.finish()
    print("All articles successfully generated!")


# ---------------------------------------------
# OTHER
# ---------------------------------------------

# Nav page
def get_nav_element(img_switch, highlight_switch):
    generated_nav_element = ""
    
    for content in content_reader.read_txt("static/external_links.txt"):
        if content:
            nav_element_important_status = content["Viktigt"]
            if str(nav_element_important_status) == str(highlight_switch):
                nav_element_image_src = content["Bild_källa"]
                if img_switch and not (nav_element_image_src is None or nav_element_image_src == ""):
                    image_context = f'<img src="{nav_element_image_src}" alt="{nav_element_image_src}">'
                else:
                    image_context = "<!-- NO IMAGE HERE -->"
                    
                if nav_element_important_status == "True":
                    highlight_context = " highlight"
                else:
                    highlight_context = ""
                
                generated_nav_element += f"""
<a class="article clickable_element nav_card{highlight_context}" target="_blank" href="{content["Länk"]}">
    <h2>{content["Rubrik"]}</h2>
    {image_context}
</a>
"""

    return generated_nav_element