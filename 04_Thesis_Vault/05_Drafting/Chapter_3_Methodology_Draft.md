# Chapter 3: Methodology (Draft)

## 3.1 Dataset Creation: The 7,601 Paired Signals
The foundation of this research relies on a high-fidelity paired dataset of original 1D ECG signals and their optically digitized counterparts. The logic chain of the dataset formulation is as follows:
1. **Clean Ground Truth:** Raw, mathematically perfect 1D time-series data from the PTB-XL database (PhysioNet 2024 Challenge).
2. **Synthetic Degradation:** The *ECG-Image-Kit* tool was used to plot these signals onto synthetic paper templates, adding grid lines, wrinkles, shading, and OCR text overlaps to simulate real-world scanned records.
3. **Deterministic Extraction (Noisy Condition):** The baseline optical digitizer was run on the generated images to extract a 1D signal. This extraction struggles with grid overlap and fading ink, resulting in a noisy 1D array.
4. **Alignment:** The optically extracted signal was cross-correlated against the clean ground truth to establish perfectly aligned pairs.

This process yielded an unprecedented, perfectly aligned dataset of 7,601 (noisy, clean) paired segments. Crucially, to prevent data leakage, the dataset underwent a strict GroupShuffleSplit based on the `ecg_id`. This guaranteed that all 12 leads from a single patient resided exclusively within the training, validation, or test set.

## 3.2 Diagnosing and Fixing Optical Extraction Failures
Initial baseline extractions yielded extremely poor paired data (Cosine Similarity ~ 0.07), preventing early diffusion models from converging. Four critical bugs in standard extraction pipelines were identified and resolved:
1. **Signal Length Duplication:** The baseline extraction script used a target length of 2500 samples. However, 2.5-second segments at 500 Hz contain exactly 1250 samples. The baseline silently duplicated samples via linear interpolation. Fixing this to `TARGET=1250` eliminated artificial data inflation.
2. **Digitizer Weakness:** Upgrading from a simple color-column sweep to an Ensemble Digitizer (sweep + neural network average) enabled robust extraction across both color and B&W scans.
3. **Data Scarcity:** Scaling the dataset from an initial 120 samples to the final 7,601 pairs prevented the highly parameterized (7.27M) diffusion model from memorizing extraction noise.
4. **The Normalization Mismatch:** Standard extraction independently normalized both clean and noisy signals to [-1, 1], destroying vital amplitude error information. A shared normalization scheme (scaling the noisy signal using the clean signal's range) was enforced during training. However, it was identified that at inference time in the real world, no clean reference is available. Retraining the model with independent normalization closed this train-inference gap.

## 3.3 Core Architecture: Conditional 1D DDPM
The base model is a 1D Conditional Denoising Diffusion Probabilistic Model (cDDPM). Instead of generating an ECG from pure noise, it acts as a post-digitization refinement layer. 

### 3.3.1 Partial Reverse Diffusion
At inference, the model does not run the full 200-step generation process. Instead, it utilizes Partial Reverse Diffusion ($t_{start}=30$). It starts from the optically digitized signal, adds only a small fraction of the noise schedule, and makes targeted corrections. This conservatively limits hallucination and prioritizes structural morphology over pure generation.

### 3.3.2 1D U-Net Backbone
The diffusion process is parameterized by a 7.27M parameter 1D U-Net featuring:
*   **Down-sampling blocks:** 1D Convolutions combined with ResNet-style skip connections.
*   **Sinusoidal Position Embeddings:** Injected at each block for explicit temporal awareness of the timestep $t$.
*   **Up-sampling blocks:** Transposed 1D Convolutions concatenated with the corresponding features from the down-sampling path.
*   **Training Configuration:** Optimized using AdamW, Cosine Annealing LR, Gradient Clipping (Max Norm 1.0), and Automatic Mixed Precision (AMP) to maximize batch throughput on GPU.

## 3.4 Advanced Architectural Upgrades
To push reconstruction beyond the U-Net baseline, two structural modifications are introduced:
1.  **Kolmogorov-Arnold Networks (KAN):** Standard linear and convolutional layers are replaced with KAN layers to provide non-linear adaptive activation functions to handle severe baseline wander introduced by simulated paper skew.
2.  **Discrete Cosine Transform (DCT) Conditioning:** The network condition is augmented with the DCT of the noisy signal to isolate and aggressively target high-frequency pixel "staircase" artifacts.

## 3.5 Task-Aware Clinical Guidance
Standard Mean Squared Error (MSE) loss prioritizes visual smoothness and can inadvertently erase micro-arrhythmias. To guarantee clinical utility, a Task-Aware Loss mechanism is implemented. A robust clinical classifier (a frozen 1D ResNet) evaluates the generated clean signal $x_0$ at every diffusion step. A Binary Cross-Entropy loss against the true PTB-XL labels mathematically penalizes the diffusion model if its artifact removal alters the underlying disease diagnosis.