
from decimal import Decimal, InvalidOperation
from supabase import create_client


class ExpenseDatabase:

    def __init__(self, url, key):
        self.client = create_client(url, key)

    def register(self, email, password):
        return self.client.auth.sign_up({
            "email": email,
            "password": password
        })

    def login(self, email, password):
        return self.client.auth.sign_in_with_password({
            "email": email,
            "password": password
        })

    def logout(self):
        return self.client.auth.sign_out()

    def current_user(self):
        response = self.client.auth.get_user()

        if response.user is None:
            raise ValueError("Please log in again.")

        return response.user

    def validate_amount(self, amount):
        try:
            value = Decimal(str(amount))
        except (InvalidOperation, ValueError, TypeError):
            raise ValueError("Enter a valid amount.")

        if not value.is_finite() or value <= 0:
            raise ValueError("Amount must be positive.")

        if value > Decimal("9999999999.99"):
            raise ValueError("Amount is too large.")

        return float(value.quantize(Decimal("0.01")))

    def add_expense(self, expense_date, category,
                    amount, description):

        user = self.current_user()

        if not category.strip():
            raise ValueError("Category cannot be empty.")

        record = {
            "user_id": user.id,
            "expense_date": str(expense_date),
            "category": category.strip(),
            "amount": self.validate_amount(amount),
            "description": description.strip()
        }

        return (
            self.client.table("expenses")
            .insert(record)
            .execute()
        )

    def get_expenses(self):
        user = self.current_user()

        response = (
            self.client.table("expenses")
            .select("*")
            .eq("user_id", user.id)
            .order("expense_date", desc=True)
            .execute()
        )

        return response.data

    def update_expense(self, expense_id, category,
                       amount, description):

        user = self.current_user()

        if not category.strip():
            raise ValueError("Category cannot be empty.")

        return (
            self.client.table("expenses")
            .update({
                "category": category.strip(),
                "amount": self.validate_amount(amount),
                "description": description.strip()
            })
            .eq("id", expense_id)
            .eq("user_id", user.id)
            .execute()
        )

    def delete_expense(self, expense_id):
        user = self.current_user()

        return (
            self.client.table("expenses")
            .delete()
            .eq("id", expense_id)
            .eq("user_id", user.id)
            .execute()
        )
