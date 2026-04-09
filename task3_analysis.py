import pandas as pd
import numpy as np

# -------------------------------
# Step 1: Load CSV
# -------------------------------
file_path = "data/cleaned_trends.csv"

try:
    df = pd.read_csv(file_path)
except Exception as e:
    print("Error loading file:", e)
    exit()

# -------------------------------
# Step 2: Basic Info
# -------------------------------
print("\nTotal Records:", len(df))
print("\nColumns:", df.columns)

# -------------------------------
# Step 3: Category Analysis
# -------------------------------
print("\n--- Category Count ---")
category_count = df["category"].value_counts()
print(category_count)

# -------------------------------
# Step 4: Average Score per Category
# -------------------------------
print("\n--- Average Score per Category ---")
avg_score = df.groupby("category")["score"].mean()
print(avg_score)

# -------------------------------
# Step 5: Top 5 Highest Scoring Posts
# -------------------------------
print("\n--- Top 5 Posts by Score ---")
top_posts = df.sort_values(by="score", ascending=False).head(5)
print(top_posts[["title", "category", "score"]])

# -------------------------------
# Step 6: Most Active Authors
# -------------------------------
print("\n--- Top Authors (by number of posts) ---")
top_authors = df["author"].value_counts().head(5)
print(top_authors)

# -------------------------------
# Step 7: NumPy Usage (extra marks)
# -------------------------------
print("\n--- NumPy Insights ---")

scores_array = np.array(df["score"])

print("Max Score:", np.max(scores_array))
print("Min Score:", np.min(scores_array))
print("Average Score:", np.mean(scores_array))

# -------------------------------
# (Optional) Save Summary
# -------------------------------
summary = {
    "total_records": len(df),
    "max_score": int(np.max(scores_array)),
    "min_score": int(np.min(scores_array)),
    "avg_score": float(np.mean(scores_array))
}

summary_df = pd.DataFrame([summary])
summary_df.to_csv("data/analysis_summary.csv", index=False)

print("\nSummary saved to data/analysis_summary.csv")
