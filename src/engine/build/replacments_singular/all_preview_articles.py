from engine.build import build_articles

# All normal articles preview that you can click and it brings you to that article page
list_of_generated_articles = build_articles.generate_preview_article("./a/", "All")
all_generated_articles = ""
for generated_articles in list_of_generated_articles:
    all_generated_articles += str(generated_articles)

output = all_generated_articles