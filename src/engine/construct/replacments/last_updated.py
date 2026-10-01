import datetime

output = {}

# Last uppdated aka the currant date at which you run this
date_today = datetime.datetime.now()
output[f"[+last_updated+]"] = f"{date_today.strftime(r"%d")}-{date_today.strftime(r"%m")}-{date_today.strftime(r"%Y")} {date_today.strftime(r"%H")}:{date_today.strftime(r"%M")}"
