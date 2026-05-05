# A Comprehensive Review of Deep Learning Approaches for ECG Digitization, Denoising, and Classification

**Date:** May 2026
**Prepared for:** Master's Thesis Chapter 2 (Literature Review)

---

## Abstract
The transition from legacy paper-based electrocardiograms (ECGs) to structured 1D time-series data is a critical bottleneck in modern cardiovascular machine learning. This review synthesizes 45 recent studies (2024–2026), primarily driven by the George B. Moody PhysioNet Challenge 2024, to evaluate the state-of-the-art in ECG image digitization, physiological denoising, and downstream classification. We critically examine the shift from traditional image processing to deep learning pipelines (YOLO, U-Net, ConvNeXt), the heavy reliance on synthetic dataset generation (ECG-Image-Kit, SynthECG), and the emerging paradigm of Deep Score-Based Diffusion Models (KAN-DeScoD, TFCDiff, TDD). A comparative analysis of architectures and evaluation metrics reveals a significant research gap: while diffusion models have achieved state-of-the-art results in physiological denoising, current optical digitization pipelines still struggle with severe pixel-quantization artifacts, necessitating a generative refinement bridge.

---

## 1. Introduction
Despite the ubiquity of digital ECG technologies, millions of clinical ECGs remain locked in non-computable formats such as scanned PDFs, thermal paper printouts, and smartphone photographs. The George B. Moody PhysioNet Challenge 2024 catalyzed a massive influx of research aimed at converting these images back into 1D time-series data (digitization) and diagnosing them (classification) (Reyna et al., 2024). However, as literature from 2024 to 2026 indicates, optical extraction is inherently lossy, introducing high-frequency spikes, staircase quantization, and baseline wander that critically destabilize downstream automated analysis.

## 2. Dataset Paradigms: The Synthetic vs. Real-World Divide
A foundational challenge in ECG image processing is the lack of large-scale, perfectly aligned image-to-signal pairs for supervised learning. 

**Synthetic Generation Frameworks:** To bypass this, researchers have heavily relied on synthetic augmentation. *ECG-Image-Kit* (Shivashankara et al., 2024) became the gold standard by taking clean time-series data from the PTB-XL dataset and artificially projecting it onto standard ECG grids, adding simulated wrinkles, shadows, and handwritten artifacts. Recently, Rahimi et al. (2026) introduced *SynthECG*, a Python framework that generated up to 261,588 synthetic single-lead segmentations, uniquely simulating overlapping waveforms from adjacent leads.

**The Domain Shift Problem:** While synthetic datasets enable the training of deep learning segmenters, they introduce a severe domain shift. Models trained purely on synthetic data (such as the *ECG-Image-Kit* variants) experience catastrophic performance drops when evaluated on real-world hidden test sets containing genuine scanner ink degradation and true optical artifacts. This underscores the urgent need for datasets built from real-world paired extractions rather than synthetic projections.

## 3. State-of-the-Art in Optical Digitization Architectures
The digitization literature presents a clear architectural consensus, generally dividing the task into two phases: Region of Interest (ROI) detection and Waveform Extraction.

**3.1. Lead Detection (ROI):** 
Object detection networks completely dominate this space. *TimeBeater* (Shen et al., 2024) utilized YOLOv10, while *VinDigitizer* (Nguyen et al., 2024) deployed a single-shot YOLOv8 detector to capture 12-lead snapshots. Alternative approaches include DETR models with ResNet-50 backbones, as seen in the *Revenger* framework (Kang et al., 2024).

**3.2. Waveform Extraction:**
For extracting the 1D signal from the cropped ROI, two distinct schools of thought emerged:
*   **Hybrid Image Processing:** *VinDigitizer* achieved competitive baseline results using Otsu’s binarization, Hough transforms for grid removal, and Viterbi’s algorithm for sampling. However, these deterministic methods struggle heavily with grid-signal overlap.
*   **Deep Semantic Segmentation:** U-Net architectures are the definitive state-of-the-art for waveform extraction. Frameworks like *WAVIE* (Verlyck et al., 2024) and the *PKU NIHDS* submission (Liang et al., 2024) utilized U-Nets to isolate the signal trace from the background. *ECGFusion* utilized DPLinkNet34 for image binarization.

