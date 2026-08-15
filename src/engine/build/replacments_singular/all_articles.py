from engine import utils
from engine.handle_content import content_reader
from engine.build import build_articles

# All normal articles fully printed
whole_content_articles = ""
for upplaga in reversed(content_reader.read_articles()):
    # go throught every article in the upplaga
    upplaga_number = upplaga["Upplaga"]
    for article_bundle in upplaga["Content"]:
        article = article_bundle[0]
        if article: # somethimes article is empty, this prevents that
            article_img_src = utils.find_img(utils.remove_html_elements(str(article["Rubrik"])), upplaga_number, "https://ostraloken.se/a/images/") # get the url to the right image
            whole_content_articles += build_articles.generate_lone_article("SHOULD_NOT_REDIRECT", article_img_src, str(article["Rubrik"]), str(article["Artikel"]), str(article["Texttyp"]), str(article["Skribent"]), 0, upplaga_number)

output = whole_content_articles