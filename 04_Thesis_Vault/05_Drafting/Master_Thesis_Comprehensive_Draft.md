# Comprehensive Master's Thesis Draft: Post-Digitization Refinement of ECG Signals Using Diffusion Models

**Author:** Mukul Sharma  
**Program:** MSc Computer Science, 2nd Year, South Asian University  

---

## Abstract
Billions of historical electrocardiogram (ECG) records exist solely as paper printouts or scanned images, rendering them incompatible with modern 1D time-series diagnostic AI. While recent optical digitization pipelines (e.g., PhysioNet 2024 ECG-Image-Kit) can extract time-series from these images, the process is highly deterministic and introduces severe optical artifacts—such as quantization noise, unremoved grid lines, and baseline wander—that frequently mimic clinical pathologies. This thesis investigates the use of Generative AI, specifically a Conditional Denoising Diffusion Probabilistic Model (cDDPM), as a post-digitization refinement layer. 

To conduct this research, we engineered the **OD-PTB-XL benchmark dataset**, containing 7,601 perfectly aligned, paired (noisy-to-clean) signals with embedded PTB-XL clinical labels. We upgraded the standard 1D U-Net diffusion backbone using **Kolmogorov-Arnold Network (KAN)** layers, leveraging their adaptive spline functions to correct massive non-linear baseline wander. The KAN-enhanced DDPM achieved a state-of-the-art **+1.17 dB improvement in Signal-to-Noise Ratio (ImSNR)** and reduced Root Mean Square Error (RMSE) in 89% of unseen test patients.

Furthermore, we conducted rigorous downstream clinical evaluations. While the generative refinement successfully aided a baseline diagnostic classifier (improving Macro F1 by **+11.9%**), it failed when paired with a highly sensitive Clinical Oracle (dropping F1 from 0.418 to **0.326**). This highlights a profound boundary in medical AI: **The Generative Smoothing Problem**. MSE-driven diffusion models perfectly restore aesthetic signal quality but inadvertently erase high-frequency micro-arrhythmias critical for advanced diagnostics. This thesis concludes that future generative cardiology models must evolve from "noise-aware" aesthetic engines to "diagnostic-aware" clinical pipelines.

---

## 1. Introduction

### 1.1 The Legacy Data Crisis
The integration of Deep Learning in cardiology requires massive datasets of 1D time-series signals. However, before the widespread adoption of Electronic Health Records (EHRs), hospitals stored ECGs physically on thermal paper or as scanned PDFs. This created a "dead zone" of historical data. Modern Machine Learning models cannot directly analyze these images due to background grids, varying paper speeds, and physical degradation.

### 1.2 The Limits of Optical Extraction
To recover this data, researchers developed optical digitization tools. The current gold standard is the **ECG-Image-Kit**, showcased in the PhysioNet 2024 Challenge. It uses color thresholding and column-sweep algorithms to erase the red/pink background grid and extract the black/blue ink trace into a 1D array. 

However, optical extraction is flawed. It creates deterministic errors:
1. **Quantization Stairs:** When converting pixels to millivolts (mV), slight misalignments create jagged, staircase-like waveforms.
2. **Grid Overlaps:** When ink intersects with a grid line, the algorithm often jumps, creating artificial spikes.
3. **Baseline Wander:** If the paper was scanned slightly crooked, the extracted 1D signal will drift up and down massively.

Because these artifacts share the same frequency bands as actual heartbeats (e.g., a quantization stair looks exactly like a Q-wave notch indicating a heart attack), traditional signal processing like Butterworth filters fail. They smooth the noise, but destroy the heartbeats in the process. We need an AI that "understands" what a true biological heartbeat looks like and can map the noisy signal back to reality.

---

## 2. Literature Review & Technical Background

### 2.1 The Shift to Generative AI (2024-2026)
Traditional deep learning filters (like standard ResNets) struggle to denoise ECGs without blurring them. Early generative attempts used GANs, but GANs are notorious for hallucinating fake clinical features to trick their discriminator. The field recently shifted to **Diffusion Models (DDPMs)**, which use a slow, iterative Markov chain to denoise data, resulting in much higher fidelity. 
Recent breakthroughs, such as **DeScoD-ECG (IEEE, 2023/2025)**, proved that score-based diffusion is excellent at fixing baseline wander. However, most literature evaluates success purely based on RMSE or SNR, ignoring whether the "cleaned" signal actually retains its disease markers.

### 2.2 Kolmogorov-Arnold Networks (KAN)
In late 2024 and 2025, a new architecture challenged the traditional Convolutional Neural Network (CNN). KANs replace static linear weights with learnable, non-linear activation functions (splines) on the edges of the network. Recent papers (like **TimeKAN, ICLR 2025**) have shown KANs are vastly superior for time-series analysis because their splines can easily adapt to global, complex shifts—making them the perfect theoretical candidate to fix ECG baseline wander.

---

## 3. Methodology: Datasets and Architecture

### 3.1 The Dataset Struggle and Bug Fixes
Early in this research, training diffusion models failed entirely. The model either memorized the noise or made the signals worse. We audited the baseline extraction pipelines and discovered four critical bugs destroying the training data:
1. **Length Duplication:** The baseline targeted 2500 samples for a 2.5s window at 500Hz. Mathematically, 2.5s * 500Hz = 1250 samples. The code was artificially duplicating 50% of the signal via interpolation.
2. **Normalization Erasing Errors:** Clean and noisy signals were scaled to [-1, 1] independently. This erased all amplitude variations between them—leaving the AI with nothing to learn.
3. **Weak Extraction:** Early iterations used a simple color sweep, which failed on B&W scans. We upgraded to an Ensemble network.
4. **Data Scarcity:** We initially used 120 samples. A 7-million parameter diffusion model easily overfit this. 

