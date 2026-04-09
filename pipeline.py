import subprocess
from tqdm import tqdm

# -------------------------
# Define pipeline steps
# -------------------------
steps = [
    ("Pass Chemistry", "src/core/pass_chemistry.py"),
    ("Proximity Chemistry", "src/core/chemistry_proximity.py"),
    ("Final Chemistry", "src/core/player_chemistry.py")
]

# -------------------------
# Run pipeline
# -------------------------
for step_name, script in tqdm(steps, desc="Pipeline Progress"):

    print(f"\n🚀 Running: {step_name}")

    result = subprocess.run(
        ["python", script],
        capture_output=True,
        text=True
    )

    print(result.stdout)

    if result.returncode != 0:
        print(f"\n❌ Error in step: {step_name}")
        print(result.stderr)
        break

else:
    print("\n✅ Pipeline completed successfully")
