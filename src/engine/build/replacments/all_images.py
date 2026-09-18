from pathlib import Path

from engine import utils
from engine import config
from engine.handle_content import content_reader
from engine.build import build_articles

# All images linked and in html-structure
generated_images_linked = ""
for utgava in reversed(content_reader.read_articles()):
    # go throught every article in the utgava
    utgava_number = utgava["Editionsnummer"]
    for article in utgava["Content"]:
        if article: # somethimes article is empty, this prevents that
            article_title = str(article[0]["Rubrik"])
            old_img_title = utils.make_image_id(article_title)
            old_img_path_no_extention = config.articles_path / f"utgava_{utgava_number}" / old_img_title
            
            # Check if there is a image linked to the article currantly looked throught
            for ext in config.img_extentions:
                if Path(f"{old_img_path_no_extention}{ext}").is_file():
                    old_img_path_with_extention = f"{old_img_path_no_extention}{ext}"
                    break
            else:
                old_img_path_with_extention = "NO_IMG" # article does not have image
            
            # There is a image linked to this article 
            if old_img_path_with_extention != "NO_IMG":
                image_id = utils.remove_åäö(utils.make_image_id(article_title))
                url_path = "https://ostraloken.se/a/images/" + image_id + ".webp"
                
                # Add this new_img_url_with_extention into a html-structure
                generated_images_linked += f"""
<div class="image_container" id="{image_id}">
    <a target="_blank" href="{url_path}"><img src="{url_path}" loading="lazy" width="800" height="600"></a>
    <h2>{article_title}</h2>
</div>
"""

output = {}
output[f"[+all_images_linked+]"] = generated_images_linked