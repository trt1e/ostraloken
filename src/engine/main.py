r"""
Att fixa senare:
- Alla artiklar innan upplaga 11-5 ska dubbelkollas om artikeln är samma i pdf som text
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
from engine.build import build_imgs
from engine.build import build_pdfs
from engine.discord_bot import bot

# UI for backend user
def run():
    print("Welcome to the backend terminal!")
    print('(Print "help" for commands)')
    while True:
        answer = input("$ ")
        try:
            if answer == "help" or answer == "h":
                print("""
    $ help (h) --> Lists all commands
    $ close (c) --> Terminate script
    $ restart (r) --> Terminate, then restart script
    
    TEMPLATES
    $ new upplaga template (new ut) --> Generates a new upplaga template with articles, notiser and hear me outs
    
    GENERATE TEXT FILES
    $ gen all (g) --> Generate all webbpage files that are generated

    COPY IMAGES
    $ copy images (ci) ...
    ... = new (n) --> Copy over only the new images
    ... = all (a) --> Copy over all images, even if they alredy exists
    ... = specific (s) --> Copy over all images in a specific upplaga
    
    COPY PDF:S
    $ copy pdfs (cp) ...
    ... = new (n) --> Copy over only the new pdf:s
    ... = all (a) --> Copy over all pdf:s, even if they alredy exists
    ... = specific (s) --> Copy over a specific upplagas pdf 
    
    FIX CONTENT
    $ inspect --> Looks through content so everything is as it should be, if not: it is reported   
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
            elif answer == "new upplaga template" or answer == "new ut":
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
                    
                template_generator.setup_new_upplaga_folder(day, month, year)
                template_generator.setup_new_upplaga_articles(amount_of_articles)
                template_generator.setup_new_notiser(amount_of_notiser, day, month, year)
                template_generator.setup_new_hear_me_outs(amount_of_hear_me_outs)
            
            # generate text files
            elif answer == "gen all" or answer == "g":
                gen_replacment_dict.replacment_for_all = gen_replacment_dict.create_dictionary()
                gen_replacment_dict.generate_all_normal_pages()
                build_articles.generate_all_articles()
                
            # images
            elif answer == "copy images new" or answer == "ci new" or answer == "ci n":
                build_imgs.copy_over_images("new")
            elif answer == "copy images all" or answer == "ci all" or answer == "ci a":
                build_imgs.copy_over_images("all")
            elif answer == "copy images specific" or answer == "ci specific" or answer == "ci s":
                upplaga_to_copy = input("Copy over images in upplaga: ")
                if re.search(r"[0-9]", upplaga_to_copy):
                    build_imgs.copy_over_images(f"specific: {upplaga_to_copy}")
                else:
                    print(f"{upplaga_to_copy} not a number")
                    
            # pdfs
            elif answer == "copy pdfs new" or answer == "cp new" or answer == "cp n":
                build_pdfs.copy_over_pdfs("new")
            elif answer == "copy pdfs all" or answer == "cp all" or answer == "cp a":
                build_pdfs.copy_over_pdfs("all")
            elif answer == "copy pdfs specific" or answer == "cp specific" or answer == "cp s":
                upplaga_to_copy = input("Copy over pdf upplaga: ")
                if re.search(r"[0-9]", upplaga_to_copy):
                    build_pdfs.copy_over_pdfs(f"specific: {upplaga_to_copy}")
                else:
                    print(f"{upplaga_to_copy} not a number")
                    
            # fix content
            elif answer == "inspect":
                content_fixer.inspect_normal_storys()
                content_fixer.inspect_short_storys()
                content_fixer.inspect_hear_me_outs()
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
Om du inte kan skriva denna upplaga, vänligen meddela det.

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