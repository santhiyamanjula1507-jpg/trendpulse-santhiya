import pandas as pd
import matplotlib.pyplot as plt
import os

# -------------------------------
# Step 1: Load Data
# -------------------------------
file_path = "data/cleaned_trends.csv"

try:
    df = pd.read_csv(file_path)
except Exception as e:
    print("Error loading file:", e)
    exit()

# Create folder for plots
if not os.path.exists("plots"):
    os.makedirs("plots")

# -------------------------------
# Step 2: Category Count Plot
# -------------------------------
category_count = df["category"].value_counts()

plt.figure()
category_count.plot(kind="bar")
plt.title("Number of Stories per Category")
plt.xlabel("Category")
plt.ylabel("Count")
plt.xticks(rotation=45)

plt.savefig("plots/category_count.png")
plt.close()

# -------------------------------
# Step 3: Average Score per Category
# -------------------------------
avg_score = df.groupby("category")["score"].mean()

plt.figure()
avg_score.plot(kind="bar")
plt.title("Average Score per Category")
plt.xlabel("Category")
plt.ylabel("Average Score")
plt.xticks(rotation=45)

plt.savefig("plots/avg_score.png")
plt.close()

# -------------------------------
# Step 4: Top Authors Plot
# -------------------------------
top_authors = df["author"].value_counts().head(5)

plt.figure()
top_authors.plot(kind="bar")
plt.title("Top 5 Authors")
plt.xlabel("Author")
plt.ylabel("Number of Posts")
plt.xticks(rotation=45)

plt.savefig("plots/top_authors.png")
plt.close()

# -------------------------------
# Output Message
# -------------------------------
print("Plots saved in 'plots/' folder")
