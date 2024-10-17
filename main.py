import pandas as pd
import csv
from datetime import datetime
from data_entry import get_amount, get_category, get_date, get_description
import matplotlib.pyplot as plt


class CSV:
    CSV_FILE = 'finance_data.csv'
    COLUMNS = ["date", "amount", "category", "description"]
    DATE_FORMAT = "%d-%m-%Y"

    ##init csv class method
    @classmethod
    def init_csv(cls):
        try:
            #read it if exists
            pd.read_csv(cls.CSV_FILE)
        except FileNotFoundError:
            #create the csv
            df = pd.DataFrame(columns=cls.COLUMNS)
            df.to_csv(cls.CSV_FILE, index=False)

    @classmethod
    def add_entry(cls, date, amount, category, description):
        #create the dictionary
        new_entry = {
            "date": date,
            "amount": amount,
            "category": category,
            "description": description,    
        }

        #open file and write to it - will close automatically 
        with open(cls.CSV_FILE, "a", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=CSV.COLUMNS)
            #add the dictionary data
            writer.writerow(new_entry);

        #show a message
        print("Entry added successfully")

    @classmethod
    def get_transactions(cls, start_date, end_date):
        #read the file    
        df = pd.read_csv(cls.CSV_FILE)    
        
        #get date column
        df["date"] = pd.to_datetime(df["date"], format=cls.DATE_FORMAT)
        start_date = datetime.strptime(start_date, cls.DATE_FORMAT)
        end_date = datetime.strptime(end_date, cls.DATE_FORMAT)
        
        #create a mask
        mask = (df["date"] >= start_date) & (df["date"] <= end_date)
        filtered_df = df.loc[mask]

        if filtered_df.empty:
            print("No transactions found in the given date range")
        else:
            print(
                f"Transactions from {start_date.strftime(CSV.DATE_FORMAT)} to {end_date.strftime(CSV.DATE_FORMAT)}"    
            )
            print(filtered_df.to_string(index=False, formatters={"date": lambda x: x.strftime(CSV.DATE_FORMAT)}))

            total_income = filtered_df[filtered_df['category'] == "Income"]['amount'].sum()
            total_expense = filtered_df[filtered_df['category'] == "Expense"]['amount'].sum()

            print("\nSummary:")
            print(f"Total Income: ${total_income:.2f}") #round to 2 decimals
            print(f"Total Expense: ${total_expense:.2f}")
            print(f"Net Savings: ${(total_income - total_expense):.2f}")

        return filtered_df    



def add():
    #init the csv
    CSV.init_csv()    
    
    #get the data from the user inputs
    date = get_date("Enter the date of the transaction (dd-mm-yyyy) or press 'Enter' key to use today's date: ", allow_default=True)
    amount = get_amount()  
    category = get_category() 
    description = get_description() 

    #add the entry to the csv file
    CSV.add_entry(date, amount, category, description)



def main():
    while True:
        print("\n1. Add a new transaction")
        print("2. View transactions and summary within a date range")
        print("3. Exit")
        choice = input("Enter your choice (1-3): ")

        if choice == "1":
            add()
        elif choice == "2":
            start_date =  get_date("Enter the start date (dd-mm-yyyy)")
            end_date =  get_date("Enter the end date (dd-mm-yyyy)")

            df = CSV.get_transactions(start_date, end_date)

            if input("Do you want to see a plot? (y/n): ").lower() == 'y':
                #show graph
                plot_transactions(df)

                
        elif choice == "3":
            print("Exiting....")
            break
        else:
            print("Invalid choice, Enter 1, 2 or 3")    


def plot_transactions(df):
    #set index for row manipulation
    df.set_index("date", inplace=True)

    #income dataframe (df)
    income_df = df[df["category"] == "Income"].resample("D").sum().reindex(df.index, fill_value=0) #will create a row for the missing days, filling them with 0 value
    expense_df = df[df["category"] == "Expense"].resample("D").sum().reindex(df.index, fill_value=0)

    #graph
    plt.figure(figsize=(10, 5))
    plt.plot(income_df.index, income_df["amount"], label='Income', color='g') # x = date, y = amount
    plt.plot(expense_df.index, expense_df["amount"], label='Expense', color='r') # x = date, y = amount
    
    #graph settings
    plt.xlabel("Date")
    plt.ylabel("Amount")
    plt.title("Income and Expenses over time")
    plt.legend()
    plt.grid(True)
    plt.show()

#init the app
if __name__ == "__main__":
    main()            


