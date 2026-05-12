# Chapter 2: Literature Review (Draft)

## 1. Blueprint (Bullet Points for your structure)
*   **2.1 The Crisis of Historical Paper ECGs:**
    *   *Context:* Explain that before 2010, the vast majority of ECGs were physical prints.
    *   *The Pivot:* Deep Learning models (like ResNet, CNNs) require digital 1D arrays, creating a "dead zone" of historical data.
*   **2.2 Current State of Optical Digitization:**
    *   *The Tool:* PhysioNet 2024 Challenge introduced ECG-Image-Kit as the standard.
    *   *The Mechanism:* Discuss how it works (color thresholding, column sweeps, OCR grid removal).
    *   *The Flaw:* Discuss the artifacts it leaves behind (pixelation "stairs", unremoved grid lines, and severe baseline wander). Note that these artifacts mimic actual diseases (e.g., a pixelated stair can look like a Q-wave notch).
*   **2.3 The Failure of Traditional Denoising:**
    *   *Standard tools:* Butterworth filters, Discrete Wavelet Transforms (DWT).
    *   *Why they fail:* Traditional signal processing assumes noise is high-frequency (static) and signal is low-frequency (heartbeat). Optical digitization noise spans the entire spectrum, overlapping with clinical features.
*   **2.4 The Direct Image Classification Alternative (2D Models):**
    *   *The Vision Approach:* Instead of extracting 1D signals, papers like Dias et al. (2024) use ConvNeXt and Gitau et al. (2024) use InceptionV3 to classify the 2D scanned image directly.
    *   *The Gap:* While these "black box" vision models work for basic classification, cardiologists require the raw 1D time-series data to measure exact intervals (like QT-prolongation) and cross-reference with modern digital EHR systems. This justifies our focus on the 1D extraction-and-refinement pathway.
*   **2.5 The Rise of Generative AI in Cardiology (2024-2026):**
    *   *Transition:* Moving from traditional filters to Deep Learning. 
    *   *Early Gen AI:* GANs (Generative Adversarial Networks) were used, but they hallucinated fake P-waves to fool the discriminator.
    *   *Diffusion Models:* Introduce DDPMs (Denoising Diffusion Probabilistic Models). Explain why they are safer (iterative Markov chain refinement rather than one-shot generation).
    *   *Recent SOTA:* Mention **DeScoD-ECG (IEEE, May 2025)** which proved Score-Based diffusion handles baseline wander, and **TFCDiff (2025)** which used Time-Frequency conditioning for noise removal.
*   **2.6 Kolmogorov-Arnold Networks (KAN) in Time-Series:**
    *   *The Shift:* Introduce the 2025/2026 shift away from CNNs towards KANs for time-series forecasting (e.g., **T-KAN, 2025**).
    *   *Relevance to ECG:* Explain that KAN's adaptive spline-based activation functions are uniquely suited for global, non-linear shifts like ECG baseline wander caused by paper skew.
*   **2.7 The Clinical Information Gap (The "Smoothing" Problem):**
    *   *The Literature Blind Spot:* Most SOTA papers (like TFCDiff) only report RMSE or SNR improvements and stop.
    *   *The TDD Warning (2025):* The paper *TDD: Task-Aware Diffusion* warned that Mean Squared Error (MSE) loss acts as a low-pass filter, potentially smoothing out the exact micro-arrhythmias needed for diagnosis.
    *   *Thesis Positioning:* This thesis bridges this exact gap by not only implementing KAN-Diffusion for signal cleanup but rigorously testing the *TDD (2025)* warning against a highly sensitive downstream clinical classifier.

---

## 2. Full Context (Paragraphs for your understanding)
*(Note: Read this to understand the flow, but paraphrase it in your own words for your final thesis to avoid AI detection).*

