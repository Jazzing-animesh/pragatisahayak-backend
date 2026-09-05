from numbers import Real


def validate_required_fields(data, fields):
    for field in fields:
        value = data.get(field) if isinstance(data, dict) else None
        if value is None or (isinstance(value, str) and not value.strip()):
            return False, f"Missing field: {field}"
    return True, None


def validate_numeric(value, min_val, max_val, field_name):
    if isinstance(value, bool) or not isinstance(value, Real):
        return False, f"{field_name} must be a number"
    if value < min_val or value > max_val:
        return False, f"{field_name} must be between {min_val} and {max_val}"
    return True, None


def sanitize_string(s, max_length=500):
    if s is None:
        return ""
    return str(s).strip()[:max_length]