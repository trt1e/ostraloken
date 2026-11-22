"""
Här läser vi in .env, konstanter och instälningar!!
"""
import os
from dotenv import load_dotenv # For reading secrets
from pathlib import Path

engine_path = Path(__file__).resolve().parent
base_path = Path(engine_path).parents[1]

img_extentions = [".jpg", ".JPG", ".jpeg", ".JPEG", ".png", ".PNG", ".webp", ".WEBP"]

webb_paths = [
    Path("nyhetsflode.ostraloken.se"),
    Path("bilder.ostraloken.se"),
    Path("ostraloken.se"),
]

articles_path = base_path / Path("content/articles")
