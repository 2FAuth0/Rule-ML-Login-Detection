# Notebook Instructions – Biometric Login Detection Project

## Files and Structure

Each ZIP archive contains a complete, runnable notebook environment:

notebooks/
├── Biometric Enchanced Login Detection Pipeline (Rule + ML Hybrid).zip
│ ├── Biometric Enchanced Login Detection Pipeline (Rule + ML Hybrid).ipynb
│ └── data/
│       └── fixed-text.csv
├── Tuning_Showcase_Thresholds.zip
│ ├── Biometric Enchanced Login Detection Pipeline (Rule + ML Hybrid).ipynb
│ └── data/
│       └── fixed-text.csv

---

## Setup Instructions

These notebooks require Python 3 and the following dependencies:

- `numpy`
- `pandas`
- `scikit-learn`
- `matplotlib`

Each notebook on top should have pip command to help install these dependencies.

## Main Notebook: Biometric Detection Pipeline

1. Extract Biometric Enchanced Login Detection Pipeline (Rule + ML Hybrid).zip
2. Open Biometric Enchanced Login Detection Pipeline (Rule + ML Hybrid).ipynb
3. Run all cells in order

No code modifications are needed. Markdown cells provide inline explanations.

## Tuning Notebook: Rule Threshold Sensitivity
1. Extract Tuning_Showcase_Thresholds.zip
2. Open Tuning_Showcase_Thresholds.ipynb
3. Run all cells.

This notebook evaluates only the rule-based system (No ML or hybrid logic)

## Notes
- The fixed-text.csv file contains fixed-text biometric samples from the KeyRecs dataset, used for ML model inference.
- All required files are local. No external datasets or downloads needed beyond installing packages.