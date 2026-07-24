# Hur fungerar ostraloken?
Östra Lökens webbsida är skapad för att enkelt kunna uppdateras då nytt innehåll läggs till. Den är skapad med en modulär struktur. Det här gör det enkelt att inte bara lägga till nya artiklar i backend:en utan man kan också enkelt lägga till en ny sida på ostraloken.se eller till och med en helt ny webbsida.

All kod är helt skriven av Vilhelm Grill som också jobbar på Östra Lökens redaktion. Om du vill kontakta honom kan du göra det på vilhelm.grill@ostraloken.se!

## 1. Backend:
**Det är här webbsidan genereras (med backend-terminalen i generate_frontend.py) och där alla artiklar, bilder, notiser, hear me out:s och mer finns lagrade.**

### generate_frontend.py
För att köra denna fil behöver du ha python installerat (tidigast 3.14) och ha ett antal bibloteket installerade. Om du inte har python kan du ladda ner den online. Om du inte har har bibloteken kan du göra "pip install [biblotek]" i din terminal.

Kommandon i backend-terminalen kan ses med "$ help". Där får du också instruktioner om vad alla kommandon gör. Kortfattat kan du:
    **1. Generera webbsidan** Då kopierar programet över filerna från templates och lägger in innehållet från content i dem.
    **2. Skapa mallar** Du kan, med ett kommando, göra allting redo för en ny upplaga genom att få mallar för artiklar, notiser och hear me out:s färdigstälda för dig. Det här gör det enkelt att bara kopiera och klistra in innehållet.
    **3. Kopiera över bilder & PDF:s** När du gör det kan du välja om du ska kopiera över alla, bara nya eller specefikt någon upplaga. Notera att när du ber den kopiera över nya kollar den endast om filerna finns, inte om de har ändrats.
    **4. Fixa till content** Den viktigaste funktionen här är "$ inspect" som söker genom content för att se om några vanliga misstag har gjorts i filerna. Om så är fallet bör de troligtvis åtgärdas, men inte nödvändigtvis. Du kan också här fixa artiklarnas fil-namn så de är korrekta (det är extra viktigt om du ska länka dem med bilder).

Kortfattat har generate_frontend.py alla verktyg du behöver för att sköta ostraloken.se!

P.S. generate_frontend.py skapar endast filer, den tar inte bort gammla, så det kan förekomma att filer med gammla namn - både artiklar och bilder - ligger kvar. Det här är dock endast om du har bytt namn, så inte om de har samma namn.

### content
I content finns själva arkivet. Här arkiveras alla artiklar, notiser, hear me out:s, insändare, pdf:er, statiskt innehåll och mer nästan exakt så de var när de publiserades. Om t.ex. en insändare inte publiserades borde den troligtvis inte vara med i arkivet. Alla stavfel och misstag måste lämnas kvar. Ändringar man får göra är att ändra bilden till en artikel eller annat, ändra artikeltyp och fixa till om fel citationstecken används (gör detta i backend-terminalen automatiskt). Bilder bör helst inte ändras men det kan exempelvis behövas om Östra Löken från första början inte hade rättigheterna till bilden eller om det finns ett starkt motiv att ändra den. 

Det bör också noteras att tidiga artiklar (innan upplaga nr. 28) tryckte inte skribent, men i dessa fall har man kunnat gå tillbaka och kolla vem som skrev dessa artiklar.

Artiklarna, notiserna och hear me out:s använder ett egetutväcklat system för att skilja på olika delar av texten. För artiklar används "### " och " ##" för att urskilja rubriken, "¤¤¤ " och " ¤¤" för artikeltyp, "@@@ " och " @@" för skribent och det efter " @@" som artikelns innehåll. Både notiser och hear me out:s använder "### " och " ##" för rubrik respektive hear me out och de båda använder också "+++ " och " ++" för innehåll respektive beskrivning. Det är därför viktigt att dessa symboler inte används i texten på sätten använda i formateringen.

Statiskt innehåll använder ett likande system. För statiska artiklar läggs de ut ganska unikt genom att sätta dem i en [+sådan här+] där deras rubrik är vad som sätts inuti, men där mellanrum (" ") bytts ut med understräck ("_").

## 2. Templates:
**Här lagras html-filerna som ska kopieras och där allt innehåll ska läggas in.**

Templates har relativt stora html-filer som är för stora för att helt enkelt vara inbakade i generate_frontend.py. Alla filer i webbpage generas från en templates fil där dess address bestäms innom en sådan här text i början: <!--@( URL )@--> 
URL kan exempelvis vara t.ex. \ostraloken\ostraloken.se\webbpage\index.html

I mallfilerna fylls information in baserat på vart sådana här finns: [+article+]. Dessa markerar ut var python-scripten ska plasera visst innehåll. Dessa bytts sedan ut med dess innehåll.

## 3. Webbpage:
**I denna map lagras själva webbsidan - det är denna som finns på webben!**

I webbpage finns det en blandning av innehåll som genereras automatiskt och som bara finns där. Alla HTML filer generas av generate_frontend.py och om du ändrar dessa filer i webbpage kommer ändringarna tas bort när webbsidan generaras på nytt.

"/a" står för "artiklar" och är där alla generade artikelsidor och bilder finns.

### CSS-filer
Uppmärksamma universal.css. Den här style-filen länkas alla html-filer till så om du ska lägga till någonting här bör de påverka en större andel av html-filerna.

Alla mappar har också en style.css-fil som endast används av html-filen i samma mapp.

Id- och class-namnen samt kommentarer och kod är alla skrivna på engelska för att öka tillgänglighet och för att följa universiella standader.

### Mappstruktur
Mappstrukturen på ostraloken.se är väldigt enkel. Index-filen och universal-filen är de enda som är på root-lagret. För allting annat än html-filen för index läggs det i en egen mapp (som allt annat). Det finns också en js-mapp för alla javascript-filer som används av flera av sidorna. Om endast en sida använder en js-fil läggs den som submapp till html- och css-filen. Samma gäller bilder.