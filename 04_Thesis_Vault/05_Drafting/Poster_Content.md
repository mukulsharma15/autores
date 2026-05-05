# Research Poster Content

**Title:** Clinically-Guided Post-Digitization Refinement of ECGs using Conditional Diffusion Models
**Author:** Mukul Sharma, South Asian University

---

## 1. The Post-Digitization Bottleneck
*   **Problem:** Optical digitizers successfully isolate ECG traces from paper but leave catastrophic pixel quantization ("staircase") and high-frequency spike artifacts. 
*   **Hypothesis:** A 1D Conditional Diffusion Probabilistic Model (cDDPM) can bridge this gap by acting as a post-extraction super-resolution layer.

## 2. Uncovering Extraction Failures & The 7,601 Dataset
*   We identified and fixed four critical flaws in baseline extractors: sample duplication (target=1250 vs 2500), weak color-sweep heuristics, data scarcity, and a fundamental train/inference normalization mismatch.
*   **Dataset:** By cross-correlating the fixed extractions, we generated a novel, perfectly aligned dataset of **7,601 (noisy, clean) paired segments**.
*   **Strict Split:** A rigid `ecg_id` GroupShuffleSplit ensured zero patient-level data leakage between train and test sets.

## 3. Methodology: Partial Reverse Diffusion
*   **Base Model:** 1D cDDPM utilizing a 7.27M parameter U-Net backbone.
*   **Mechanism:** Rather than full generation, we employ **Partial Reverse Diffusion ($t_{start}=30$)**. The model injects minimal noise into the digitized signal and denoises it, refining artifacts while mathematically restricting biological hallucination.
*   **Visual:** Architecture diagram of the 1D cDDPM showing the conditional input and the $t=30$ injection.

## 4. Signal Reconstruction Results
Evaluated on an unseen test set of 1,507 patient samples:
*   **+1.03 dB ImSNR** (Improved Signal-to-Noise Ratio).
*   **9.47% Reduction in RMSE.**
*   **5.15% Improvement in KS_Stat**, proving the generated signal matches the continuous biological distribution far better than the quantized digitizer output.
*   **Visual Evidence:** A high-quality 4-panel figure showing Original vs. Refined overlay, Zoomed QRS (fixing the staircase), Absolute Error, and Power Spectral Density.

## 5. Architectural Upgrades: KAN & DCT
*   To further push the reconstruction envelope, two upgrades were implemented:
    *   **Kolmogorov-Arnold Networks (KAN):** Replaced static U-Net bottlenecks with adaptive KAN layers to mathematically model non-linear baseline wander.
    *   **Discrete Cosine Transform (DCT):** Passed the DCT magnitude to the network to explicitly isolate high-frequency optical spikes.

## 6. The Task-Aware Clinical Oracle
*   **The Warning:** Standard Mean Squared Error (MSE) loss smooths over clinical micro-arrhythmias, endangering downstream AI diagnostic performance despite visual improvements.
*   **The Solution:** A robust 1D ResNet clinical oracle evaluates the diffusion output $x_0$ at every step. A Task-Aware binary cross-entropy loss heavily penalizes the diffusion model if the refined signal alters the clinical PTB-XL diagnosis.

## 7. Conclusion
*   Deterministic optical extraction is insufficient for clinical AI. Conditional Diffusion Models successfully bridge this gap, but architectural upgrades and Task-Aware clinical guidance are mandatory to preserve diagnostic integrity.