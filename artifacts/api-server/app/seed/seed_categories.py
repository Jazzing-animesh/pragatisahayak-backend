from app import db
from app.models import BusinessCategory


CATEGORIES = [
    ("Flour Mill", "आटा चक्की", "Manufacturing", 200000, 500000, 25.0, "Medium", 12, "Grain sourcing, machine operation"),
    ("Dairy Farm", "डेयरी फार्म", "Manufacturing", 150000, 400000, 30.0, "Medium", 10, "Animal care, dairy hygiene"),
    ("Poultry Farm", "मुर्गी पालन", "Manufacturing", 100000, 300000, 20.0, "High", 8, "Poultry care, biosecurity"),
    ("Mobile Repair Shop", "मोबाइल रिपेयर", "Service", 50000, 200000, 40.0, "Low", 6, "Electronics repair, customer service"),
    ("Grocery Store", "किराना दुकान", "Trading", 100000, 300000, 15.0, "Low", 8, "Inventory management, retail"),
    ("Tailoring Unit", "सिलाई केंद्र", "Service", 50000, 150000, 35.0, "Low", 6, "Tailoring, garment finishing"),
    ("Oil Mill", "तेल मिल", "Manufacturing", 300000, 800000, 20.0, "Medium", 14, "Seed processing, machine operation"),
    ("Agarbatti Making", "अगरबत्ती निर्माण", "Manufacturing", 50000, 200000, 30.0, "Medium", 8, "Handcrafting, packaging"),
    ("Papad Making", "पापड़ निर्माण", "Manufacturing", 50000, 150000, 35.0, "Low", 6, "Food preparation, packaging"),
    ("Brick Kiln", "भट्ठा", "Manufacturing", 500000, 1500000, 25.0, "High", 18, "Clay preparation, kiln operation"),
]


def seed():
    if BusinessCategory.query.first():
        print("Business categories already seeded")
        return

    for (
        name,
        name_hi,
        sector,
        investment_min,
        investment_max,
        typical_margin,
        risk_level,
        breakeven_months,
        required_skills,
    ) in CATEGORIES:
        db.session.add(
            BusinessCategory(
                name=name,
                name_hi=name_hi,
                sector=sector,
                investment_min=investment_min,
                investment_max=investment_max,
                typical_margin=typical_margin,
                risk_level=risk_level,
                breakeven_months=breakeven_months,
                required_skills=required_skills,
            )
        )

    db.session.commit()
    print(f"Seeded {len(CATEGORIES)} business categories")


if __name__ == "__main__":
    from app import create_app

    app = create_app()
    with app.app_context():
        seed()