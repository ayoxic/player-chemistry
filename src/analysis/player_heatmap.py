import pandas as pd
import matplotlib.pyplot as plt

# load player positions
df = pd.read_csv("data/player_positions.csv")

# choose one player
player_id = df["player_id"].unique()[0]

player_data = df[df["player_id"] == player_id]

plt.figure(figsize=(8,5))

plt.hist2d(
    player_data["x"],
    player_data["y"],
    bins=50
)

plt.colorbar()
plt.title(f"Heatmap - Player {player_id}")
plt.xlabel("X position")
plt.ylabel("Y position")

plt.savefig("data/player_heatmap.png")

print("Heatmap saved to data/player_heatmap.png")