**3.3. Digitization Performance Bottleneck:**
Despite these advanced architectures, the reconstruction fidelity on real-world hidden data remains remarkably poor. *WAVIE* achieved a Signal-to-Noise Ratio (SNR) of only 5.469 dB (ranking 3rd), while others like *VinDigitizer* and *PKU NIHDS* scored negative SNRs (-0.066 dB and -1.103 dB, respectively). This proves that 2D-to-1D optical extraction fundamentally leaves behind residual noise that cannot be solved by segmentation alone.

## 4. Generative AI and Diffusion Models in ECG Processing
To address complex noise that evades standard filters, the 2025–2026 literature shifted toward Deep Score-Based Diffusion Models (DMs). However, their application has been strictly segregated from optical digitization.

**4.1. Diffusion for Image Augmentation:**
In the digitization space, DMs have only been used as 2D image generators. Liang et al. (2024) utilized DMs solely for data augmentation, generating synthetic multi-layout ECG images to increase the robustness of their U-Net digitizer, rather than using diffusion to refine the 1D signal itself.

**4.2. 1D Diffusion for Physiological Denoising:**
In the 1D time-series domain, DMs have established a new state-of-the-art for *physiological* denoising (removing muscle artifact, baseline wander, and electrode motion). 
*   **Architecture Innovations:** Shu et al. (2026) introduced *KAN-DeScoD*, demonstrating that standard linear transformations in U-Nets lack the flexibility to fit morphologically variable QRS complexes. They integrated Kolmogorov–Arnold Network (KAN) layers into the diffusion backbone to vastly improve high-noise robustness. 
*   **Frequency-Domain Diffusion:** Li et al. (2025) proposed *TFCDiff*, arguing that time-domain diffusion is suboptimal. They operate in the Discrete Cosine Transform (DCT) domain, using DCT coefficients as conditioning input to effectively separate overlapping noise frequencies from the biological signal.
*   **Task-Aware Optimization:** Fang et al. (2025) introduced *TDD (Task-Aware Diffusion Dual-Matching)*, revealing a critical flaw in standard L1/L2 diffusion loss functions: they prioritize visual smoothness over structural clinical accuracy. *TDD* integrates downstream classification gradients into the reverse diffusion trajectory, ensuring the denoised signal preserves pathological indicators.

## 5. Downstream Classification and Clinical Utility
The ultimate metric for digitization is whether the extracted signal can be correctly diagnosed by an algorithm. 

**Architectures:** For image-based and digitized signal classification, the literature relies heavily on highly parameterized CNNs pre-trained on massive datasets (e.g., PTB-XL, CODE15). *AIMED* (Dias et al., 2024) secured 1st place using a pre-trained **ConvNeXt** architecture. *ECGFusion* utilized **GoogLeNet**, and *DSAIL* (Gitau et al., 2024) fine-tuned **InceptionV3**. 

**Evaluation Metrics:** The literature uniformly rejects simple "Accuracy" due to the extreme class imbalance in cardiac datasets (e.g., normal sinus rhythm vastly outnumbering rare arrhythmias). The gold standard metrics across all 2024–2026 studies are:
1.  **Macro F-measure (F1-Score):** Evaluates precision and recall across all classes equally.
2.  **SNR and SNR_med:** For reconstruction fidelity.
3.  **Cosine Similarity & Pearson Correlation:** Mentioned in recent frameworks (like *SynthECG*) to prove morphological shape preservation, which is clinically more critical than absolute point-wise distance.

## 6. Conclusion and Identification of the Research Gap
The literature from 2024 to 2026 establishes two clear, disjointed facts. First, deterministic optical digitizers (YOLO + U-Net) successfully extract ECGs but leave behind severe pixel-quantization artifacts, resulting in SNR scores near or below 0 dB on real scans. Second, 1D Conditional Diffusion Models (enhanced by KAN layers and DCT features) are the premier technology for denoising complex physiological signals. 

A critical research gap exists at the intersection of these two domains. No current literature employs 1D Conditional Diffusion as a *post-digitization refinement layer* to correct the algorithmic errors of optical extraction. Bridging this gap by mapping flawed deterministic extractions back to the natural biological manifold using score-based generative priors represents a highly novel and necessary contribution to the field of cardiovascular informatics.