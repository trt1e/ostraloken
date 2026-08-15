from engine.build import build_articles

combined_output = {}

combined_output["[+nav_highlight_cards+]"] = build_articles.get_nav_element(True, True) # image and highlight
combined_output["[+no_img_nav_highlight_cards+]"] = build_articles.get_nav_element(False, True) # no image but highlight
combined_output["[+nav_normal_cards+]"] = build_articles.get_nav_element(True, False) # image but not highlight
combined_output["[+no_img_nav_normal_cards+]"] = build_articles.get_nav_element(False, False) # no image or highlight