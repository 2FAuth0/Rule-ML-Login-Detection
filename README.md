# Biometric Login Detection System
## Layered Detection of Suspicious Logins Using Keystroke Dynamics Rules, Machine Learning


This project implements a dual-layered detection pipeline that flags suspicious login behavior:
- Rule-Based logic
- Supervised machine learning

Three detection paths are evaluated:
- Rule-based only
- ML-based only
- Hybrid pipeline (rule OR ML)

**Features**
- Behavior login simulator with embedded keystroke timin
- Rule engine based on login metadata & typing patters
- ML classifier trained on real-worl keystroke biometrics (KeyRecs dataset)
- Full evaluation suite: precision, recall, F1, confusion matrix, bar charts

**Citataion**
Keystroke biometric data based on:
_KeyRecs: A Real-World Keystroke Dynamic Dataset for User Identification_
https://doi.org/10.1016/j.dib.2023.109509


## Deliverables
- Reproducible notebook (or Colab link)
- Evaluation metrics: accuracy, precision, recall, F1, confusion matrix
- Final report and short demo video

## License
This project is licensed under the MIT License.
