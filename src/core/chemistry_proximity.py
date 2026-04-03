import pandas as pd
import numpy as np
from itertools import combinations
from tqdm import tqdm

# -------------------------
# Load data
# -------------------------
df = pd.read_csv("data/player_positions.csv")

# load player names (optional)
try:
    names = pd.read_csv("data/player_names.csv")
    use_names = True
except:
    use_names = False

# -------------------------
# Parameters
# -------------------------
DIST_THRESHOLD = 100

players = df["player_id"].unique()
frames = df.groupby("frame")
total_frames = df["frame"].nunique()

chemistry = {}

# -------------------------
# Compute chemistry
# -------------------------
for frame_id, group in tqdm(frames, total=total_frames, desc="Computing chemistry"):

    positions = {
        row["player_id"]: (row["x"], row["y"])
        for _, row in group.iterrows()
    }

    for p1, p2 in combinations(players, 2):

        if p1 in positions and p2 in positions:

            x1, y1 = positions[p1]
            x2, y2 = positions[p2]

            dist = np.linalg.norm(np.array([x1,y1]) - np.array([x2,y2]))

            if dist < DIST_THRESHOLD:
                key = tuple(sorted((p1, p2)))
                chemistry[key] = chemistry.get(key, 0) + 1

# -------------------------
# Convert to dataframe
# -------------------------
results = []

for (p1, p2), count in chemistry.items():

    score = count / total_frames

    results.append({
        "player1": int(p1),
        "player2": int(p2),
        "chemistry": round(score, 3)
    })

df_result = pd.DataFrame(results)

# -------------------------
# Add names (if available)
# -------------------------
if use_names:

    df_result = df_result.merge(
        names, left_on="player1", right_on="player_id"
    ).rename(columns={"name": "Player 1"}).drop(columns=["player_id"])

    df_result = df_result.merge(
        names, left_on="player2", right_on="player_id"
    ).rename(columns={"name": "Player 2"}).drop(columns=["player_id"])

    final_df = df_result[["Player 1", "Player 2", "chemistry"]]

else:
    final_df = df_result

# -------------------------
# Sort results
# -------------------------
final_df = final_df.sort_values(by="chemistry", ascending=False)

# -------------------------
# Output
# -------------------------
print("\n🔥 FINAL CHEMISTRY TABLE 🔥\n")
print(final_df.head(15))

# save
final_df.to_csv("data/final_chemistry_table.csv", index=False)

print("\n✅ Saved to data/final_chemistry_table.csv")