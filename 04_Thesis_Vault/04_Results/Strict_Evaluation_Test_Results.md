# v2 Strict Evaluation Results (7601 Dataset)
**Date:** May 2026

## Methodology
To prevent data leakage, the 7,601 extracted samples were grouped by `ecg_id`. This ensured that multiple leads from the same patient did not appear across the train, validation, and test sets. The model was trained for 200 epochs, checkpointed on validation loss, and evaluated exclusively on an unseen test set of 1,507 samples.

## Key Metrics (Test Set, n=1507)
| Metric | Input (Noisy) | Refined (DM) | Improvement |
| :--- | :--- | :--- | :--- |
| **Cosine_Sim** | 0.9736 | 0.9774 | +0.39% |
| **Pearson_r** | 0.9227 | 0.9327 | +1.08% |
| **RMSE** | 0.1063 | 0.0962 | +9.47% |
| **MAE** | 0.0510 | 0.0469 | +8.10% |
| **MAD (Max Spike)** | 0.7702 | 0.7298 | +5.23% |
| **PRD** | 21.567% | 19.455% | +9.79% |
| **SNR** | 14.12 dB | 15.16 dB | +7.35% |
| **SNR_med** | 28.18 dB | 28.61 dB | +1.50% |
| **KS_Stat** | 0.1302 | 0.1235 | +5.15% |

**Golden Metric (ImSNR):** +1.03 dB
**Overall Success Rate:** 84.3% (1,271 out of 1,507 samples saw RMSE reduction).
