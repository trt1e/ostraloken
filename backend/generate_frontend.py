import os
import re

base_path = os.getcwd()

# READ TEXT
normal_story_path = base_path + r"\ostraloken\backend\content\normal_storys_and_other"
short_story_path = base_path + r"\ostraloken\backend\content\short_storys.txt"
hear_me_outs_path = base_path + r"\ostraloken\backend\content\hear_me_outs.txt"

def read_normal_storys(): # To get the files and their content from all normal articals 
    upplaga_list = os.listdir(normal_story_path) # list all folders in dir
    upplaga_number = 0
    article_output_sum = []
    output_sum = []
    for upplaga in upplaga_list: # go thrpguth every folder to get all the upplagor
        file_list = os.listdir(normal_story_path + "\\" + upplaga) # list all files in dir  
        number_of_articles = 0
        article_output_sum = []
        upplaga_number = upplaga.split("_")[1]
        for file in file_list: # Go througth every file in the list and extract the content
            if file != "upplaga_info.txt":
                number_of_articles += 1
                content = open(normal_story_path + "\\" + upplaga + "\\" + file, "tr", encoding="utf-8") # extract
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
        
        output = ({"Number": number_of_hear_me_outs, "Content": {"Har_me_out": hear_me_out, "Description": desc}})
        output_sum.append(output)
    
    content.close() # at the end
        
    return output_sum

# GENERATE SITES
lone_article_template_path = base_path + r"\ostraloken\frontend\template\lone_article.html"

index_template_path = base_path + r"\ostraloken\frontend\template\index.html"
index_generated_path = base_path + r"\ostraloken\frontend\webbpage\index.html"

articles_page_template_path = base_path + r"\ostraloken\frontend\template\articles_site.html"
articles_page_generated_path = base_path + r"\ostraloken\frontend\webbpage\artiklar\index.html"

article_template_path = base_path + r"\ostraloken\frontend\template\articles_pages.html"
generated_articles_path = base_path + r"\ostraloken\frontend\webbpage\a" + "\\"

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
        final_article = template[:redirect_href_title_pos] + redirect_src + template[redirect_href_title_pos:img_src_title_pos] + img_src +  template[img_src_title_pos:article_title_pos] + title + template[article_title_pos:article_type_pos] + type + template[article_type_pos:article_content_pos] + content + template[article_content_pos:article_author_pos] + author + template[article_author_pos:]
    else: # make article not ancor
        first_a_pos = template.find("<a") + 1
        second_a_pos = template.find("</a", first_a_pos) + 2
        final_article = template[:first_a_pos] + "div" + template[(first_a_pos + 1):img_src_title_pos] + img_src +  template[img_src_title_pos:article_title_pos] + title + template[article_title_pos:article_type_pos] + type + template[article_type_pos:article_content_pos] + content + template[article_content_pos:article_author_pos] + author + template[article_author_pos:second_a_pos] + "div" + template[(second_a_pos + 1):]
        
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
                article_title = article["Title"]
                article_main_text = article["Article"][:400]
                article_main_text_last_caracter = article_main_text.find(". ", 200)
                article_type = article["Type"]
                article_author = article["Writer"]
                article_img_src = "./images/Test.png"
                generated_articles += generate_lone_article(("./a/" + re.sub(r"[^a-zA-Z0-9 åäöÅÄÖ]", "", article_title) + ".html"), article_img_src, article_title,(article_main_text[:article_main_text_last_caracter] + "..."), article_type, article_author)
    
    generated_file = open(index_generated_path, "w", encoding="utf-8") # create / find the file
    generated_file.write(template[:article_container_pos] + generated_articles + template[article_container_pos:]) #write to it
    
    template_opend.close()
    
    print("Index successfully generated!")

def generate_articles_page():
    template_opend = open(articles_page_template_path, encoding="utf-8")
    template = template_opend.read()
    
    # Find where it says <!-- [+articles+] -->
    article_container_pos = template.find("<!-- [+articles+] -->") + 22
    
    generated_articles = ""
    
    for upplaga in reversed(read_normal_storys()):
        content = upplaga["Content"]
        if content:
            for article in content:
                article_title = article["Title"]
                article_main_text = article["Article"][:400]
                article_main_text_last_caracter = article_main_text.find(". ", 200)
                article_type = article["Type"]
                article_author = article["Writer"]
                article_img_src = "./images/Test.png"
                generated_articles += generate_lone_article(("./a/" + re.sub(r"[^a-zA-Z0-9 åäöÅÄÖ]", "", article_title) + ".html"), article_img_src, article_title,(article_main_text[:article_main_text_last_caracter] + "..."), article_type, article_author)
    
    generated_file = open(articles_page_generated_path, "w", encoding="utf-8") # create / find the file
    generated_file.write(template[:article_container_pos] + generated_articles + template[article_container_pos:]) #write to it
    
    template_opend.close()
    
    print("Articles page successfully generated!")

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
            
                generated_file = open((generated_articles_path + re.sub(r"[^a-zA-Z0-9 åäöÅÄÖ]", "", article_title) + ".html"), "w", encoding="utf-8") # create / find the file
                generated_file.write(template[:article_pos] + generated_articles + template[article_pos:]) # write to it
            
    template_opend.close()
        
    print("All articles successfully generated!")

# print(read_normal_storys())    
generate_index()
generate_articles_page()
generate_all_articles()