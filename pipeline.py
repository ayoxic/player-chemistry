import subprocess
from tqdm import tqdm

# -------------------------
# Define pipeline steps
# -------------------------
steps = [
    "python src/core/pass_chemistry.py",
    "python src/core/chemistry_proximity.py",
    "python src/core/player_chemistry.py"
]
# -------------------------
# Run pipeline with progress bar
# -------------------------
for step_name, script in tqdm(steps, desc="Pipeline Progress"):

    print(f"\n🚀 Running: {step_name}")

    result = subprocess.run(
        ["python", script],
        capture_output=True,
        text=True
    )

    # print script output
    print(result.stdout)

    # check for errors
    if result.returncode != 0:
        print(f"\n❌ Error in step: {step_name}")
        print(result.stderr)
        break

else:
    print("\n✅ Pipeline completed successfully")