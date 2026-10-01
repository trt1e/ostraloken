from engine.handle_content import reader
from engine.construct import articles

output = {}

# Dynamicly add all static articles
for content in reader.read_txt("static/articles.txt"):
    replacment_name = content["Rubrik"].replace(" ", "_")
    # generate article
    generated_section = articles.generate_static_section(content["Rubrik"], content["Artikel"], content["Bild_källa"])
    output[f"[+{replacment_name}+]"] = generated_section # like ex "[+test+]"
    
    # generate without image
    generated_section = articles.generate_static_section(content["Rubrik"], content["Artikel"], "")
    output[f"[+{replacment_name}:no_img+]"] = generated_section # like ex "[+no_img_test+]"
    
    # add just the article
    output[f"[+{replacment_name}:just_article+]"] = content["Artikel"] # like ex "[+test_article+]"
