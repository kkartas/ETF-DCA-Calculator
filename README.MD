# DCA ETF Calculator

This application calculates the potential earnings from Dollar-Cost Averaging (DCA) investments in ETFs. It uses historical data from Yahoo Finance and allows users to input their initial investment, periodic investment amount, investment frequency, and the total years for investment calculation.

## Features

- Load historical ETF data from a CSV file exported from Yahoo Finance.
- Input fields for initial investment, periodic investment amount, and investment frequency (daily, monthly, yearly).
- Select the period for interest calculation using a slider.
- Calculate and display the average annual interest rate, total invested amount, future value, and profit.
- Plot the investment growth over time with interactive tooltips.

## Requirements

- Python 3.6+
- Required Python libraries (listed in `requirements.txt`)

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/kkartas/dca-etf-calculator.git
    cd dca-etf-calculator
    ```

2. Create a virtual environment and activate it:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required libraries:
    ```bash
    pip install -r requirements.txt
    ```

4. Run the application:
    ```bash
    python etfdcacalc.py
    ```

## Usage

1. Launch the application.
2. Click the "Select CSV File" button to load your historical ETF data.
3. Enter the initial investment amount, periodic investment amount, and select the investment frequency.
4. Use the slider to select the period for interest calculation.
5. Enter the total years for the investment calculation.
6. Click the "Calculate" button to see the results and plot the investment growth.

## Downloading Data from Yahoo Finance

1. Visit [Yahoo Finance](https://finance.yahoo.com/).
2. In the search bar, type the ticker symbol of the ETF you want to download (e.g., `VUAA` for Vanguard S&P 500 UCITS ETF).
3. On the ETF's page, click on the "Historical Data" tab.
4. Select the desired time period for the data.
5. Click the "Apply" button.
6. Click the "Download" button to save the data as a CSV file.
7. Load this CSV file into the DCA ETF Calculator application.

## Example

Below is an example of how to use the application with a CSV file downloaded from Yahoo Finance:

1. Download the CSV file for `SPY` ETF from Yahoo Finance as described above.
2. Run the application and select the downloaded CSV file.
3. Enter the initial investment amount, periodic investment amount, and select the investment frequency (e.g., monthly).
4. Use the slider to select the period for interest calculation (e.g., from January 2015 to December 2020).
5. Enter the total years for the investment calculation (e.g., 10 years).
6. Click the "Calculate" button to see the results and the investment growth plot.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request or open an issue for any bugs or feature requests.

## Acknowledgments

- [Yahoo Finance](https://finance.yahoo.com/) for providing the historical data.