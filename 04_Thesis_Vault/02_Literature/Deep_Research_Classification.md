# Deep Research: SOTA ECG Classification from Images (2024)
**Focus:** Metrics, Models, and Clinical Utility of Digitized ECGs
**Date:** April 2026

## 1. The Clinical Classification Problem
The second half of the PhysioNet 2024 Challenge (and the ultimate goal of digitization) is **Classification**. It is not enough for a digitized ECG to "look" like the original; it must yield the exact same clinical diagnosis (e.g., Atrial Fibrillation, Myocardial Infarction, Normal Sinus Rhythm).

### SOTA Classification Architectures (from Literature):
The papers in our CSV reveal a clear consensus on how researchers are classifying these signals:
*   **AIMED Team (Dias et al., 2024):** Used a **ConvNeXt** architecture pre-trained on the CODE15 dataset, achieving a Macro F1-score of **0.817** (1st place on the hidden validation set).
*   **TimeBeater (Shen et al., 2024):** Used **GoogLeNet** for multi-label classification, achieving a Macro F1-score of **0.833** on their training subset.
*   **DSAIL (Gitau et al., 2024):** Fine-tuned an **InceptionV3** model on the PTB-XL dataset (21,799 records), achieving a Macro F-measure of **0.429**.
*   **Revenger (Kang et al., 2024):** Used a lightweight **ConvNeXt**, scoring **0.33** Macro F1.

### SOTA Evaluation Metrics:
Across all papers, **Accuracy is heavily discouraged** because ECG datasets are massively imbalanced (e.g., 70% of samples might be "Normal"). Instead, the global standard metrics are:
1.  **Macro F1-Score (F-measure):** The primary metric for PhysioNet 2024. It calculates the F1 score for each disease class independently and averages them, treating rare diseases equally to common ones.
2.  **AUROC (Area Under the Receiver Operating Characteristic Curve):** Measures the model's ability to distinguish between classes.
3.  **AUPRC (Area Under the Precision-Recall Curve):** Especially critical for highly imbalanced clinical datasets.

---

## 2. Your Thesis: The "Downstream Clinical Utility" Experiment
To truly make your thesis groundbreaking, you must answer this question: **"Does the Diffusion Model actually help a doctor (or an AI) make a better diagnosis?"**

If you run the Noisy (Baseline) signal through a classifier and get an F1-score of 0.65, and then run your DM-Denoised signal through the *exact same classifier* and get an F1-score of 0.78, you have absolute, undeniable proof of clinical utility. 

### The Experimental Design:
1.  **The Classifier:** Take a standard 1D CNN (like a 1D ResNet) trained on clean PTB-XL data.
2.  **Test 1 (Baseline):** Feed it the `noisynew2.npy` array. Record the Macro F1 and AUROC.
3.  **Test 2 (Your Model):** Feed it the DM-refined array. Record the Macro F1 and AUROC.
4.  **The Result:** Calculate the $\Delta$ F1-score. 

**Note on Labels:** To do this, you need the actual disease labels (e.g., SNOMED CT codes) for your 7,601 samples. If your extraction script only saved the arrays and not the `.csv` or `.hea` labels, you will need to map the file names back to their original PhysioNet labels to run this clinical test.