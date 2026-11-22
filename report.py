
import pandas as pd


class ExpenseReport:

    def __init__(self, records):
        self.data = pd.DataFrame(records)

        if self.data.empty:
            self.data = pd.DataFrame(columns=[
                "id",
                "expense_date",
                "category",
                "amount",
                "description"
            ])

        self.data["amount"] = pd.to_numeric(
            self.data["amount"],
            errors="raise"
        )

        self.data["expense_date"] = pd.to_datetime(
            self.data["expense_date"],
            errors="raise"
        )

    def total_expenses(self, data=None):
        if data is None:
            data = self.data

        return round(float(data["amount"].sum()), 2)

    def transaction_count(self, data=None):
        if data is None:
            data = self.data

        return len(data)

    def category_summary(self, data=None):
        if data is None:
            data = self.data

        if data.empty:
            return pd.Series(dtype=float)

        return (
            data.groupby("category")["amount"]
            .sum()
            .sort_values(ascending=False)
        )

    def filter_expenses(
        self,
        category="All Categories",
        start_date=None,
        end_date=None
    ):
        filtered = self.data.copy()

        if category != "All Categories":
            filtered = filtered[
                filtered["category"] == category
            ]

        if start_date is not None:
            filtered = filtered[
                filtered["expense_date"].dt.date >= start_date
            ]

        if end_date is not None:
            filtered = filtered[
                filtered["expense_date"].dt.date <= end_date
            ]

        return filtered

    def monthly_summary(self):
        if self.data.empty:
            return pd.Series(dtype=float)

        monthly = self.data.copy()

        monthly["month"] = (
            monthly["expense_date"]
            .dt.to_period("M")
            .astype(str)
        )

        return (
            monthly.groupby("month")["amount"]
            .sum()
            .sort_index()
        )
