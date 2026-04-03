import pandas as pd

# load data
passes = pd.read_csv("data/passes.csv")
names = pd.read_csv("data/player_names.csv")

# count passes
pair_counts = passes.groupby(["passer","receiver"]).size().reset_index(name="passes")

# total passes
total_passes = pair_counts["passes"].sum()

# compute chemistry
pair_counts["chemistry"] = pair_counts["passes"] / total_passes

# map names
pair_counts = pair_counts.merge(names, left_on="passer", right_on="player_id")
pair_counts = pair_counts.rename(columns={"name": "passer_name"}).drop(columns=["player_id"])

pair_counts = pair_counts.merge(names, left_on="receiver", right_on="player_id")
pair_counts = pair_counts.rename(columns={"name": "receiver_name"}).drop(columns=["player_id"])

# sort by chemistry
pair_counts = pair_counts.sort_values(by="chemistry", ascending=False)

# display
print(pair_counts[["passer_name","receiver_name","chemistry"]])

# save
pair_counts.to_csv("data/player_chemistry.csv", index=False)

print("Saved chemistry ranking")