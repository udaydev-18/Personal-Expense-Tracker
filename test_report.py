
from report import ExpenseReport

expenses = [
    {
        "id": 1,
        "expense_date": "2026-11-20",
        "category": "Food",
        "amount": 250,
        "description": "Lunch"
    },
    {
        "id": 2,
        "expense_date": "2026-11-21",
        "category": "Travel",
        "amount": 100,
        "description": "Bus"
    },
    {
        "id": 3,
        "expense_date": "2026-11-22",
        "category": "Food",
        "amount": 150,
        "description": "Dinner"
    }
]

report = ExpenseReport(expenses)

print("Total Expenses:", report.total_expenses())
print("Transactions:", report.transaction_count())

print("\nCategory Summary:")
print(report.category_summary())

print("\nFood Expenses:")
print(report.filter_expenses(category="Food"))

print("\nMonthly Summary:")
print(report.monthly_summary())
