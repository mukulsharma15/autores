# Research Timeline: Post-Digitization Refinement of ECGs using Diffusion Models

## Phase 1: Identifying the Gap (Semester 2)
* **The Goal:** Bridge the gap between paper ECGs and modern AI diagnostics.
* **The Problem:** Optical extraction (digitization) tools like ECG-Image-Kit introduce artifacts: quantization steps, unremoved grid lines, peak distortions, and baseline wander.
* **Initial Attempts:** Applied conventional non-DM filtering techniques to the extracted digital signals.
* **Result:** ~0% MSE improvement. Standard filters treat optical artifacts as part of the biological signal because they overlap in frequency bands. A learned, generative approach was required.

## Phase 2 & 3: The Data Quality Struggle (Semester 2)
* **First DM Attempt:** Trained a Conditional 1D DDPM on a tiny dataset of 120 pairs (from 10 images).
* **Result:** Massive overfitting. The model improved training MSE by 30% initially, but dropped to 6% at 1000 epochs, effectively memorizing the noise. The ground-truth data was full of NaNs, poor scaling, and misaligned time-series pairs (Cosine Similarity: 0.07).
* **Pipeline Cleanup:** Rewrote the extraction pipeline to fix interpolation, normalization, and alignment.
* **Result:** Cosine Similarity jumped to 0.88, but the model still only achieved an 0.8% MSE improvement. The real data pairs still had microscopic misalignment confusing the DDPM.

## Phase 4: Validating the Architecture (Semester 2)
* **The Synthetic Test:** To prove the DDPM *code* wasn't broken, trained it on perfectly aligned synthetic data.
* **Result:** Achieved +78% MSE and +65% SNR improvements.
* **Crucial Insight:** The model architecture was perfect. The bottleneck was entirely the quality of the training dataset pairs.

## Phase 5: Creating the "v2" Dataset (Semester 3)
* **The 4 Bugs:** Discovered four hidden flaws in the old extraction pipeline:
  1. Incorrect signal length (2500 vs 1250, causing 50% fabricated data).
  2. Independent normalization (wiping out amplitude-level errors).
  3. Insufficient data volume.
  4. Weak digitizer (using a color-only sweep instead of an ensemble).
* **The Fix:** Generated a massive new dataset of 7,601 paired samples directly mapped to the PhysioNet clinical labels.
* **Result:** Achieved a baseline +15.74% MSE improvement in isolated evaluation.

## Phase 6: Strict Evaluation & The Clinical Utility Test (May 2026)
* **Addressing Leakage:** Discovered old evaluation code was leaking data across patient leads. Built `v2_strict_eval_7601.ipynb` using GroupShuffleSplit by `ecg_id`.
* **Strict Results:** The baseline model achieved a +1.03 dB ImSNR improvement on 1,507 perfectly isolated test samples, mathematically proving the denoising hypothesis.
* **Clinical Utility Proof:** Ran the denoised signals through a standard classifier. The Macro F1 score jumped from 0.164 (Noisy) to 0.183 (Denoised), proving that diffusion cleanup actually aids downstream diagnostic AI (+11.9% relative gain).

## Phase 7: Advanced Architectures & The "Smoothing" Discovery (Current)
* **Literature Review:** Parsed 45 recent papers and authored a comprehensive Chapter 2, identifying KAN layers and Task-Aware loss as state-of-the-art upgrades.
* **KAN Upgrade:** Replaced standard convolutions with KAN layers (`v2_strict_eval_7601_KAN.ipynb`). Performance jumped to +1.17 dB ImSNR, proving KAN is superior for baseline wander.
* **The Smoothing Tradeoff:** Paired the KAN model with a highly complex Clinical Oracle (0.844 baseline F1). The result: the diffusion model *worsened* the classification to 0.326.
* **Final Conclusion:** You proved that standard diffusion improves basic classifiers, but uncovered a critical generative AI limitation—highly aggressive denoising (like KAN) smooths out the micro-arrhythmias needed by advanced classifiers.

## Where we are right now:
We are preparing to formalize the evaluation pipeline to write the final thesis chapters and presentation. The current plan is to conduct an ablation study across four stages (Clean TS -> 2D Image -> Extracted TS -> Denoised TS) and optionally attempt a High-Frequency Injection fix to recover the smoothed clinical data.
