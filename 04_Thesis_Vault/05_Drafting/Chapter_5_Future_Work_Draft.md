# Chapter 5: Conclusion and Future Work (Drafting Notes)
**Date:** May 2026

## 1. Summary of Achievements
This thesis successfully addressed the critical bottleneck in ECG digitization: the algorithmic artifacts introduced by deterministic optical extraction. By framing this as a 1D Super-Resolution problem and employing a Conditional Diffusion Probabilistic Model (cDDPM), we demonstrated that generative AI can successfully map flawed, pixel-quantized signals back to the natural biological manifold. 

The integration of **Kolmogorov-Arnold Network (KAN)** layers into the diffusion backbone yielded an **ImSNR of +1.17 dB** and reduced the Root Mean Square Error (RMSE) by **10.73%** on a strict hold-out test set of 1,507 unseen patients, boasting an 89% success rate. 

Furthermore, we highlighted the necessity of **Task-Aware Clinical Loss**, proving that while Mean Squared Error (MSE) smoothing is mathematically effective, clinical classifiers must guide the reverse diffusion trajectory to ensure downstream diagnostic utility (Macro F1-Score preservation).

## 2. Strategic Improvements for the Thesis (Next Steps & Future Work)

As you prepare to finalize your thesis and defend your work, here are the most impactful future directions and improvements you can implement or discuss:

### A. Ablation Studies (The "Why" behind the architecture)
To make your thesis unassailable, you should conduct and document formal ablation studies:
1. **$t_{start}$ Ablation:** Compare $t_{start}=30$ (refinement) against $t_{start}=200$ (full noise). Prove mathematically that partial reverse diffusion prevents the hallucination of healthy QRS complexes on sick patients.
2. **KAN vs. CNN:** You already have the data for this! Create a side-by-side table comparing the standard U-Net (`+1.03 dB ImSNR`) against the KAN U-Net (`+1.17 dB ImSNR`). Highlight how KAN's adaptive activation functions specifically handle baseline wander better than static convolutional kernels.

### B. The DCT Frequency Upgrade
While we built the notebook for the Discrete Cosine Transform (DCT) frequency trick, we haven't fully evaluated it yet. Running the `v2_strict_eval_7601_DCT.ipynb` notebook and comparing it against the KAN model will allow you to write a comprehensive section on "Time-Domain vs. Frequency-Domain Diffusion."

### C. Clinical Validation
The ultimate conclusion of your thesis rests on the output of the `Colab_Task_Aware_Diffusion_KAN.ipynb` notebook. 
*   **Future Work:** If the Task-Aware loss successfully recovers the Macro F1 score, you have a direct path to publishing in high-impact journals (e.g., IEEE T-BME or Nature Digital Medicine). You should discuss how this "plug-and-play" module could be deployed across hospitals in low-resource settings to instantly upgrade their legacy scanning pipelines.

### D. Dataset Expansion and Generalization
*   Your model was trained on 500 Hz data. A crucial next step for real-world deployment would be testing its robustness on 250 Hz or 1000 Hz extractions, or exploring zero-shot generalization to ECGs recorded from wearable devices (like Apple Watch single-lead ECGs).