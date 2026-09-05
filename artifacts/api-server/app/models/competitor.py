from app import db


class Competitor(db.Model):
    __tablename__ = "competitors"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    category_id = db.Column(
        db.Integer,
        db.ForeignKey("business_categories.id"),
        nullable=False,
    )
    village = db.Column(db.String(100), nullable=False)
    block_id = db.Column(db.Integer, db.ForeignKey("blocks.id"), nullable=False)
    distance_km = db.Column(db.Float, nullable=False)
    estimated_revenue = db.Column(db.BigInteger, nullable=False)
    years_active = db.Column(db.Integer, default=3, nullable=False)
    lat = db.Column(db.Float)
    lng = db.Column(db.Float)
    category = db.relationship("BusinessCategory", backref="competitors")
    block = db.relationship("Block", backref="competitors")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "category_id": self.category_id,
            "village": self.village,
            "block_id": self.block_id,
            "distance_km": self.distance_km,
            "estimated_revenue": self.estimated_revenue,
            "years_active": self.years_active,
            "lat": self.lat,
            "lng": self.lng,
        }