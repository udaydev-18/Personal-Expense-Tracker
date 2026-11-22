
import streamlit as st
from datetime import date

from database import ExpenseDatabase
from report import ExpenseReport


st.set_page_config(
    page_title="Personal Expense Tracker",
    page_icon="💰",
    layout="wide"
)

CATEGORIES = [
    "Food", "Travel", "Shopping",
    "Bills", "Health", "Education", "Other"
]


# Create a separate database client per browser session.
# Do not cache an authenticated Supabase client globally.
if "db" not in st.session_state:
    try:
        st.session_state.db = ExpenseDatabase(
            st.secrets["SUPABASE_URL"],
            st.secrets["SUPABASE_KEY"]
        )
    except Exception:
        st.error("Unable to initialize the database.")
        st.stop()

db = st.session_state.db


def show_login():
    st.title("💰 Personal Expense Tracker")
    st.write("Manage your expenses securely in one place.")

    login_tab, register_tab = st.tabs([
        "Login", "Register"
    ])

    with login_tab:
        st.subheader("Welcome Back")

        with st.form("login_form"):
            email = st.text_input("Email")
            password = st.text_input(
                "Password", type="password"
            )
            login_submit = st.form_submit_button("Login")

        if login_submit:
            if not email.strip() or not password:
                st.error("Enter your email and password.")
            else:
                try:
                    response = db.login(
                        email.strip(), password
                    )

                    if response.user and response.session:
                        st.session_state.logged_in = True
                        st.rerun()
                    else:
                        st.error("Login was unsuccessful.")

                except Exception:
                    st.error(
                        "Login failed. Check your credentials "
                        "and confirm your email if required."
                    )

    with register_tab:
        st.subheader("Create Your Account")

        with st.form("register_form"):
            new_email = st.text_input(
                "Email Address"
            )
            new_password = st.text_input(
                "Create Password", type="password"
            )
            confirm_password = st.text_input(
                "Confirm Password", type="password"
            )
            register_submit = st.form_submit_button(
                "Register"
            )

        if register_submit:
            if not new_email.strip():
                st.error("Enter an email address.")
            elif len(new_password) < 8:
                st.error(
                    "Password must contain at least "
                    "8 characters."
                )
            elif new_password != confirm_password:
                st.error("Passwords do not match.")
            else:
                try:
                    db.register(
                        new_email.strip(), new_password
                    )
                    st.success(
                        "Registration submitted. Check your "
                        "email for a confirmation link if "
                        "your project requires verification. "
                        "Then return here and log in."
                    )
                except Exception:
                    st.error(
                        "Registration could not be completed."
                    )


def show_dashboard(report):
    st.header("📊 Dashboard")

    data = report.data

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Total Expenses",
        f"₹{report.total_expenses():,.2f}"
    )
    col2.metric(
        "Transactions",
        report.transaction_count()
    )
    col3.metric(
        "Categories",
        data["category"].nunique()
    )

    st.subheader("Category-wise Spending")

    summary = report.category_summary()

    if not summary.empty:
        st.bar_chart(summary)
    else:
        st.info("No expenses recorded yet.")

    st.subheader("Recent Transactions")

    if not data.empty:
        st.dataframe(
            data.head(10),
            hide_index=True,
            use_container_width=True
        )
    else:
        st.info("Add your first expense to get started.")


def show_add_expense():
    st.header("➕ Add Expense")

    with st.form("add_expense_form"):
        expense_date = st.date_input(
            "Expense Date", value=date.today()
        )

        category = st.selectbox(
            "Category", CATEGORIES
        )

        amount = st.number_input(
            "Amount (₹)",
            min_value=0.01,
            value=100.0,
            step=10.0,
            format="%.2f"
        )

        description = st.text_input(
            "Description",
            placeholder="Example: Lunch at restaurant"
        )

        submitted = st.form_submit_button(
            "Save Expense"
        )

    if submitted:
        try:
            db.add_expense(
                expense_date,
                category,
                amount,
                description
            )
            st.success("Expense saved successfully!")
        except ValueError as error:
            st.error(str(error))
        except Exception:
            st.error(
                "Unable to save the expense. "
                "Please try again."
            )


