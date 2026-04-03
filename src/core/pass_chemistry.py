import pandas as pd

df = pd.read_csv("data/passes.csv")

# -------------------------
# FILTER BAD IDS
# -------------------------
df = df[(df["passer"] < 50) & (df["receiver"] < 50)]

# -------------------------
# UNDIRECTED PAIRS
# -------------------------
df["pair"] = df.apply(
    lambda row: tuple(sorted((row["passer"], row["receiver"]))),
    axis=1
)

pair_counts = df.groupby("pair").size().reset_index(name="passes")

pair_counts[["player1","player2"]] = pd.DataFrame(
    pair_counts["pair"].tolist(), index=pair_counts.index
)

# -------------------------
# CHEMISTRY
# -------------------------
total_passes = pair_counts["passes"].sum()
pair_counts["chemistry"] = pair_counts["passes"] / total_passes

# -------------------------
# SORT
# -------------------------
pair_counts = pair_counts.sort_values(by="chemistry", ascending=False)

print("\n🔥 FINAL CHEMISTRY TABLE 🔥\n")
print(pair_counts[["player1","player2","chemistry"]])

pair_counts.to_csv("data/final_chemistry.csv", index=False)

print("\n✅ Saved to data/final_chemistry.csv")