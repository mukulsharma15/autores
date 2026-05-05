# DECISIONS.md
## ECG Post-Digitization Refinement — Decision Log
**Project:** Post-Digitization Refinement of ECG Signals Using Diffusion Models  
**Researcher:** Mukul Sharma | SAU/CS/MSc/2024/08  
**Supervisor:** Prof. Pranab K. Muhuri  
**Last updated:** April 2026

---

## How to use this file
Every non-obvious technical or research decision is logged here with its rationale and date. If you revisit this project after a break, this file is where you reconstruct your thinking.

---

## D-001 — Use Diffusion Model as post-processing, not as digitizer
**Date:** Semester 2 (2nd year)  
**Decision:** Apply a conditional DDPM *after* the existing ECG-Image-Kit digitization pipeline, not replace the digitizer itself.  
**Reason:** The baseline digitizer already handles the hard image-to-signal conversion. The residual noise (staircase artifacts, spikes, grid remnants, quantization errors) is a well-defined denoising problem that DMs are suited for. Replacing the digitizer entirely would require retraining on 85.75 GB of data — outside compute budget.  
**Status:** Confirmed. Still the right approach.

---

## D-002 — Use partial reverse diffusion (t_start=30), not full generation
**Date:** Semester 3 (3rd sem mid-term)  
**Decision:** At inference, start the reverse diffusion from t=30 (not t=200).  
**Reason:** Full generation (t=200) starts from pure noise — it can hallucinate ECG morphology not present in the digitized input. Refinement (t=30) starts from the digitized signal, adds only 15% of the noise schedule, and makes targeted corrections. This is safer for clinical morphology.  
**Alternative considered:** t=50, t=100. Chose t=30 empirically as the best balance between correction and morphology preservation.  
**Status:** Current default. Should be ablated over t_start values in future work.

---

## D-003 — TARGET signal length = 1250, not 2500
**Date:** Semester 3 (this semester — Bug Fix #1)  
**Decision:** Extract 1250 samples per signal, not 2500.  
**Reason:** The real PhysioNet signals at 500 Hz are 2.5 seconds = 1250 samples. The v1 pipeline used TARGET=2500, which silently duplicated every other sample (linear interpolation artefact). This meant 50% of the training data was fabricated. Fixed by setting TARGET=1250.  
**Impact:** This single fix was the largest contributor to dataset quality improvement.  
**Status:** Fixed in v2 dataset.

---

## D-004 — Normalize noisy signal using clean signal's range (shared normalization)
**Date:** Semester 3 (this semester — Bug Fix #2)  
**Decision:** When creating training pairs, scale the noisy signal using the clean signal's min/max range, not its own range.  
**Reason:** Independent normalization (each signal scaled to [-1,1] by its own range) erases amplitude errors — the very thing the DM needs to learn. If noisy and clean are both mapped to exactly [-1,1], there is nothing left for the model to correct at the amplitude level.  
**Known problem:** At inference time, no clean reference signal is available. Independent normalization must be used at inference, creating a train/inference mismatch.  
**Next step (D-009):** Retrain using independent normalization from the start so training and inference conditions match.  
**Status:** Used in v2 training. Known mismatch with inference. Needs fix.

---

## D-005 — Use ensemble digitizer (sweep + NN), not color sweep only
**Date:** Semester 3 (this semester — Bug Fix #4)  
**Decision:** Use the ensemble digitizer (column sweep + neural network average) for extraction.  
**Reason:** The v1 pipeline used color sweep only, which is designed for color images. The PhysioNet dataset includes B&W scans, grayscale images, and mobile photos. The ensemble method handles both color and B&W, producing higher cosine similarity pairs (mean CS: 0.884 → 0.9735).  
**Status:** Fixed in v2 dataset.

---

## D-006 — Minimum 500 training pairs
**Date:** Semester 3 (this semester — Bug Fix #3)  
**Decision:** Extract until 500 high-quality (noisy, clean) pairs are collected. v1 had only 120 pairs from 10 ECG images.  
**Reason:** 120 samples is insufficient for a DM with 7.27M parameters to learn real noise patterns. The model was effectively memorizing rather than generalizing.  
**Result:** 500 pairs from 69 ECG images. 56% have cosine similarity > 0.98.  
**Status:** Done. v2 dataset = 500 pairs.

---

## D-007 — Model architecture: Conditional DDPM with 1D UNet, 7.27M params
**Date:** Semester 2  
**Decision:** Use a 1D UNet as the backbone for the conditional DDPM.  
**Reason:** 1D UNet is the standard architecture for time-series denoising with DMs. Conditioning signal (digitized ECG) is concatenated with x_t as input.  
**Parameters:** 7.27M — appropriate for 500 training samples (not too large to overfit, not too small to underfit).  
**Status:** Unchanged. Same architecture used in v2.

---

## D-008 — Training config: 200 epochs, LR=0.0001, batch=32, 400/100 split
**Date:** Semester 3  
**Decision:** Train for 200 epochs with the above hyperparameters.  
**Reason:** Learning curve shows stable convergence by epoch 150 (train: 0.02066, val: 0.02510, best_val: 0.01503). No signs of severe overfitting. Best val loss: 0.01348 at epoch 200.  
**Status:** Current config. Could benefit from LR scheduling in future.

---

## D-009 — RESOLVED: Retrain with massive dataset and full metrics
**Date:** April 2026  
**Decision:** ✅ DONE.  
**What:** Retrained the DM using 7,601 aligned pairs on Colab T4 GPU for 500 epochs with Automatic Mixed Precision (AMP), Cosine Annealing, and Gradient Clipping.  
**Result:** Replaced the simple MSE/SNR evaluation with an exhaustive 12-metric suite (Cosine Sim, Pearson r, RMSE, MAE, SSD, MAD, PRD, SNR, SNR_med, ImSNR, KS_Stat, WAD). The model successfully reduced overall error (RMSE by 13%) and achieved an ImSNR of +1.76 dB.  
**Status:** Completed.

---

## D-011 — PENDING: Downstream Clinical Utility Evaluation
**Date:** April 2026
**Decision:** Execute a SOTA classification comparison to prove clinical impact.
**What:** Map the `metadata.csv` (using the public PTB-XL labels) and run the Noisy vs. DM-Refined arrays through a pre-trained 1D ResNet. 
**Why:** The literature explicitly discourages "Accuracy" for ECGs. We will use Macro F1-Score, AUROC, and AUPRC to prove that the DM actually improves disease diagnosis, elevating the thesis from "signal processing" to "clinical impact."
**Status:** ⚠️ PENDING — this is the final experiment to run before thesis defense.
