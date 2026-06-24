import pandas as pd
from pathlib import Path


DATA_PATH = Path("data/support_tickets.csv")


def load_data():
    """
    Load and preprocess support ticket data.
    """

    df = pd.read_csv(DATA_PATH)

    # Convert datetime column
    df["created_at"] = pd.to_datetime(df["created_at"])

    # Standardize text columns
    text_columns = ["category", "priority", "status", "agent_id"]

    for col in text_columns:
        df[col] = df[col].astype(str).str.strip()

    return df


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