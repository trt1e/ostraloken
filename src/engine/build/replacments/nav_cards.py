from engine.build import articles

output = {}

output["[+nav_highlight_cards+]"] = articles.get_nav_element(True, True) # image and highlight
output["[+nav_highlight_cards:no_img+]"] = articles.get_nav_element(False, True) # no image but highlight
output["[+nav_normal_cards+]"] = articles.get_nav_element(True, False) # image but not highlight
output["[+nav_normal_cards:no_img+]"] = articles.get_nav_element(False, False) # no image or highlight