from app import db


class GovernmentScheme(db.Model):
    __tablename__ = "government_schemes"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True, nullable=False)
    ministry = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)
    max_loan = db.Column(db.BigInteger, nullable=False)
    min_loan = db.Column(db.BigInteger, default=0, nullable=False)
    interest_rate = db.Column(db.Float, nullable=False)
    subsidy_percent = db.Column(db.Float, default=0, nullable=False)
    tenure_years = db.Column(db.Integer, default=5, nullable=False)
    eligibility_criteria = db.Column(db.JSON, default=list, nullable=False)
    applicable_states = db.Column(db.JSON, default=lambda: ["All"], nullable=False)
    applicable_categories = db.Column(db.JSON, default=lambda: ["All"], nullable=False)
    application_url = db.Column(db.String(500))
    is_active = db.Column(db.Boolean, default=True, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "ministry": self.ministry,
            "description": self.description,
            "max_loan": self.max_loan,
            "min_loan": self.min_loan,
            "interest_rate": self.interest_rate,
            "subsidy_percent": self.subsidy_percent,
            "tenure_years": self.tenure_years,
            "eligibility_criteria": self.eligibility_criteria or [],
            "applicable_states": self.applicable_states or ["All"],
            "applicable_categories": self.applicable_categories or ["All"],
            "application_url": self.application_url,
            "is_active": self.is_active,
        }