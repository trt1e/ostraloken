from engine.handle_content import content_reader

# All hear me outs
generated_roda_flaggor = ""
for id_nr, content in enumerate(reversed(content_reader.read_txt("roda_flaggor.txt"))):
    article_rod_flagga = content["Rod_flagga"]
    article_desc = content["Beskrivning"]
    if article_desc != "":
        article_desc = "<b>Förklaring:</b> " + article_desc
    if len(article_rod_flagga) > 70:
        article_hear_me_out = article_rod_flagga[:70] + "..."
    if len(article_desc) > 500:
        article_desc = article_desc[:500] + "..."
    generated_roda_flaggor += f"""
<article class="article rod_flagga" id="HMO_nr_{id_nr}">
    <h2>{article_rod_flagga}</h2>
    <p>{article_desc}</p>
    <div class="rod_flagga_area">
        <button class="RF_button smash_button"><i style="color: red;">Röd flagga</i></button>
        <button class="RF_button pass_button"><i>Inte röd flagga</i></button>
    </div>
</article>
"""

output = {}
output[f"[+all_roda_flaggor+]"] = generated_roda_flaggor