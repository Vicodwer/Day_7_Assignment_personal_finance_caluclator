"""
Personal Finance Calculator with Part B (Stretch Goals)

- Indian number formatting (lakhs/crores) via format_inr()
- Compare two employees side-by-side
- Financial health score
"""

from typing import Dict


def format_inr(amount: float) -> str:
    """
    Format a number into Indian-style currency string with ₹ and lakh/crore grouping.
    Example: 1200000.5 -> '₹12,00,000.50'
    """
    sign = "-" if amount < 0 else ""
    amt = abs(round(amount, 2))
    integer_str, decimal_str = f"{amt:.2f}".split(".")
    if len(integer_str) <= 3:
        grouped = integer_str
    else:
        last3 = integer_str[-3:]
        rest = integer_str[:-3]
        parts = []
        while len(rest) > 2:
            parts.insert(0, rest[-2:])
            rest = rest[:-2]
        if rest:
            parts.insert(0, rest)
        grouped = ",".join(parts) + "," + last3
    return f"{sign}₹{grouped}.{decimal_str}"


def get_valid_float(prompt: str, min_value: float = None, max_value: float = None) -> float:
    """(Re-used) Prompt the user for a float input and validate range if provided."""
    while True:
        try:
            value = float(input(prompt))
            if min_value is not None and value < min_value:
                print(f"Value must be >= {min_value}. Please try again.")
                continue
            if max_value is not None and value > max_value:
                print(f"Value must be <= {max_value}. Please try again.")
                continue
            return value
        except ValueError:
            print("Please enter a valid numeric value.")


def calculate_tax(amount: float, tax_percentage: float) -> float:
    """Calculate tax amount based on percentage."""
    return amount * tax_percentage / 100.0


def calculate_savings(net_salary: float, savings_percentage: float) -> float:
    """Calculate savings amount from net salary."""
    return net_salary * savings_percentage / 100.0


def financial_health_score(net_monthly_salary: float,
                           monthly_rent: float,
                           savings_amount: float,
                           weight_rent: float = 0.5,
                           weight_savings: float = 0.5) -> int:
    """
    Return 0-100 health score based on rent ratio and savings ratio.
    Default weights: 50% rent, 50% savings.
    """
    if net_monthly_salary <= 0:
        return 0

    rent_ratio = monthly_rent / net_monthly_salary
    savings_ratio = savings_amount / net_monthly_salary

    # Rent component: ideal <= 30% of net
    rent_component = max(0.0, (0.3 - rent_ratio) / 0.3) * 100.0

    # Savings component: ideal >= 20% of net
    savings_component = min(savings_ratio / 0.2, 1.0) * 100.0

    total_w = weight_rent + weight_savings
    w_r = weight_rent / total_w
    w_s = weight_savings / total_w

    score = int(round(rent_component * w_r + savings_component * w_s))
    return max(0, min(100, score))


def collect_employee_finances() -> Dict:
    """Collect inputs for an employee and compute monthly & annual figures."""
    name = input("Enter employee name: ").strip() or "Unknown"

    annual_salary = get_valid_float("Enter annual salary: ", min_value=0.01)

    tax_percentage = get_valid_float("Enter tax bracket percentage (0-50): ", min_value=0.0, max_value=50.0)

    monthly_rent = get_valid_float("Enter monthly rent: ", min_value=0.0)

    savings_percentage = get_valid_float("Enter savings goal percentage (0-100): ", min_value=0.0, max_value=100.0)

    monthly_salary = annual_salary / 12.0
    monthly_tax = calculate_tax(monthly_salary, tax_percentage)
    net_monthly_salary = monthly_salary - monthly_tax
    savings_amount = calculate_savings(net_monthly_salary, savings_percentage)
    rent_ratio = (monthly_rent / net_monthly_salary) * 100.0 if net_monthly_salary > 0 else 0.0
    disposable_income = net_monthly_salary - monthly_rent - savings_amount

    annual_tax = monthly_tax * 12.0
    annual_rent = monthly_rent * 12.0
    annual_savings = savings_amount * 12.0

    health_score = financial_health_score(net_monthly_salary, monthly_rent, savings_amount)

    return {
        "name": name,
        "annual_salary": annual_salary,
        "monthly_salary": monthly_salary,
        "monthly_tax": monthly_tax,
        "net_monthly_salary": net_monthly_salary,
        "monthly_rent": monthly_rent,
        "rent_ratio_percent": rent_ratio,
        "savings_percentage": savings_percentage,
        "savings_amount": savings_amount,
        "disposable_income": disposable_income,
        "annual_tax": annual_tax,
        "annual_rent": annual_rent,
        "annual_savings": annual_savings,
        "health_score": health_score,
        "tax_percentage": tax_percentage,
    }


