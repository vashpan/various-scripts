#!/usr/bin/env python3

# script to calculate appliance depreciation based on purchase date

from datetime import datetime

def calculate_value(initial_value: float, months_passed: int) -> float:
    if months_passed < 0:
        raise ValueError("months_passed must be non-negative")

    first_year_drop = 0.25  # 25% drop after first year
    annual_drop = 0.10      # 10% drop each additional year

    if months_passed <= 12:
        value = initial_value * (1 - first_year_drop * (months_passed / 12))
    else:
        value_after_first = initial_value * (1 - first_year_drop)
        additional_years = (months_passed - 12) / 12
        value = value_after_first * (1 - annual_drop * additional_years)

    return round(value, 2)

def months_between(d1: datetime, d2: datetime) -> int:
    """count number of full months between two dates"""
    return (d2.year - d1.year) * 12 + (d2.month - d1.month)

if __name__ == "__main__":
    try:
        initial = float(input("Enter initial equipment value (in PLN): "))
        purchase_date_str = input("Enter purchase date (YYYY-MM-DD): ")
        purchase_date = datetime.strptime(purchase_date_str, "%Y-%m-%d")
        today = datetime.today()

        months = months_between(purchase_date, today)
        current_value = calculate_value(initial, months)

        print(f"Months passed: {months}")
        print(f"Estimated current value: {current_value} PLN")
    except Exception as e:
        print(f"Error: {e}")