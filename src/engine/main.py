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
from engine.handle_content import content_reader
from engine.build import gen_replacment_dict
from engine.build import build_articles
from engine.build import build_sitemap
from engine.build import build_imgs
from engine.build import build_pdfs
from engine.discord_bot import bot


class command:
    def __init__(
        self,
        base: str, 
        base_short: str | None,
        keys: dict[str, list[str]] | None, 
        keys_short: dict[str, list[str | None]] | None, 
        desc: str,
        catagory: str = "Base"
    ):
        self.base = base
        self.base_short = base_short
        self.keys = keys
        self.keys_short = keys_short
        self.desc = desc
        self.catagory = catagory 

    def check_match_base(self, command: str) -> bool:
        command_parts = command.strip().lower().split(" ")
        base_parts = self.base.split(" ")
        
        match_bool = False
        for element in command_parts:
            if self.base_short:
                base_short_parts = self.base_short.split(" ")
                if (element in base_parts) or (element in base_short_parts):
                    match_bool = True
                    break
            else:
                if element in base_parts:
                    match_bool = True
                    break
        
        return match_bool
    
    def check_match_keys(self, command: str) -> list:
        matched_keys = []
        if self.keys:
            command_parts = command.strip().lower().split(" ")
            keys_parts = []
            short_keys_parts = []

            for i, value_list in enumerate(self.keys.values()):
                for j, value in enumerate(value_list):
                    keys_parts.append(str(value))
                    
                    if self.keys_short and list(self.keys_short.values())[i][j]:
                        short_keys_parts.append(str(list(self.keys_short.values())[i][j]))
            

            for element in command_parts:
                if element in keys_parts:
                    matched_keys.append(element)
                elif element in short_keys_parts:
                    matched_keys.append(keys_parts[short_keys_parts.index(element)])
        
        return matched_keys
    
    def print_help(self) -> str:
        if self.keys:
            if len(self.keys) > 25:
                print("WARNING: Cant have a command with more than 25 keys!")
            alphabet = "AA BB CC DD EE FF GG HH II JJ KK LL MM NN PP QQ RR SS TT UU VV WW XX YY ZZ"[:len(self.keys) * 3 - 1]
            if self.base_short:
                print_string = f"    $ {self.base} ({self.base_short}) {alphabet} --> {self.desc}"
            else:
                print_string = f"    $ {self.base} {alphabet} --> {self.desc}"
            
            for i, value_list in enumerate(self.keys.values()):
                currant_key = str(list(self.keys.keys())[i])
                print_string += f"\n        - {currant_key}:"
                for j, value in enumerate(value_list):
                    if self.keys_short and list(self.keys_short.values())[i][j]:
                        short_key = list(self.keys_short.values())[i][j]
                        print_string += f"\n            {str(alphabet[i * 3 + 1]) + str(alphabet[i * 3])} = {value} ({short_key})"
                    else:
                        print_string += f"\n            {str(alphabet[i * 3 + 1]) + str(alphabet[i * 3])} = {value}"
            
        else:
            if self.base_short:
                print_string = f"    $ {self.base} ({self.base_short}) --> {self.desc}"
            else:
                print_string = f"    $ {self.base} --> {self.desc}"
        
        print(print_string)
        return print_string


all_commands = {
    "help": command("help", "h", None, None, "Lists all commands"),
    "close": command("close", "c", None, None, "Terminate program"),
    "restart": command("restart", "r", None, None, "Restart program"),
    "utgava template": command("utgava template", "ut", None, None, "Generates a new utgava template with articles, notiser and hear me outs", "Templates"),
    "gen all": command("gen all", "g", None, None, "Generate all webbpage files", "Generate text files"),
    "copy images": command("copy images", "ci", 
        {
            "gen_type": ["all", "new", "specific"], 
            "output_type": ["article images", "social media images", "article qr codes"]
        }, {
            "gen_type": ["a", "n", "s"], 
            "output_type": ["ai", "smi", "qr"]
        }, "Copy over images", "Copy images"
    ),
    "copy pdfs": command("copy pdfs", "cp", 
        {"gen_type": ["all", "new", "specific"]}, 
        {"gen_type": ["a", "n", "s"]}, 
        "Copy over PDF:s", "copy PDF:s"
    ), "inspect": command("inspect", "i", None, None, "Looks through content so everything is as it should be, if not: it's reported", "Fix content"),
    "fix": command("fix", None, 
        {"gen_selection": ["citationmarks", "article names"]}, 
        {"gen_selection": ["c", "an"]}, 
        "Fix up content so that it is as it should be", "Fix content"
    ),
    "bot": command("bot", None, 
        {"gen_selection": ["start", "reminder", "send"]}, 
        None, "Handle the discord bot", "Bot"
    )
}

