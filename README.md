# Hur fungerar ostraloken.se?
Östra Lökens hemsida är skapad för att webbsidan enkelt ska kunna uppdateras då nya artiklar, notiser och hear me out:s skapas. Därmed har webbsidan tre distinkta mappar. Kortfattat kan man säga att **backend** används för att lagra allting, **templates** är för att ha en mall att lägga in backends content i och **webbpage** är där webbsidan är.

Den här webbsidan är helt skriven av mig (Vilhelm Grill) som också jobbar på Östra Lökens redaktion. Om du vill kontakta mig kan du göra det på vilhelm.grill@ostraloken.se. 

## 1. Backend:
**Det är här webbsidan genereras (med backend-terminalen i generate_frontend.py) och där alla artiklar, bilder, notiser och hear me out:s finns lagrade.**

### generate_frontend.py
För att köra denna fil behöver du (1) ha python installerat (tidigast 3.14) och (2) ha bibloteket PIL installerat. Om du inte har python kan du ladda ner den online. Om du inte har PIL kan du göra "pip install Pillow" i din terminal.

Kommandon i backend-terminalen kan ses med "$ help". Där får du också instruktioner om vad alla kommandon gör. Kortfattat kan du (1) generera webbsidan, då kopierar programet över filerna från templates och lägger in saker från content i dem. Du kan också (2) kopiera över bilder. När du gör det kan du välja om du ska kopiera över alla bilder eller bara nya, notera att när du ber den kopiera över nya kollar den endast om filerna finns, inte om de har ändrats. Den tredje viktiga saken du kan göra är att (3) fixa till content. Den viktigaste funktionen här är "$ inspect" som söker genom content för att se om några vanliga misstag har gjorts i filerna. Om så är fallet bör de troligtvis åtgärdas, men inte nödvändigtvis. Du kan också här fixa artiklarnas fil-namn så de är korrekta (det är extra viktigt om du ska länka dem med bilder). Du kan också göra mer med python-filen, men det här är det viktigaste.

Kortfattat har generate_frontend.py alla verktyg du behöver för att sköta ostraloken.se!

P.S. generate_frontend.py skapar endast filer, den tar inte bort gammla, så det kan förekomma att filer med gammla namn - både artiklar och bilder - ligger kvar.

P.P.S. Du kan också skapa mallar när du ska lägga in en ny upplaga genom att skriva "$ new upplaga template". Det gör det extremt enkelt att bara copy + paste:a in alla artiklar, notiser och hear me outs!

### content
I content finns själva arkivet. Här arkiveras alla artiklar, notiser, hear me out:s, insändare och mer nästan exakt så de var när de publiserades. Om t.ex. en insändare inte publiserades borde den troligtvis inte vara med i arkivet. Alla stavfel och misstag måste lämnas kvar. Ändringar man får göra är att ändra bilden till en artikel eller annat, ändra artikeltyp och fixa till om fel citationstecken används (gör detta i backend-terminalen automatiskt). Bilder bör helst inte ändras men det kan exempelvis behövas om Östra Löken från första början inte hade rättigheterna till bilden eller om det finns ett starkt motiv att ändra den. 

Det bör också noteras att tidiga artiklar (innan upplaga nr. 28) tryckte inte skribent, men i dessa fall har man kunnat gå tillbaka och kolla vem som skrev dessa artiklar.

Artiklarna, notiserna och hear me out:s använder ett egetutväcklat system för att skilja på olika delar av texten. För artiklar används "### " och " ##" för att urskilja rubriken, "¤¤¤ " och " ¤¤" för artikeltyp, "@@@ " och " @@" för skribent och det efter " @@" som artikelns innehåll. Både notiser och hear me out:s använder "### " och " ##" för rubrik respektive hear me out och de båda använder också "+++ " och " ++" för innehåll respektive beskrivning. Det är därför viktigt att dessa symboler inte används i texten på sätten använda i formateringen.

### Extra
Kom ihåg att PDF:er inte lagras på backenden eftersom backenden inte finns på servern (servern är endast webbpage). Mer info om hur man lägger till PDF:er finns på kapitel 3. 

## 2. Templates:
**Här lagras html-filerna som ska kopieras och där artiklar, bilder, hear me out:s och notiser ska läggas in i.**

Templates har relativt stora html-filer som är för stora för att helt enkelt vara inbakade i generate_frontend.py men som samtidigt behöver kunna kopieras och ha innehåll lagt i sig. Dessa filer är därför separerade från webbpage just för att de filerna aldrig används - de kopieras bara.

I mallfilerna fylls information in primärt baserat på vart sådana här finns: \<!-- [+article+] -->. Dessa markerar ut var python-scripten ska plasera visst innehåll, men de är inte de ända delarna av filen som generars. Den största av dem omarkerade sakerna som generas är <title>. Detta är för att man inte kan lägga kommentarer i dessa utan att de syns. Det finns också på andra ställen men då brukar platsen vara kommenterad.

## 3. Webbpage:
**I denna map lagras själva webbsidan - det är denna som finns på webben!**

I webbpage finns det en blandning av innehåll som genereras automatiskt och som bara finns där. Notera att index.html, notiser/index.html, hear_me_outs/index.html och alla .html och .webp filer i /a alla generars med generate_frontend.py och kan därmed endast ändras permanent i templates eller genom att ändra python koden (rekomenderas ej). Om du ändrar dessa filer i webbpage kommer ändringarna tas bort när webbsidan generaras på nytt.

/a står för "artiklar" och är där alla generade artiklar och bilder finns.

### CSS-filer
Uppmärksamma universal.css. Den här style-filen länkas alla html-filer till så om du ska lägga till någonting här bör de påverka en större andel av html-filerna. 

Alla mappar har också en style.css-fil som endast används av html-filen i samma mapp.

Id- och class-namnen är alla skrivna på engelska för att öka tillgänglighet och för att följa universiella standader.

### Mappstruktur
Mappstrukturen på ostraloken.se är väldigt enkel. Index-filen och universal-filen är de enda som är på root-lagret. För allting annat än html-filen för index läggs det i en egen mapp (som allt annat). Det finns också en js-mapp för alla javascript-filer som används av flera av sidorna. Om endast en sida använder en js-fil läggs den som submapp till html- och css-filen. Samma gäller bilder.

### Nav & PDF:er 
Annat än de generarde filerna bör endast nav och PDF:er mapparna behöva ändras. Eftersom dessa inte generars med generate_frontend.py så redigerar man dem som en vanlig html-fil. 

Om det ska läggas till en PDF behöver du (1) lägga in PDF:en i rätt mapp, (2) skriva dess namn rätt (Ex. för upplaga 14: Östra_Löken_upplaga_14.pdf) och (3) uppdatera variabeln "const amoutPDfs" i filen PDFjs_reader.js och sätta den till mängden artiklar nu i arkivet.
