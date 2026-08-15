from engine import utils
from engine.build import build_articles

# The latest story title
most_recent_story_list = build_articles.generate_preview_article("../a/", "List")[0]
output = utils.remove_html_elements(most_recent_story_list["Rubrik"]).replace('"', "&quot;")