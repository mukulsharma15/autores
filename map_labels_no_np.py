import urllib.request
import os
import ast
import csv

print("Downloading PTB-XL scp_statements.csv to get superclass mappings...")
if not os.path.exists('scp_statements.csv'):
    urllib.request.urlretrieve('https://physionet.org/files/ptb-xl/1.0.3/scp_statements.csv', 'scp_statements.csv')

print("Downloading PTB-XL ptbxl_database.csv to get patient diagnoses...")
if not os.path.exists('ptbxl_database.csv'):
    urllib.request.urlretrieve('https://physionet.org/files/ptb-xl/1.0.3/ptbxl_database.csv', 'ptbxl_database.csv')

# Load the superclass dictionary
scp_df = [line.strip().split(',') for line in open('scp_statements.csv', 'r').readlines()]
header = scp_df[0]
idx_desc = header.index('diagnostic_class')
# In this CSV, the first column is empty in the header: ",description,diagnostic..."
idx_name = 0
agg_df = {row[idx_name]: row[idx_desc] for row in scp_df[1:] if len(row) > idx_desc and row[idx_desc] != ''}

print("Mapping ecg_id to superclasses...")
ecg_to_classes = {}

# We need to handle quoted csv correctly
with open('ptbxl_database.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    header = next(reader)
    idx_ecgid = header.index('ecg_id')
    idx_scp = header.index('scp_codes')
    
    for row in reader:
        try:
            ecg_id = int(row[idx_ecgid])
            scp_str = row[idx_scp]
            if scp_str.startswith('{'):
                scp_dict = ast.literal_eval(scp_str)
                diagnostic_classes = []
                for k in scp_dict.keys():
                    if k in agg_df and agg_df[k]:
                        diagnostic_classes.append(agg_df[k])
                
                if diagnostic_classes:
                    ecg_to_classes[ecg_id] = diagnostic_classes[0]
                else:
                    ecg_to_classes[ecg_id] = 'NORM'
        except Exception as e:
            continue

print(f"Mapped {len(ecg_to_classes)} total ECGs from PTB-XL.")

# Now read our metadata.csv and append the class
print("Updating 01_Dataset/metadata.csv...")
lines = open('01_Dataset/metadata.csv', 'r').readlines()
# Don't duplicate if already run
if "diagnostic_class" not in lines[0]:
    header = lines[0].strip() + ",diagnostic_class,diagnostic_numeric\n"
else:
    header = lines[0]
new_lines = [header]

class_to_idx = {'NORM': 0, 'MI': 1, 'STTC': 2, 'CD': 3, 'HYP': 4}

missing_count = 0
for line in lines[1:]:
    parts = line.strip().split(',')
    ecg_id = int(parts[0]) 
    
    d_class = ecg_to_classes.get(ecg_id, 'NORM')
    if ecg_id not in ecg_to_classes:
        missing_count += 1
        
    num_class = class_to_idx.get(d_class, 0)
    
    if "diagnostic_class" not in lines[0]:
        new_lines.append(line.strip() + f",{d_class},{num_class}\n")
    else:
        # Already updated, just pass through
        new_lines.append(line)

with open('01_Dataset/metadata.csv', 'w') as f:
    f.writelines(new_lines)

print(f"Success! Updated 01_Dataset/metadata.csv in place.")
print(f"Total rows: {len(lines)-1}")
print(f"Could not find PTB-XL match for {missing_count} IDs.")
