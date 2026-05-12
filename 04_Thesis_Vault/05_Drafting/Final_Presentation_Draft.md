# Title Slide

**Post-Digitization Refinement of ECG Signals Using Diffusion Models**

Presenter: Mukul Sharma  
Program: MSc Computer Science, 2nd Year  
Roll No: SAU/CS/MSc/2024/08  
Supervisor: Prof. Pranab K. Muhuri  

---

# Background
**The Challenge of Legacy ECGs:**  
*   **The Problem:** Billions of historical ECGs exist only as paper printouts or scanned PDFs.  
*   **The Gap:** Modern AI and Machine Learning diagnostics require clean 1-D time-series arrays, making physical records useless.  
*   **The Solution (Digitization):** Tools like PhysioNet's *ECG-Image-Kit* convert images back into time-series data.  
*   **The Reality:** These tools are deterministic. They leave behind severe artifacts (baseline wander, quantization stairs, unremoved grid lines).  
*   **The Impact:** Poor digitization → Hallucinated morphology → Incorrect clinical diagnosis.

---

# The Baseline Digitization Pipeline
*(Visual: Flowchart showing the ECG-Image-Kit process)*
*   Input: Scanned ECG Image
*   Step 1: Pre-processing (Lead marker detection, grid removal).
*   Step 2: Signal Extraction (Ensemble of Column Sweep and Neural Network).
*   Step 3: Post-processing (Scaling pixels to mV).
*   Output: 12-Lead Time Series (mV).
*   **The Bottleneck:** Even after this full pipeline, the output waveform remains noisy and clinically unreliable.

---

# Problem Statement & Hypothesis
*   **Problem Statement:** Can we restore clinically meaningful ECG morphology from imperfect, optically digitized signals where conventional denoising filters fail?
*   **Hypothesis:** Traditional signal processing (like Butterworth filters) fails because optical noise shares the same frequency band as clinical micro-arrhythmias. We require a learned, Generative AI approach.
*   **The Idea:** Use a Conditional Denoising Diffusion Probabilistic Model (cDDPM) as a targeted post-processing refinement layer.

---

# Recap of Last Semester: The Data Quality Struggle
*   **Phase 1 (Non-DM Filters):** ~0% improvement. Filters could not distinguish noise from signal.
*   **Phase 2 (Poor Real Data):** Trained DM on 120 samples. Cosine similarity was 0.07. Resulted in massive overfitting (+30% training MSE improvement, dropping to +6% over time).
*   **Phase 3 (Improved Pipeline):** Cleaned alignment, cosine jumped to 0.88, but MSE dropped to -2.7%.
*   **Phase 4 (The Synthetic Test):** Trained the exact same DM on perfectly clean synthetic data (Cosine 0.99). Resulted in **+78.8% MSE improvement**.
*   **Central Finding:** The DM architecture was perfect. The bottleneck was entirely the real-world dataset.

---

# Creating the "v2" Benchmark Dataset
*   We identified four hidden bugs in standard extraction pipelines (Signal length duplication, independent normalization hiding amplitude errors, weak color-sweep digitizers, and low sample count).
*   **The Fix:** Generated a massive new dataset directly from the PhysioNet PTB-XL database.
*   **The Result (OD-PTB-XL Dataset):** 
    *   7,601 perfectly aligned (Noisy, Clean) paired signals.
    *   Hard-coded 70/15/15 splits grouped strictly by `ecg_id` to prevent data leakage.
    *   Permanently embedded Clinical Labels (NORM, MI, STTC, CD, HYP) for downstream evaluation.

---

# Model Architecture: KAN-Enhanced DDPM
*   **Baseline:** 1D Conditional U-Net (7.27M parameters).
*   **The SOTA Upgrade (2025):** Replaced standard convolutions with Kolmogorov-Arnold Network (KAN) layers. KAN's adaptive splines are mathematically superior for handling the massive non-linear shifts of ECG baseline wander.
*   **Inference Mechanism:** *Partial Reverse Diffusion* ($t_{start} = 30$). We do not generate from pure noise; we start from the noisy digitized signal and perform only the final 30 denoising steps to prevent the AI from hallucinating healthy heartbeats.

