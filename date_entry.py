from datetime import datetime

DATE_FORMAT = "%d-%m-%Y"
CATEGORIES = {"I": "Income", "E": "Expense"}

def get_date(prompt, allow_default=False):
    date_str = input(prompt)
    if allow_default and not date_str:
        return datetime.today().strftime(DATE_FORMAT)
    else:
        try:
            valid_date = datetime.strptime(date_str, DATE_FORMAT)
            return valid_date.strftime(DATE_FORMAT)
        except ValueError:
            print("Invalid date, please enter the date in 'dd-mm-yyyy' format")
            get_date(prompt, allow_default)

def get_amount():
    try:
        amount = float(input("Enter the amount: "))
        if amount <= 0:
            raise ValueError("Invalid amount, please enter amount greater than 0")
        return amount
    except ValueError as e:
        print(e)
        get_amount()
        

def get_category():
    category = input("Enter the category, 'I' for Income and 'E' for Expenses: ").upper()
    if category in CATEGORIES:
        return CATEGORIES[category]
    
    else:
        print("Invalid category, please enter either 'I' or 'E'")
        return get_category()

def get_description():
    return input("Enter a description(optional): ")