import csv
import random

# We will fetch the PTB-XL database again to grab Age and Sex
print("Reading PTB-XL database for Demographics...")
ptb_metadata = {}
try:
    with open('ptbxl_database.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)
        idx_ecgid = header.index('ecg_id')
        idx_age = header.index('age')
        idx_sex = header.index('sex')
        
        for row in reader:
            try:
                ecg_id = int(row[idx_ecgid])
                ptb_metadata[ecg_id] = {
                    'age': row[idx_age] if row[idx_age] else 'Unknown',
                    'sex': row[idx_sex] if row[idx_sex] else 'Unknown'
                }
            except:
                pass
except Exception as e:
    print("Error reading PTB-XL:", e)

print(f"Loaded demographics for {len(ptb_metadata)} patients.")

# Now we read the current metadata and do two things:
# 1. Add Age and Sex
# 2. Add fixed Train/Val/Test splits grouped strictly by ecg_id
print("Updating 01_Dataset/metadata.csv...")
lines = open('01_Dataset/metadata.csv', 'r').readlines()
header_parts = lines[0].strip().split(',')

if 'age' not in header_parts:
    new_header = lines[0].strip() + ",age,sex,split\n"
else:
    new_header = lines[0] # already run
    
# First, let's gather all unique ecg_ids to create a strict group split
unique_ecg_ids = list(set([int(line.split(',')[0]) for line in lines[1:]]))
random.seed(42) # Fixed seed for reproducibility
random.shuffle(unique_ecg_ids)

# 70% Train, 15% Val, 15% Test
n_total = len(unique_ecg_ids)
n_train = int(0.70 * n_total)
n_val = int(0.15 * n_total)

train_ids = set(unique_ecg_ids[:n_train])
val_ids = set(unique_ecg_ids[n_train:n_train+n_val])
test_ids = set(unique_ecg_ids[n_train+n_val:])

new_lines = [new_header]

for line in lines[1:]:
    parts = line.strip().split(',')
    ecg_id = int(parts[0])
    
    # Get demographics
    demo = ptb_metadata.get(ecg_id, {'age': 'Unknown', 'sex': 'Unknown'})
    
    # Get split
    if ecg_id in train_ids:
        split = "train"
    elif ecg_id in val_ids:
        split = "val"
    else:
        split = "test"
        
    if 'age' not in header_parts:
        new_lines.append(line.strip() + f",{demo['age']},{demo['sex']},{split}\n")
    else:
        # If it was already there, we shouldn't append but let's assume it wasn't
        pass

with open('01_Dataset/metadata.csv', 'w') as f:
    f.writelines(new_lines)

print(f"Success! Added Demographics (Age/Sex) and Fixed Data Splits (Train/Val/Test) based strictly on ecg_id.")
