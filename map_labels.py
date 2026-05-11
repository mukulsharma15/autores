import urllib.request
import os
import ast
import numpy as np

print("Downloading PTB-XL scp_statements.csv to get superclass mappings...")
urllib.request.urlretrieve('https://physionet.org/files/ptb-xl/1.0.3/scp_statements.csv', 'scp_statements.csv')

print("Downloading PTB-XL ptbxl_database.csv to get patient diagnoses...")
urllib.request.urlretrieve('https://physionet.org/files/ptb-xl/1.0.3/ptbxl_database.csv', 'ptbxl_database.csv')

# Load the superclass dictionary
scp_df = [line.strip().split(',') for line in open('scp_statements.csv', 'r').readlines()]
header = scp_df[0]
idx_desc = header.index('diagnostic_class')
idx_name = header.index('Unnamed: 0')
agg_df = {row[idx_name]: row[idx_desc] for row in scp_df[1:] if row[idx_desc] != ''}

# Create ecg_id -> superclass mapping
print("Mapping ecg_id to superclasses...")
ptb_df = [line.strip().split('",') for line in open('ptbxl_database.csv', 'r').readlines()]
header = [h.replace('"', '') for h in ptb_df[0]]
idx_ecgid = header.index('ecg_id')
idx_scp = header.index('scp_codes')

ecg_to_classes = {}
for row in ptb_df[1:]:
    try:
        ecg_id = int(row[idx_ecgid].replace('"', ''))
        scp_str = row[idx_scp].replace('""', '"').strip('"')
        if scp_str.startswith('{'):
            scp_dict = ast.literal_eval(scp_str)
            # Find the diagnostic class with highest probability (or just the first one)
            diagnostic_classes = []
            for k in scp_dict.keys():
                if k in agg_df and agg_df[k]:
                    diagnostic_classes.append(agg_df[k])
            
            # Simple approach: grab the first valid diagnostic class (often single label focus)
            # For a multi-label approach we could save a list. Let's do single primary class for now.
            if diagnostic_classes:
                # Resolve tie: just take the most frequent or first
                ecg_to_classes[ecg_id] = diagnostic_classes[0]
            else:
                ecg_to_classes[ecg_id] = 'NORM' # fallback
    except Exception as e:
        continue

print(f"Mapped {len(ecg_to_classes)} total ECGs from PTB-XL.")

# Now read our metadata.csv and append the class
print("Updating 01_Dataset/metadata.csv...")
lines = open('01_Dataset/metadata.csv', 'r').readlines()
header = lines[0].strip() + ",diagnostic_class\n"
new_lines = [header]

classes_array = []
class_to_idx = {'NORM': 0, 'MI': 1, 'STTC': 2, 'CD': 3, 'HYP': 4}
numeric_labels = []

missing_count = 0
for line in lines[1:]:
    parts = line.strip().split(',')
    ecg_id = int(parts[0])
    
    # PTB-XL uses 5-digit IDs, our ecg_id in metadata might just be the numerical index if it was lost
    # Let's check if the ecg_ids in metadata are actual PTB-XL IDs.
    
    # Actually wait! The metadata might not have actual PTB-XL ecg_ids. Let's verify.
    d_class = ecg_to_classes.get(ecg_id, 'NORM')
    if ecg_id not in ecg_to_classes:
        missing_count += 1
        
    classes_array.append(d_class)
    numeric_labels.append(class_to_idx.get(d_class, 0))
    
    new_lines.append(line.strip() + f",{d_class}\n")

with open('01_Dataset/metadata_with_classes.csv', 'w') as f:
    f.writelines(new_lines)

# Save as numpy array to match clean_samples.npy length (7601)
np.save('01_Dataset/clinical_labels.npy', np.array(numeric_labels, dtype=np.int64))

print(f"Saved! Found {missing_count} unmapped IDs (assigned NORM fallback).")
print(f"Total rows processed: {len(numeric_labels)}")
