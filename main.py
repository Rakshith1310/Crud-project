import pandas as pd
import csv
from datetime import datetime
from date_entry import get_amount, get_category, get_date, get_description
import matplotlib.pyplot as plt


class CSV:
    CSV_FILE = "finance_data.csv"
    COLUMNS = ["date", "amount", "category", "description"]
    DATE_FORMAT = "%d-%m-%Y"

    @classmethod
    def initilaze_csv(cls):
        try:
            pd.read_csv(cls.CSV_FILE)
        except FileNotFoundError:
            df = pd.DataFrame(columns=cls.COLUMNS)
            df.to_csv(cls.CSV_FILE, index=False)

    @classmethod
    def add_transaction(cls, date, amount, category, description):
        new_entry = {
            "date": date,
            "amount": amount,
            "category": category,
            "description": description,
        }
        with open(cls.CSV_FILE, "a", newline="") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=cls.COLUMNS)
            writer.writerow(new_entry)
        print("Entry added successfully")

    @classmethod
    def get_transactions(cls, start_date, end_date):
        df = pd.read_csv(cls.CSV_FILE)
        df["date"] = pd.to_datetime(df["date"], format=cls.DATE_FORMAT)

        start_date = datetime.strptime(start_date, cls.DATE_FORMAT)
        end_date = datetime.strptime(end_date, cls.DATE_FORMAT)

        filter = (df["date"] >= start_date) & (df["date"] <= end_date)
        filtered_df = df.loc[filter]

        if filtered_df.empty:
            print("No transactions found within the given date range.")
        else:
            print(
                f"Transaction from {start_date.strftime(cls.DATE_FORMAT)} to {end_date.strftime(cls.DATE_FORMAT)}"
            )
            print(
                filtered_df.to_string(
                    index=False,
                    formatters={"date": lambda date: date.strftime(cls.DATE_FORMAT)},
                )
            )

            total_income = filtered_df[filtered_df["category"] == "Income"][
                "amount"
            ].sum()
            total_expense = filtered_df[filtered_df["category"] == "Expense"][
                "amount"
            ].sum()
            net_savings = total_income - total_expense

            print("\nSummary")
            print(f"Total Income: {total_income:.2f}")
            print(f"Total Expense: {total_expense:.2f}")
            print(f"Net Savings is: {net_savings:.2f}")

            return filtered_df


def plotGraph(dataframe):

    # Sets date as an index so that we can manipulate data using the index.
    dataframe.set_index("date", inplace=True)

    income_df = (
        # Here, when there is no income for a given date, the plot would look disconnected hence Daily frequency 'D' is set
        # Sum() aggregated the data date wise and provides a summation
        # reIndex() fills value with zero when there is no Income or Expense for a given date
        dataframe[dataframe["category"] == "Income"]
        .resample("D")
        .sum()
        .reindex(dataframe.index, fill_value=0)
    )
    expense_df = (
        dataframe[dataframe["category"] == "Expense"]
        .resample("D")
        .sum()
        .reindex(dataframe.index, fill_value=0)
    )

    plt.figure(figsize=(10, 5))

    # income_df.index means we are plotting the date
    plt.plot(income_df.index, income_df["amount"], label="Income", color="g")
    plt.plot(expense_df.index, expense_df["amount"], label="Expense", color="r")
    plt.xlabel("Date")
    plt.ylabel("Amount")
    plt.title("Income and Expense over time")
    plt.legend()
    plt.grid(True)
    plt.show()


def add():
    date = get_date(
        "Enter the date of the transaction in the format dd-mm-yy format or press Enter for today's date: ",
        allow_default=True,
    )
    amount = get_amount()
    category = get_category()
    description = get_description()

    CSV.add_transaction(date, amount, category, description)


def main():
    while True:
        print("\nFinance Tracker")
        print("1. Add a mew transaction")
        print("2. Get transactions")
        print("3. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            add()
        elif choice == "2":
            start_date = get_date("Enter the start date (dd-mm-yyyy) format: ")
            end_date = get_date("Enter the end date (dd-mm-yyyy) format: ")
            dataframe = CSV.get_transactions(start_date, end_date)

            if input("Do you want to see the graph? (y/n): ").lower() == "y":
                plotGraph(dataframe)

        elif choice == "3":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again by entering 1/2/3.")


if __name__ == "__main__":
    main()

# CSV.initilaze_csv()
# CSV.add_transaction("08-09-2024", 999, "Income", "Test")
# add()
# CSV.get_transactions("08-09-2024", "15-09-2024")
