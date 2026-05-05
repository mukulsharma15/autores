import os
import subprocess
import sys
import shutil
import wfdb
import numpy as np
from pathlib import Path

# --- Compatibility Patch for imgaug ---
# Newer numpy versions removed aliases like np.bool, np.int, etc.
# We patch them back so imgaug can import successfully.
_builtins = __builtins__ if isinstance(__builtins__, dict) else vars(__builtins__)
for _alias in ('bool', 'int', 'float', 'complex', 'object', 'str'):
    if not hasattr(np, _alias):
        setattr(np, _alias, _builtins.get(_alias))

# --- Configuration ---
NUM_RECORDS = 5000
PTB_XL_DB = 'ptb-xl'
BASE_DIR = Path(__file__).parent.absolute()
DOWNLOAD_DIR = BASE_DIR / 'ptbxl_records'
OUTPUT_DIR = BASE_DIR / 'ecg_images_output'
GENERATOR_DIR = BASE_DIR / 'codes' / 'ecg-image-generator'
VENV_PYTHON = BASE_DIR / '.venv_ecg' / 'Scripts' / 'python.exe'

def setup_directories():
    """Create necessary directories if they don't exist."""
    DOWNLOAD_DIR.mkdir(exist_ok=True)
    OUTPUT_DIR.mkdir(exist_ok=True)
    print(f"Directories setup: \n - {DOWNLOAD_DIR}\n - {OUTPUT_DIR}")

def download_ptbxl_data(num_records=5000):
    """Download clean records from PhysioNet PTB-XL."""
    print(f"Fetching list of available records from PTB-XL...")
    
    try:
        # Get all records available in the current version of PTB-XL
        all_records = wfdb.get_record_list(PTB_XL_DB)
        
        # Filter for high-resolution records (records500) and take the first N
        valid_records = [r for r in all_records if r.startswith('records500/')]
        
        if len(valid_records) < num_records:
            print(f"Warning: requested {num_records} but only {len(valid_records)} high-res records are available.")
            num_records = len(valid_records)
            
        record_ids = valid_records[:num_records]
        print(f"Selected {len(record_ids)} valid records (handling gaps in version 1.0.3).")
        
    except Exception as e:
        print(f"Error fetching record list: {e}")
        sys.exit(1)
    
    print(f"Downloading records from PhysioNet...")
    try:
        wfdb.dl_database(
            PTB_XL_DB,
            dl_dir=str(DOWNLOAD_DIR),
            records=record_ids,
            annotators=None,
            keep_subdirs=False, # Flatten for easier batch processing
            overwrite=False
        )
        print(f"Successfully downloaded/verified records in {DOWNLOAD_DIR}")
    except Exception as e:
        print(f"Error downloading data: {e}")
        sys.exit(1)

def generate_images():
    """Run the ECG-Image-Kit pipeline to generate synthetic paper images."""
    print("Starting image generation pipeline...")
    
    # Note: We must run the script from inside its own directory because of relative path assumptions (e.g. Fonts/)
    cmd = [
        str(VENV_PYTHON),
        "gen_ecg_images_from_data_batch.py",
        "-i", str(DOWNLOAD_DIR),
        "-o", str(OUTPUT_DIR),
        "-se", "42",
        "-r", "200",
        "--print_header",
        "--calibration_pulse", "1.0",
        "--random_grid_present", "1.0",
        "--store_config", "1",
        "--standard_grid_color", "5"
    ]
    
    print(f"Executing: {' '.join(cmd)}")
    
    try:
        # Run with current working directory set to the generator folder
        result = subprocess.run(cmd, cwd=str(GENERATOR_DIR), check=True)
        print(f"Successfully generated images in {OUTPUT_DIR}")
    except subprocess.CalledProcessError as e:
        print(f"Error during image generation: {e}")
        sys.exit(1)

if __name__ == "__main__":
    setup_directories()
    download_ptbxl_data(NUM_RECORDS)
    generate_images()
    
    print("\n--- Summary ---")
    generated_pngs = list(OUTPUT_DIR.glob("*.png"))
    print(f"Total images generated: {len(generated_pngs)}")
    if generated_pngs:
        print(f"Sample image location: {generated_pngs[0]}")
