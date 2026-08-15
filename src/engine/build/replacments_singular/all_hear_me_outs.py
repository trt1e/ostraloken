from engine.handle_content import content_reader

# All hear me outs
generated_hear_me_outs = ""
for content in reversed(content_reader.read_txt("hear_me_outs.txt")):
    article_hear_me_out = content["Hear_me_out"]
    article_desc = content["Beskrivning"]
    if article_desc != "":
        article_desc = "<b>Förklaring:</b> " + article_desc
    if len(article_hear_me_out) > 70:
        article_hear_me_out = article_hear_me_out[:70] + "..."
    if len(article_desc) > 500:
        article_desc = article_desc[:500] + "..."
    generated_hear_me_outs += f"""
<article class="article hear_me_out">
    <h2>{article_hear_me_out}</h2>
    <p>{article_desc}</p>
    <div class="smash_pass_area">
        <button class="HMO_button smash_button"><i>SMASH</i></button>
        <button class="HMO_button pass_button"><i>PASS</i></button>
    </div>
</article>
"""

output = generated_hear_me_outs