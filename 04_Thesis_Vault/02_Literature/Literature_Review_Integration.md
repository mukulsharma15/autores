# 02_Literature/Literature_Review_Integration.md

## How to integrate the Literature Review

*This document summarizes the current State-of-the-Art in ECG Diffusion Models and how to compare your work against them.*

### Key Papers
1. **DeScoD-ECG (Li et al., 2024)**
   * **Focus:** Deep Score-Based Diffusion for ECG Denoising (Hospital noise, muscle wander).
   * **Result:** Achieved a PRD of ~40% and a Cosine Similarity of 0.92.
   * **How you compare:** "We extend this generative paradigm to the domain of optical digitization. Our conditional architecture achieves a superior morphological preservation with a Cosine Similarity of 0.9724."

2. **ECG-Image-Kit (Shivashankara et al., 2024)**
   * **Focus:** Deterministic computer vision extraction.
   * **Result:** Achieved standard SNR of 11.88 dB and $SNR_{med}$ of 26.54 dB on *synthetic*, perfectly printed images.
   * **How you compare:** "While Shivashankara et al. achieved a Median SNR of 26.54 dB strictly on synthetic images, our post-digitization refinement model achieves a highly competitive 26.98 dB on heavily distorted, real-world scanned records."

3. **PTB-IMAGE / VinDigitizer (Nguyen et al., 2025)**
   * **Focus:** Advanced AI-driven digitizers for real scanned paper.
   * **Result:** Reported an average SNR of ~0.01 dB when running baseline deterministic optical extraction on scanned PTB papers, using the KS Statistic to measure distribution drift.
   * **How you compare:** "Recent benchmarks demonstrate that standard optical extraction algorithms fail to reconstruct clean biological signals. Our Super-Resolution Diffusion pipeline bypasses this bottleneck, correcting the statistical drift introduced by optical quantization with an improved KS Statistic of 0.0822."
