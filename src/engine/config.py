"""
Här läser vi in .env, konstanter och instälningar!!
"""
import os
from dotenv import load_dotenv # For reading secrets
from pathlib import Path

engine_path = Path(__file__).resolve().parent
base_path = Path(engine_path).parents[1]

img_extentions = [".jpg", ".JPG", ".jpeg", ".JPEG", ".png", ".PNG", ".webp", ".WEBP"]

base_webb_paths = [
    base_path / Path("generated/webb/nyhetsflode.ostraloken.se"),
    base_path / Path("generated/webb/bilder.ostraloken.se"),
    base_path / Path("generated/webb/ostraloken.se")
]

articles_path = base_path / Path("content/articles")
