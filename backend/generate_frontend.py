import os
import re

is_linux = False

base_path = os.getcwd()

# READ TEXT
# give dirs
if is_linux == True:
    normal_story_path = base_path + r"/backend/content/normal_storys_and_other"
    short_story_path = base_path + r"/backend/content/short_storys.txt"
    hear_me_outs_path = base_path + r"/backend/content/hear_me_outs.txt"
else:
    normal_story_path = base_path + r"\ostraloken\backend\content\normal_storys_and_other"
    short_story_path = base_path + r"\ostraloken\backend\content\short_storys.txt"
    hear_me_outs_path = base_path + r"\ostraloken\backend\content\hear_me_outs.txt"


def read_normal_storys(): # To get the files and their content from all normal articals 
    upplaga_list = os.listdir(normal_story_path) # list all folders in dir
    upplaga_number = 0
    article_output_sum = []
    output_sum = []
    for upplaga in upplaga_list: # go thrpguth every folder to get all the upplagor
        # list all files in dir  
        if is_linux == True:
            file_list = os.listdir(normal_story_path + "/" + upplaga) 
        else:
            file_list = os.listdir(normal_story_path + "\\" + upplaga)
        number_of_articles = 0
        article_output_sum = []
        upplaga_number = upplaga.split("_")[1]
        for file in file_list: # Go througth every file in the list and extract the content
            if file != "upplaga_info.txt":
                number_of_articles += 1
                # extract
                if is_linux == True:
                    content = open(normal_story_path + "/" + upplaga + "/" + file, "tr", encoding="utf-8")
                else:
                    content = open(normal_story_path + "\\" + upplaga + "\\" + file, "tr", encoding="utf-8")
                whole_text = content.read() # read it
                
                # find the positions of difrent key parts
                title_pos1 = whole_text.find("### ") + 4
                title_pos2 = whole_text.find(" ##")
                type_pos1 = whole_text.find("¤¤¤ ") + 4
                type_pos2 = whole_text.find(" ¤¤")
                writer_pos1 = whole_text.find("@@@ ") + 4
                writer_pos2 = whole_text.find(" @@")
                
                # Sum up into the title, type, writer and article
                title = whole_text[title_pos1:title_pos2]
                type = whole_text[type_pos1:type_pos2]
                writer = whole_text[writer_pos1:writer_pos2]
                article = whole_text[(writer_pos2 + 4):]
                
                """
                print("Title:", title)
                print("Type:", type)
                print("Writer:", writer)
                print("Article:", article)
                """
                
                content.close() # at the end
                
                article_output = ({"Title": title, "Type": type, "Writer": writer, "Article": article})
                article_output_sum.append(article_output)
        output = ({"Upplaga": int(upplaga_number), "Content": article_output_sum})
        output_sum.append(output)
        
    output_sum.sort(key=lambda x: int(x["Upplaga"])) # sortera den baserat på upplaga_number
    return output_sum

def read_short_storys(): # To get the files and their content from all short articals 
    content = open(short_story_path, "tr", encoding="utf-8") # extract
    whole_text = content.read() # read it
    last_final_pos = 0
    output_sum = []
    for number_of_articles in range(whole_text.count("## ")): # repeat for how many hear me outs there are in the txt
        # find the positions of difrent key parts
        title_pos1 = whole_text.find("### ", last_final_pos) + 4
        title_pos2 = whole_text.find(" ##", last_final_pos)
        article_pos1 = whole_text.find("+++ ", last_final_pos) + 4
        article_pos2 = whole_text.find(" ++", last_final_pos)
        last_final_pos = article_pos2 + 3
        
        # Sum up into the title, type, writer and article
        title = whole_text[title_pos1:title_pos2]
        article = whole_text[article_pos1:article_pos2]
        
        """
        print("Hear_me_out:", hear_me_out)
        print("Description:", desc)
        """
        
        output = ({"Number": number_of_articles, "Contet": {"Title": title, "Article": article}})
        output_sum.append(output)
    
    content.close() # at the end
        
    return output_sum

