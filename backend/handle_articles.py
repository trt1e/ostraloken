from flask import Flask, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app, origins=["http://127.0.0.1:5500"])

base_path = os.getcwd()
normal_story_path = base_path + r"\ostraloken\backend\content\normal_storys_and_other"
short_story_path = base_path + r"\ostraloken\backend\content\short_storys"
hear_me_outs_path = base_path + r"\ostraloken\backend\content\hear_me_outs.txt"

"""
base_path = r"content/articles/lead_storys"
file_list = os.listdir(base_path)
"""
"""
def read_normal_storys(): # To get the files and their content from all normal articals 
    file_list = os.listdir(normal_story_path) # list all files in dir
    for file in file_list: # Go througth every file in the list and extract the content
        content = open(normal_story_path + "\\" + file, "tr", encoding="utf-8") # extract
        whole_text = content.read() # read it
        
        # find the positions of difrent key parts
        title_pos1 = whole_text.find("## ") + 3
        title_pos2 = whole_text.find(" ##")
        type_pos1 = whole_text.find("¤¤ ") + 3
        type_pos2 = whole_text.find(" ¤¤")
        writer_pos1 = whole_text.find("@@ ") + 3
        writer_pos2 = whole_text.find(" @@")
        
        # Sum up into the title, type, writer and article
        title = whole_text[title_pos1:title_pos2]
        type = whole_text[type_pos1:type_pos2]
        writer = whole_text[writer_pos1:writer_pos2]
        article = whole_text[(writer_pos2 + 4):]
        
        print("Title:", title)
        print("Type:", type)
        print("Writer:", writer)
        print("Article:", article)
        
        content.close() # at the end

def read_short_storys(): # To get the files and their content from all short articals 
    file_list = os.listdir(short_story_path) # list all files in dir
    for file in file_list: # Go througth every file in the list and extract the content
        content = open(short_story_path + "\\" + file, "tr", encoding="utf-8") # extract
        whole_text = content.read() # read it
        
        # find the positions of difrent key parts
        title_pos1 = whole_text.find("## ") + 3
        title_pos2 = whole_text.find(" ##")
        
        # Sum up into the title, type, writer and article
        title = whole_text[title_pos1:title_pos2]
        article = whole_text[(title_pos2 + 4):]
        
        print("Title:", title)
        print("Article:", article)
        
        content.close() # at the end

def read_hear_me_outs(): # To get the contents from all hear me outs
    content = open(hear_me_outs_path, "tr", encoding="utf-8") # extract
    whole_text = content.read() # read it
    last_final_pos = 0
    final_hear_me_outs = []
    final_descs = []
    
    for number_of_HMOs in range(whole_text.count("## ")): # repeat for how many hear me outs there are in the txt
        # find the positions of difrent key parts
        hear_me_out_pos1 = whole_text.find("## ", last_final_pos) + 3
        hear_me_out_pos2 = whole_text.find(" ##", last_final_pos)
        desc_pos1 = whole_text.find("++ ", last_final_pos) + 3
        desc_pos2 = whole_text.find(" ++", last_final_pos)
        last_final_pos = desc_pos2 + 3
        
        # Sum up into the title, type, writer and article
        hear_me_out = whole_text[hear_me_out_pos1:hear_me_out_pos2]
        desc = whole_text[desc_pos1:desc_pos2]
        
        final_hear_me_outs += hear_me_out
        final_descs += desc
        
        print("Hear_me_out:", hear_me_out)
        print("Description:", desc)
    
    content.close() # at the end
    
    return final_hear_me_outs, final_descs
"""

# read_normal_storys()
# read_short_storys()
# read_hear_me_outs()


@app.route("/", methods=["GET"])
def home():
    return jsonify({"data": "hello world"})

@app.route("/normal_storys", methods=["GET"])
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
        output = ({upplaga_number: article_output_sum})
        output_sum.append(output)
        
    return jsonify(output_sum)

@app.route("/short_storys", methods=["GET"])
def read_short_storys(): # To get the files and their content from all short articals 
    file_list = os.listdir(short_story_path) # list all files in dir
    number_of_articles = 0
    output_sum = []
    for file in file_list: # Go througth every file in the list and extract the content
        number_of_articles += 1
        content = open(short_story_path + "\\" + file, "tr", encoding="utf-8") # extract
        whole_text = content.read() # read it
        
        # find the positions of difrent key parts
        title_pos1 = whole_text.find("## ") + 3
        title_pos2 = whole_text.find(" ##")
        
        # Sum up into the title, type, writer and article
        title = whole_text[title_pos1:title_pos2]
        article = whole_text[(title_pos2 + 4):]
        
        """
        print("Title:", title)
        print("Article:", article)
        """
        
        content.close() # at the end
                
        output = ({f"full_info_article_{number_of_articles}": {"Title": title, "Article": article}})
        output_sum.append(output)
        
    return jsonify(output_sum)

@app.route("/hear_me_outs", methods=["GET"])
def read_hear_me_outs(): # To get the contents from all hear me outs
    content = open(hear_me_outs_path, "tr", encoding="utf-8") # extract
    whole_text = content.read() # read it
    last_final_pos = 0
    number_of_hear_me_outs = 0
    output_sum = []
    for number_of_HMOs in range(whole_text.count("## ")): # repeat for how many hear me outs there are in the txt
        number_of_hear_me_outs += 1
        # find the positions of difrent key parts
        hear_me_out_pos1 = whole_text.find("## ", last_final_pos) + 3
        hear_me_out_pos2 = whole_text.find(" ##", last_final_pos)
        desc_pos1 = whole_text.find("++ ", last_final_pos) + 3
        desc_pos2 = whole_text.find(" ++", last_final_pos)
        last_final_pos = desc_pos2 + 3
        
        # Sum up into the title, type, writer and article
        hear_me_out = whole_text[hear_me_out_pos1:hear_me_out_pos2]
        desc = whole_text[desc_pos1:desc_pos2]
        
        """
        print("Hear_me_out:", hear_me_out)
        print("Description:", desc)
        """
        
        output = ({f"full_info_hear_me_out_{number_of_hear_me_outs}": {"Har_me_out": hear_me_out, "Description": desc}})
        output_sum.append(output)
    
    content.close() # at the end
        
    return jsonify(output_sum)

if __name__ == "__main__":
    app.run(debug=True)

"""
Vad som behövs:
 [] API för normala storys
 [] API för korta storys
 [x] API för hear me outs
 [] API för att läsa in igen


@app.route("/", methods=["GET"])
def home():
    return jsonify({"data": "hello world"})

@app.route("/home/<int:num>", methods=["GET"])
def disp(num):
    return jsonify({"data": num ** 2})

if __name__ == "__main__":
    app.run(debug=True)
    
"""