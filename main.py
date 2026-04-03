print("Running full pipeline...")

import os

os.system("python src/tracking/extract_player_positions.py")
os.system("python src/analysis/pass_chemistry.py")
os.system("python src/analysis/chemistry_proximity.py")
os.system("python src/analysis/player_chemistry.py")

print("Done.")