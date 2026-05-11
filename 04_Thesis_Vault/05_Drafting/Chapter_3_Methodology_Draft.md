# Chapter 3: Methodology (Draft)

## 1. Blueprint (Bullet Points for your structure)
*   **3.1 Dataset Creation (The 7,601 Pairs):**
    *   *Source:* PTB-XL clean 1D records.
    *   *Degradation:* Plotted via ECG-Image-Kit onto synthetic paper templates (added grid, wrinkles, OCR text).
    *   *Extraction:* Ran baseline optical digitizer to get the 1D Noisy signal.
    *   *Alignment:* Cross-correlated noisy vs clean to get perfect 1:1 pairs.
    *   *Metadata Enrichment:* Permanently embedded Demographics (Age/Sex) and exact PTB-XL Clinical Labels (NORM, MI, STTC, CD, HYP) to allow researchers to test for AI bias and clinical retention.
    *   *Leakage Prevention:* Embedded a fixed, strict GroupShuffleSplit by `ecg_id` directly into the metadata CSV (70/15/15 split) to ensure that all 12 leads from one patient stay together, preventing data leakage and guaranteeing a standardized test set for future researchers.
*   **3.2 Fixing Previous Extraction Bugs:**
    *   *Bug 1 (Length):* Fixed 2500 target length to 1250 to stop interpolation duplication.
    *   *Bug 2 (Digitizer):* Upgraded from color-sweep to Ensemble Digitizer for robustness.
    *   *Bug 3 (Scale):* Increased from 120 samples to 7,601 to stop model memorization.
    *   *Bug 4 (Normalization):* Moved from independent to shared normalization during training.
*   **3.3 The Core Architecture:**
    *   *Model:* 1D Conditional DDPM (7.27M parameters).
    *   *Mechanism:* Partial Reverse Diffusion ($t_{start}=30$). Model starts with noisy signal, adds minor noise, and does 30 correction steps.
    *   *Backbone:* U-Net with sinusoidal position embeddings for time ($t$).
*   **3.4 SOTA Upgrade: Kolmogorov-Arnold Networks (KAN):**
    *   Replaced standard Conv1D blocks with KAN layers.
    *   *Reasoning:* KAN's adaptive, non-linear activation functions (splines) are theoretically superior at mapping massive non-linear shifts, like severe baseline wander from paper skew.
*   **3.5 Clinical Evaluation Setup:**
    *   Built a downstream 1D ResNet Classifier (The Clinical Oracle).
    *   Trained on ground-truth clean data to recognize diseases (MI, STTC, HYP).
    *   Used to test the final generated signals to see if the "disease" survived the denoising.

---

## 2. Full Context (Paragraphs for your understanding)
*(Note: Read this to understand the flow, but paraphrase it in your own words for your final thesis to avoid AI detection).*

The foundation of this methodology relies on the generation of a high-fidelity paired dataset. Because supervised diffusion requires perfect mapping between a degraded state and a target state, the dataset was constructed by reverse-engineering the digitization process. Clean, 1D time-series ground truth data was sourced from the PTB-XL database. These signals were computationally plotted onto synthetic paper templates using the ECG-Image-Kit, introducing physical artifacts such as grid lines, shading, wrinkles, and overlapping text. The baseline optical digitizer was then applied to these images to extract the "noisy" 1D condition. Finally, the extracted signals were cross-correlated against the original ground truth to establish perfectly aligned, 1-to-1 paired segments. To ensure absolute clinical validity and prevent data leakage, the 7,601 paired samples were partitioned using a strict GroupShuffleSplit based on patient ID, guaranteeing that all 12 leads of a single patient resided exclusively within the training, validation, or testing sets.

Early iterations of this research revealed that standard extraction pipelines contained hidden flaws that prevented generative models from converging. Four critical bugs were identified and resolved. First, a signal length duplication error was fixed; the baseline pipeline erroneously targeted 2500 samples for a 2.5-second, 500 Hz signal, which artificially duplicated data. This was corrected to 1250 samples. Second, the extraction tool was upgraded to an Ensemble Digitizer to handle both color and grayscale scans effectively. Third, dataset volume was scaled from 120 isolated samples to 7,601 to prevent the highly parameterized model from simply memorizing the noise distribution. Finally, a normalization mismatch was corrected; independent scaling of the pairs had been destroying amplitude error data, which was resolved by enforcing shared normalization ranges.

The core architecture utilized is a 1D Conditional Denoising Diffusion Probabilistic Model (cDDPM). Instead of generating an ECG from pure Gaussian noise—which poses severe risks of hallucinating healthy heartbeats on pathological patients—this methodology employs Partial Reverse Diffusion. The inference process begins at $t_{start}=30$. A corresponding fraction of the noise schedule is added directly to the optically digitized signal, and the model performs only the final 30 denoising steps. This constrains the generative process, acting as a targeted refinement layer rather than a complete reconstruction. 

To push the reconstruction capability beyond standard architectures, the U-Net backbone was upgraded with Kolmogorov-Arnold Network (KAN) layers. Standard convolutional networks utilize static linear weights, which can struggle with the severe, non-linear global shifts characteristic of ECG baseline wander. KAN layers replace these with learnable, non-linear activation functions parameterized as splines along the edges of the network. This provides the architecture with the necessary flexibility to track and correct massive waveform distortions.

Ultimately, to evaluate the efficacy of the denoising, a clinical validation pipeline was established. A 1D ResNet diagnostic classifier, termed the Clinical Oracle, was trained on the clean ground truth data to recognize primary pathologies (e.g., Myocardial Infarction, Conduction Disturbance). This oracle was subsequently used to evaluate the noisy and diffusion-refined signals, providing a direct measurement of whether the generative cleanup successfully preserved the diagnostic integrity of the heartbeat.