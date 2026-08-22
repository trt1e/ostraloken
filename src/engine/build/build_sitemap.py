from pathlib import Path
import datetime

def create_sitemap_url_part(loc, changefreq, priority):
    # Get currant date
    date_today = datetime.datetime.now()
    
    return f"""
    <url>
        <loc>{loc}</loc>
        <lastmod>{date_today.strftime(r"%Y")}-{date_today.strftime(r"%m")}-{date_today.strftime(r"%d")}</lastmod>
        <changefreq>{changefreq}</changefreq>
        <priority>{priority}</priority>
    </url>
"""

def gen_sitemap(webb_path):
    webbsite_path = webb_path / Path("webbsite")
    webb_address_root = webbsite_path.parent.name
    
    paths_to_search = [Path(webbsite_path)]
    
    content = ""

    for path in paths_to_search:
        distance_from_root = 0
        for i in range(len(path.parents)):
            if path.parents[i].name == webb_address_root:
                distance_from_root = i

        if distance_from_root == 0:
            currant_location = ""
        else:
            # (This one doesnt work if distance_from_root == 0)
            currant_location = str(Path(*path.parts[min(int(0 - distance_from_root), 0):])).replace("\\", "/") + "/"
        currant_base_webb_address = "https://" + webb_address_root + "/" + currant_location
        
        for item in path.iterdir():
            if item.is_dir(): # is a folder
                paths_to_search.append(Path(path / item))
            elif item.is_file(): # is a file
                if item.suffix == ".html":
                    if item.name == "index.html":
                        currant_webb_address = currant_base_webb_address
                    else:
                        currant_webb_address = currant_base_webb_address + item.stem

                    change_frequency = "weekly"
                    if distance_from_root == 0:
                        change_frequency = "daily"
                        
                    priority = 1.0 - (0.2 * distance_from_root)
                    if item.name != "index.html":
                        priority -= 0.1
                    if priority < 0.2:
                        priority = 0.2
                    priority = round(priority, 2)
        
                    content += create_sitemap_url_part(currant_webb_address, change_frequency, priority)  

        sitemap = f"""
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    {content}
</urlset>
"""
        # Create/write to the sitemap file
        sitemap_path = webbsite_path / "sitemap.xml"
        with open(sitemap_path, "w", encoding="utf-8") as sitemap_file:
            sitemap_file.write(sitemap) # Write the file
        
    print(f"Created sitemap for {webb_address_root}")