The application of deep learning to cardiology is inherently bottlenecked by data format. Prior to the widespread adoption of digital Electronic Health Records (EHR), the vast majority of electrocardiograms were recorded as physical printouts on thermal grid paper or stored as scanned PDFs. This created a massive "dead zone" of historical data inaccessible to modern 1D diagnostic AI. To bridge this gap, optical digitization pipelines, such as the ECG-Image-Kit popularized by the PhysioNet 2024 Challenge, were developed. These tools utilize color thresholding, column sweeps, and Optical Character Recognition (OCR) to erase the background grid and extract the ink trace into a 1D time-series. However, this process is deterministic and highly lossy. The extracted signals are frequently corrupted by quantization noise (staircase effects from pixel-to-millivolt conversion), unremoved grid lines, and severe baseline wander caused by physical paper skew. Crucially, these artifacts often mimic true clinical pathologies; for example, a quantization artifact can simulate an abnormal Q-wave notch indicative of a Myocardial Infarction. 

Traditional signal processing methodologies, such as Butterworth low-pass filters or standard Discrete Wavelet Transforms (DWT), are insufficient for post-digitization refinement. These techniques operate under the assumption that noise and signal occupy distinct frequency bands. However, the optical artifacts introduced by digitization span the entire frequency spectrum, overlapping directly with critical physiological features. Applying a standard low-pass filter to remove optical jaggedness inadvertently destroys the high-frequency components of the QRS complex. This necessitates the shift toward learned, non-linear generative approaches.

An alternative approach found in recent literature avoids 1D extraction entirely by using Computer Vision to classify the 2D scanned ECG images directly. Papers such as Dias et al. (2024) and Gitau et al. (2024) have successfully deployed models like ConvNeXt and InceptionV3 to read ECG printouts like photographs. While these end-to-end "black box" models are effective for basic classification, they fail to provide the underlying raw physiological data. Cardiologists require the 1D time-series array to manually calculate millisecond intervals (such as QT-prolongation) and to integrate historical data with modern digital hospital systems. Therefore, our research prioritizes the 1D extraction-and-refinement pathway to preserve clinical interpretability.

The years 2024 to 2026 saw a rapid acceleration in the use of Generative AI for ECG enhancement. While early attempts utilized Generative Adversarial Networks (GANs), these architectures proved too unstable for clinical use, frequently hallucinating entirely fake cardiac complexes to satisfy the discriminator network. Consequently, the field shifted toward Denoising Diffusion Probabilistic Models (DDPMs). Because diffusion models rely on an iterative Markov chain to gradually map noise back to a learned data manifold, they provide a much more stable and structurally faithful reconstruction. Recent breakthroughs, such as the DeScoD-ECG model (IEEE, 2023), demonstrated that score-based diffusion is highly effective at removing baseline wander. Concurrently, papers like TFCDiff (2025) proved the efficacy of time-frequency complementary diffusion for complex artifact removal. 

Simultaneously, the architectural backbones of these models are evolving. In late 2025 and 2026, time-series analysis saw a shift away from standard Convolutional Neural Networks (CNNs) toward Kolmogorov-Arnold Networks (KAN), as seen in models like T-KAN. KANs replace static linear weights with learnable, non-linear spline functions. This makes them uniquely suited for ECG reconstruction, as their adaptive activations are theoretically superior at handling massive, non-linear global shifts—such as the baseline wander introduced by skewed paper scans. 

Despite these architectural advancements, a critical gap remains in the literature. The vast majority of current SOTA diffusion papers report success solely based on signal-level metrics, such as Root Mean Square Error (RMSE) or Signal-to-Noise Ratio (SNR). They fail to evaluate the clinical impact of the denoising. The 2025 paper *TDD* (Task-Aware Diffusion) issued a theoretical warning that models optimized purely via Mean Squared Error (MSE) act as aggressive low-pass smoothers. While they fix the baseline wander, they risk smoothing out the high-frequency micro-arrhythmias required by downstream diagnostic classifiers. This thesis positions itself directly within this literature gap. By implementing a state-of-the-art KAN-based conditional diffusion model and subjecting the output to rigorous downstream clinical evaluation, this work seeks to empirically test the boundary between aesthetic signal denoising and actual diagnostic feature retention.
