import json
import os
import pandas as pd

# -------------------------------
# Step 1: Load JSON file
# -------------------------------

# Automatically find latest JSON file in data folder
data_folder = "data"
files = [f for f in os.listdir(data_folder) if f.endswith(".json")]

if not files:
    print("No JSON files found in data folder!")
    exit()

# Pick the latest file
files.sort(reverse=True)
latest_file = os.path.join(data_folder, files[0])

with open(latest_file, "r", encoding="utf-8") as f:
    data = json.load(f)

# Convert to DataFrame
df = pd.DataFrame(data)

# -------------------------------
# Step 2: Data Cleaning
# -------------------------------

# Remove duplicates based on post_id
df = df.drop_duplicates(subset="post_id")

# Handle missing values
df["score"] = df["score"].fillna(0)
df["num_comments"] = df["num_comments"].fillna(0)
df["author"] = df["author"].fillna("unknown")

# Convert data types
df["score"] = df["score"].astype(int)
df["num_comments"] = df["num_comments"].astype(int)

# Remove rows with missing title/category
df = df.dropna(subset=["title", "category"])

# -------------------------------
# Step 3: Save as CSV
# -------------------------------

output_file = "data/cleaned_trends.csv"
df.to_csv(output_file, index=False)

# -------------------------------
# Output message
# -------------------------------
print(f"Cleaned data saved to {output_file}")
print(f"Total records after cleaning: {len(df)}")