---

# Results: Signal Quality Metrics
*(Visual: Line charts showing SNR/RMSE improvements)*
*   Tested on a strict hold-out set of 1,507 unseen paired samples.
*   **Standard U-Net:** Achieved an ImSNR of **+1.03 dB**.
*   **KAN Architecture:** Achieved an ImSNR of **+1.17 dB**.
*   **Success Rate:** The KAN diffusion model successfully reduced the Root Mean Square Error (RMSE) on **89.0%** of all test patients.
*   **Conclusion:** Mathematically, the model successfully removes optical artifacts and baseline wander better than deterministic baseline methods.

---

# The True Test: Clinical Utility
*   Signal metrics (RMSE/SNR) are not enough for healthcare. The real question is: *Does this generative cleanup actually help an AI diagnose heart disease?*
*   We trained a downstream 1D ResNet diagnostic classifier on the clean ground truth data.
*   **The Baseline Test (Weak Classifier):** 
    *   Noisy Signal F1: 0.164
    *   KAN Refined Signal F1: 0.183
    *   **Result:** A relative improvement of **+11.9%** in diagnostic F1-Score. The core hypothesis is proven.

---

# The Major Discovery: The "Smoothing Problem"
*(Visual: Bar chart comparing Noisy, Refined, and Clean F1 scores for the Strong Oracle)*
*   We upgraded the test using a highly sensitive "Clinical Oracle" (Baseline F1 = 0.844).
*   **The Drop:** When tested on this Oracle, the KAN-Refined signal dropped the accuracy to **0.326** (worse than the raw noisy data at 0.418).
*   **Why?** Generative AI using MSE loss acts as an aggressive smoother. While it perfectly fixes the baseline (making it visually pleasing), it inadvertently erases the high-frequency micro-arrhythmias (e.g., Q-wave notches) that advanced AI relies on for diagnosis.

---

# Contributions to the Field
*   **Dataset:** Created the OD-PTB-XL dataset (7,601 pairs with clinical labels and fixed splits).
*   **Architecture:** Proved that KAN layers outperform standard CNNs for 1D ECG Super-Resolution (+1.17 dB SNR).
*   **Clinical Literature:** Validated the theoretical warning from *TDD (2025)*. Empirically proved that visually/metrically "clean" generative signals do not automatically equal clinically useful signals.

---

# Future Work
How do we solve the clinical smoothing problem and expand the evaluation?
1.  **High-Frequency Residual Blending:** Use signal processing (High/Low pass filters) to bypass the neural network, retaining the exact jagged clinical spikes while utilizing the AI solely for the baseline.
2.  **Wavelet-Domain Diffusion:** Run diffusion on the Discrete Wavelet Transform (DWT), allowing explicit loss penalties on high-frequency "Detail" coefficients.
3.  **Latent Clinical Diffusion:** Use a VQ-VAE to compress the ECG into a latent space tightly bound to a clinical classifier, preventing time-domain blurring.
4.  **2D Vision Ablation Study:** Benchmark our 1D Refinement pipeline against models that classify the 2D scanned images directly (e.g., Vision Transformers/ConvNeXt) to definitively compare "black box" vision classification vs. interpretable 1D extraction.

---

# Conclusion
Generative AI is a highly powerful tool for the rescue of historical ECG data, capable of mathematically restoring optically degraded signals. However, this thesis proves a critical boundary: for safe deployment in advanced diagnostic pipelines, future generative architectures must shift from being merely "noise-aware" to becoming strictly "diagnostic-aware."

---

# References
[1] Ho, J., et al. (2020). Denoising Diffusion Probabilistic Models. *NeurIPS*.
[2] Shivashankara, K., et al. (2024). ECG-Image-Kit: a synthetic image generation toolbox. *Physiological Measurement*.
[3] Li, H., et al. (2023). DeScoD-ECG: Deep Score-Based Diffusion Model for ECG Baseline Wander and Noise Removal. *IEEE JBHI*.
[4] Barkalov, et al. (2025). Reconstructing ECG from indirect signals: a denoising diffusion approach (RhythmDiff). *RSPTA*.
