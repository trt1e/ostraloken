from engine import utils
from engine.handle_content import content_reader
from engine.build import build_articles

# All normal articles fully printed
whole_content_articles = ""
for utgava in reversed(content_reader.read_articles()):
    # go throught every article in the utgava
    utgava_number = utgava["Editionsnummer"]
    for article_bundle in utgava["Content"]:
        article = article_bundle[0]
        if article: # somethimes article is empty, this prevents that
            article_img_src = utils.find_img(utils.remove_html_elements(str(article["Rubrik"])), utgava_number, "https://ostraloken.se/a/images/") # get the url to the right image
            whole_content_articles += build_articles.generate_lone_article("SHOULD_NOT_REDIRECT", article_img_src, str(article["Rubrik"]), str(article["Artikel"]), str(article["Texttyp"]), str(article["Skribent"]), -1, utgava_number)

output = {}
output[f"[+all_articles+]"] = whole_content_articles


# All normal articles preview that you can click and it brings you to that article page
list_of_generated_articles = build_articles.get_all_articles("./a/", "All")
all_generated_articles = ""
for generated_articles in list_of_generated_articles:
    all_generated_articles += str(generated_articles)

output[f"[+all_articles:preview+]"] = all_generated_articles