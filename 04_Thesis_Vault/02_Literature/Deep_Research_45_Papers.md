# Deep Research: SOTA Literature Review (45-Paper Expansion)
**Date:** April 2026

## 1. Architectural Upgrades for 1D Diffusion (The "What we can steal" section)

I have analyzed the new 2025/2026 Diffusion papers in your `ECG-image-DM-45.csv` file. Your current architecture is a highly effective Conditional 1D DDPM with a U-Net backbone. However, the newest literature offers three specific architectural upgrades that we can test to push your ImSNR beyond +1.76 dB.

### A. The "KAN" (Kolmogorov-Arnold Network) Upgrade
**Paper:** *KAN-DeScoD: Kolmogorov–Arnold Network Enhanced Deep Score-Based Diffusion Model for ECG Denoising (Shu et al., 2026)*
*   **The Finding:** Standard U-Nets use linear transformations (Conv1D and Linear layers). Shu et al. proved that linear layers struggle to fit non-stationary noise (like baseline wander) and morphologically variable features (like QRS complexes). They replaced the linear layers in their score-based diffusion model with **KAN layers**.
*   **How we use this:** We can swap the standard `nn.Linear(time_emb_dim, out_channels)` and `nn.Conv1d` blocks in your U-Net's `Block1D` for `KAN` layers. This theoretically improves robustness to the severe baseline wander introduced by poorly scanned ECGs.

### B. The "DCT" (Discrete Cosine Transform) Frequency Domain Trick
**Paper:** *TFCDiff: Robust ECG Denoising via Time-Frequency Complementary Diffusion (Li et al., 2025)*
*   **The Finding:** Instead of feeding raw time-series arrays to the Diffusion Model, Li et al. convert the noisy signal into the **Discrete Cosine Transform (DCT) domain** and use the DCT coefficients as the conditional input. 
*   **How we use this:** Optical extraction artifacts (staircasing) are fundamentally *high-frequency noise*. By passing the DCT coefficients of `noisynew2.npy` as the `cond` tensor to your U-Net, the model will explicitly see which frequencies are biological and which are scanner artifacts. 

### C. The "Task-Aware" Loss Function
**Paper:** *TDD: Task-Aware Diffusion Dual-Matching for Robust Electrocardiogram Denoising (2025)*
*   **The Finding:** The authors point out a massive flaw in current denoising models: optimizing purely for L1/L2 Loss (which you are currently doing) does not guarantee that the *diagnostic* features of the ECG are preserved. They propose a "Task-Aware Dual-Matching" loss that penalizes the model if downstream classification or segmentation tasks fail.
*   **How we use this:** Since your ultimate goal is the Downstream Clinical Utility experiment (improving Macro F1 scores), we can inject a pre-trained ECG classifier directly into your training loop. Your loss function would become: `Loss = L1(noise_pred, noise_true) + $\lambda$ * CrossEntropy(Classifier(Clean), Classifier(Denoised))`. This forces the diffusion model to preserve the disease labels while removing the noise.

---

## 2. Incorporating the 45 Papers into your Lit Review Draft

Here is how you should structure your expanded Literature Review in Chapter 2, citing the massive 45-paper library you uploaded:

### Section 2.1: The Limits of Deterministic Digitization
*"The rapid digitization of legacy paper ECGs has been driven by the introduction of open-source toolkits such as ECG-Image-Kit (Shivashankara et al., 2024) and the George B. Moody PhysioNet Challenge 2024 (Reyna et al., 2024). While state-of-the-art approaches utilizing YOLO object detection and U-Net segmentation (Verlyck et al., 2024; Nguyen et al., 2024) successfully isolate lead traces, they fundamentally fail to extract clean biological signals from real-world scans. As demonstrated by the top submissions to the PhysioNet 2024 challenge, deterministic pipelines struggle to achieve Signal-to-Noise Ratios (SNR) above 5 dB on degraded physical printouts, introducing severe pixel-quantization artifacts and baseline wander."*

### Section 2.2: Generative AI for Physiological Denoising
*"To address complex noise in electrocardiograms, recent literature has shifted toward Deep Generative Models. Score-based diffusion models, such as DeScoD-ECG (Li et al., 2024), demonstrated the viability of reverse diffusion for mitigating muscle artifacts and hospital noise. Subsequent advancements in 2025 and 2026 have refined this approach. For instance, TFCDiff (Li et al., 2025) introduced Time-Frequency Complementary Diffusion in the DCT domain to isolate non-stationary noise, while KAN-DeScoD (Shu et al., 2026) integrated Kolmogorov-Arnold Networks to better model morphologically variable QRS complexes."*

### Section 2.3: The Gap: Optical Super-Resolution
*"However, the current literature exhibits a critical gap. The 2024 computer vision literature (Liang et al., 2024) utilizes diffusion exclusively for 2D image augmentation to train OCR systems. Conversely, the 2025–2026 generative literature (Shu et al.; Li et al.) utilizes 1D diffusion exclusively for physiological patient-level denoising. To date, no literature has bridged these domains by deploying 1D Conditional Diffusion Models as a post-digitization refinement layer to explicitly target and resolve algorithmic optical extraction errors. Furthermore, this limits the downstream clinical utility of digitized ECGs, as standard classifiers—such as the ConvNeXt (Dias et al., 2024) and InceptionV3 (Gitau et al., 2024) architectures popularized in recent challenges—suffer severe performance degradation when analyzing signals corrupted by optical artifacts."*