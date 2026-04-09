import requests
import json
import time
import os
from datetime import datetime

# -------------------------------
# API URLs
# -------------------------------
TOP_STORIES_URL = "https://hacker-news.firebaseio.com/v0/topstories.json"
ITEM_URL = "https://hacker-news.firebaseio.com/v0/item/{}.json"

# Header (important as per question)
headers = {"User-Agent": "TrendPulse/1.0"}

# -------------------------------
# Category keywords
# -------------------------------
categories = {
    "technology": ["ai", "software", "tech", "code", "computer", "data", "cloud", "api", "gpu", "llm"],
    "worldnews": ["war", "government", "country", "president", "election", "climate", "attack", "global"],
    "sports": ["nfl", "nba", "fifa", "sport", "game", "team", "player", "league", "championship"],
    "science": ["research", "study", "space", "physics", "biology", "discovery", "nasa", "genome"],
    "entertainment": ["movie", "film", "music", "netflix", "game", "book", "show", "award", "streaming"]
}

# -------------------------------
# Function to assign category
# -------------------------------
def get_category(title):
    title = title.lower()
    for category, keywords in categories.items():
        for word in keywords:
            if word in title:
                return category
    return None  # ignore if no match

# -------------------------------
# Step 1: Fetch top story IDs
# -------------------------------
try:
    response = requests.get(TOP_STORIES_URL, headers=headers)
    story_ids = response.json()[:500]  # first 500 IDs
except Exception as e:
    print("Error fetching top stories:", e)
    story_ids = []

# -------------------------------
# Step 2: Fetch story details
# -------------------------------
collected_data = []
category_count = {cat: 0 for cat in categories}

for story_id in story_ids:
    try:
        res = requests.get(ITEM_URL.format(story_id), headers=headers)
        story = res.json()

        if not story or "title" not in story:
            continue

        # Assign category
        category = get_category(story["title"])
        if category is None:
            continue

        # Limit 25 per category
        if category_count[category] >= 25:
            continue

        # Extract required fields
        data = {
            "post_id": story.get("id"),
            "title": story.get("title"),
            "category": category,
            "score": story.get("score", 0),
            "num_comments": story.get("descendants", 0),
            "author": story.get("by"),
            "collected_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        collected_data.append(data)
        category_count[category] += 1

        # Stop if all categories reached 25
        if all(count >= 25 for count in category_count.values()):
            break

    except Exception as e:
        print(f"Error fetching story {story_id}: {e}")
        continue

# -------------------------------
# Step 3: Save to JSON file
# -------------------------------
# Create folder if not exists
if not os.path.exists("data"):
    os.makedirs("data")

# File name with date
filename = f"data/trends_{datetime.now().strftime('%Y%m%d')}.json"

with open(filename, "w", encoding="utf-8") as f:
    json.dump(collected_data, f, indent=4)

# -------------------------------
# Output message
# -------------------------------
print(f"Collected {len(collected_data)} stories. Saved to {filename}")
