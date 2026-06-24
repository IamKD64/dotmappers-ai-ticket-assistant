id="dgiv1v"
import pandas as pd
from pathlib import Path


# --------------------------------------------------
# DATA FILE LOCATION
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = (
    BASE_DIR
    / "data"
    / "support_tickets.csv"
)


# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

def load_data():
    """
    Load and preprocess support ticket data.
    """

    try:

        df = pd.read_csv(DATA_PATH)

    except Exception as e:

        raise FileNotFoundError(
            f"Dataset not found: {DATA_PATH}"
        )

    # ------------------------------------------
    # Datetime Conversion
    # ------------------------------------------

    if "created_at" in df.columns:

        df["created_at"] = pd.to_datetime(
            df["created_at"],
            errors="coerce"
        )

    # ------------------------------------------
    # Standardize Text Columns
    # ------------------------------------------

    text_columns = [
        "category",
        "priority",
        "status",
        "agent_id"
    ]

    for col in text_columns:

        if col in df.columns:

            df[col] = (
                df[col]
                .astype(str)
                .str.strip()
            )

    return df


# --------------------------------------------------
# TEST
# --------------------------------------------------

if __name__ == "__main__":

    df = load_data()

    print("\nDataset Shape:")
    print(df.shape)

    print("\nColumns:")
    print(df.columns.tolist())

    print("\nMissing Values:")
    print(df.isnull().sum())

    print("\nSample Data:")
    print(df.head())
