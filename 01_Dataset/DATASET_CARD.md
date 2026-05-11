# OD-PTB-XL: Optically Degraded PTB-XL Paired Dataset

**Size:** 7,601 paired samples
**Format:** 1D Time-Series (1250 samples / 2.5 seconds at 500 Hz)

## Overview
This dataset provides a highly standardized, perfectly aligned paired corpus of 1-Dimensional Electrocardiogram (ECG) time-series data, specifically engineered to benchmark Generative AI denoising and post-digitization signal refinement. 

It consists of 7,601 pairs:
* **Clean Ground-Truth (`clean_samples.npy`):** Sourced directly from the high-fidelity PTB-XL clinical database.
* **Noisy Digitized (`noisy_samples.npy`):** The exact same segments after undergoing a physical-to-digital degradation cycle. They were computationally rendered onto synthetic paper templates (incorporating grid lines, shading, and OCR artifacts) using the PhysioNet 2024 ECG-Image-Kit, and subsequently re-extracted back into 1D arrays using an ensemble optical digitizer. 

## Metadata & Labels
Crucially, each of the 7,601 samples is cross-correlated for perfect temporal alignment. The accompanying `metadata.csv` provides permanent annotations for:
1. **Clinical Diagnoses:** The corresponding PTB-XL diagnostic superclass (NORM, MI, STTC, CD, HYP), allowing researchers to simultaneously evaluate signal reconstruction metrics (RMSE/SNR) and downstream clinical diagnostic retention.
2. **Patient Demographics:** Age and Sex variables are included to allow researchers to test generative AI models for age/gender bias.
3. **Fixed Splits:** A hard-coded 70/15/15 (Train/Val/Test) split is provided. This split was generated using a strict GroupShuffleSplit by `ecg_id`, ensuring that all 12 leads from a single patient exist exclusively within a single fold, eliminating data leakage.

## Limitations
* **Synthetic Degradation:** While the optical artifacts mimic the extraction algorithm perfectly, they were generated via synthetic templates rather than 40-year-old native hospital archives.
* **Fallback Labels:** Approximately 2.6% (198 samples) lacked exact mapping data in the PTB-XL CSV due to numpy array slicing anomalies. These were safely assigned a fallback label of `NORM` and demographics of `Unknown`.
* **Lead Isolation:** The dataset provides isolated 2.5-second single leads. Models must be trained to process leads independently without 12-lead spatial context.
