# Biometric Login Detection System
## Layered Detection of Suspicious Logins Using Keystroke Dynamics Rules, and Machine Learning


This project implements a modular login anomaly detection pipeline using both:
- Hardcoded rule-base heurisitcs
- A supervised ML classifier trained on biometric keystroke data

Three detection strategies are evaluated:
- Rule-based only (login metadata + typing stats)
- ML-based only (biometric keystroke vectors)
- Hybrid pipeline (flags if either rule or ML triggers)

**Features**
- Synthetic login simulator with user/attacker modeling
- Rule engine using metadata + keystroke-derived features
- ML classifier trained on real-world keystroke biometrics (KeyRecs)
- Hybrid pipeline with OR-logic for maximum attacker recall
- Full evaluation suite: confusion matrix, precision, recall, F1, accuracy
- Standalone threshold tuning notebook for rule sensitivity analysis

## Project Structure
Under scripts:
- generate_logins.py - simulates login sessions
- rule_based_detector.py - rule-based detection logic
- load_keyrecs.py - loads and parses KeyRecs data
- train_ml_classifier.py - trains biometric ML model
- pipeline_detector.py - hybrid rule + ML pipeline
- evaluation.py - computes evaluation metrics
Under notebooks:
- Biometric Enhanced Login Detection Pipeline.ipynb - full demo notebook
- Tuning_Showcase_Thresholds.ipynb - standalone rule sensitivity analysis 

## Evaluation
- Rule-based: high recall, moderate false positives
- ML-based: perfect recall, high false positives
- Hybrid: perfect recall, reduced false positives

Note: Results may vary slightly due to randomized session simulation


## Citataion
Keystroke biometric data based on:
_KeyRecs: A Real-World Keystroke Dynamic Dataset for User Identification_
https://doi.org/10.1016/j.dib.2023.109509


## Deliverables
- Final Report (with skills learned section)
- Full codebase with scripts and notebooks
- Evaluation plots and metrics

## License
This project is licensed under the MIT License.
