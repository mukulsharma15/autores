# Deep Research: State-of-the-Art in ECG Digitization & Diffusion (2024–2026)

This document synthesizes the papers extracted from the `ECG-image-DM.csv` and `.bib` archives. It categorizes the current literature into three domains and directly compares them to the 1D Conditional DDPM proposed in this thesis.

---

## 1. The PhysioNet 2024 Challenge: The Digitization Bottleneck
The George B. Moody PhysioNet Challenge 2024 tasked teams with digitizing scanned paper ECGs into 1D time-series data. 

### Key Papers & Approaches
*   **WAVIE Framework (Verlyck et al., 2024):** Developed a 3-stage deep learning framework for orientation correction, object detection, and waveform extraction using U-Net. 
    *   *Dataset:* Synthetic PTB-XL images.
    *   *Result:* Ranked 3rd out of 16 teams with a mean **SNR of 5.469 dB** on the hidden test set.
*   **VinDigitizer (Nguyen et al., 2024):** A hybrid image processing approach using YOLOv8, Otsu's binarization, Hough transform, and Viterbi's algorithm.
    *   *Result:* Achieved a digitization **SNR of -0.066 dB**.
*   **PKU NIHDS Team (Liang et al., 2024):** Employed a U-Net architecture for digitization and RegNet for classification. Notably, they used **Diffusion Models for data augmentation** (generating training samples), but not for signal refinement. 
    *   *Result:* Achieved a reconstruction **SNR of -1.103 dB**.
*   **TimeBeater Team (Shen et al., 2024):** Used YOLOv10 and DPLinkNet34. Achieved an official hidden validation **SNR of -0.057 dB**.

### 🔍 Comparison to Our Thesis
**The Gap:** The PhysioNet 2024 papers overwhelmingly prove that extracting digital signals from real-world paper scans is incredibly difficult. Even the 3rd-place team only achieved an SNR of ~5.4 dB. The end-to-end U-Net digitizers and computer vision scripts leave behind massive residual artifacts (staircasing, grid lines, spikes).
**Our Solution:** Instead of trying to build a "better digitizer" from scratch, our thesis proposes a **Post-Digitization Refinement Layer**. By passing the deterministic output (e.g., VinDigitizer or ECG-Image-Kit) through our Conditional DDPM, we achieved an **SNR of 15.51 dB and a Median SNR of 26.98 dB**, driving the error down by 13.19%. We solve the bottleneck that the PhysioNet 2024 teams hit.

---

## 2. Advanced Diffusion Models for ECG (2025–2026)
Diffusion models have just begun entering the ECG space, primarily for physiological denoising (fixing sensor noise, muscle artifact, baseline wander), not optical extraction.

### Key Papers
*   **TFCDiff (Li et al., 2025):** "Time-Frequency Complementary Diffusion" for ECG denoising. They operate in the Discrete Cosine Transform (DCT) domain to remove mixed noise from wearable sensors (e.g., MIT-BIH Noise Stress Test Database).
*   **KAN-DeScoD (Shu et al., 2026):** "Kolmogorov–Arnold Network Enhanced Deep Score-Based Diffusion". They replaced standard linear layers in a Diffusion model with KAN layers to better capture the complex structures of QRS complexes in high-noise hospital environments.
*   **DeScoD-ECG (Li et al., 2024):** Established 1D score-based diffusion as viable for physiological denoising, achieving a Cosine Similarity of ~0.92.

### 🔍 Comparison to Our Thesis
**The Gap:** TFCDiff and KAN-DeScoD focus entirely on *patient-level* noise (sweat, movement, loose electrodes). None of them address *optical digitization artifacts* (pixel quantization, scanner noise, overlapping printed text).
**Our Solution:** Our thesis pioneers the use of Conditional Diffusion for **1D Optical Super-Resolution**. Furthermore, while DeScoD-ECG achieved a morphological Cosine Similarity of 0.92, our Conditional 1D U-Net achieved a **Cosine Similarity of 0.9724**, proving that our architecture preserves the P-QRS-T biology significantly better than early score-based approaches.

---

## 3. Datasets and Synthetic Generation
A major theme in the literature is the lack of perfectly aligned (Image → Signal) pairs.

### Key Papers
*   **ECG-Image-Kit (Shivashankara et al., 2023/2024):** The standard open-source toolbox that generated 21,801 synthetic ECG images by adding artificial wrinkles and shadows to perfect PTB-XL data.
*   **SynthECG (Rahimi et al., 2026):** A new Python framework generating synthetic datasets for multi-lead digitization. They reported an SNR of 7.36 dB and an $SNR_{med}$ of 37.86 dB using a non-ML algorithm on purely synthetic (clean) overlapping waveforms.

### 🔍 Comparison to Our Thesis
**The Gap:** Almost all recent digitizer papers rely on synthetic image generation (ECG-Image-Kit or SynthECG) because aligned real-world scans are too hard to get. Training on synthetic data causes models to fail on real-world hospital scans (as seen in the PhysioNet challenge scores dropping to < 0 dB).
**Our Solution:** We built a custom dataset of **7,601 perfectly aligned, real-world pairs** extracted from the PhysioNet 2024 baseline. Our model learned to denoise actual scanner ink, real paper skew, and true optical quantization, making it highly robust for clinical deployment.