def print_side_by_side(emp1: Dict, emp2: Dict) -> None:
    """Print a side-by-side comparison of two employee financial summaries."""
    col_width = 30
    label = lambda t: f"{t:<{col_width}}"
    left = lambda s: f"{s:<20}"
    right = lambda s: f"{s:>20}"

    def c(val):  # currency helper
        return format_inr(val)

    print("\n" + "=" * (col_width * 2 + 4))
    print(f"{'FIELD':<{col_width}}  |  EMPLOYEE A{'':<6}EMPLOYEE B")
    print("-" * (col_width * 2 + 4))

    rows = [
        ("Name", emp1["name"], emp2["name"]),
        ("Annual Salary", c(emp1["annual_salary"]), c(emp2["annual_salary"])),
        ("Monthly Gross", c(emp1["monthly_salary"]), c(emp2["monthly_salary"])),
        (f"Tax ({emp1['tax_percentage']:.1f}%)", c(emp1["monthly_tax"]), c(emp2["monthly_tax"])),
        ("Net Monthly", c(emp1["net_monthly_salary"]), c(emp2["net_monthly_salary"])),
        ("Monthly Rent", c(emp1["monthly_rent"]), c(emp2["monthly_rent"])),
        ("Rent (% of net)", f"{emp1['rent_ratio_percent']:.1f}%", f"{emp2['rent_ratio_percent']:.1f}%"),
        (f"Savings ({emp1['savings_percentage']:.1f}%)", c(emp1["savings_amount"]), c(emp2["savings_amount"])),
        ("Disposable Monthly", c(emp1["disposable_income"]), c(emp2["disposable_income"])),
        ("Annual Tax", c(emp1["annual_tax"]), c(emp2["annual_tax"])),
        ("Annual Savings", c(emp1["annual_savings"]), c(emp2["annual_savings"])),
        ("Annual Rent", c(emp1["annual_rent"]), c(emp2["annual_rent"])),
        ("Financial Health", f"{emp1['health_score']}/100", f"{emp2['health_score']}/100"),
    ]

    for label_text, a_val, b_val in rows:
        print(f"{label_text:<{col_width}} | {a_val:<20} {b_val:>20}")

    print("=" * (col_width * 2 + 4) + "\n")


def main_menu() -> None:
    """
    Main menu to choose single summary or compare two employees.
    """
    print("Personal Finance Calculator — Part B (Stretch Goals)\n")
    print("1) Single employee summary")
    print("2) Compare two employees")
    print("3) Exit")

    choice = input("Choose an option [1-3]: ").strip()
    if choice == "1":
        emp = collect_employee_finances()
        # print a formatted single summary (reuse print_financial_summary if available)
        print("\nDetailed Summary (single employee):")
        print("─" * 44)
        print(f"Employee : {emp['name']}")
        print(f"Annual Salary : {format_inr(emp['annual_salary'])}")
        print("─" * 44)
        print("Monthly Breakdown:")
        print(f"Gross Salary : {format_inr(emp['monthly_salary'])}")
        print(f"Tax ({emp['tax_percentage']:.1f}%) : {format_inr(emp['monthly_tax'])}")
        print(f"Net Salary : {format_inr(emp['net_monthly_salary'])}")
        print(f"Rent : {format_inr(emp['monthly_rent'])} ({emp['rent_ratio_percent']:.1f}% of net)")
        print(f"Savings ({emp['savings_percentage']:.1f}%) : {format_inr(emp['savings_amount'])}")
        print(f"Disposable : {format_inr(emp['disposable_income'])}")
        print("─" * 44)
        print("Annual Projection:")
        print(f"Total Tax : {format_inr(emp['annual_tax'])}")
        print(f"Total Savings : {format_inr(emp['annual_savings'])}")
        print(f"Total Rent : {format_inr(emp['annual_rent'])}")
        print("─" * 44)
        print(f"Financial Health Score: {emp['health_score']}/100\n")

    elif choice == "2":
        print("\nCollect data for Employee A:")
        emp_a = collect_employee_finances()
        print("\nCollect data for Employee B:")
        emp_b = collect_employee_finances()
        # print side-by-side
        print_side_by_side(emp_a, emp_b)

    else:
        print("Goodbye.")


if __name__ == "__main__":
    main_menu()