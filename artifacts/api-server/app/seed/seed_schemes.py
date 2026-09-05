from app import db
from app.models import GovernmentScheme


SCHEMES = [
    ("PMEGP", "Ministry of MSME", 5000000, 50000, 10.5, 25, 5, [], ["All"], ["All"], "https://www.kviconline.gov.in/pmegpportal/"),
    ("PMMY Mudra", "Ministry of Finance", 1000000, 10000, 10, 0, 5, [], ["All"], ["All"], "https://www.mudra.org.in/"),
    ("Stand-Up India", "Ministry of Finance", 10000000, 1000000, 8.5, 0, 7, ["SC/ST/Women entrepreneurs only"], ["All"], ["All"], "https://www.standupmitra.in/"),
    ("PMFME", "Ministry of Food Processing", 1000000, 50000, 9, 35, 5, [], ["All"], ["Flour Mill", "Oil Mill", "Papad Making", "Agarbatti Making"], "https://pmfme.mofpi.gov.in/"),
    ("AIF", "Ministry of Agriculture", 20000000, 100000, 7, 3, 7, [], ["All"], ["Dairy Farm", "Poultry Farm", "Flour Mill", "Oil Mill"], "https://agriinfra.dac.gov.in/"),
    ("DAY-NRLM", "Ministry of Rural Development", 1000000, 10000, 7, 3, 5, [], ["All"], ["All"], "https://nrlm.gov.in/"),
    ("CGTMSE", "Ministry of MSME", 20000000, 100000, 10, 0, 5, ["Collateral-free guarantee cover"], ["All"], ["All"], "https://www.cgtmse.in/"),
    ("ASPIRE", "Ministry of MSME", 5000000, 100000, 9, 30, 5, [], ["All"], ["All"], "https://aspire.msme.gov.in/"),
    ("SFURTI", "Ministry of MSME", 5000000, 500000, 0, 100, 5, ["Traditional industry clusters"], ["All"], ["Agarbatti Making", "Papad Making", "Tailoring Unit"], "https://sfurti.msme.gov.in/"),
    ("PM-DAKSH", "Ministry of Social Justice", 500000, 10000, 8, 50, 5, ["SC/ST/OBC entrepreneurs"], ["All"], ["All"], "https://pmdaksh.dosje.gov.in/"),
    ("NABARD Agri-Clinics", "NABARD", 2000000, 100000, 8, 36, 7, [], ["All"], ["Dairy Farm", "Poultry Farm"], "https://www.nabard.org/"),
    ("KVIC Margin Money", "KVIC", 2500000, 50000, 9, 25, 5, [], ["All"], ["All"], "https://www.kvic.org.in/"),
    ("UP Mukhyamantri Yuva Swarozgar", "UP Government", 2500000, 50000, 9, 25, 5, [], ["Uttar Pradesh"], ["All"], "https://upmsme.in/"),
    ("MP Mukhyamantri Udyam Kranti", "MP Government", 5000000, 100000, 8, 30, 5, [], ["Madhya Pradesh"], ["All"], "https://msme.mp.gov.in/"),
    ("RJ Bhamashah Rojgar Srijan", "RJ Government", 1000000, 25000, 9, 25, 5, [], ["Rajasthan"], ["All"], "https://industries.rajasthan.gov.in/"),
    ("NULM", "Ministry of Housing", 200000, 10000, 7, 5, 3, ["Urban poor", "SHG members"], ["All"], ["All"], "https://nulm.gov.in/"),
]


def seed():
    if GovernmentScheme.query.first():
        print("Government schemes already seeded")
        return

    for (
        name,
        ministry,
        max_loan,
        min_loan,
        interest_rate,
        subsidy_percent,
        tenure_years,
        eligibility_criteria,
        applicable_states,
        applicable_categories,
        application_url,
    ) in SCHEMES:
        db.session.add(
            GovernmentScheme(
                name=name,
                ministry=ministry,
                description=f"{name} support for eligible rural entrepreneurs.",
                max_loan=max_loan,
                min_loan=min_loan,
                interest_rate=interest_rate,
                subsidy_percent=subsidy_percent,
                tenure_years=tenure_years,
                eligibility_criteria=eligibility_criteria,
                applicable_states=applicable_states,
                applicable_categories=applicable_categories,
                application_url=application_url,
                is_active=True,
            )
        )

    db.session.commit()
    print(f"Seeded {len(SCHEMES)} government schemes")


if __name__ == "__main__":
    from app import create_app

    app = create_app()
    with app.app_context():
        seed()