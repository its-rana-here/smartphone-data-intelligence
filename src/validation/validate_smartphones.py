from pathlib import Path
import pandas as pd

# 1. Define the Processed data path
PROJECT_ROOT =  Path(__file__).resolve().parents[2]

DATA_PATH = (
    PROJECT_ROOT / "data" / "processed" / "smartphone_cleaned_0.1.csv"
)


# 2. Define required columns

REQUIRED_COLUMNS = [
    "brand_name",
    "model",
    "price",
    "avg_rating",
    "num_cores",
    "processor_speed",
    "battery_capacity",
    "ram_capacity",
    "os"
]

# 3. Validate datasets

def validate_smartphones(df: pd.DataFrame) -> dict:
    """check basic smartphones data-quality rules"""

    report = {}

    # Check required columns
    missing_columns = []

    for column in REQUIRED_COLUMNS:
        if column not in df.columns:
            missing_columns.append(column)

    report["missing_required_column"] = missing_columns

    #checking missing values

    missing_values = df.isna().sum()
    report["missing_value"] = missing_values[
        missing_values > 0
    ].to_dict()


    #Check exact duplicate rows
    report["duplicate_row"] = int(df.duplicated().sum())

    #check invalid prices, if the price column exist
    if "price" in df.columns:
        report["invalid_price"] = int(
            (df["price"] < 0 ).sum()
        )
    else:
        report["invalid_prices"] = "Cannot check: price column missing"

    #check binary columns contain only 0 or 1

    binary_column = [
        "5G_or_not",
        "fast_charging_available",
        "extended_memory_available",

    ]

    invalid_binary = {}

    for column in binary_column:
        if column in df.columns:
            invalid_count = (
                ~df[column].isin([0, 1]) & df[column].notna()
            ).sum()

            invalid_binary[column] = int(invalid_count)

    report["invalid_binary_values"] = invalid_binary

    return report

# 4. Load data and print the validation report

def main() -> None:
    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Processed dataset not found: {DATA_PATH}" 
        )
    df = pd.read_csv(DATA_PATH)

    report = validate_smartphones(df)

    print("\nSMARTPHONE DATA VALIDATION REPORT")
    print("=" * 40)

    print(f"Dataset shape: {df.shape}")

    for check, result in report.items():
        print(f"\n{check}")
        print(result)

     # Determine basic validation status
    passed = True
    if report["missing_required_column"]:
        passed = False
    if report["invalid_price"] != 0:
        passed = False
    
    for count in report["invalid_binary_values"].values():
        if count != 0:
            passed = False

    print("\n" + "=" * 40)
    print(
        "Basic validation:",
        "PASSED" if passed else "CHECK REQUIRED"
    )


# 5. Execute the script
if __name__ == "__main__":
    main()
