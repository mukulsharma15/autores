# results/v2_summary.md
## Experiment Summary — Dataset v2 + DM Training
**Date:** 3rd Semester Mid-Term  
**Status:** Complete (isolated evaluation). Integration gap identified. Retrain pending.

---

## Dataset v2

| Property | v1 | v2 |
|---|---|---|
| ECG images | 10 | 69 |
| Total samples | 120 | 500 |
| Signal length | 2500 (50% duplicate) | 1250 (real) |
| Mean cosine similarity | 0.884 | 0.9735 |
| Min cosine similarity | −0.129 | 0.8699 |
| Normalization | Independent | Shared clean scale |
| Digitizer | Color sweep only | Ensemble (sweep + NN) |

56% of 500 samples have cosine similarity > 0.98.

---

## Model Config

| Property | Value |
|---|---|
| Architecture | Conditional DDPM, 1D UNet |
| Parameters | 7.27M |
| Epochs | 200 |
| Learning rate | 0.0001 |
| Batch size | 32 |
| Train / Val split | 400 / 100 |
| Inference t_start | 30 (partial reverse diffusion) |

---

## Training Curve

| Epoch | Train loss | Val loss | Best val |
|---|---|---|---|
| 50 | 0.02539 | 0.05038 | 0.02061 |
| 100 | 0.02384 | 0.02404 | 0.01639 |
| 150 | 0.02066 | 0.02510 | 0.01503 |
| 200 | 0.01785 | 0.03058 | 0.01348 |

Best val loss: **0.01348** (saved checkpoint).  
Note: Val loss at epoch 200 (0.03058) is higher than best val (0.01348) — slight overfitting at end. Best checkpoint used for evaluation.

---

## Isolated Evaluation Results (v2, 500 samples)

Condition: noisy signal normalized using clean signal's range (matches training).

| Metric | Input | Refined | Improvement |
|---|---|---|---|
| MSE | 0.0121 | 0.0102 | **+15.74%** |
| MAE | 0.0539 | 0.0499 | **+7.46%** |
| SNR (dB) | 14.1801 | 15.3396 | **+8.18%** |
| PRD (%) | 21.3945 | 19.2479 | **+10.03%** |
| Cosine Sim | 0.9735 | 0.9774 | +0.40% |

Samples improved: **429 / 500**  
Best improvement: +68.67%  
Worst case: −36.25%

---

## Pipeline Integration Results (real inference)

Condition: noisy signal normalized independently (no clean reference at inference).

| Metric | Improvement |
|---|---|
| MSE | +0.68% |
| SNR | ~0% |

**Root cause of gap:** Train/inference normalization mismatch.  
Training used shared normalization (noisy scaled by clean's range).  
Inference must use independent normalization (no clean reference available).  
Model sees differently-scaled inputs at inference than during training.

---

## Key Qualitative Results

**Best case (ECG 26, Lead V2, CS=0.988):**  
MSE: 0.0022 → 0.0017 (+22.0%). Clean separation of digitization artifacts.

**Median case (ECG -, Lead aVF, CS=0.968):**  
MSE: 0.0163 → 0.0148 (+9.1%). Moderate staircase smoothing.

**Worst case (ECG 22, Lead aVF, CS=0.979):**  
MSE: 0.0094 → 0.0102 (−8.7%). DM slightly over-smoothed a sharp peak.

---

## Open Issue

**D-009:** Retrain DM using independent normalization from the start.  
Expected outcome: pipeline integration gain improves toward the +15.7% isolated result.  
This is the primary next experiment.
