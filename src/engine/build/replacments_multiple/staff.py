from engine.handle_content import content_reader

# Add content from staff
generated_sections = ""
staff_list = ""
for content in content_reader.read_txt("static/staff.txt"):
    staff_list += f'<p>{content["Namn"]}</p>'
    
    name = content["Namn"]
    image_src = content["Bild_källa"]
    if image_src is None or image_src == "":
        image_context = "<!-- NO IMAGE HERE -->"
    else:
        image_context = f'<img src="{image_src}" alt="{name}">'
    
    generated_sections += f"""
<div class="kontakt_card" id="{name.replace(" ", "_")}">
    <div class="kontakt_card_not_link_section">
        {image_context}
        <div class="kontakt_card_text_section">
            <h2>{content["Titel"]}: {name}</h2>
            <p>{content["Beskrivning"]}</p>
        </div>
    </div>
    <!--
    <a class="article clickable_element highlight" href="mailto:{content["Epost"]}"><p><b>Skicka epost till {name}</b></p></a>
    -->
</div>
"""

combined_output = {}

# List of staff as html button elements which lead to their email
combined_output["[+staff_email_buttons+]"] = generated_sections
# List of staff as links to their kontaktinfo page
combined_output["[+staff_list+]"] = staff_list