# web_scraper.py
import requests
from bs4 import BeautifulSoup
from prettytable import PrettyTable
import pandas as pd

def main():
    data = get_exchange_rates()
    export_CSV(data)
    print_exchange_rates(data)
    currency_from, currency_to, currency_amount = get_user_inputs(data)
    converted_currency_amount = convert_currency(data, currency_from, currency_to, currency_amount)
    print_converted_currency(currency_from, currency_to, currency_amount, converted_currency_amount)


def get_exchange_rates():
    url = "https://www.iban.com/exchange-rates"
    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'lxml')

    # Extracting the table data
    table = soup.find('table')
    table_rows = table.find_all('tr')

    data = []
    for row in table_rows:
        cols = row.find_all(['td', 'th'])
        cols = [col.text.strip() for col in cols]
        cols.pop(-1)
        data.append(cols)
    return data


def export_CSV(data):
    # Converting data to a pandas DataFrame
    df = pd.DataFrame(data[1:], columns=data[0])

    # Cleaning the DataFrame
    df = df.dropna()
    df = df.reset_index(drop=True)

    # Saving the DataFrame to a CSV file
    df.to_csv('exchange_rates.csv', index=False)


def print_exchange_rates(data):
    # Set headers
    t = PrettyTable(data[0])

    # Set rows
    for rows in data[1:]:
        t.add_row(rows)

    print(t)


def get_user_inputs(data):
    # Ask user input for continuation
    print("-------------------------------------------")
    print("Would you like to convert currencies? Y/N")
    print("-------------------------------------------")
    while True:
        isContinue = input().capitalize()
        if isContinue == "Y":
            break
        elif isContinue == "N":
            return
        else:
            print("ERROR, wrong input. Input:- Y/N")

    # Get list of currency codes to validate user input
    currency_codes = []
    for rows in data[1:]:
        currency_codes.append(rows[0])

    # Ask user input for currency to convert FROM
    print("-----------------------------------------------------------------------------")
    print("Please enter the 3 letter currency code to convert FROM. Ex: USD, CNY, SGD...")
    print("-----------------------------------------------------------------------------")
    while True:
        currency_from = input().upper()
        if currency_from in currency_codes:
            break
        else:
            print("ERROR, wrong input. Input the 3 letter currency code.")

    # Ask user input for currency to convert TO
    print("-----------------------------------------------------------------------------")
    print("Please enter the 3 letter currency code to convert TO. Ex: USD, CNY, SGD...")
    print("-----------------------------------------------------------------------------")
    while True:
        currency_to = input().upper()
        if currency_to in currency_codes:
            break
        else:
            print("ERROR, wrong input. Input the 3 letter currency code.")

    # Ask user input for currency amount
    print("-------------------------------------------------")
    print("Please enter the currency amount to be converted.")
    print("-------------------------------------------------")
    while True:
        currency_amount = input().upper()
        try:
            float(currency_amount)
            break
        except ValueError:
            print("ERROR, wrong input. Input the currency amount to be converted.")

    return(currency_from, currency_to, currency_amount)


def convert_currency(data, currency_from_code, currency_to_code, currency_amount):
    # Fetch values of currencies
    for rows in data:
        if rows[0] == currency_from_code:
            currency_from_value = rows[2]
        if rows[0] == currency_to_code:
            currency_to_value = rows[2]

    converted_currency_amount = float(currency_from_value) * float(currency_to_value) * float(currency_amount)
    return(converted_currency_amount)


def print_converted_currency(currency_from, currency_to, currency_amount, converted_currency_amount):
    print("-------------------------------")
    print(f"{currency_amount} {currency_from} = {converted_currency_amount} {currency_to}")
    print("-------------------------------")

main()

# take 3 inputs from user:- input currency, output currency and amount to be exchanged. Perform function and return value