# UI for backend user
def run():
    print("Welcome to the backend terminal!")
    print('(Print "help" for commands)')
    while True:
        answer = input("$ ").strip().lower()
        try:
            if all_commands["help"].check_match_base(answer):
                currant_catagory = ""
                print("--------------------------------------------------------")
                for currant_command in list(all_commands.values()):
                    if currant_command.catagory != "Base" and currant_catagory != currant_command.catagory:
                        print(f"\n    {currant_command.catagory.upper()}")
                    currant_command.print_help()
                    currant_catagory = currant_command.catagory
                print("--------------------------------------------------------")
            
            elif all_commands["close"].check_match_base(answer):
                break

            elif all_commands["restart"].check_match_base(answer):
                print("Restarting...")
                subprocess.run(f'python -u "{config.engine_path / Path("main.py")}"')
                break
                
            # new content
            elif all_commands["utgava template"].check_match_base(answer):
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
                    
                next_utgava_number = len(content_reader.read_articles()) + 1
    
                template_generator.setup_new_utgava_folder(next_utgava_number, day, month, year)
                template_generator.setup_new_utgava_articles(next_utgava_number, amount_of_articles)
                template_generator.setup_new_notiser(next_utgava_number, amount_of_notiser, day, month, year)
                template_generator.setup_new_hear_me_outs(next_utgava_number, amount_of_hear_me_outs)
            
            # generate text files
            elif all_commands["gen all"].check_match_base(answer):
                gen_replacment_dict.replacment_for_all = gen_replacment_dict.create_dictionary()
                gen_replacment_dict.generate_all_normal_pages()
                build_articles.generate_all_articles()
                build_sitemap.generate_all_sitemaps()
                
            # images
            elif all_commands["copy images"].check_match_base(answer):
                matching_keys = all_commands["copy images"].check_match_keys(answer)
                
                gen_type = []
                output_type = []
                
                if "new" in matching_keys:
                    gen_type.append("new")
                if "all" in matching_keys:
                    gen_type.append("all")
                if "specific" in matching_keys:
                    utgava_to_copy = input("Copy over images in utgava: ")
                    if re.search(r"[0-9]", utgava_to_copy):
                        gen_type.append(f"specific: {utgava_to_copy}")
                    else:
                        print(f"{utgava_to_copy} not a number")
                
                if "article images" in matching_keys:
                    output_type.append("article_images")
                if "social media images" in matching_keys:
                    output_type.append("social_media_images")
                if "article qr codes" in matching_keys:
                    output_type.append("article_qr_codes")
                
                if matching_keys == [] or output_type == []:
                    print('WARNING: All inputs are not given. Nothing will be generated. For more info: do "$ help"')
                
                build_imgs.copy_over_images(output_type, gen_type)
            # pdfs
            elif all_commands["copy pdfs"].check_match_base(answer):
                matching_keys = all_commands["copy pdfs"].check_match_keys(answer)
                
                gen_type = []

                if "new" in matching_keys:
                    gen_type.append("new")
                if "all" in matching_keys:
                    gen_type.append("all")
                if "specific" in matching_keys:
                    utgava_to_copy = input("Copy over images in utgava: ")
                    if re.search(r"[0-9]", utgava_to_copy):
                        gen_type.append(f"specific: {utgava_to_copy}")
                    else:
                        print(f"{utgava_to_copy} not a number")
                
                if matching_keys == []:
                    print('WARNING: All inputs are not given. Nothing will be generated. For more info: do "$ help"')
                
                build_pdfs.copy_over_pdfs(gen_type)
                    
            # fix content
            elif all_commands["inspect"].check_match_base(answer):
                content_fixer.inspect_all()
            elif all_commands["fix"].check_match_base(answer):
                matching_keys = all_commands["fix"].check_match_keys(answer)

                has_generated = False

                if "citationmarks" in matching_keys:
                    content_fixer.fix_citationmarks()
                    has_generated = True
                if "article names" in matching_keys:
                    content_fixer.fix_all_backend_articles_names()
                    has_generated = True
                    
                if not has_generated:
                    print('WARNING: All inputs are not given. Nothing will be generated. For more info: do "$ help"')
            
            # discord bot
            elif all_commands["bot"].check_match_base(answer):
                # Start
                print("[Discord] Starting bot...")
                bot_thread = threading.Thread(target=bot.run_discord_bot, daemon=True)
                bot_thread.start()
                bot.bot_ready_event.wait()
                
                # Reminder
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
                
                # Send
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