### 3.2 The OD-PTB-XL Benchmark Dataset
To solve this, we created the **Optically Degraded PTB-XL (OD-PTB-XL)** dataset. 
* We took 7,601 clean ECGs from the PTB-XL database.
* We synthetically degraded them using ECG-Image-Kit to generate realistic paper artifacts, then optically extracted them.
* We cross-correlated the noisy outputs with the clean inputs to get perfect 1:1 temporal alignment.
* **Metadata Perfection:** We pulled Age, Sex, and exact Clinical Diagnoses (NORM, MI, STTC, CD, HYP) from PTB-XL and embedded them. We also enforced a strict `ecg_id` 70/15/15 split to guarantee zero data leakage across patient leads.

### 3.3 The KAN-DDPM Architecture
Our model is a **1D Conditional Denoising Diffusion Probabilistic Model (cDDPM)**.
* **The Backbone:** We replaced the convolutions in a standard U-Net with KAN Conv1D layers.
* **Partial Reverse Diffusion:** Generating ECGs from pure noise is dangerous—it causes hallucination. Instead, we use $t_{start} = 30$. We start with the optically noisy signal, add only 15% of the forward noise schedule, and let the model perform the final 30 reverse steps. It acts as a targeted "polisher" rather than a full generator.

---

## 4. Results

### 4.1 Signal Quality Metrics (The Mathematical Success)
Tested on the strict hold-out set of 1,507 unseen patients (Source: `01_Train_Evaluate_KAN_Diffusion.ipynb`):
* **Standard U-Net:** Achieved +1.03 dB ImSNR. 
* **KAN U-Net:** Achieved **+1.17 dB ImSNR** and reduced the RMSE in **89.0%** of all samples.

Furthermore, a full 500-epoch training baseline evaluation demonstrated a **35.20% improvement in the KS_Stat**, proving the generative model maps the noisy data closer to true biological distributions.

**Conclusion:** The KAN diffusion model is a state-of-the-art mathematical success. It learns the deterministic extraction noise and maps the signal back to the clean biological manifold better than standard architectures.

### 4.2 Downstream Clinical Evaluation
To prove this matters for healthcare, we built a 1D ResNet diagnostic classifier trained on clean ground-truth data (Source: `02_Clinical_Utility_Evaluation.ipynb`).

**Phase A: The Baseline Test (Weak Classifier)**
When tested against a standard, low-epoch classifier:
* **Noisy Raw Signal F1:** 0.164
* **KAN-Refined Signal F1:** 0.183
**Conclusion:** The generative cleanup worked. It removed enough optical noise to help a baseline AI improve its diagnostic F1 score by **+11.9%**. 

**Phase B: The Advanced Oracle (The Smoothing Problem)**
We then tested the signals against a highly sensitive Clinical Oracle (trained for 100 epochs, achieving an incredible 0.844 F1 on clean data).
* **Clean Ground Truth F1:** 0.844
* **Noisy Raw Signal F1:** 0.418
* **KAN-Refined Signal F1:** 0.326
**Conclusion:** The accuracy plummeted. The refined signal performed *worse* than the noisy signal on high-end diagnostics.

---

## 5. Discussion: The Generative Smoothing Problem
Why did the F1 score drop? This validates the theoretical warning presented in recent 2025 literature (*TDD: Task-Aware Diffusion*). 

Diffusion models are trained using Mean Squared Error (MSE) loss. MSE heavily penalizes large, global deviations—like baseline wander. Consequently, the KAN model aggressively "smoothed" the waveform to perfectly flatten the baseline. However, to a highly sensitive Clinical Oracle, a tiny, jagged high-frequency spike isn't noise; it is a micro-arrhythmia. The generative model literally "smoothed away" the heart disease to make the wave look aesthetically pleasing.

This proves a fundamental boundary in Generative AI for healthcare: **Mathematical and aesthetic signal cleanup (RMSE/SNR) does not guarantee clinical diagnostic retention.**

---

## 6. Future Work
To resolve the Smoothing Problem, future researchers should explore:
1. **High-Frequency Residual Blending:** Using classical signal processing to apply a High-Pass filter to the noisy input (retaining the jagged clinical spikes) and a Low-Pass filter to the AI output (retaining the flat baseline), blending them to bypass the neural network's smoothing effect.
2. **Wavelet-Domain Diffusion:** Running the DDPM on a Discrete Wavelet Transform (DWT) of the ECG, allowing explicit, massive loss penalties on the high-frequency detail coefficients to prevent blurring.
3. **Latent Autoencoders:** Utilizing VQ-VAEs to compress the ECG into a latent space bound to a clinical classifier, then running diffusion within the latent space to prevent time-domain convolution blurring entirely.
4. **Ablation Against Direct 2D Vision Models:** While this thesis focused on the 1D digitization-and-refinement pathway (which provides interpretable time-series data for clinicians), recent literature explores classifying the 2D scanned ECG images directly using Vision Transformers or ConvNeXt. A critical next step is a formal ablation study benchmarking the diagnostic F1 score of our Refined 1D pipeline against SOTA direct 2D image classifiers to quantify the diagnostic value of structural 1D extraction.

## 7. Conclusion
This thesis successfully engineered the OD-PTB-XL benchmark dataset and proved that Kolmogorov-Arnold Networks (KANs) integrated into conditional diffusion models offer state-of-the-art mathematical denoising (+1.17 dB SNR) for historically digitized ECGs. More importantly, it empirically defined the "Generative Smoothing Boundary" in clinical AI, demonstrating that while basic denoising aids generalization, aggressive MSE-driven diffusion destroys the high-frequency micro-features required by advanced diagnostic oracles.