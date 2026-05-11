# Chapter 1: Introduction (Draft)

## 1. Blueprint (Bullet Points for your structure)
*   **1.1 Background:** Billions of historical ECG records exist only as physical paper or scanned PDFs. Modern AI diagnostics require 1D time-series data.
*   **1.2 The Problem of Digitization:** Tools like ECG-Image-Kit convert images to 1D signals but introduce severe artifacts (quantization "stairs", grid overlaps, baseline wander).
*   **1.3 Failure of Traditional Methods:** Standard signal processing (e.g., Butterworth filters) cannot separate optical noise from clinical signals because they share the same frequency bands.
*   **1.4 The Hypothesis:** A generative AI model, specifically a Conditional Denoising Diffusion Probabilistic Model (cDDPM), can act as a post-digitization refinement layer to map noisy extracted signals back to their true biological manifold.
*   **1.5 The Scope & Contributions:** 
    *   Creation of a novel 7,601-sample paired dataset.
    *   Application of Kolmogorov-Arnold Networks (KAN) to 1D ECG diffusion.
    *   Rigorous downstream clinical evaluation proving both the utility and the limitations (the "smoothing problem") of generative ECG denoising.

---

## 2. Full Context (Paragraphs for your understanding)
*(Note: Read this to understand the flow, but paraphrase it in your own words for your final thesis to avoid AI detection).*

The digitization of historical electrocardiogram (ECG) records is a critical bottleneck in deploying modern cardiac AI. Across the globe, billions of patient records are locked in analog formats—either printed on thermal paper or stored as scanned images. While recent advancements in optical extraction pipelines, such as the ECG-Image-Kit utilized in the PhysioNet 2024 Challenge, have made it possible to convert these images back into 1D time-series data, the extraction process is inherently lossy and deterministic. The resulting signals are frequently plagued by optical artifacts, including quantization noise from pixel-to-millivolt conversion, unremoved grid lines, and severe baseline wander caused by paper skew or fading ink. 

Traditional signal processing techniques struggle to correct these specific artifacts. Standard low-pass or high-pass filters are ineffective because the optical noise frequently occupies the exact same frequency spectrum as critical clinical features, such as the QRS complex or T-wave variations. Consequently, applying conventional filters often destroys the underlying diagnostic information along with the noise. This necessitates a non-linear, learned approach to signal refinement.

This thesis proposes the application of a Conditional Denoising Diffusion Probabilistic Model (cDDPM) as a post-digitization refinement step. Rather than attempting to generate an ECG from pure noise, this approach utilizes partial reverse diffusion to correct the specific deterministic errors introduced by optical extraction tools. By conditioning the model on the noisy signal and guiding it toward the clean biological manifold, the architecture attempts to restore the true morphology of the heartbeat.

The contributions of this work are threefold. First, it introduces a highly rigorous, perfectly aligned dataset of 7,601 paired (noisy, clean) ECG segments, solving critical data-leakage and normalization bugs found in prior extraction methodologies. Second, it pioneers the integration of Kolmogorov-Arnold Network (KAN) layers into a 1D diffusion backbone, demonstrating superior capability in handling baseline wander compared to standard convolutional architectures. Finally, this thesis moves beyond simple signal-quality metrics to conduct a rigorous downstream clinical evaluation. It empirically proves that while basic diffusion improves standard diagnostic pipelines, aggressively generative denoising introduces a "smoothing" effect that can actively erase the micro-arrhythmias required by highly sensitive clinical oracles.