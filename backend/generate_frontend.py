import os

base_path = os.getcwd()
normal_story_path = base_path + r"\ostraloken\backend\content\normal_storys_and_other"

def read_normal_storys(): # To get the files and their content from all normal articals 
    upplaga_list = os.listdir(normal_story_path) # list all folders in dir
    upplaga_number = 0
    article_output_sum = []
    output_sum = []
    for upplaga in upplaga_list: # go thrpguth every folder to get all the upplagor
        file_list = os.listdir(normal_story_path + "\\" + upplaga) # list all files in dir  
        number_of_articles = 0
        article_output_sum = []
        upplaga_number = upplaga.split("_")[1]
        for file in file_list: # Go througth every file in the list and extract the content
            number_of_articles += 1
            content = open(normal_story_path + "\\" + upplaga + "\\" + file, "tr", encoding="utf-8") # extract
            whole_text = content.read() # read it
            
            # find the positions of difrent key parts
            title_pos1 = whole_text.find("### ") + 4
            title_pos2 = whole_text.find(" ##")
            type_pos1 = whole_text.find("¤¤¤ ") + 4
            type_pos2 = whole_text.find(" ¤¤")
            writer_pos1 = whole_text.find("@@@ ") + 4
            writer_pos2 = whole_text.find(" @@")
            
            # Sum up into the title, type, writer and article
            title = whole_text[title_pos1:title_pos2]
            type = whole_text[type_pos1:type_pos2]
            writer = whole_text[writer_pos1:writer_pos2]
            article = whole_text[(writer_pos2 + 4):]
            
            """
            print("Title:", title)
            print("Type:", type)
            print("Writer:", writer)
            print("Article:", article)
            """
            
            content.close() # at the end
            
            article_output = ({"Title": title, "Type": type, "Writer": writer, "Article": article})
            article_output_sum.append(article_output)
        output = ({"Upplaga": upplaga_number, "Content": article_output_sum})
        output_sum.append(output)
        
def put_into_html(title, article):
    new_file = """
    <!DOCTYPE html>
    <html lang="sv">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Östra Löken Hemsidan</title>
        <link rel="stylesheet" href="../universal.css">
        <link rel="stylesheet" href="./article_universal.css">
    </head>
    <body>
        <header>
            <p id="header_date"><b>Söndag 29 mars</b></p>
            <img id="header_titel_image" alt="Östra Löken logo" src="../images/logo/östra löken i östra format rak vit text.png">
            <p><b>Hotfult nära verkligheten</b></p>
        </header>
        <div id="dropdown">•••
            <div id="dropdown_button_container">
                <a href="" class="dropdown_button">Hem</a>
                <a href="" class="dropdown_button">Artiklar</a>
                <a href="" class="dropdown_button">PDF:er</a>
                <a href="" class="dropdown_button">Notiser</a>
                <a href="" class="dropdown_button">Hear me out:s</a>
                <a href="" class="dropdown_button">Om oss</a>
                <a href="" class="dropdown_button">Kontaktinfo</a>
            </div>
        </div>
        <main>
            <div class="article">
                <img src="../images/Test.png">
                <h2>{title}</h2>
                <p>{article}</p>
            </div>
        </main>
        <footer id="footer">
            <div class="footer_text">
                <p>Östra Lökens Policy:</p>
                <p>
                    <br>Alla elevers namn är påhittade. <br>
                    Östra Löken siktar på att slå <br>
                    uppåt med satiren, inte neråt. <br>
                    Alla artiklar är skrivna av människor. <br>
                    Tidningen är satir. <br>
                </p>
            </div>
            <div class="footer_text" style="text-align: center;">
                <p>Östra Löken produceras av:</p>
                <p>
                <br>Vilhelm Grill <br>
                Joar Stange <br>
                John Ericson <br>
                Magne Nordström <br>
                Elliot Sandström <br>
                </p> 
            </div>
            <div class="footer_text" style="text-align: right;">
                <p>Nå oss på:</p>
                <p>
                    <br>Instagram: ostra_loken <br>
                    Email: ostraloken@gmail.com <br>
                    Linktree: linktr.ee/ostraloken <br>
                </p>
            </div>
        </footer>

        <script src="./index/js/receive_articles.js"></script>
    </body>
    </html>
    """