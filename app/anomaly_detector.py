from app.data_loader import load_data


def detect_anomalies():
    """
    Detect anomalies in support tickets.

    Rule 1:
    Critical tickets that are not resolved.

    Rule 2:
    Tickets with unusually high resolution times
    (greater than mean + 2 * standard deviation).
    """

    df = load_data()

    anomalies = {}

    # Critical unresolved tickets
    critical_unresolved = df[
        (df["priority"] == "Critical")
        & (df["status"] != "Resolved")
    ]

    anomalies["critical_unresolved"] = critical_unresolved

    # Long resolution time tickets
    resolved_df = df[df["resolution_time_hrs"].notna()]

    mean_time = resolved_df["resolution_time_hrs"].mean()
    std_time = resolved_df["resolution_time_hrs"].std()

    threshold = mean_time + (2 * std_time)

    long_resolution = resolved_df[
        resolved_df["resolution_time_hrs"] > threshold
    ]

    anomalies["long_resolution"] = long_resolution

    return anomalies


if __name__ == "__main__":
    anomalies = detect_anomalies()

    print(
        f"Critical Unresolved Tickets: "
        f"{len(anomalies['critical_unresolved'])}"
    )

    print(
        f"Long Resolution Tickets: "
        f"{len(anomalies['long_resolution'])}"
    )