def show_expenses(report):
    st.header("📋 Expense History")

    data = report.data

    categories = ["All Categories"] + sorted(
        data["category"].dropna().unique().tolist()
    )

    selected_category = st.selectbox(
        "Select Category", categories
    )

    enable_date_filter = st.checkbox(
        "Enable Date Filter"
    )

    start_date = None
    end_date = None

    if enable_date_filter:
        col1, col2 = st.columns(2)

        with col1:
            start_date = st.date_input(
                "Start Date",
                value=date.today(),
                key="filter_start"
            )

        with col2:
            end_date = st.date_input(
                "End Date",
                value=date.today(),
                key="filter_end"
            )

        if start_date > end_date:
            st.error(
                "Start Date cannot be after End Date."
            )
            return

    filtered = report.filter_expenses(
        category=selected_category,
        start_date=start_date,
        end_date=end_date
    )

    col1, col2 = st.columns(2)

    col1.metric(
        "Filtered Total",
        f"₹{report.total_expenses(filtered):,.2f}"
    )
    col2.metric(
        "Transactions",
        report.transaction_count(filtered)
    )

    st.dataframe(
        filtered,
        hide_index=True,
        use_container_width=True
    )

    st.download_button(
        "Download CSV",
        data=filtered.to_csv(index=False),
        file_name="my_expenses.csv",
        mime="text/csv"
    )


def show_manage_expenses(report):
    st.header("✏️ Edit or Delete Expenses")

    data = report.data

    if data.empty:
        st.info("No expenses available.")
        return

    options = {
        f"#{int(row['id'])} | "
        f"{row['category']} | "
        f"₹{row['amount']:.2f} | "
        f"{row['expense_date'].date()}": int(row["id"])
        for _, row in data.iterrows()
    }

    selected = st.selectbox(
        "Select an Expense",
        list(options.keys())
    )

    expense_id = options[selected]

    row = data[data["id"] == expense_id].iloc[0]

    with st.form("edit_expense_form"):
        category = st.text_input(
            "Category",
            value=str(row["category"])
        )

        amount = st.number_input(
            "Amount (₹)",
            min_value=0.01,
            value=float(row["amount"]),
            format="%.2f"
        )

        description = st.text_input(
            "Description",
            value=str(row["description"] or "")
        )

        update_submit = st.form_submit_button(
            "Update Expense"
        )

    if update_submit:
        try:
            db.update_expense(
                expense_id,
                category,
                amount,
                description
            )
            st.success("Expense updated successfully!")
            st.rerun()
        except ValueError as error:
            st.error(str(error))
        except Exception:
            st.error("Unable to update the expense.")

    st.warning(
        "Deleting an expense cannot be undone."
    )

    confirm_delete = st.checkbox(
        "I confirm that I want to delete this expense"
    )

    if st.button(
        "Delete Expense",
        disabled=not confirm_delete
    ):
        try:
            db.delete_expense(expense_id)
            st.success("Expense deleted successfully!")
            st.rerun()
        except Exception:
            st.error("Unable to delete the expense.")


def show_reports(report):
    st.header("📈 Expense Reports")

    summary = report.category_summary()

    if summary.empty:
        st.info("No expenses available for reporting.")
        return

    st.subheader("Spending by Category")
    st.bar_chart(summary)

    st.subheader("Monthly Spending")

    monthly = report.monthly_summary()

    if not monthly.empty:
        st.line_chart(monthly)

    st.metric(
        "Overall Spending",
        f"₹{report.total_expenses():,.2f}"
    )


# ---------------- MAIN APPLICATION ----------------

if not st.session_state.get("logged_in", False):
    show_login()
    st.stop()

# Validate the authenticated user on each rerun.
try:
    user = db.current_user()
except Exception:
    st.session_state.logged_in = False
    st.session_state.pop("db", None)
    st.warning(
        "Your session is no longer valid. "
        "Please log in again."
    )
    st.stop()

st.sidebar.title("💰 Expense Tracker")
st.sidebar.write(f"Logged in as: {user.email}")

menu = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Add Expense",
        "View Expenses",
        "Edit / Delete",
        "Reports"
    ]
)

if st.sidebar.button("Logout"):
    try:
        db.logout()
    except Exception:
        pass

    st.session_state.logged_in = False
    st.session_state.pop("db", None)
    st.rerun()


try:
    records = db.get_expenses()
    report = ExpenseReport(records)

except Exception as e:
    st.error("Unable to load expenses.")
    st.exception(e)
    st.stop()


if menu == "Dashboard":
    show_dashboard(report)

elif menu == "Add Expense":
    show_add_expense()

elif menu == "View Expenses":
    show_expenses(report)

elif menu == "Edit / Delete":
    show_manage_expenses(report)

elif menu == "Reports":
    show_reports(report)