def read_hear_me_outs(): # To get the contents from all hear me outs
    content = open(hear_me_outs_path, "tr", encoding="utf-8") # extract
    whole_text = content.read() # read it
    last_final_pos = 0
    output_sum = []
    for number_of_hear_me_outs in range(whole_text.count("## ")): # repeat for how many hear me outs there are in the txt
        # find the positions of difrent key parts
        hear_me_out_pos1 = whole_text.find("### ", last_final_pos) + 4
        hear_me_out_pos2 = whole_text.find(" ##", last_final_pos)
        desc_pos1 = whole_text.find("+++ ", last_final_pos) + 4
        desc_pos2 = whole_text.find(" ++", last_final_pos)
        last_final_pos = desc_pos2 + 3
        
        # Sum up into the title, type, writer and article
        hear_me_out = whole_text[hear_me_out_pos1:hear_me_out_pos2]
        desc = whole_text[desc_pos1:desc_pos2]
        
        """
        print("Hear_me_out:", hear_me_out)
        print("Description:", desc)
        """
        
        output = ({"Number": int(number_of_hear_me_outs), "Content": {"Hear_me_out": hear_me_out, "Description": desc}})
        output_sum.append(output)
    
    content.close() # at the end
        
    return output_sum


# FIX ARTICLES NAMES
def fix_all_backend_articles_names(): # Make the names in articles more consistant
    upplaga_list = os.listdir(normal_story_path) # list all folders in dir
    for upplaga in upplaga_list: # go thrpguth every folder to get all the upplagor
        file_number = 0
        
        # list all files in dir  
        if is_linux == True:
            file_list = os.listdir(normal_story_path + "/" + upplaga) 
        else:
            file_list = os.listdir(normal_story_path + "\\" + upplaga)
        for file in file_list: # Go througth every file in the list and extract the content
            if file != "upplaga_info.txt":
                file_number += 1
                
                # extract
                if is_linux == True:
                    content = open(normal_story_path + "/" + upplaga + "/" + file, "tr", encoding="utf-8")
                else:
                    content = open(normal_story_path + "\\" + upplaga + "\\" + file, "tr", encoding="utf-8")
                whole_text = content.read() # read it
                
                # find the positions of difrent key parts
                title_pos1 = whole_text.find("### ") + 4
                title_pos2 = whole_text.find(" ##")
                
                # Sum up into the title, type, writer and article
                title = whole_text[title_pos1:title_pos2]
                
                content.close() # at the end
                
                new_file_name = str(file_number) + " " + re.sub(r"[^a-zA-Z0-9 åäöÅÄÖ]", "", title).replace(" ", "_")[:100] + ".txt"
                
                if is_linux == True:
                    os.rename((normal_story_path + "/" + upplaga + "/" + file), (normal_story_path + "/" + upplaga + "/" + new_file_name))
                else:
                    os.rename((normal_story_path + "\\" + upplaga + "\\" + file), (normal_story_path + "\\" + upplaga + "\\" + new_file_name))

    print("Article names successfully fixed!")


# GENERATE SITES
# give dirs
if is_linux == True:
    lone_article_template_path = base_path + r"/frontend/template/lone_article.html"

    index_template_path = base_path + r"/frontend/template/index.html"
    index_generated_path = base_path + r"/frontend/webbpage/index.html"

    article_template_path = base_path + r"/frontend/template/articles_pages.html"
    generated_articles_path = base_path + r"/frontend/webbpage/a" + "//"

    hear_me_outs_template_path = base_path + r"/frontend/template/hear_me_outs.html"
    lone_hear_me_out_template_path = base_path + r"/frontend/template/lone_hear_me_out.html"
    hear_me_outs_generated_path = base_path + r"/frontend/webbpage/hear_me_outs/index.html"
else:
    lone_article_template_path = base_path + r"\ostraloken\frontend\template\lone_article.html"

    index_template_path = base_path + r"\ostraloken\frontend\template\index.html"
    index_generated_path = base_path + r"\ostraloken\frontend\webbpage\index.html"

    article_template_path = base_path + r"\ostraloken\frontend\template\articles_pages.html"
    generated_articles_path = base_path + r"\ostraloken\frontend\webbpage\a" + "\\"

    hear_me_outs_template_path = base_path + r"\ostraloken\frontend\template\hear_me_outs.html"
    lone_hear_me_out_template_path = base_path + r"\ostraloken\frontend\template\lone_hear_me_out.html"
    hear_me_outs_generated_path = base_path + r"\ostraloken\frontend\webbpage\hear_me_outs\index.html"

