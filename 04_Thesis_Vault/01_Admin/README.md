# ECG Post-Digitization Refinement Using Diffusion Models

**Researcher:** Mukul Sharma | SAU/CS/MSc/2024/08  
**Supervisor:** Prof. Pranab K. Muhuri  
**Program:** MSc Computer Science, 2nd Year — South Asian University

---

## What This Is

A conditional Diffusion Model (cDDPM) that refines ECG signals *after* digitization. Legacy ECG records (paper/scans) are digitized into time-series by ECG-Image-Kit, but the output still contains artifacts. This model learns to correct those artifacts by training on (noisy digitized, clean original) signal pairs.

```
ECG Image → ECG-Image-Kit Digitizer → Noisy Signal → cDDPM → Refined Signal
```

---

## Current Status

| Phase                           | Result                        |
| ------------------------------- | ----------------------------- |
| Non-DM filters                  | ~0% improvement               |
| DM on v1 dataset (120 samples)  | −2.7% MSE (degraded)          |
| DM on synthetic data            | +78.8% MSE                    |
| **DM on v2 dataset — isolated** | **+15.74% MSE, +8.18% SNR** ✅ |

s
**Primary open experiment:** Retrain with independent normalization to close the isolated vs. integrated gap.

---

## Repository Structure

```
├── README.md                   ← this file
├── DECISIONS.md                ← all key technical decisions with rationale
├── RESEARCH_NARRATIVE.md       ← full research story, findings, open questions
│
├── data/
│   ├── README.md               ← dataset descriptions, where files are stored
│   └── .gitignore              ← excludes .npy files (too large for Git)
│
├── notebooks/
│   ├── 01_extraction.ipynb     ← pair extraction from PhysioNet baseline
│   ├── 02_training.ipynb       ← DM training
│   └── 03_evaluation.ipynb     ← metrics + visualizations
│
├── src/
│   ├── extract.py              ← extraction pipeline (v2 fixes applied)
│   ├── model.py                ← 1D UNet cDDPM architecture
│   ├── train.py                ← training loop
│   └── evaluate.py             ← evaluation metrics
│
└── results/
    ├── v1_summary.md           ← v1 dataset experiment results
    └── v2_summary.md           ← v2 dataset experiment results (current)
```

---

## How to Run

```bash
# 1. Extract pairs from PhysioNet baseline
python src/extract.py --output data/pairs_v2.npy --target 1250 --samples 500

# 2. Train the DM
python src/train.py --data data/pairs_v2.npy --epochs 200 --lr 0.0001

# 3. Evaluate
python src/evaluate.py --checkpoint checkpoints/best.pt --data data/pairs_v2.npy
```

---

## Key References

- Ho et al. — Denoising Diffusion Probabilistic Models — NeurIPS 2020
- Shivashankara et al. — ECG-Image-Kit — Physiological Measurement 2024
- Reyna et al. — PhysioNet Challenge 2024 — Computing in Cardiology 2024

---

## Data

Training data is from the PhysioNet Challenge 2024. 977 ECGs (85.75 GB) available; v2 uses 69 images → 500 pairs. Data is not stored in this repository. See `data/README.md` for storage location.
