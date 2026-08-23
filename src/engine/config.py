"""
Här läser vi in .env, konstanter och instälningar!!
"""
import os
from dotenv import load_dotenv # For reading secrets
from pathlib import Path

engine_path = Path(__file__).resolve().parent
base_path = Path(engine_path).parents[1]

img_extentions = ["jpg", "JPG", "jpeg", "JPEG", "png", "PNG", "webp", "WEBP"]

articles_path = base_path / Path("content/articles")
notiser_path = base_path / Path("content/notiser.txt")
hear_me_outs_path = base_path / Path("content/hear_me_outs.txt")

load_dotenv() # load .env
# access .env
discord_bot_token = os.getenv("discord_bot_token")
discord_channel_id = os.getenv("discord_channel_id")
discord_role_taged_in_reminders = os.getenv("discord_role_taged_in_reminders")