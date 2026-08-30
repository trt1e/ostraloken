r"""
Att fixa senare:
- Alla artiklar innan utgava 11-5 ska dubbelkollas om artikeln är samma i pdf som text


<!--
    <dialog class="popup">
        <img class="loken_image" alt="Östra Löken logo" src="./images/logo/östra_löken_i_östra_format_rak_vit_text.webp">
        <h2>Hjälp Löken tjäna övervinster</h2>
        <p>
Just nu går jättemånga företag med rekordvinst, men inte vi – tills nu!
Hjälp oss betala av våra enorma SMS-lån genom att prenumerera på Östra Löken Premium++ Basic.
Vi tar gladerligen emot alla stora mängder av pengar, vare sig det är jättestora mängder pengar eller bara ganska stora mängder pengar.
Allt stöd kommer varmhjärtat ignoreras av oss på Löken ❤️.
<br><br>Östra Löken Premium++ Basic kostar just nu <b>bara 43 990 kr per månad</b>!
</p>
        <button class="popup_button clickable_element" id="popup_buy_button"><p><b>Prenumerera idag!</b></p></button>
        <button class="popup_button clickable_element" id="popup_deny_button"><p><b>Nej, jag är fattig och töntig.</b></p></button>
    </dialog>
-->
"""
print("BOOTING OSTRALOKEN!")

import re
from pathlib import Path
import subprocess # To run "$ restart" in the terminal
import threading # for discord bot to run separetly

# import scripts
from engine import config
from engine.handle_content import content_fixer
from engine.handle_content import template_generator
from engine.build import gen_replacment_dict
from engine.build import build_articles
from engine.build import build_sitemap
from engine.build import build_imgs
from engine.build import build_pdfs
from engine.discord_bot import bot

"""
class command:
    def __init__(
        self,
        base: str, 
        base_short: str | None,
        keys: dict[str, list[str]] | None, 
        keys_short: dict[str, list[str]] | None, 
        desc: str | None,
        catagory: str = "Base"
    ):
        self.base = base
        self.base_short = base_short
        self.keys = keys
        self.keys_short = keys_short
        self.desc = desc
        self.catagory = catagory
        
    def check_match(self, command: str) -> bool:
        command = command.strip().lower()
        if self.base_short:
            match_bool = command == self.base or command == self.base_short
        else:
            match_bool = command == self.base
        return match_bool
    
    def print_help(self) -> str:
        if self.keys:
            keys_section = ""
            for key in self.keys:
                print(key)
                keys_section += f""
            
            print_string = f"    $ {self.base} ({self.base_short}) ... --> {self.desc}"
            
        else:
            print_string = f"    $ {self.base} ({self.base_short}) --> {self.desc}"
        return print_string

command("help", "h", None, None, "Lists all commands")
command("close", "c", None, None, "Terminate program")
command("restart", "r", None, None, "Restart program")
command("new utgava template", "new ut", None, None, "Generates a new utgava template with articles, notiser and hear me outs", "Templates")
command("gen all", "g", None, None, "Generate all webbpage files", "Generate text files")
command("copy images", "ci", 
    {
        "gen_type": ["all", "new", "specific"], 
        "output_type": ["article_images", "social_media_images", "article_qr_codes"]
    }, {
        "gen_type": ["a", "n", "s"], 
        "output_type": ["ai", "smi", "qrc"]
    }, "Copy over images", "Copy images"
).print_help()
command("copy pdfs", "cp", 
    {"gen_type": ["all", "new", "specific"]}, 
    {"gen_type": ["a", "n", "s"]}, 
    "Copy over PDF:s", "copy PDF:s"
)
command("inspect", "i", 
    {"gen_type": ["all", "new", "specific"]}, 
    {"gen_type": ["a", "n", "s"]}, 
    "Looks through content so everything is as it should be, if not: it's reported", "Fix content"
)
command("fix", None, 
    {"gen_selection": ["citationmarks", "article names"]}, 
    {"gen_selection": ["c", "an"]}, 
    "Fix up content so that it is as it should be", "Fix content"
)
command("bot", None, 
    {"gen_selection": ["start", "reminder", "send"]}, 
    None, "Handle the discord bot", "Bot"
)
"""

