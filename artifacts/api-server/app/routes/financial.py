from flask import Blueprint, jsonify, request

financial_bp = Blueprint("financial", __name__, url_prefix="/api")


@financial_bp.post("/calculate-loan")
def calculate_loan():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "error": True,
            "message": "Request body must be a JSON object",
            "code": "INVALID_JSON",
        }), 400

    required = ["loan_amount", "interest_rate", "tenure_years"]

    for field in required:
        if field not in data:
            return jsonify({
                "error": True,
                "message": f"{field} is required",
                "code": "MISSING_FIELDS",
            }), 400

    try:
        principal = float(data["loan_amount"])
        annual_rate = float(data["interest_rate"])
        years = float(data["tenure_years"])
    except (TypeError, ValueError):
        return jsonify({
            "error": True,
            "message": "Loan amount, interest rate and tenure must be numbers",
            "code": "INVALID_FINANCIAL_DATA",
        }), 400

    if principal <= 0 or annual_rate < 0 or years <= 0:
        return jsonify({
            "error": True,
            "message": "Financial values must be valid positive numbers",
            "code": "INVALID_FINANCIAL_DATA",
        }), 400

    months = int(years * 12)
    monthly_rate = annual_rate / 12 / 100

    if monthly_rate == 0:
        emi = principal / months
    else:
        emi = (
            principal
            * monthly_rate
            * (1 + monthly_rate) ** months
            / ((1 + monthly_rate) ** months - 1)
        )

    total_payment = emi * months
    total_interest = total_payment - principal

    return jsonify({
        "loan_amount": principal,
        "interest_rate": annual_rate,
        "tenure_years": years,
        "monthly_emi": round(emi, 2),
        "total_payment": round(total_payment, 2),
        "total_interest": round(total_interest, 2),
    }), 200
