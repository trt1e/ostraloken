from engine import utils
from engine.build import build_articles

output = {}

# The latest story
output[f"[+latest_article+]"] = build_articles.get_all_articles("../a/", "All")[0]

# The latest story title
most_recent_story_list = build_articles.get_all_articles("../a/", "List")[0]
output[f"[+latest_title+]"] = utils.remove_html_elements(most_recent_story_list["Rubrik"]).replace('"', "&quot;")
