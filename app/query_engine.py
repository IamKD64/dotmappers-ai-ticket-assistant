from app.data_loader import load_data


def process_query(question: str):
    """
    Process natural language queries against support ticket data.
    """

    df = load_data()

    question = question.lower().strip()

    # -------------------------
    # Ticket Counts
    # -------------------------

    if question == "total tickets":
        return f"Total tickets: {len(df)}"

    elif question == "open tickets":
        count = len(df[df["status"] == "Open"])
        return f"Open tickets: {count}"

    elif (
        "critical" in question
        and "unresolved" in question
    ):
        count = len(
            df[
                (df["priority"] == "Critical")
                & (df["status"] != "Resolved")
            ]
        )

        return f"Critical unresolved tickets: {count}"

    elif question == "resolved tickets":
        count = len(df[df["status"] == "Resolved"])
        return f"Resolved tickets: {count}"

    # -------------------------
    # Customer Ratings
    # -------------------------

    elif "average rating" in question:
        avg_rating = round(
            df["customer_rating"].mean(),
            2
        )

        return (
            f"Average customer rating: "
            f"{avg_rating}"
        )

    # -------------------------
    # Category Analysis
    # -------------------------

    elif (
        "category" in question
        and "most tickets" in question
    ):

        category_counts = df["category"].value_counts()

        top_category = category_counts.idxmax()
        top_count = category_counts.max()

        return (
            f"Category with most tickets: "
            f"{top_category} "
            f"({top_count} tickets)"
        )

    # -------------------------
    # Agent Analysis
    # -------------------------

    elif (
        "highest rating" in question
        and "agent" in question
    ):

        agent_ratings = (
            df.groupby("agent_id")["customer_rating"]
            .mean()
        )

        best_agent = agent_ratings.idxmax()
        best_rating = round(
            agent_ratings.max(),
            2
        )

        return (
            f"Highest rated agent: "
            f"{best_agent} "
            f"({best_rating})"
        )

    elif (
        "most tickets" in question
        and "agent" in question
    ):

        agent_counts = (
            df["agent_id"]
            .value_counts()
        )

        top_agent = agent_counts.idxmax()
        top_count = agent_counts.max()

        return (
            f"Agent handling most tickets: "
            f"{top_agent} "
            f"({top_count} tickets)"
        )

    # -------------------------
    # Unknown Question
    # -------------------------

    return (
        "Sorry, I couldn't understand that question. "
        "Try asking about total tickets, open tickets, "
        "resolved tickets, ratings, categories, or agents."
    )


if __name__ == "__main__":

    test_questions = [
        "total tickets",
        "open tickets",
        "resolved tickets",
        "critical unresolved tickets",
        "average rating",
        "which category has most tickets",
        "which agent has highest rating",
        "which agent handles most tickets",
    ]

    for q in test_questions:
        print(f"\nQuestion: {q}")
        print(process_query(q))