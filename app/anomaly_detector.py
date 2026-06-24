from app.data_loader import load_data


def detect_anomalies():
    """
    Detect support ticket anomalies.

    Rule 1:
    Critical tickets that are not resolved.

    Rule 2:
    Tickets whose resolution time exceeds:
    mean + 2 * standard deviations.
    """

    df = load_data()

    # -----------------------------------------
    # Critical Unresolved Tickets
    # -----------------------------------------

    critical_unresolved = df[
        (df["priority"] == "Critical")
        & (df["status"] != "Resolved")
    ]

    # -----------------------------------------
    # Long Resolution Tickets
    # -----------------------------------------

    resolved_df = df[
        df["resolution_time_hrs"].notna()
    ]

    mean_time = (
        resolved_df["resolution_time_hrs"]
        .mean()
    )

    std_time = (
        resolved_df["resolution_time_hrs"]
        .std()
    )

    threshold = mean_time + (
        2 * std_time
    )

    long_resolution = resolved_df[
        resolved_df["resolution_time_hrs"]
        > threshold
    ]

    # -----------------------------------------
    # Return Summary
    # -----------------------------------------

    return {
        "critical_unresolved_count":
            len(critical_unresolved),

        "long_resolution_count":
            len(long_resolution),

        "critical_unresolved_tickets":
            critical_unresolved.to_dict(
                orient="records"
            ),

        "long_resolution_tickets":
            long_resolution.to_dict(
                orient="records"
            )
    }


if __name__ == "__main__":

    results = detect_anomalies()

    print(
        f"Critical Unresolved Tickets: "
        f"{results['critical_unresolved_count']}"
    )

    print(
        f"Long Resolution Tickets: "
        f"{results['long_resolution_count']}"
    )