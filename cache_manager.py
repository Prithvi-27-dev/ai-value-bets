import json
import os
from datetime import datetime

CACHE_FILE = "daily_cache.json"

def _load_cache():
    if not os.path.exists(CACHE_FILE):
        return {"date": "", "matches": []}
    with open(CACHE_FILE, "r") as f:
        return json.load(f)

def _save_cache(cache):
    with open(CACHE_FILE, "w") as f:
        json.dump(cache, f, indent=2)

def get_today_cache():
    today = datetime.now().strftime("%Y-%m-%d")
    cache = _load_cache()
    if cache["date"] != today:
        cache = {"date": today, "matches": []}
        _save_cache(cache)
    return set(tuple(match.items()) for match in cache["matches"])

def add_to_cache(matches):
    today = datetime.now().strftime("%Y-%m-%d")
    cache = _load_cache()
    if cache["date"] != today:
        cache = {"date": today, "matches": []}
    for match in matches:
        if match not in cache["matches"]:
            cache["matches"].append(match)
    _save_cache(cache)

def is_match_cached(match):
    today_cache = get_today_cache()
    return tuple(match.items()) in today_cache