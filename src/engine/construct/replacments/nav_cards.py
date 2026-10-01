from engine.construct import articles

output = {}

output["[+nav_highlight_cards+]"] = articles.get_nav_element(True, {"Viktig": " highlight", "Speciell": "highlight attention"}) # image and highlight
output["[+nav_highlight_cards:no_img+]"] = articles.get_nav_element(False, {"Viktig": " highlight", "Speciell": "highlight attention"}) # no image but highlight
output["[+nav_normal_cards+]"] = articles.get_nav_element(True, None) # image but not highlight
output["[+nav_normal_cards:no_img+]"] = articles.get_nav_element(False, None) # no image or highlight