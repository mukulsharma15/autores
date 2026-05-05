# Literature Review: Extending ECG-Image-Kit with Conditional Diffusion Models

## 1. Context and Problem Statement
The digitization of legacy paper electrocardiograms (ECGs) is a critical step in bridging historical cardiovascular data with modern machine learning analytics. **ECG-Image-Kit** ([Shivashankara et al., 2024](https://arxiv.org/abs/2307.01946)) provides a pipeline to generate synthetic, realistic paper ECG images from 1D time-series data to train digitization models. 

Currently, the default digitization pipeline in ECG-Image-Kit relies on a combination of Optical Character Recognition (OCR), a standard Denoising CNN (DnCNN) for grid removal, and 1D heuristic extraction (e.g., minimum column-wise intensity and Connected Component Analysis). While effective, these deterministic and basic deep-learning methods often introduce **algorithmic extraction artifacts**—specifically "staircase" effects due to pixel quantization and "spike" noises when text or grid residuals are misinterpreted as signal peaks. 

Generative models, specifically **Diffusion Models**, have recently emerged as the state-of-the-art for signal denoising and imputation, offering a probabilistic way to map noisy or artifact-corrupted signals back to the true data distribution. Applying conditional diffusion to the outputs of ECG-Image-Kit represents a highly novel approach to solving digitization artifacts.

---

## 2. State of the Art: Paper ECG Digitization vs. Generative Models

Recent literature (2023–2025) highlights a massive intersection between solving the messy optical digitization problem and the rise of Deep Generative Models. 

### 2.1 The Bottleneck of Optical Extraction
*   **PTB-IMAGE & VinDigitizer (Nguyen et al., Feb 2025)** - *A Scanned Paper ECG Dataset for Digitization* ([arXiv:2502.14909](https://arxiv.org/abs/2502.14909))
    *   **Insight:** The authors printed and scanned the PTB dataset to create a real-world digitization benchmark. They note that standard heuristic waveform extraction achieves a mean Signal-to-Noise Ratio (SNR) of only ~0.01 dB. This vividly illustrates the exact problem your thesis aims to solve: scanning and optical digitization introduce massive distortions (grid overlap, fading) that ruin the 1D signal.
*   **SLPM: Lightweight Deep Learning for Paper ECG Digitization (2024)** ([10.1088/1361-6579/ae3fe5](https://doi.org/10.1088/1361-6579/ae3fe5))
    *   **Insight:** Highlights the ongoing struggle to build end-to-end models that bypass heuristic 1D extraction entirely, proving the immense demand for better post-digitization signal refinement.

### 2.2 Deep Generative Models as the Solution
*   **Deep Generative Models: The winning key for large and easily accessible ECG datasets? (2023)** ([10.1016/j.compbiomed.2023.107655](https://doi.org/10.1016/j.compbiomed.2023.107655)) & **Synthetic ECG signals generation: A scoping review (2024)** ([10.1016/j.compbiomed.2024.109453](https://doi.org/10.1016/j.compbiomed.2024.109453))
    *   **Insight:** These scoping reviews map the explosion of Generative Adversarial Networks (GANs), Variational Autoencoders (VAEs), and newly, Diffusion Models for ECG data. They conclude that generative modeling is essential not just for faking data, but for translating corrupted records (like digitized paper artifacts) back into clinically viable signal manifolds.

### 2.3 Foundational 1D ECG Diffusion Architectures
*   **DeScoD-ECG (Li et al., Sept 2024)** - *Deep Score-Based Diffusion Model for ECG Baseline Wander and Noise Removal* ([arXiv:2208.00542](https://arxiv.org/abs/2208.00542))
    *   **Contribution:** One of the first studies to deploy a conditional score-based diffusion model specifically for ECG denoising. Proves that conditional diffusion can handle extreme noise significantly better than previous autoencoders. 
*   **TFCDiff (Li et al., Nov 2025)** - *Robust ECG Denoising via Time-Frequency Complementary Diffusion* ([arXiv:2511.16627](https://arxiv.org/abs/2511.16627))
    *   **Contribution:** Operates entirely in the Discrete Cosine Transform (DCT) domain. Scanned paper artifacts (spikes and staircasing) manifest heavily in the high-frequency spectrum, making frequency-domain diffusion perfect for targeting digitization quantization noise.

### 2.4 Expanding Architectures: State Space Models & Super-Resolution Context
*   **MSECG: Incorporating Mamba for Robust and Efficient ECG Super-Resolution (Dec 2024)** ([arXiv:2412.04861](https://arxiv.org/abs/2412.04861))
    *   **Insight:** Digitizer extraction essentially creates a down-sampled, quantized ("staircase") version of the original signal. Therefore, fixing these algorithmic artifacts is mathematically identical to a **Super-Resolution (SR)** inverse problem. The MSECG paper introduces Mamba (Selective State Space Models) specifically for reconstructing high-frequency fidelity from low-resolution ECGs.

---

## 3. Extending ECG-Image-Kit with Diffusion Models

Based on the literature, **1D Post-Digitization Refinement** directly targets the core novelty of the thesis.

The standard ECG-Image-Kit pipeline is run, producing a 1D signal $\tilde{x}$ that contains "staircase" quantization and "spike" artifacts (as verified by the poor SNR in the PTB-IMAGE paper). A **1D Conditional DDPM (cDDPM)** is then trained:
*   **Forward Process:** Diffuses the *clean* ground truth ECG time-series $x_0$ into Gaussian noise $x_T$.
*   **Reverse Process:** Learns a denoising function $\epsilon_\theta(x_t, t, \tilde{x})$, where the noisy, artifact-ridden 1D signal $\tilde{x}$ extracted by the optical digitizer is used as the **condition**.
*   *Pros:* Capable of smoothing staircase artifacts (restoring the continuous nature of the biological signal) and imputing gaps left by OCR text removal. Mathematically, it treats optical digitization artifacts as a Super-Resolution/Denoising hybrid problem.

---

## 4. Proposed Autoresearch Optimization Target

To turn this literature into a measurable, iterative code loop (`pi-autoresearch`), we define the following framework:

*   **Baseline Codebase:** A Python script that utilizes `ECG-Image-Kit` (or the new `PTB-IMAGE` dataset) to generate a noisy 1D extraction, paired with the ground-truth 1D signal.
*   **Model:** A PyTorch-based 1D cDDPM.
*   **Optimization Target (Metric):** 
    *   **$SNR_{med}$ (Median Signal-to-Noise Ratio):** As proposed in the ECG-Image-Kit paper, standard SNR is highly sensitive to spikes. $SNR_{med}$ uses median noise power and is a better evaluator for spike-noise removal. (Higher is better).
    *   **Clinical Parameter Error (MSE of QRS width & QT interval):** Ensuring the biological features aren't smoothed out by the diffusion process.
*   **Benchmark Command:** `python train_and_evaluate_cddpm.py` (which will run a fast 1-epoch training/inference cycle on a subset of the dataset).

## 5. Next Steps
1.  **Repository Setup:** Write a minimal scaffold for the 1D cDDPM.
2.  **Dataset Generation:** Use `ECG-Image-Kit` (or extract from the PTB-Image dataset) to generate a paired dataset: `[Ground Truth 1D, Image-Kit Extracted Noisy 1D]`.
3.  **Initiate Autoresearch:** Begin the iterative loop focusing on tuning the diffusion noise schedule, architecture (e.g., U-Net vs Mamba), and conditioning injection method.