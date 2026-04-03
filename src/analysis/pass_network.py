import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# load pass dataset
df = pd.read_csv("data/passes.csv")

# count passes between players
pass_counts = df.groupby(["passer", "receiver"]).size().reset_index(name="count")

# create graph
G = nx.DiGraph()

for _, row in pass_counts.iterrows():
    passer = row["passer"]
    receiver = row["receiver"]
    weight = row["count"]

    G.add_edge(passer, receiver, weight=weight)

# draw graph
pos = nx.spring_layout(G)

weights = [G[u][v]["weight"] for u,v in G.edges()]

nx.draw(
    G,
    pos,
    with_labels=True,
    node_color="lightblue",
    node_size=2000,
    font_size=10,
    width=weights
)

plt.title("Pass Network")
plt.savefig("data/pass_network.png")
print("Graph saved to data/pass_network.png")