# articles
def generate_lone_article(redirect_src, img_src, title, content, type, author):
    # if you dont want a ancor redirecting to be generated, set redirect_src to "SHOULD_NOT_REDIRECT"
    if redirect_src is None or redirect_src == "":
        redirect_src = "./"
    if img_src is None or img_src == "":
        img_src = "Null"
    if title is None or title == "":
        title = "Null"
    if content is None or content == "":
        content = "Null"
        
    template_opend = open(lone_article_template_path)
    template = template_opend.read()
    

    # Find where you put the redirect src
    redirect_href_title_pos = template.find('a href="') + 8
    # Find where you put the img src
    img_src_title_pos = template.find('img src="') + 9
    # Find where it says <!-- [+title+] -->
    article_title_pos = template.find("<!-- [+title+] -->") + 18 
    # Find where it says <!-- [+type+] -->
    article_type_pos = template.find("<!-- [+type+] -->") + 17
    # Find where it says <!-- [+content+] -->
    article_content_pos = template.find("<!-- [+content+] -->") + 20 
    # Find where it says <!-- [+author+] -->
    article_author_pos = template.find("<!-- [+author+] -->") + 19
    
    if redirect_src != "SHOULD_NOT_REDIRECT":
        final_article = template[:redirect_href_title_pos] + redirect_src + template[redirect_href_title_pos:img_src_title_pos] + img_src +  template[img_src_title_pos:article_type_pos] + type + template[article_type_pos:article_title_pos] + title + template[article_title_pos:article_content_pos] + content + template[article_content_pos:article_author_pos] + author + template[article_author_pos:]
    else: # make article not ancor
        first_a_pos = template.find("<a") + 1
        second_a_pos = template.find("</a", first_a_pos) + 2
        final_article = template[:first_a_pos] + "div" + template[(first_a_pos + 1):img_src_title_pos] + img_src +  template[img_src_title_pos:article_type_pos] + type + template[article_type_pos:article_title_pos] + title + template[article_title_pos:article_content_pos] + content + template[article_content_pos:article_author_pos] + author + template[article_author_pos:second_a_pos] + "div" + template[(second_a_pos + 1):]
        
    template_opend.close()
    return final_article

def generate_index():
    template_opend = open(index_template_path, encoding="utf-8")
    template = template_opend.read()
    
    # Find where it says <!-- [+articles+] -->
    article_container_pos = template.find("<!-- [+articles+] -->") + 22
    
    generated_articles = ""
    
    for upplaga in reversed(read_normal_storys()):
        content = upplaga["Content"]
        if content:
            for article in content:
                extra_after_last_caracter = ""
                extra_span = ""
                article_title = article["Title"]
                org_article_title = article_title
                if len(article_title) >= 70 and article_title.count("</span>") == 0:
                    article_title = article_title[:70] + "..."
                    
                article_main_text = article["Article"][:400]
                # remove any bolding
                if "<b>" in article_main_text:
                    article_main_text = article_main_text.replace("<b>", "")
                    article_main_text = article_main_text.replace("</b>", "")
                # find the last caracter
                article_main_text_last_caracter = article_main_text.find(". ", 200)
                if article_main_text[:article_main_text_last_caracter].find("<br>") != -1: # if <br> exists
                    if article_main_text[article_main_text.find("<br>") - 1] != ">": # so if for example something ends with </i> the i isnt cut of
                        article_main_text_last_caracter = article_main_text.find("<br>") - 1
                    else:
                        article_main_text_last_caracter = article_main_text.find("<br>") - 5
                        extra_after_last_caracter = article_main_text[(article_main_text.find("<br>") - 4):(article_main_text.find("<br>"))]
                # closes span if it was left open
                if article_main_text.count("<span") > article_main_text.count("</span"): 
                    extra_span = "</span>"
                
                article_type = article["Type"]
                article_author = article["Writer"]
                article_img_src = "./images/Test.png"
                generated_articles += generate_lone_article(("./a/" + re.sub(r"[^a-zA-Z0-9 åäöÅÄÖ]", "", org_article_title)[:100].replace(" ", "_") + ".html"), article_img_src, article_title, (article_main_text[:article_main_text_last_caracter] + extra_after_last_caracter + extra_span + "..."), article_type, article_author)
    
    generated_file = open(index_generated_path, "w", encoding="utf-8") # create / find the file
    generated_file.write(template[:article_container_pos] + generated_articles + template[article_container_pos:]) #write to it
    
    template_opend.close()
    
    print("Index successfully generated!")

