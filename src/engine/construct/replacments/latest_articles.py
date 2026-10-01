from engine import utils
from engine.construct import articles

output = {}

# The latest story
output[f"[+latest_article+]"] = articles.get_all_articles("../a/", "All")[0]

# The latest story title
most_recent_story_list = articles.get_all_articles("../a/", "List")[0]
output[f"[+latest_title+]"] = utils.remove_html_elements(most_recent_story_list["Rubrik"]).replace('"', "&quot;")
