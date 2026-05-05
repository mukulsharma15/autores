# Comprehensive Literature Review & Gap Analysis
**Topic:** Post-Digitization Refinement of Electrocardiograms using Conditional Diffusion Models

## 1. Literature Review

### 1.1 The Challenge of ECG Digitization
Historically, ECGs were printed on thermal paper. Modern clinical machine learning relies heavily on 1D digital time-series data. Tools like **ECG-Image-Kit** (Shivashankara et al., 2024) provide synthetic pipelines to train digitization algorithms. However, as **Nguyen et al. (2025)** definitively proved in their introduction of the **PTB-IMAGE** dataset, relying on classical computer vision or basic thresholding for signal extraction yields catastrophic results. Testing on real scanned images, they achieved a mean Signal-to-Noise Ratio (SNR) of barely ~0.01 dB. This is caused by overlapping background grids, text artifacts, and the discretization of pixel locations, causing "staircase" quantization in the extracted biological signal.

Efforts to solve this include **SLPM** (Bruoth et al., 2024), a lightweight end-to-end model for paper ECG digitization. While end-to-end approaches map the image directly to a clinical diagnosis or a digital trace, they act as "black boxes" and often smooth out crucial high-frequency clinical indicators (like a notched QRS complex). 

### 1.2 The Paradigm Shift to Deep Generative Models
Given the failure of deterministic extraction, the field is transitioning to probabilistic Deep Generative Models (DGMs). Two recent scoping reviews in *Computers in Biology and Medicine* (2023, 2024) have independently mapped this shift. They conclude that GANs, VAEs, and primarily **Diffusion Models** are the "winning key" not just for synthesizing fake ECG datasets, but for generating clean biological manifolds from corrupted inputs. 

### 1.3 Diffusion Models for 1D Signal Denoising
**DeScoD-ECG** (Li et al., 2024) introduced a conditional Score-Based Diffusion model tailored for ECG baseline wander and noise. It iteratively removes Gaussian noise while conditioning on the corrupted signal. In late 2025, **TFCDiff** (Li et al., 2025) pushed this further by moving the diffusion process entirely into the Discrete Cosine Transform (DCT) domain. Because digitization artifacts (like pixel staircasing and spikes) manifest predominantly as high-frequency noise, TFCDiff’s frequency-domain diffusion provides a highly relevant architectural precursor for targeting extraction artifacts.

### 1.4 State Space Models and Super-Resolution
Finally, extracting a 1D trace from a low-DPI image mathematically mimics downsampling. Thus, fixing digitizer output is a **Super-Resolution (SR)** inverse problem. The recent **MSECG** paper (2024) introduced Mamba (Selective State-Space Models) to perform ECG super-resolution robustly. Similarly, **CSDI** (Tashiro et al., 2021) demonstrated how score-based diffusion acts as the premier architecture for continuous time-series imputation, perfectly suited for hallucinating the missing gaps in an ECG when Optical Character Recognition (OCR) deletes overlapping printed text.

---

## 2. Gap Analysis (What is missing in current research?)

1. **The "Artifact Mismatch" Gap:** Existing ECG diffusion models (like DeScoD-ECG and TFCDiff) are trained to remove *physiological and sensor noise* (muscle artifacts, baseline wander, electrode motion). **No paper currently uses a Diffusion Model trained specifically to remove optical extraction artifacts (staircasing, OCR gaps, threshold spikes).** 
2. **The Digitization Pipeline Gap:** Current digitization papers either stop at 1D optical extraction (leaving a noisy signal, as in PTB-IMAGE) or try to go End-to-End from Image directly to a Diagnosis (as in SLPM). There is a massive gap for a dedicated **"Refinement Layer"** that sits *after* optical extraction but *before* clinical diagnosis.
3. **The Imputation/Denoising Dual-Task Gap:** Optical extraction requires fixing two distinct mathematical problems simultaneously: Denoising (smoothing the staircase) and Imputation (filling OCR gaps). Existing literature treats these as separate tasks (MSECG for SR, CSDI for imputation). 

---

## 3. Best Paths for Your Thesis Research

Based on the gaps above, here are the most novel and impactful paths for your Master's thesis:

### Path A: The "Super-Resolution" 1D cDDPM (Recommended)
**Concept:** Build a 1D Conditional Denoising Diffusion Probabilistic Model (cDDPM). Take a clean dataset (PTB-XL) and use `ECG-Image-Kit` to synthetically convert it to an image and back to a 1D trace. Use the noisy extracted trace as the "condition" and the original clean signal as the "target".
**Why it's great:** It perfectly bridges Gap 1 and Gap 2. It introduces a completely new use-case for ECG diffusion.

### Path B: Frequency-Domain Diffusion for Digitization Artifacts
**Concept:** Similar to Path A, but you explicitly apply the diffusion in the Discrete Cosine Transform (DCT) domain (inspired by TFCDiff). 
**Why it's great:** Because pixelated "staircase" artifacts are inherently high-frequency noise, a frequency-domain diffusion model will theoretically smooth these artifacts much faster and with less compute than a time-domain U-Net.

### Path C: The "Mamba" (State Space Model) Diffusion Refiner
**Concept:** Replace the standard U-Net backbone in your diffusion model with a Mamba (Selective State Space) architecture.
**Why it's great:** Mamba is the absolute hottest topic in deep learning right now (2024/2025). Combining Mamba with Diffusion for ECG Super-Resolution of optical artifacts guarantees an incredibly high-impact thesis that looks extremely modern to reviewers.