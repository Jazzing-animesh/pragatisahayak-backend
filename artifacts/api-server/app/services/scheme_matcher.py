"""Pure government-scheme eligibility matching."""


def _get(obj, name, default=None):
    if isinstance(obj, dict):
        return obj.get(name, default)
    return getattr(obj, name, default)


def _as_list(value, default):
    if value is None:
        return list(default)
    if isinstance(value, str):
        return [value]
    try:
        return list(value)
    except TypeError:
        return list(default)


def _to_dict(scheme):
    if hasattr(scheme, "to_dict"):
        result = scheme.to_dict()
        return dict(result) if isinstance(result, dict) else {}
    if isinstance(scheme, dict):
        return dict(scheme)
    return {}


def match_schemes(category_name, state_name, loan_amount, all_schemes=None):
    """Return active schemes eligible for a category, state, and loan amount.

    Args:
        category_name: Business category name to match.
        state_name: State name to match.
        loan_amount: Required loan amount in rupees.
        all_schemes: Iterable of scheme objects or dictionaries. Each scheme
            must expose active status, loan limits, and applicability lists.

    Returns:
        Eligible scheme dictionaries, sorted by subsidy percentage descending.
        Each result includes ``is_eligible`` and ``why_eligible``.
    """
    if not all_schemes:
        return []

    try:
        loan_amount = max(0.0, float(loan_amount))
    except (TypeError, ValueError):
        loan_amount = 0.0

    matched = []
    for scheme in all_schemes:
        if not _get(scheme, "is_active", False):
            continue

        try:
            min_loan = float(_get(scheme, "min_loan", 0))
            max_loan = float(_get(scheme, "max_loan", 0))
        except (TypeError, ValueError):
            continue
        if loan_amount < min_loan or loan_amount > max_loan:
            continue

        applicable_states = _as_list(_get(scheme, "applicable_states"), ["All"])
        if "All" not in applicable_states and state_name not in applicable_states:
            continue

        applicable_categories = _as_list(
            _get(scheme, "applicable_categories"), ["All"]
        )
        if "All" not in applicable_categories and category_name not in applicable_categories:
            continue

        try:
            subsidy_percent = max(0.0, float(_get(scheme, "subsidy_percent", 0)))
        except (TypeError, ValueError):
            subsidy_percent = 0.0

        reasons = [
            f"Loan amount ₹{loan_amount:,.0f} is within the "
            f"₹{min_loan:,.0f} - ₹{max_loan:,.0f} range."
        ]
        if subsidy_percent > 0:
            reasons.append(
                f"You get {subsidy_percent:g}% subsidy "
                f"(₹{loan_amount * subsidy_percent / 100:,.0f})."
            )
        if state_name in applicable_states:
            reasons.append(f"This scheme is specifically available in {state_name}.")

        scheme_dict = _to_dict(scheme)
        scheme_dict["is_eligible"] = True
        scheme_dict["why_eligible"] = " ".join(reasons)
        matched.append(scheme_dict)

    matched.sort(
        key=lambda item: float(item.get("subsidy_percent", 0) or 0), reverse=True
    )
    return matched