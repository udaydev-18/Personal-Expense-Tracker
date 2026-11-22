
# Personal Expense Tracker

A personal expense management web application built with Python, Streamlit, Pandas, and Supabase.

The application helps users record expenses, analyze spending patterns, and manage transactions through a web-based interface.

## Features

- User registration and login using Supabase Authentication
- Expense management: add, view, edit, and delete
- Personal expense history with category and date filters
- Dashboard showing total spending and transaction count
- Category-wise spending analysis
- Monthly expense reports and visualizations
- CSV export of filtered expenses
- PostgreSQL database for persistent storage
- Row Level Security (RLS) for user-specific data access

## Tech Stack

| Technology | Purpose |
|---|---|
| Python | Backend application logic |
| Streamlit | Web interface |
| Supabase Auth | User authentication |
| PostgreSQL | Expense data storage |
| Pandas | Data analysis and reporting |
| Git & GitHub | Version control |

## Project Structure

```text
Expense Tracker/
├── app.py
├── database.py
├── report.py
├── requirements.txt
├── .gitignore
├── README.md
└── .streamlit/
    └── secrets.toml (local only)
```

## How It Works

1. A user registers and logs in.
2. Supabase Auth authenticates the user.
3. The user adds an expense with date, category, amount, and description.
4. Expense records are stored in Supabase PostgreSQL.
5. Row Level Security restricts database access to the authenticated user's records.
6. Pandas processes expense data to generate summaries and reports.
7. Streamlit displays the dashboard, transactions, and visualizations.

## Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/Personal-Expense-Tracker.git
cd Personal-Expense-Tracker
```

### 2. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 3. Configure Supabase

Create `.streamlit/secrets.toml`:

```toml
SUPABASE_URL = "YOUR_SUPABASE_PROJECT_URL"
SUPABASE_KEY = "YOUR_SUPABASE_PUBLISHABLE_KEY"
```

Configure a Supabase project with Authentication, an `expenses` table, and appropriate Row Level Security policies.

Never commit database passwords or secret/service-role keys.

### 4. Start the application

```bash
python -m streamlit run app.py
```

Open the local address shown in the terminal.

## Security

- Supabase Authentication identifies registered users.
- PostgreSQL Row Level Security restricts access to user-owned expenses.
- Database queries are scoped to the authenticated user.
- Local credentials are excluded from Git using `.gitignore`.
- Two-user application-level data isolation has been tested.

## Future Improvements

- Password reset functionality
- Budget limits and alerts
- Additional expense categories
- Advanced financial analytics
- Automated tests and CI/CD

## Author

Kuruva Uday Kiran

Computer Science Engineering Student
