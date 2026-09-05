from app import db


class BusinessCategory(db.Model):
    __tablename__ = "business_categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    name_hi = db.Column(db.String(100))
    sector = db.Column(db.String(30), nullable=False)
    investment_min = db.Column(db.BigInteger, nullable=False)
    investment_max = db.Column(db.BigInteger, nullable=False)
    typical_margin = db.Column(db.Float, nullable=False)
    risk_level = db.Column(db.String(20), nullable=False)
    breakeven_months = db.Column(db.Integer, nullable=False)
    required_skills = db.Column(db.Text)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "name_hi": self.name_hi,
            "sector": self.sector,
            "investment_min": self.investment_min,
            "investment_max": self.investment_max,
            "typical_margin": self.typical_margin,
            "risk_level": self.risk_level,
            "breakeven_months": self.breakeven_months,
            "required_skills": self.required_skills,
        }