from engine import utils
from engine.handle_content import content_reader

# All short storys
generated_short_storys = ""
for content in reversed(content_reader.read_txt("notiser.txt")):
    short_story_id = utils.make_notis_id(content["Rubrik"], content["Artikel"])
    generated_short_storys += f"""
<a class="article notis" id="{short_story_id}">
    <article class="">
        <h2>{content["Rubrik"]}</h2>
        <p>{content["Artikel"]}</p>
    </article>
</a>
"""

output = {}
output[f"[+all_notiser+]"] = generated_short_storys