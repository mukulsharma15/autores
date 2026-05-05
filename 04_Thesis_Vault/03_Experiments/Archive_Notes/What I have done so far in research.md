Started with PhysioNet Challenge. Picked the baseline from there and found flaws : Core Problem I Identified:  Digitization ≠ Clean Signal, research gap:  Post-digitization denoising, introduced: Diffusion Model (DM) as a post-processing step, Pipeline:
Image → Digitizer → Noisy Signal → Diffusion Model → Refined Signal

# **ECG Digitization + Diffusion Models**

## **1. Understanding the Paper & Baseline**

- You started with the  Kaggle PhysioNet Challenge.   Picked the baseline from there and found flaws
    
- Key idea:
    
    - Convert ECG images → time-series.
        
    - Pipeline includes **OCR, grid removal (DnCNN), and signal extraction**.
        
- Problem identified:  
    👉 Even after digitization, **noise and distortions remain**.
    

---

## **2. Core Problem You Identified**

> Digitization ≠ Clean Signal

Residual issues:

- Grid artifacts
    
- Spike noise
    
- Quantization errors
    
- Wrong peaks (local maxima/minima)
    
- Misalignment, NaNs
    

👉 This became your research gap:  
**Post-digitization denoising**

---

## **3. Your Approach**

You introduced:

> **Diffusion Model (DM) as a post-processing step**

Pipeline:

Image → Digitizer → Noisy Signal → Diffusion Model → Refined Signal

---

## **4. Your Experimental Journey (4 Phases)**

### **Phase 1 — Non-DM**

- Tried filters / ML / simple models
    
- Result:
    
    - ~1% improvement overall
        
    - ❌ Not effective
        

---

### **Phase 2 — DM on Poor Real Dataset**

- Issues:
    
    - NaNs, misalignment, scaling problems
        
    - Cosine similarity = **0.07**
        
- After preprocessing:
    
    - 30% improvement (200 epochs)
        
    - 6% improvement (1000 epochs → overfitting)
        
- ❗ Problem: dataset quality
    

---

### **Phase 3 — DM on Improved Real Dataset**

- Cleaned extraction pipeline
    
- Cosine similarity = **0.88**
    
- Result:
    
    - Only **~0.8% improvement**
        
- ❗ Insight:
    
    - Real data is complex
        
    - DM limited by imperfect ground truth
        

---

### **Phase 4 — DM on Synthetic Dataset**

- Clean, perfectly aligned data
    
- Cosine = **0.99**
    
- Results:
    
    - **70–78% improvement**
        
    - Very strong performance
        
- ❗ Issue:
    
    - Missed local maxima/minima at high epochs
        

---

## **5. Key Insight (MOST IMPORTANT)**

> ❗ **The model is NOT the bottleneck — the data is.**

- DM works extremely well with clean data
    
- Fails when ground truth is noisy or inconsistent
    
- Real-world digitization introduces irreversible errors
    

---

## **6. Technical Learnings**

- Fixed preprocessing:
    
    - NaNs → interpolation
        
    - normalization → [-1, 1]
        
    - alignment issues
        
- Learned:
    
    - Overfitting happens with noisy labels
        
    - Cosine similarity can be misleading
        
    - Peak preservation is critical in ECG
        

---

## **7. Your Contributions**

- Applied **Diffusion Models to ECG post-digitization**
    
- Compared across **real vs synthetic datasets**
    
- Identified **data quality as the main limitation**
    
- Analyzed **failure modes (extrema mismatch, overfitting, noise types)**