# UI for backend user
def run():
    print("Welcome to the backend terminal!")
    print('(Print "help" for commands)')
    while True:
        answer = input("$ ").strip().lower()
        try:
            if answer == "help" or answer == "h":
                print("""
    $ help (h) --> Lists all commands
    $ close (c) --> Terminate script
    $ restart (r) --> Terminate, then restart script
    
    TEMPLATES
    $ new utgava template (new ut) --> Generates a new utgava template with articles, notiser and hear me outs
    
    GENERATE TEXT FILES
    $ gen all (g) --> Generate all webbpage files

    COPY IMAGES
    $ copy images (ci) ...
    ... = new (n) --> Copy over only the new images
    ... = all (a) --> Copy over all images, even if they alredy exists
    ... = specific (s) --> Copy over all images in a specific utgava
    
    COPY PDF:S
    $ copy pdfs (cp) ...
    ... = new (n) --> Copy over only the new pdf:s
    ... = all (a) --> Copy over all pdf:s, even if they alredy exists
    ... = specific (s) --> Copy over a specific utgavas pdf 
    
    FIX CONTENT
    $ inspect (i) --> Looks through content so everything is as it should be, if not: it's reported   
    $ fix ...
    ... = citationmarks (c) --> Replace all “ and ” with ", as they should be
    ... = article names (an) --> Rename normal storys to their title (keeping them in the same order)

    DISCORD BOT
    $ bot ...
    ... = start --> Start the discord bot
    ... = reminder --> Send a reminder that they should write this week
    ... = send --> Send any message you want via the bot
""")
            elif answer == "close" or answer == "c":
                break
            elif answer == "restart" or answer == "r":
                print("Restarting...")
                subprocess.run(f'python -u "{config.engine_path / Path("main.py")}"')
                break
                
            # new content
            elif answer == "new utgava template" or answer == "new ut":
                amount_of_articles = input("Amount articles: ")
                if amount_of_articles is None or amount_of_articles == "" or not re.search(r"[0-9]", amount_of_articles):
                    amount_of_articles = 0
                amount_of_notiser = input("Amount notiser: ")
                if amount_of_notiser is None or amount_of_notiser == "" or not re.search(r"[0-9]", amount_of_notiser):
                    amount_of_notiser = 0
                amount_of_hear_me_outs = input("Amount hear me outs: ")
                if amount_of_hear_me_outs is None or amount_of_hear_me_outs == "" or not re.search(r"[0-9]", amount_of_hear_me_outs):
                    amount_of_hear_me_outs = 0
                    
                day = input("Day of release: ")
                if day is None or day == "" or not re.search(r"[0-9]", day):
                    day = "DD"
                month = input("Month of release: ")
                if month is None or month == "" or not re.search(r"[0-9]", month):
                    month = "MM"
                year = input("Year of release: ")
                if year is None or year == "" or not re.search(r"[0-9]", year):
                    year = "ÅÅÅÅ"
                    
                template_generator.setup_new_utgava_folder(day, month, year)
                template_generator.setup_new_utgava_articles(amount_of_articles)
                template_generator.setup_new_notiser(amount_of_notiser, day, month, year)
                template_generator.setup_new_hear_me_outs(amount_of_hear_me_outs)
            
            # generate text files
            elif answer == "gen all" or answer == "g":
                gen_replacment_dict.replacment_for_all = gen_replacment_dict.create_dictionary()
                gen_replacment_dict.generate_all_normal_pages()
                build_articles.generate_all_articles()
                build_sitemap.generate_all_sitemaps()
                
            # images
            elif "copy images" in answer or "ci" in answer:
                gen_type = ""
                if answer == "copy images new" or answer == "ci new" or answer == "ci n":
                    build_imgs.copy_over_images(["article_images", "social_media_images", "article_qr_codes"], "new")
                elif answer == "copy images all" or answer == "ci all" or answer == "ci a":
                    build_imgs.copy_over_images(["article_images", "social_media_images", "article_qr_codes"], "all")
                elif answer == "copy images specific" or answer == "ci specific" or answer == "ci s":
                    utgava_to_copy = input("Copy over images in utgava: ")
                    if re.search(r"[0-9]", utgava_to_copy):
                        build_imgs.copy_over_images(["article_images", "social_media_images", "article_qr_codes"], f"specific: {utgava_to_copy}")
                    else:
                        print(f"{utgava_to_copy} not a number")
                    
            # pdfs
            elif answer == "copy pdfs new" or answer == "cp new" or answer == "cp n":
                build_pdfs.copy_over_pdfs("new")
            elif answer == "copy pdfs all" or answer == "cp all" or answer == "cp a":
                build_pdfs.copy_over_pdfs("all")
            elif answer == "copy pdfs specific" or answer == "cp specific" or answer == "cp s":
                utgava_to_copy = input("Copy over pdf utgava: ")
                if re.search(r"[0-9]", utgava_to_copy):
                    build_pdfs.copy_over_pdfs(f"specific: {utgava_to_copy}")
                else:
                    print(f"{utgava_to_copy} not a number")
                    
            # fix content
            elif answer == "inspect" or answer == "i":
                content_fixer.inspect_all()
            elif answer == "fix citationmarks" or answer == "fix c":
                content_fixer.fix_citationmarks()
            elif answer == "fix article names" or answer == "fix an":
                content_fixer.fix_all_backend_articles_names()
            
            # discord bot
            elif answer == "bot start":
                print("[Discord] Starting bot...")
                bot_thread = threading.Thread(target=bot.run_discord_bot, daemon=True)
                bot_thread.start()
                bot.bot_ready_event.wait()
            elif answer == "bot reminder":
                days_left = input('Time left (ex. "2 dagar" or "36h"): ')
                if days_left != "":
                    bot_message = f"""# Bara {days_left} kvar!!!
Om du inte har skrivit din/dina artiklar än bör du kanske göra det snart!
<@&{config.discord_role_taged_in_reminders}>, skriv skriv skriv!!!
Om du inte kan skriva denna utgava, vänligen meddela det.

[Dokumentet hittar du här](https://drive.google.com/drive/folders/1AoPutNvMHKQpdiVQZescx4kgKbubEwPF)

Det bör påminnas också att det är __väldigt jobbigt__ för mig (Vilhelm) att behöva sitta sent på en söndagskväll och sätta ihop layout för att någon väntade till sista sekunden för att skriva.

Tack på förhand :heart: :heart: """
                    bot.send_discord_message(bot_message)
            elif answer == "bot send":
                bot_input = input("Message: ")
                if bot_input != "":
                    bot.send_discord_message(bot_input)
                
            else:
                if answer != "":
                    print(f'"{answer}" is not a command')
        except Exception as e:
            print(f"ERROR: {e}")

if __name__ == "__main__":
    run()