def generate_all_articles():
    template_opend = open(article_template_path, encoding="utf-8")
    template = template_opend.read()
    
    # Find where it says <!-- [+article+] -->
    article_pos = template.find("<!-- [+article+] -->") + 21
    
    # go throught every upplaga
    for upplaga in read_normal_storys():
        # go throught every article in the upplaga
        for article in upplaga["Content"]:
            if article: # somethimes article is empty, this prevents that
                generated_articles = "" # where we put the article

                article_title = str(article["Title"])
                article_main_text = str(article["Article"])
                article_type = str(article["Type"])
                article_author = str(article["Writer"])
                article_img_src = "../images/Test.png"
                generated_articles += generate_lone_article("SHOULD_NOT_REDIRECT", article_img_src, article_title, article_main_text, article_type, article_author)
            
                generated_file = open((generated_articles_path + re.sub(r"[^a-zA-Z0-9 åäöÅÄÖ]", "", article_title)[:100].replace(" ", "_") + ".html"), "w", encoding="utf-8") # create / find the file
                generated_file.write(template[:article_pos] + generated_articles + template[article_pos:]) # write to it
            
    template_opend.close()
        
    print("All articles successfully generated!")

# hear me outs
def generate_lone_hear_me_out(hear_me_out, description):
    if hear_me_out is None or hear_me_out == "":
        hear_me_out = "Null"
    if description is None:
        description = "Null"
    if description != "":
        description = "<b>Förklaring:</b> " + description
        
    template_opend = open(lone_hear_me_out_template_path)
    template = template_opend.read()
    

    # Find where it says <!-- [+hear_me_out+] -->
    article_hear_me_out_pos = template.find("<!-- [+hear_me_out+] -->") + 24
    # Find where it says <!-- [+desc+] -->
    article_desc_pos = template.find("<!-- [+desc+] -->") + 17
    
    if len(hear_me_out) > 70:
        hear_me_out = hear_me_out[:70] + "..."
        
    if len(description) > 500:
        description = description[:500] + "..."
    
    final_article = template[:article_hear_me_out_pos] + hear_me_out + template[article_hear_me_out_pos:article_desc_pos] + description + template[article_desc_pos:]
        
    template_opend.close()
    return final_article

def generate_hear_me_outs():
    template_opend = open(hear_me_outs_template_path, encoding="utf-8")
    template = template_opend.read()
    
    # Find where it says <!-- [+hear_me_outs+] -->
    hear_me_out_container_pos = template.find("<!-- [+hear_me_outs+] -->") + 26
    
    generated_hear_me_out = ""
    
    for upplaga in reversed(read_hear_me_outs()):
        content = upplaga["Content"]
        if content:
            article_hear_me_out = content["Hear_me_out"]
            article_main_desc = content["Description"]
            generated_hear_me_out += generate_lone_hear_me_out(article_hear_me_out, article_main_desc)
    
    generated_file = open(hear_me_outs_generated_path, "w", encoding="utf-8") # create / find the file
    generated_file.write(template[:hear_me_out_container_pos] + generated_hear_me_out + template[hear_me_out_container_pos:]) #write to it
    
    template_opend.close()
    
    print("Hear me outs successfully generated!")

# print(read_normal_storys())    
generate_index()
generate_hear_me_outs()
generate_all_articles()
fix_all_backend_articles_names()

"""
Saker att lägga till
- sökfunktion
- infinite scroll

Att fixa senare:
- Från och innan upplaga 6 ska skribenterna dubbelkollas
- Alla " ska fixas 
- Alla artiklar innan upplaga 11-5 ska dubbelkollas om artikeln är samma i pdf som text 
- går så alla ettor med <b> har <b>
- dubbelkolla allas typ
- gör system för bilder
- LÄGG TILL BILDER FÖR ALLT
- gör så att den första censurerade blir som den i upplaga 32


GÖR ARTIKLAR <article>
SE TILL ATT LIGHTHOUSE FUNGERAR!!!


Hur man gör så den har infinite scroll:
- Alla artikelsidor har också en bit av rå info som index kan enkelt fetcha
- indexfilen har massa länkar till artikelsidornas info
- js genererar rätt mängd artiklar taget från fetchningen
"""