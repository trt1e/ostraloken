# Östra Löken - webbplatsgenerator

Det här projektet genererar webbsidorna för Östra Löken, Östra Gymnasiets skolsatirtidning. Koden läser in text, artiklar, bilder och PDF:er från `content/` och bygger statiska sidor i `generated/webb/`.

Projektet är byggt som ett litet editor-verktyg i terminalen: en redaktion kan skapa nya utgåvor, kopiera in mediafiler, kontrollera innehåll och generera hela webbplatsen.

## Krav

- Python 3.14 eller senare
- `pip` för installation

## Installation

```bash
git clone https://github.com/trt1e/ostraloken.git
cd ostraloken
python -m pip install -e .
```

Det installerar projektet och registrerar CLI-kommandot `runlok`.

## Starta programmet

```bash
runlok
```

Alternativt kan du köra den inbyggda huvudfilen direkt:

```bash
python -m engine
```

Det startar en interaktiv terminal där du kan skriva kommandon som:

- `help`
- `gen all`
- `new template`
- `copy images ...`
- `copy pdfs ...`
- `inspect`
- `fix ...`
- `close`

## Vanliga kommandon

### `help`
Visar tillgängliga kommandon och deras användning.

### `new template`
Skapar en ny utgåva-mall. Programmet frågar efter antal artiklar, notiser, hear me out:s och röda flaggor samt datum och genererar därefter mappstruktur för den nya utgåvan.

### `gen all`
Genererar webbplatsens textinnehåll. Detta byggar om sidornas innehåll utifrån källfiler i `content/`.

### `copy images`
Kopierar bilder från `content/` till de mappar som används i den genererade webbplatsen.

Exempel:

```bash
$ copy images all social media images
$ copy images new article images
$ copy images specific article qr codes
```

### `copy pdfs`
Kopierar PDF:er för utgåvorna till den genererade webbplatsen.

Exempel:

```bash
$ copy pdfs all
$ copy pdfs new
$ copy pdfs specific
```

### `inspect`
Går igenom innehållet för att hitta vanliga fel och problem i publiceringsfilerna.

### `fix`
Fixar de vanligaste formaterings- eller namnrelaterade problemen. Exempelvis med citationstecken eller artikelnamn.

## Projektstruktur

```text
.
├── content/
│   ├── articles/
│   ├── extra/
│   ├── static/
│   ├── utgavor_pdfs/
│   └── ...
├── generated/
│   ├── social_media_imgs/
│   └── webb/
├── src/
│   └── engine/
│       ├── construct/
│       ├── handle_content/
│       ├── config.py
│       ├── utils.py
│       └── main.py
├── pyproject.toml
├── README.md
└── ...
```

### `content/`
Här lagras redaktionens källmaterial: artiklar, notiser, hear me out:s, röda flaggor, statiskt innehåll, bilder och PDF:er.

### `generated/`
Här skapas den producerade webbplatserna och de exporterade mediafilerna.

### `src/engine/`
Här finns själva generatorn:

- `construct/`: byggare för sidor, navigering, artiklar och sitemap
- `handle_content/`: läsning, validering, generering och lagning av innehåll
- `config.py`: sökvägar och projektkonstanter
- `utils.py`: användbara funktioner för hela projektet
- `main.py`: interaktiv terminal och kommandon

## Arbetsflöde

1. Skapa ny utgåva med `$ utgava template`
2. Fyll i artiklar och övrigt innehåll i `content/`
3. Laga namnen med `$ fix article names`, rätta citationstecken med `$ fix citationmarks` och se till så att allting är rätt med `$ inspect`
4. Kopiera över bilder och PDF:er om det behövs
5. Kör `$ gen all` för att bygga webbsidan
6. Publisera de genererade webbsidorna till internet med `git add .`, `git commit -m "..."` och `git push`

## Notering

Projektet skriver och uppdaterar genererade filer, men det tar inte bort gamla filer automatiskt. Det kan därför förekomma äldre artefakter om namn på filer eller mappar ändrats.

## Licens och ansvar

Det här projektet används för att driva Östra Lökens webbsida och publiceringsflöde. Koden och filerna är ämnade för den interna produktionen kring tidningen.
