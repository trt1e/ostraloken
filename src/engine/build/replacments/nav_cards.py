from engine.build import build_articles

output = {}

output["[+nav_highlight_cards+]"] = build_articles.get_nav_element(True, True) # image and highlight
output["[+nav_highlight_cards:no_img+]"] = build_articles.get_nav_element(False, True) # no image but highlight
output["[+nav_normal_cards+]"] = build_articles.get_nav_element(True, False) # image but not highlight
output["[+nav_normal_cards:no_img+]"] = build_articles.get_nav_element(False, False) # no image or highlight