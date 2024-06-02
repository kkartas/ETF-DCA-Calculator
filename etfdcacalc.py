import tkinter as tk
from tkinter import filedialog
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def read_csv(file_path):
    df = pd.read_csv(file_path)
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.set_index('Date')
    df = df.sort_index()
    return df

def calculate_average_interest(df):
    df['Return'] = df['Close'].pct_change()
    average_interest = df['Return'].mean() * 252  # Annualize the daily return
    return average_interest

def dca_calculation(initial_investment, periodic_investment, period, years, average_interest):
    periods_per_year = {'daily': 252, 'monthly': 12, 'yearly': 1}[period]
    total_periods = periods_per_year * years
    total_invested = initial_investment + periodic_investment * total_periods
    
    future_value = initial_investment * (1 + average_interest/periods_per_year)**total_periods
    for i in range(1, total_periods + 1):
        future_value += periodic_investment * (1 + average_interest/periods_per_year)**(total_periods - i)
    
    profit = future_value - total_invested
    return total_invested, future_value, profit

class DCAApp:
    def __init__(self, root):
        self.root = root
        self.root.title("DCA ETF Calculator")

        self.file_path = None
        self.df = None

        # File Selection
        self.select_file_button = tk.Button(root, text="Select CSV File", command=self.load_file)
        self.select_file_button.pack()

        # Initial Investment
        self.initial_label = tk.Label(root, text="Initial Investment:")
        self.initial_label.pack()
        self.initial_entry = tk.Entry(root)
        self.initial_entry.pack()

        # Periodic Investment
        self.periodic_label = tk.Label(root, text="Periodic Investment:")
        self.periodic_label.pack()
        self.periodic_entry = tk.Entry(root)
        self.periodic_entry.pack()

        # Period
        self.period_label = tk.Label(root, text="Period (daily, monthly, yearly):")
        self.period_label.pack()
        self.period_entry = tk.Entry(root)
        self.period_entry.pack()

        # Years
        self.years_label = tk.Label(root, text="Years:")
        self.years_label.pack()
        self.years_entry = tk.Entry(root)
        self.years_entry.pack()

        # Calculate Button
        self.calculate_button = tk.Button(root, text="Calculate", command=self.calculate)
        self.calculate_button.pack()

        # Result Label
        self.result_label = tk.Label(root, text="")
        self.result_label.pack()

    def load_file(self):
        self.file_path = filedialog.askopenfilename()
        self.df = read_csv(self.file_path)

    def calculate(self):
        initial_investment = float(self.initial_entry.get())
        periodic_investment = float(self.periodic_entry.get())
        period = self.period_entry.get()
        years = int(self.years_entry.get())
        
        average_interest = calculate_average_interest(self.df)
        total_invested, future_value, profit = dca_calculation(
            initial_investment, periodic_investment, period, years, average_interest
        )
        
        result_text = f"Total Invested: ${total_invested:.2f}\n"
        result_text += f"Future Value: ${future_value:.2f}\n"
        result_text += f"Profit: ${profit:.2f}"
        self.result_label.config(text=result_text)
        
        self.plot_results(initial_investment, periodic_investment, period, years, average_interest)

    def plot_results(self, initial_investment, periodic_investment, period, years, average_interest):
        periods_per_year = {'daily': 252, 'monthly': 12, 'yearly': 1}[period]
        total_periods = periods_per_year * years
        future_values = []

        future_value = initial_investment * (1 + average_interest/periods_per_year)**total_periods
        for i in range(1, total_periods + 1):
            future_value += periodic_investment * (1 + average_interest/periods_per_year)**(total_periods - i)
            future_values.append(future_value)

        plt.figure()
        plt.plot(range(total_periods), future_values, label='Future Value')
        plt.xlabel('Periods')
        plt.ylabel('Value')
        plt.title('DCA Investment Growth')
        plt.legend()
        plt.grid(True)
        plt.show()

if __name__ == "__main__":
    root = tk.Tk()
    app = DCAApp(root)
    root.mainloop()
