from pathlib import Path
import pandas as pd



# 1. Define project paths
PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_DATA_PATH = PROJECT_ROOT / "data" / "raw" / "smartphones.csv"

PROCESSED_DATA_PATH = (
    PROJECT_ROOT / "data" / "processed" / "smartphone_cleaned_0.1.csv"
)

# 2.Define cleaning rules

NUMERIC_COLUMS = [
    "num_cores",
    "processor_speed",
    "battery_capacity",
    "primary_camera_front",
]

CATEGORICAL_COLUMNS = [
    "processor_brand",
    "os",
]

# 3. Clean the Datasets

def clean_smartphones(df: pd.DataFrame) -> tuple[pd.DataFrame,pd.DataFrame]:
    """Clean selcted missing values and record each decision"""

    df_clean = df.copy()
    cleaning_log = []

    # Rule: A: Fill selected numeric missing values with medians

    for column in NUMERIC_COLUMS:
        missing_before = df_clean[column].isna().sum()

        if missing_before > 0:
            median_value = df_clean[column].median()
            df_clean[column] = df_clean[column].fillna(median_value)

            cleaning_log.append({
                "column" : column,
                "missing_before" : missing_before,
                "action" : "Median Imputation",
                "value_used" : median_value,
                "reason" : "Preserve record using the observed median",
            })

    # Rule B: Mark missing categories as Unknown
    for column in CATEGORICAL_COLUMNS:
        missing_before = df_clean[column].isna().sum()

        if missing_before > 0:
            df_clean[column] = df_clean[column].fillna("Unknown")

            cleaning_log.append({
                "column" : column,
                "missing_before" : missing_before,
                "action" : 'Replace missing values with "Unknown"',
                "value_used" : "Unknown",
                "reason" : "Avoid inventing a category"
            })

    # Rule C: Keep avr_rating and fast _charging missing value unchanged
    for column in ["avg_rating", "fast_charging"]:
        missing_count = df_clean[column].isna().sum()

        if missing_count > 0:
            cleaning_log.append({
                "column" : column,
                "missing_before" : missing_count,
                "action" : "Retain missing values",
                "value_used": None,
                "reason": "No reliable replacement value established",
            })

    return df_clean, pd.DataFrame(cleaning_log)

# 4 Load, clean , save , and report

def main() -> None:
    """Execute the complete smartphone cleaning pipeline."""

    if not RAW_DATA_PATH.exists():
        raise FileNotFoundError(
            f"Raw dataset not found {RAW_DATA_PATH}"
        )

    # Load original dataset
    df = pd.read_csv(RAW_DATA_PATH)

    #capture input statistics
    input_shape = df.shape
    missing_before = int(df.isna().sum().sum())
    duplicates_before = int(df.duplicated().sum())

    # Apply  cleaning rules
    df_clean, cleaning_log = clean_smartphones(df)

    # capture aoutput statistics

    missing_after = int(df_clean.isna().sum().sum())
    duplicates_after = int(df_clean.duplicated().sum())

    # Save Processed dataset
    PROCESSED_DATA_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    df_clean.to_csv(PROCESSED_DATA_PATH, index=False)

    #generate report

    print("\nSMARTPHONE DATA CLEANING REPORT")

    print("=" * 50)

    print(f"Input shape:             {input_shape}"  )
    print(f"Output shape:            {df_clean.shape}")
    print(f"Missing cells Before:    {missing_before}")
    print(f"Missing cells After:     {missing_after}")
    print(f"Missinf cells filled:    {missing_before - missing_after}")
    print(f"Duplicated before:       {duplicates_before}")
    print(f"Duplictaed after:        {duplicates_after}")


    print("\nREMAINING MISSING VALUES")
    print("=" * 50)

    remaining = df_clean.isna().sum()
    remaining = remaining[remaining > 0]

    if remaining.empty:
        print("No missing value")
    else:
        print(remaining.to_string())

    print("\nCLEANING DECISION LOG")
    print("=" * 50)

    if cleaning_log.empty:
        print("No Cleaning action required.")
    else:
        print(cleaning_log.to_string(index = False))

    print(f"Processed file saved to:\n{PROCESSED_DATA_PATH}")


if __name__ == "__main__":
    main()