# Smartphone Data Intelligence System

## Overview
A Python-based data analysis project that explores smartphone specifications, data quality, and pricing patterns.

## Objectives
- Inspect and understand raw smartphone data.
- Identify and handle missing values.
- Validate basic data-quality rules.
- Analyze smartphone price distributions and compare brands.
- Build a reproducible foundation for future machine-learning projects.

## Tech Stack
- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Jupyter Notebook
- Git and GitHub

## Project Structure
```text
smartphone-data-intelligence/
├── data/
│   ├── raw/
│   └── processed/
├── notebooks/
│   ├── 01_data_inspection.ipynb
│   ├── 02_data_cleaning.ipynb
│   └── 03_price_analysis.ipynb
├── src/
│   ├── cleaning/
│   └── validation/
├── reports/
├── requirements.txt
└── README.md
```

## Workflow
1. Inspect the raw dataset.
2. Clean selected missing values using documented rules.
3. Validate required columns and basic data-quality conditions.
4. Analyze smartphone prices, brands, and selected features.
5. Save processed data and analysis reports.

## Data Quality Notes
The cleaning process preserves the original CSV and creates a separate processed dataset. Missing ratings and charging-speed values are retained when reliable replacement values are unavailable.

## How to Run
Activate your virtual environment, install dependencies from `requirements.txt`, and run the notebooks or Python scripts from the project root.

## Learning Goals
Practice reproducible data processing, exploratory data analysis, validation, and version control.