import os
import pandas as pd
import shutil

# 1) Define Paths
metadata_path = "/Users/water/Desktop/large_data/validated.tsv"
clips_folder = "/Users/water/Desktop/large_data/clips"
validated_clips_folder = "/Users/water/Desktop/large_data/validated_clips"

# 2) Create validated_clips folder if it doesn't exist
os.makedirs(validated_clips_folder, exist_ok=True)

# 3) Load the metadata
metadata = pd.read_csv(metadata_path, sep="\t")

# Extract just the unique parts (e.g., `common_voice_en_XXXX`) from the "path" column
metadata_core_ids = [os.path.splitext(os.path.basename(p))[0] for p in metadata["path"]]

# 4) List actual files in the clips folder
actual_files = os.listdir(clips_folder)

# Extract just the core identifiers (e.g., `common_voice_en_XXXX`) from the actual filenames
actual_core_ids = {os.path.splitext(f)[0]: f for f in actual_files}

# [Debug] Print samples to understand mismatches
print("Sample from metadata_core_ids (first 5):", metadata_core_ids[:5])
print("Sample from actual_core_ids (first 5):", list(actual_core_ids.keys())[:5])

# 5) Match files by core identifiers
matches = {}
for core_id in metadata_core_ids:
    if core_id in actual_core_ids:
        matches[core_id] = actual_core_ids[core_id]
    else:
        print(f"No match found for: {core_id}")

# 6) Move matched files to validated_clips_folder
for core_id, actual_file in matches.items():
    old_path = os.path.join(clips_folder, actual_file)
    new_path = os.path.join(validated_clips_folder, actual_file)
    
    shutil.move(old_path, new_path)
    print(f"Moved file: {actual_file} -> {new_path}")
