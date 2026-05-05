# Presentation Content: Master's Thesis Defense

**Title:** Clinically-Guided Post-Digitization Refinement of Electrocardiograms using Conditional Diffusion Models

---

## Slide 1: Title Slide
*   **Title:** Clinically-Guided Post-Digitization Refinement of ECGs
*   **Name:** Mukul Sharma
*   **Visual:** Side-by-side comparison of a noisy extracted ECG and the diffusion-refined ECG.

## Slide 2: The Logic Chain of Legacy ECGs
*   **Step 1:** Perfect biological 1D data (PTB-XL).
*   **Step 2:** Placed on messy paper (ECG-Image-Kit).
*   **Step 3:** Baseline deterministic digitizers attempt to extract the 1D signal but fail due to grid lines and wrinkles.
*   **Step 4 (Our Solution):** A Diffusion Model maps the noisy optical extraction back to the clean biological manifold.

## Slide 3: Diagnosing Optical Extraction Failures
*   **The Baseline Flaws:** We discovered four major bugs in existing extraction pipelines:
    1.  *Signal Duplication:* Target length incorrectly set to 2500 instead of 1250.
    2.  *Weak Heuristics:* Upgraded to an Ensemble Digitizer over a basic color sweep.
    3.  *Data Scarcity:* Scaled from 120 pairs to 7,601 pairs.
    4.  *The Normalization Mismatch:* Fixed the train/inference gap where independent scaling erased amplitude errors.

## Slide 4: The 7,601 Paired Dataset
*   **Achievement:** Cross-correlated and perfectly aligned 7,601 paired segments (Noisy vs. Clean).
*   **Strict Split:** Implemented a strict `ecg_id` GroupShuffleSplit. The model never sees a patient's morphology across Train/Val/Test boundaries, eliminating data leakage.

## Slide 5: The Model - Partial Reverse Diffusion
*   **Architecture:** 1D Conditional DDPM (7.27M parameters, 1D U-Net backbone).
*   **Key Innovation:** Partial Reverse Diffusion ($t_{start}=30$). Instead of full generation, we add 15% noise to the digitized signal and reverse-diffuse. This refines artifacts without hallucinating new heartbeats.

## Slide 6: Strict Evaluation Results (The Proof)
*   **Test Set:** Evaluated on 1,507 completely unseen patient samples.
*   **Metrics:** 
    *   **+1.03 dB ImSNR**
    *   **9.47% RMSE Reduction**
    *   **5.15% KS_Stat Improvement** (Proving the signal returns to a biological distribution).
*   **Visual:** 4-panel Thesis Plot (Full Overlay, Zoomed QRS Staircase, Absolute Error, PSD).

## Slide 7: Pushing the SOTA - KAN and DCT
*   **Limitation:** Base U-Net struggles with extreme non-linear baseline wander.
*   **Upgrades:** 
    *   *KAN Layers:* Adaptive activations for baseline wander.
    *   *DCT Conditioning:* Explicit frequency-domain isolation of "staircase" pixel quantization.

## Slide 8: The Clinical Danger of MSE Loss
*   **The Problem:** Standard diffusion MSE loss just minimizes distance. It will smooth over a diagnostic micro-arrhythmia if it mathematically lowers the overall error. 
*   **Evidence:** The visually cleaner ECGs can actually cause a drop in downstream AI classification (F1-Score).

## Slide 9: Task-Aware Clinical Guidance
*   **The Fix:** Introduced Task-Aware Loss based on *TDD (2025)*.
*   **Mechanism:** A frozen clinical oracle (ResNet1D) grades the denoised signal $x_0$ during training. If the diagnosis changes from the ground-truth PTB-XL labels, the diffusion model is penalized.

## Slide 10: Conclusion and Impact
*   **Summary:** We proved that generative refinement is mandatory to fix the +0 dB SNR artifacts left by deterministic optical extractors. 
*   **Impact:** Unlocks millions of paper ECGs for deep learning diagnostics by mathematically guaranteeing clinical preservation.

## Slide 11: Q&A
*   Thank you. Any questions?