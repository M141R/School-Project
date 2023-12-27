import mysql.connector
import matplotlib.pyplot as plt
import pandas as pd

# Connect to MySQL database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database="budgetapp"
)

cursor = db.cursor()

# Create Income and Expenses tables if they don't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Income(
        source VARCHAR(255),
        amount DECIMAL(10, 2),
        date DATE
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Expenses(
        category VARCHAR(255),
        amount DECIMAL(10, 2),
        date DATE
    )
''')

# Function to add a new income source
def add_income():
    source = input("Enter the income source: ")
    amount = float(input("Enter the amount: "))
    date = input("Enter the date (YYYY-MM-DD): ")
    cursor.execute("INSERT INTO Income (source, amount, date) VALUES (%s, %s, %s)", (source, amount, date))
    db.commit()

# Function to add a new expense
def add_expense():
    category = input("Enter the expense category: ")
    amount = float(input("Enter the amount: "))
    date = input("Enter the date (YYYY-MM-DD): ")
    cursor.execute("INSERT INTO Expenses (category, amount, date) VALUES (%s, %s, %s)", (category, amount, date))
    db.commit()

# Function to fetch data into a DataFrame
def fetch_data(table_name):
    query = f"SELECT * FROM {table_name}"
    df = pd.read_sql(query, db)
    return df

# Function to calculate balance
def calculate_balance():
    income_df = fetch_data("Income")
    expenses_df = fetch_data("Expenses")
    total_income = income_df['amount'].sum()
    total_expenses = expenses_df['amount'].sum()
    balance = total_income - total_expenses
    print(f"Your balance is: {balance}")

# Function to visualize data
def visualize_data():
    expenses_df = fetch_data("Expenses")
    grouped_expenses = expenses_df.groupby('category')['amount'].sum()

    plt.pie(grouped_expenses, labels=grouped_expenses.index, autopct='%1.1f%%')
    plt.title('Expenses by Category')
    plt.show()

# Main program loop
while True:
    print("\n1. Add income\n2. Add expense\n3. Calculate balance\n4. Visualize data\n5. Quit")
    choice = input("Enter your choice: ")

    if choice == '1':
        add_income()
    elif choice == '2':
        add_expense()
    elif choice == '3':
        calculate_balance()
    elif choice == '4':
        visualize_data()
    elif choice == '5':
        break
    else:
        print("Invalid choice. Please try again.")