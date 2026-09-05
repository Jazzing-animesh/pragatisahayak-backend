"""Pure loan and amortization calculations."""


def _non_negative(value, default=0.0):
    try:
        return max(0.0, float(value))
    except (TypeError, ValueError):
        return float(default)


def _scheme_value(scheme, key, default):
    if isinstance(scheme, dict):
        return scheme.get(key, default)
    return getattr(scheme, key, default)


def calculate_emi(principal, annual_rate, tenure_years):
    """Calculate EMI and a year-by-year amortization schedule.

    Args:
        principal: Loan amount after subsidy in rupees.
        annual_rate: Annual interest rate as a percentage, such as ``10.5``.
        tenure_years: Loan tenure in years.

    Returns:
        ``(monthly_emi, quarterly_emi, total_interest, total_payment,
        amortization_list)``. Monetary values are rounded to two decimals.
    """
    principal = _non_negative(principal)
    annual_rate = _non_negative(annual_rate)
    try:
        tenure_years = int(tenure_years)
    except (TypeError, ValueError):
        tenure_years = 0

    if principal <= 0:
        return 0.0, 0.0, 0.0, 0.0, []
    if tenure_years <= 0:
        return round(principal, 2), round(principal * 3, 2), 0.0, round(principal, 2), []

    total_months = tenure_years * 12
    monthly_rate = (annual_rate / 12.0) / 100.0

    if monthly_rate == 0:
        monthly_emi = principal / total_months
        total_payment = principal
        total_interest = 0.0
    else:
        factor = (1 + monthly_rate) ** total_months
        monthly_emi = (principal * monthly_rate * factor) / (factor - 1)
        total_payment = monthly_emi * total_months
        total_interest = total_payment - principal

    quarterly_emi = monthly_emi * 3
    amortization = []
    balance = principal

    for year in range(1, tenure_years + 1):
        year_interest = 0.0
        year_principal = 0.0
        opening_balance = balance

        for _month in range(12):
            if balance <= 0:
                break
            interest_month = balance * monthly_rate
            principal_month = min(monthly_emi - interest_month, balance)
            if principal_month < 0:
                principal_month = 0.0
            balance -= principal_month
            year_interest += interest_month
            year_principal += principal_month

        amortization.append(
            {
                "year": year,
                "opening_balance": round(opening_balance, 2),
                "emi_paid": round(year_interest + year_principal, 2),
                "interest": round(year_interest, 2),
                "principal": round(year_principal, 2),
                "closing_balance": max(0.0, round(balance, 2)),
            }
        )
        if balance <= 0:
            break

    return (
        round(monthly_emi, 2),
        round(quarterly_emi, 2),
        round(total_interest, 2),
        round(total_payment, 2),
        amortization,
    )


def calculate_loan_details(investment, capital, scheme_dict):
    """Calculate required borrowing, subsidy, EMI, and loan readiness.

    Args:
        investment: Total estimated investment in rupees.
        capital: User's available margin money in rupees.
        scheme_dict: Mapping or object containing interest_rate,
            subsidy_percent, tenure_years, max_loan, and optionally min_loan.

    Returns:
        A dictionary with loan amounts, EMI values, amortization, and a
        readiness score from 0 to 100.
    """
    investment = _non_negative(investment)
    capital = _non_negative(capital)
    scheme_dict = scheme_dict or {}

    subsidy_percent = min(100.0, _non_negative(_scheme_value(scheme_dict, "subsidy_percent", 0)))
    interest_rate = _non_negative(_scheme_value(scheme_dict, "interest_rate", 10.0))
    tenure_years = max(0, int(_non_negative(_scheme_value(scheme_dict, "tenure_years", 5))))
    max_loan = _non_negative(_scheme_value(scheme_dict, "max_loan", 0))
    loan_needed = max(0.0, investment - capital)

    if loan_needed == 0:
        return {
            "loan_needed": 0,
            "subsidy_amount": 0,
            "effective_loan": 0,
            "monthly_emi": 0,
            "quarterly_emi": 0,
            "total_interest": 0,
            "total_payment": 0,
            "amortization": [],
            "loan_readiness_score": 100,
        }

    subsidy_amount = loan_needed * (subsidy_percent / 100.0)
    effective_loan = loan_needed - subsidy_amount
    monthly_emi, quarterly_emi, total_interest, total_payment, amortization = calculate_emi(
        effective_loan, interest_rate, tenure_years
    )

    margin_ratio = capital / investment if investment > 0 else 0
    if margin_ratio >= 0.25:
        readiness = 40
    elif margin_ratio >= 0.15:
        readiness = 30
    elif margin_ratio >= 0.10:
        readiness = 20
    else:
        readiness = 10

    if subsidy_percent >= 25:
        readiness += 30
    elif subsidy_percent > 0:
        readiness += 20
    else:
        readiness += 10

    readiness += 30 if effective_loan <= max_loan else 10

    return {
        "loan_needed": round(loan_needed, 2),
        "subsidy_amount": round(subsidy_amount, 2),
        "effective_loan": round(effective_loan, 2),
        "interest_rate": interest_rate,
        "tenure_years": tenure_years,
        "monthly_emi": monthly_emi,
        "quarterly_emi": quarterly_emi,
        "total_interest": total_interest,
        "total_payment": total_payment,
        "amortization": amortization,
        "loan_readiness_score": min(100, readiness),
    }