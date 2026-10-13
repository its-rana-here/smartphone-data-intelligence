
from pathlib import Path
import pandas as pd


# 1. Define project paths
PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_DATA_PATH = PROJECT_ROOT / "data" / "raw" / "smartphones.csv"

PROCESSED_DATA_PATH = (
    PROJECT_ROOT / "data" / "processed" / "smartphones_clean.csv"
)


# 2. Define cleaning rules
NUMERIC_COLUMNS = [
    "num_cores",
    "processor_speed",
    "battery_capacity",
    "primary_camera_front",
]

CATEGORICAL_COLUMNS = [
    "processor_brand",
    "os",
]


# 3. Clean the dataset
def clean_smartphones(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Clean selected missing values and record each decision."""

    df_clean = df.copy()
    cleaning_log = []

    # Rule A: Fill selected numeric missing values with medians
    for column in NUMERIC_COLUMNS:
        missing_before = df_clean[column].isna().sum()

        if missing_before > 0:
            median_value = df_clean[column].median()
            df_clean[column] = df_clean[column].fillna(median_value)

            cleaning_log.append({
                "column": column,
                "missing_before": missing_before,
                "action": "Median imputation",
                "value_used": median_value,
                "reason": "Preserve records using the observed median",
            })

    # Rule B: Mark missing categories as Unknown
    for column in CATEGORICAL_COLUMNS:
        missing_before = df_clean[column].isna().sum()

        if missing_before > 0:
            df_clean[column] = df_clean[column].fillna("Unknown")

            cleaning_log.append({
                "column": column,
                "missing_before": missing_before,
                "action": 'Replace missing values with "Unknown"',
                "value_used": "Unknown",
                "reason": "Avoid inventing a category",
            })

    # Rule C: Keep avg_rating and fast_charging missing values unchanged
    for column in ["avg_rating", "fast_charging"]:
        missing_count = df_clean[column].isna().sum()

        if missing_count > 0:
            cleaning_log.append({
                "column": column,
                "missing_before": missing_count,
                "action": "Retain missing values",
                "value_used": None,
                "reason": "No reliable replacement value established",
            })

    return df_clean, pd.DataFrame(cleaning_log)


# 4. Load, clean, save, and report
def main() -> None:
    """Execute the complete smartphone cleaning pipeline."""

    if not RAW_DATA_PATH.exists():
        raise FileNotFoundError(
            f"Raw dataset not found: {RAW_DATA_PATH}"
        )

    # Load original dataset
    df = pd.read_csv(RAW_DATA_PATH)

    # Capture input statistics
    input_shape = df.shape
    missing_before = int(df.isna().sum().sum())
    duplicates_before = int(df.duplicated().sum())

    # Apply cleaning rules
    df_clean, cleaning_log = clean_smartphones(df)

    # Capture output statistics
    missing_after = int(df_clean.isna().sum().sum())
    duplicates_after = int(df_clean.duplicated().sum())

    # Save processed dataset
    PROCESSED_DATA_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    df_clean.to_csv(PROCESSED_DATA_PATH, index=False)

    # Generate report
    print("\nSMARTPHONE DATA CLEANING REPORT")
    print("=" * 40)

    print(f"Input shape:             {input_shape}")
    print(f"Output shape:            {df_clean.shape}")
    print(f"Missing cells before:    {missing_before}")
    print(f"Missing cells after:     {missing_after}")
    print(f"Missing cells filled:    {missing_before - missing_after}")
    print(f"Duplicates before:       {duplicates_before}")
    print(f"Duplicates after:        {duplicates_after}")

    print("\nREMAINING MISSING VALUES")
    print("-" * 40)

    remaining = df_clean.isna().sum()
    remaining = remaining[remaining > 0]

    if remaining.empty:
        print("No missing values.")
    else:
        print(remaining.to_string())

    print("\nCLEANING DECISION LOG")
    print("-" * 40)

    if cleaning_log.empty:
        print("No cleaning actions required.")
    else:
        print(cleaning_log.to_string(index=False))

    print(f"\nProcessed file saved to:\n{PROCESSED_DATA_PATH}")


# 5. Run only when this file is executed directly
if __name__ == "__main__":
    main()
