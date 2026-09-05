from app import db


class State(db.Model):
    __tablename__ = "states"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    name_hi = db.Column(db.String(100))
    districts = db.relationship(
        "District",
        backref="state",
        cascade="all, delete-orphan",
        lazy=True,
    )

    def to_dict(self):
        return {"id": self.id, "name": self.name, "name_hi": self.name_hi}


class District(db.Model):
    __tablename__ = "districts"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    state_id = db.Column(db.Integer, db.ForeignKey("states.id"), nullable=False)
    lat = db.Column(db.Float)
    lng = db.Column(db.Float)
    blocks = db.relationship(
        "Block",
        backref="district",
        cascade="all, delete-orphan",
        lazy=True,
    )
    __table_args__ = (db.UniqueConstraint("name", "state_id", name="uq_district_state"),)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "state_id": self.state_id,
            "lat": self.lat,
            "lng": self.lng,
        }


class Block(db.Model):
    __tablename__ = "blocks"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    district_id = db.Column(db.Integer, db.ForeignKey("districts.id"), nullable=False)
    villages = db.relationship(
        "Village",
        backref="block",
        cascade="all, delete-orphan",
        lazy=True,
    )
    __table_args__ = (db.UniqueConstraint("name", "district_id", name="uq_block_district"),)

    def to_dict(self):
        return {"id": self.id, "name": self.name, "district_id": self.district_id}


class Village(db.Model):
    __tablename__ = "villages"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    block_id = db.Column(db.Integer, db.ForeignKey("blocks.id"), nullable=False)
    population = db.Column(db.Integer, default=3000)
    literacy_rate = db.Column(db.Float, default=60.0)
    primary_occupation = db.Column(db.String(100), default="Agriculture")
    nearest_city_km = db.Column(db.Float, default=15.0)
    lat = db.Column(db.Float)
    lng = db.Column(db.Float)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "block_id": self.block_id,
            "population": self.population,
            "literacy_rate": self.literacy_rate,
            "primary_occupation": self.primary_occupation,
            "nearest_city_km": self.nearest_city_km,
            "lat": self.lat,
            "lng": self.lng,
        }