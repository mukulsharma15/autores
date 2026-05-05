# 05_Drafting/Thesis_Outline.md

## Structured Outline for Master's Thesis

**Title:** Clinically-Guided Post-Digitization Refinement of Electrocardiograms using Conditional Diffusion Models

### Chapter 1: Introduction
- **The Problem:** Billions of ECGs are locked in scanned PDF/JPG format. Modern clinical AI requires 1D time-series data.
- **The Gap:** Current optical digitizers (like ECG-Image-Kit) successfully align the data but introduce severe pixel quantization ("staircase") and high-frequency spike artifacts.
- **The Hypothesis:** Framing post-digitization artifact removal as a 1D Super-Resolution problem and solving it via a Conditional Diffusion Probabilistic Model (cDDPM).

### Chapter 2: Literature Review
- **Traditional Denoising:** Why Butterworth and FIR filters fail (digitization noise is not frequency-separable from the QRS complex).
- **Deep Generative Models for ECGs:** Review of *DeScoD-ECG* and *TFCDiff* (fixing hospital/sensor noise).
- **State-of-the-Art Digitizers:** Review of *ECG-Image-Kit* and *PTB-IMAGE/VinDigitizer* (the baseline deterministic extractions).

### Chapter 3: Methodology
- **Dataset Creation (The 7,601 Pairs):** How the PhysioNet 2024 Challenge data was extracted, cross-correlated for perfect alignment, and normalized into a paired `.npy` dataset.
- **Model Architecture (1D U-Net):** Details of the Sinusoidal Position Embeddings, the Down/Mid/Up block structure, and the skip-connections.
- **Diffusion Process:** The forward (noise addition) and partial reverse (t_start=30) diffusion math.
- **Optimization:** The use of L1 Loss, AdamW, Cosine Annealing, Gradient Clipping, and Automatic Mixed Precision (AMP).

### Chapter 4: Experiments and Results
- **The Baseline Comparison:** Displaying the Exhaustive 12-Metric suite table.
- **Key Findings:**
    - The +1.76 dB ImSNR gain.
    - The -13% drop in RMSE.
    - The preservation of morphology (Cosine Sim = 0.97).
    - The correction of statistical distribution (KS_Stat = 0.08).
- **Visual Evidence:** Including the 4-panel Thesis Plots (Full Overlay, Zoomed QRS Staircase, Absolute Error, and Power Spectral Density).
- **Downstream Clinical Utility:** Demonstrating the impact of the DM on AI-driven diagnostics (Macro F1-Score & AUROC improvement on a 1D ResNet).

### Chapter 5: Conclusion and Future Work
- **Conclusion:** The model successfully mitigated optical extraction artifacts, proving DMs are a viable post-digitization refinement layer.
- **Future Work:** Ablation studies on `t_start` values, replacing DDPM with DDIM for faster clinical inference, and testing the model on 250 Hz or 1000 Hz extractions.

### (Updated from CSV Literature)
- **Chapter 2: Literature Review** now incorporates the massive gap exposed by the 2024 PhysioNet Challenge (where top teams like *WAVIE* and *VinDigitizer* struggled to break 5 dB SNR on real scanned paper) and positions the 2025/2026 Diffusion papers (*TFCDiff* and *KAN-DeScoD*) as solving a completely different problem (hospital noise, not optical digitization noise).
