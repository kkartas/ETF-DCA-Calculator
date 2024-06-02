import tkinter as tk
from tkinter import filedialog
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import mplcursors

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
    rate_per_period = average_interest / periods_per_year

    total_invested = initial_investment
    future_value = initial_investment
    future_values = [future_value]
    invested_values = [total_invested]

    for i in range(1, total_periods + 1):
        future_value = future_value * (1 + rate_per_period) + periodic_investment
        total_invested += periodic_investment
        future_values.append(future_value)
        invested_values.append(total_invested)

    profit = future_value - total_invested
    return total_invested, future_value, profit, future_values, invested_values

class DoubleSlider(tk.Canvas):
    def __init__(self, master, from_, to, initial_low, initial_high, **kwargs):
        super().__init__(master, **kwargs)
        self.from_ = from_
        self.to = to
        self.low = initial_low
        self.high = initial_high
        self.width = 320  # Adjusted for space at the ends
        self.height = 60
        self.slider_width = self.width - 40  # Adjusted for space at the ends

        self.low_var = tk.StringVar(value=self.format_date(self.low))
        self.high_var = tk.StringVar(value=self.format_date(self.high))

        self.config(width=self.width, height=self.height)
        self.bind("<B1-Motion>", self.move_slider)
        self.bind("<Button-1>", self.move_slider)
        
        self.low_handle = None
        self.high_handle = None
        self.slider_line = None
        self.low_label = None
        self.high_label = None

        self.draw_slider()

    def draw_slider(self):
        self.delete("all")
        self.slider_line = self.create_line(20, self.height // 2, self.width - 20, self.height // 2, fill="lightgrey", width=2)
        self.low_handle = self.create_oval(self.get_x(self.low) - 10, self.height // 2 - 10, self.get_x(self.low) + 10, self.height // 2 + 10, fill="grey", outline="black", width=2)
        self.high_handle = self.create_oval(self.get_x(self.high) - 10, self.height // 2 - 10, self.get_x(self.high) + 10, self.height // 2 + 10, fill="grey", outline="black", width=2)
        self.low_label = self.create_text(self.get_x(self.low), self.height // 2 + 20, text=self.format_date(self.low), fill="black")
        self.high_label = self.create_text(self.get_x(self.high), self.height // 2 + 20, text=self.format_date(self.high), fill="black")
        self.update_slider_line()

    def format_date(self, value):
        year = int(value)
        month = int((value - year) * 12) + 1
        return f"{month:02d}-{year}"

    def get_month(self, value):
        return int((value - int(value)) * 12) + 1

    def get_x(self, value):
        if self.to == self.from_:
            return 20
        return 20 + (value - self.from_) / (self.to - self.from_) * self.slider_width

    def get_value(self, x):
        return self.from_ + (x - 20) / self.slider_width * (self.to - self.from_)

    def move_slider(self, event):
        x = event.x
        if x < 20:
            x = 20
        elif x > self.width - 20:
            x = self.width - 20

        value = self.get_value(x)

        if abs(value - self.low) < abs(value - self.high):
            self.low = min(value, self.high - 1 / 12)
            self.low_var.set(self.format_date(self.low))
        else:
            self.high = max(value, self.low + 1 / 12)
            self.high_var.set(self.format_date(self.high))

        self.draw_slider()

    def update_slider_line(self):
        self.coords(self.slider_line, self.get_x(self.low), self.height // 2, self.get_x(self.high), self.height // 2)
        self.coords(self.low_label, self.get_x(self.low), self.height // 2 + 20)
        self.itemconfig(self.low_label, text=self.format_date(self.low))
        self.coords(self.high_label, self.get_x(self.high), self.height // 2 + 20)
        self.itemconfig(self.high_label, text=self.format_date(self.high))

    def get(self):
        return self.low, self.high

class DCAApp:
    def __init__(self, root):
        self.root = root
        self.root.title("DCA ETF Calculator")

        self.file_path = None
        self.df = None
        self.start_year = None
        self.end_year = None

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
        self.period_label = tk.Label(root, text="Period:")
        self.period_label.pack()
        
        self.period_var = tk.StringVar(value='daily')
        self.daily_radio = tk.Radiobutton(root, text="Daily", variable=self.period_var, value='daily')
        self.daily_radio.pack()
        self.monthly_radio = tk.Radiobutton(root, text="Monthly", variable=self.period_var, value='monthly')
        self.monthly_radio.pack()
        self.yearly_radio = tk.Radiobutton(root, text="Yearly", variable=self.period_var, value='yearly')
        self.yearly_radio.pack()

        # Years Selection
        self.years_label = tk.Label(root, text="Select Period (Years and Months) for Interest Calculation:")
        self.years_label.pack()

        self.year_slider_frame = tk.Frame(root)
        self.year_slider_frame.pack(fill=tk.X, expand=True)
        self.year_slider = DoubleSlider(self.year_slider_frame, from_=0, to=1, initial_low=0, initial_high=1)
        self.year_slider.pack(pady=10)

        # Slider Text Entries
        self.slider_text_frame = tk.Frame(root)
        self.slider_text_frame.pack(fill=tk.X, expand=True)
        self.low_label_text = tk.Label(self.slider_text_frame, text="Start Month-Year:")
        self.low_label_text.pack(side=tk.LEFT, padx=5)
        self.low_entry = tk.Entry(self.slider_text_frame, textvariable=self.year_slider.low_var)
        self.low_entry.pack(side=tk.LEFT, padx=5)
        self.high_label_text = tk.Label(self.slider_text_frame, text="End Month-Year:")
        self.high_label_text.pack(side=tk.LEFT, padx=5)
        self.high_entry = tk.Entry(self.slider_text_frame, textvariable=self.year_slider.high_var)
        self.high_entry.pack(side=tk.LEFT, padx=5)

        # Total Years
        self.total_years_label = tk.Label(root, text="Total Years for Investment Calculation:")
        self.total_years_label.pack()
        self.total_years_entry = tk.Entry(root)
        self.total_years_entry.pack()

        # Calculate Button
        self.calculate_button = tk.Button(root, text="Calculate", command=self.calculate)
        self.calculate_button.pack()

        # Result Label
        self.result_label = tk.Label(root, text="")
        self.result_label.pack()

    def load_file(self):
        self.file_path = filedialog.askopenfilename()
        self.df = read_csv(self.file_path)
        self.start_year = self.df.index.min()
        self.end_year = self.df.index.max()
        self.year_slider.from_ = self.start_year.year + (self.start_year.month - 1) / 12
        self.year_slider.to = self.end_year.year + (self.end_year.month - 1) / 12
        self.year_slider.low = self.year_slider.from_
        self.year_slider.high = self.year_slider.to
        self.year_slider.low_var.set(self.year_slider.format_date(self.year_slider.from_))
        self.year_slider.high_var.set(self.year_slider.format_date(self.year_slider.to))
        self.year_slider.draw_slider()

    def calculate(self):
        initial_investment = float(self.initial_entry.get())
        periodic_investment = float(self.periodic_entry.get())
        period = self.period_var.get()
        years = int(self.total_years_entry.get())

        start_year, end_year = self.year_slider.get()

        start_date = pd.to_datetime(f"{int(start_year)}-{self.year_slider.get_month(start_year):02d}-01")
        end_date = pd.to_datetime(f"{int(end_year)}-{self.year_slider.get_month(end_year):02d}-01") + pd.DateOffset(months=1) - pd.DateOffset(days=1)

        selected_df = self.df[(self.df.index >= start_date) & (self.df.index <= end_date)]
        average_interest = calculate_average_interest(selected_df)
        
        total_invested, future_value, profit, future_values, invested_values = dca_calculation(
            initial_investment, periodic_investment, period, years, average_interest
        )
        
        result_text = f"Average Annual Interest Rate: {average_interest*100:.2f}%\n"
        result_text += f"Total Invested: ${total_invested:,.2f}\n"
        result_text += f"Future Value: ${future_value:,.2f}\n"
        result_text += f"Profit: ${profit:,.2f}"
        self.result_label.config(text=result_text)
        
        file_name = self.file_path.split("/")[-1].replace(".csv", "")
        self.plot_results(future_values, invested_values, years, file_name)

    def plot_results(self, future_values, invested_values, years, file_name):
        total_periods = len(future_values) - 1
        years_labels = np.linspace(0, years, num=total_periods + 1)

        plt.figure()
        plt.plot(years_labels, future_values, label='Future Value')
        plt.plot(years_labels, invested_values, label='Total Invested', linestyle='--')
        plt.xlabel('Years')
        plt.ylabel('Money ($)')
        plt.title(f'DCA Investment Growth - {file_name}')
        plt.legend()
        plt.grid(True)

        # Add tooltips
        cursor = mplcursors.cursor(hover=True)
        @cursor.connect("add")
        def on_add(sel):
            year_index = int(sel.target.index)
            year_fraction = years_labels[year_index]
            year = int(year_fraction)
            month = int((year_fraction - year) * 12) + 1
            sel.annotation.set(text=f"Month-Year: {month:02d}-{year}\nFuture Value: ${future_values[year_index]:,.2f}\nInvested: ${invested_values[year_index]:,.2f}")

        plt.show()

if __name__ == "__main__":
    root = tk.Tk()
    app = DCAApp(root)
    root.mainloop()
