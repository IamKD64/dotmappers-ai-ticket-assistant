import pandas as pd
from app.llm_service import ask_llm


class QueryEngine:
    def __init__(self, df):
        self.df = df

    def execute_query(self, question: str):

        # ==================================================
        # Special Handling for Anomaly Questions
        # ==================================================

        if any(word in question.lower() for word in [
            "anomaly",
            "anomalies",
            "outlier",
            "unusual"
        ]):

            anomalies = self.df[
                self.df["resolution_time_hrs"]
                >
                self.df["resolution_time_hrs"].quantile(0.95)
            ]

            return {
                "question": question,
                "answer": f"Found {len(anomalies)} tickets with unusually high resolution times.",
                "raw_result": anomalies.head(10).to_string()
            }

        # ==================================================
        # Schema Context
        # ==================================================

        schema = f"""
Dataset Columns:
{list(self.df.columns)}

Column Meanings:

ticket_id - ticket identifier
created_at - ticket creation date
category - Billing / Technical / General
priority - Low / Medium / High / Critical
status - Open / Resolved / Escalated
response_time_hrs - first response time
resolution_time_hrs - resolution duration
agent_id - assigned agent
customer_rating - customer satisfaction rating
issue_summary - ticket description
"""

        # ==================================================
        # Query Generation Prompt
        # ==================================================

        prompt = f"""
You are a Python Pandas expert.

{schema}

DataFrame Name:
df

User Question:
{question}

IMPORTANT RULES:

- Use exact column names.
- DataFrame name is df.
- Store final output in variable result.
- Return ONLY executable pandas code.
- No markdown.
- No explanations.
- No comments.
- No print statements.

Special Rules:

- Critical tickets => priority == "Critical"
- Unresolved tickets => status != "Resolved"
- Open tickets => status == "Open"
- Resolved tickets => status == "Resolved"

Examples:

result = df[df["status"]=="Open"].shape[0]

result = df[
    (df["priority"]=="Critical") &
    (df["status"]!="Resolved")
]

result = (
    df.groupby("agent_id")["customer_rating"]
      .mean()
      .sort_values(ascending=False)
      .head(5)
)

result = (
    df.groupby("category")["customer_rating"]
      .mean()
      .idxmax()
)

result = (
    df.groupby("agent_id")
      .agg({{
          "customer_rating":"mean",
          "response_time_hrs":"mean",
          "resolution_time_hrs":"mean"
      }})
)
"""

        # ==================================================
        # Generate Pandas Code
        # ==================================================

        code = ask_llm(prompt)

        code = (
            code.replace("```python", "")
            .replace("```", "")
            .strip()
        )

        local_vars = {
            "df": self.df.copy(),
            "pd": pd
        }

        try:

            print("\n" + "=" * 60)
            print("QUESTION:")
            print(question)

            print("\nGENERATED CODE:")
            print(code)

            exec(code, {}, local_vars)

            result = local_vars.get("result")

            print("\nRESULT TYPE:")
            print(type(result))

            print("\nRESULT:")
            print(result)

            print("=" * 60 + "\n")

            # ==================================================
            # Explanation Prompt
            # ==================================================

            explanation_prompt = f"""
You are analyzing a customer support dataset.

Question:
{question}

Actual Data Result:
{result}

Instructions:

1. Use ONLY the supplied result.
2. Do NOT use generic industry knowledge.
3. Mention actual values from the result.
4. Keep answer concise.
5. Explain what the result means.
6. Maximum 100 words.

Answer:
"""

            final_answer = ask_llm(explanation_prompt)

            # ==================================================
            # Clean Result Preview
            # ==================================================

            if isinstance(result, pd.DataFrame):
                result_preview = result.head(10).to_string()

            elif isinstance(result, pd.Series):
                result_preview = result.head(10).to_string()

            else:
                result_preview = str(result)

            return {
                "question": question,
                "answer": final_answer,
                "raw_result": result_preview
            }

        except Exception as e:

            print("\nEXECUTION ERROR:")
            print(str(e))

            return {
                "question": question,
                "answer": f"Failed to execute query: {str(e)}",
                "raw_result": None
            }