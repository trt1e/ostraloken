from engine import utils
from engine.build import build_articles

output = {}

# The latest story
output[f"[+latest_article+]"] = build_articles.generate_preview_article("../a/", "All")[0]

# The latest story title
most_recent_story_list = build_articles.generate_preview_article("../a/", "List")[0]
output[f"[+latest_title+]"] = utils.remove_html_elements(most_recent_story_list["Rubrik"]).replace('"', "&quot;")
