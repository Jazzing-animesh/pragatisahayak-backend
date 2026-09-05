from app import db
from app.models import Block, District, State, Village


LOCATION_DATA = [
    ("Uttar Pradesh", "उत्तर प्रदेश", [
        ("Lucknow", 26.85, 80.95, [("Malihabad", ["Gosainganj", "Kakori"]), ("Mohanlalganj", ["Nagram", "Sultanpur Kheda"])]),
        ("Kanpur", 26.45, 80.33, [("Bilhaur", ["Baraigarh", "Makanpur"]), ("Ghatampur", ["Kishunpur", "Parade"])]),
        ("Varanasi", 25.32, 83.01, [("Pindra", ["Babatpur", "Kathiraon"]), ("Sevapuri", ["Baraini", "Kashi Dehat"])]),
    ]),
    ("Madhya Pradesh", "मध्य प्रदेश", [
        ("Bhopal", 23.26, 77.41, [("Berasia", ["Barkheda Salam", "Khamkheda"]), ("Phanda", ["Kolar", "Ratibad"])]),
        ("Indore", 22.72, 75.86, [("Mhow", ["Gawli Palasia", "Kodariya"]), ("Depalpur", ["Gautampura", "Kshipra"])]),
        ("Jabalpur", 23.18, 79.99, [("Panagar", ["Barela", "Khamaria"]), ("Sihora", ["Gosalpur", "Khितौला"])]),
    ]),
    ("Rajasthan", "राजस्थान", [
        ("Jaipur", 26.91, 75.79, [("Amber", ["Jamwa Ramgarh", "Kho Nagoriyan"]), ("Sanganer", ["Bagru", "Chaksu"])]),
        ("Jodhpur", 26.24, 73.02, [("Luni", ["Doli", "Kakani"]), ("Bhopalgarh", ["Asop", "Balesar"])]),
        ("Udaipur", 24.59, 73.69, [("Girwa", ["Bhalon Ka Guda", "Jhamar Kotra"]), ("Mavli", ["Khamlighat", "Madar"])]),
    ]),
    ("Maharashtra", "महाराष्ट्र", [
        ("Mumbai", 19.08, 72.88, [("Borivali", ["Aarey", "Gorai"]), ("Kurla", ["Chunabhatti", "Vikhroli"])]),
        ("Pune", 18.52, 73.86, [("Haveli", ["Manjri", "Wadgaon"]), ("Mulshi", ["Paud", "Pirangut"])]),
        ("Nashik", 20.00, 73.79, [("Sinnar", ["Dapur", "Wavi"]), ("Igatpuri", ["Ghoti", "Vaitarna"])]),
    ]),
    ("Tamil Nadu", "தமிழ்நாடு", [
        ("Chennai", 13.08, 80.27, [("Ambattur", ["Mogappair", "Pattaravakkam"]), ("Sholinganallur", ["Karanaithangal", "Semmenchery"])]),
        ("Madurai", 9.93, 78.12, [("Melur", ["Alanganallur", "Keelavalavu"]), ("Thirumangalam", ["Kalligudi", "Tirumal"])]),
        ("Coimbatore", 11.02, 76.96, [("Pollachi", ["Anaimalai", "Kinathukadavu"]), ("Mettupalayam", ["Karamadai", "Sirumugai"])]),
    ]),
    ("Karnataka", "ಕರ್ನಾಟಕ", [
        ("Bangalore", 12.97, 77.59, [("Anekal", ["Bannerghatta", "Jigani"]), ("Devanahalli", ["Doddaballapur", "Yelahanka"])]),
        ("Mysore", 12.30, 76.66, [("Nanjangud", ["Hullahalli", "Suttur"]), ("Hunsur", ["Bilikere", "Gavadagere"])]),
        ("Hubli", 15.36, 75.12, [("Dharwad", ["Alnavar", "Garag"]), ("Kalghatgi", ["Dhummawad", "Tavaragera"])]),
    ]),
    ("Gujarat", "ગુજરાત", [
        ("Ahmedabad", 23.02, 72.57, [("Daskroi", ["Bopal", "Sanathal"]), ("Sanand", ["Nalsarovar", "Shela"])]),
        ("Surat", 21.17, 72.83, [("Choryasi", ["Dumas", "Vesu"]), ("Bardoli", ["Kadod", "Mota"])]),
        ("Vadodara", 22.31, 73.19, [("Savli", ["Desar", "Koyali"]), ("Padra", ["Mujpur", "Sokhda"])]),
    ]),
    ("West Bengal", "পশ্চিমবঙ্গ", [
        ("Kolkata", 22.57, 88.36, [("Bhangar", ["Bamanghata", "Chandaneswar"]), ("Bishnupur", ["Amtala", "Joka"])]),
        ("Howrah", 22.59, 88.31, [("Amta", ["Bagnan", "Udaynarayanpur"]), ("Uluberia", ["Jalalasi", "Shyampur"])]),
        ("Siliguri", 26.73, 88.40, [("Matigara", ["Dabgram", "Kawakhali"]), ("Naxalbari", ["Hatighisa", "Rangapani"])]),
    ]),
    ("Bihar", "बिहार", [
        ("Patna", 25.61, 85.14, [("Danapur", ["Bihta", "Maner"]), ("Phulwari", ["Gonpura", "Kurji"])]),
        ("Gaya", 24.79, 85.00, [("Tekari", ["Belaganj", "Paharpur"]), ("Bodh Gaya", ["Bodhgaya", "Dariyapur"])]),
        ("Muzaffarpur", 26.12, 85.39, [("Kanti", ["Madhopur", "Panapur"]), ("Sakra", ["Dihuli", "Muraul"])]),
    ]),
    ("Telangana", "తెలంగాణ", [
        ("Hyderabad", 17.39, 78.49, [("Shamshabad", ["Kothwalguda", "Narkhoda"]), ("Quthbullapur", ["Bachupally", "Dundigal"])]),
        ("Warangal", 17.97, 79.60, [("Hanamkonda", ["Hasanparthy", "Madikonda"]), ("Parkal", ["Narlapur", "Regonda"])]),
        ("Karimnagar", 18.44, 79.13, [("Huzurabad", ["Jammikunta", "Veenavanka"]), ("Manakondur", ["Ganneruvaram", "Kodimial"])]),
    ]),
    ("Andhra Pradesh", "ఆంధ్ర ప్రదేశ్", [
        ("Visakhapatnam", 17.69, 83.22, [("Bheemunipatnam", ["Nidigattu", "Sangivalasa"]), ("Anakapalle", ["Kasimkota", "Munagapaka"])]),
        ("Vijayawada", 16.51, 80.63, [("Gannavaram", ["Bapulapadu", "Kesarapalle"]), ("Mylavaram", ["G Konduru", "Ibrahimpatnam"])]),
        ("Tirupati", 13.63, 79.42, [("Chandragiri", ["Agaram", "Mungilipattu"]), ("Srikalahasti", ["Akkurthi", "Thondamanadu"])]),
    ]),
    ("Haryana", "हरियाणा", [
        ("Gurugram", 28.46, 77.03, [("Sohna", ["Bhondsi", "Ghamroj"]), ("Pataudi", ["Haily Mandi", "Jatauli"])]),
        ("Faridabad", 28.41, 77.31, [("Ballabgarh", ["Chhainsa", "Nangla Gujran"]), ("Tigaon", ["Mohna", "Palla"])]),
        ("Panipat", 29.39, 76.97, [("Samalkha", ["Chulkana", "Dhanana"]), ("Israna", ["Bal Jattan", "Nara"])]),
    ]),
    ("Punjab", "ਪੰਜਾਬ", [
        ("Ludhiana", 30.90, 75.85, [("Jagraon", ["Agwar Gujjran", "Sidhwan Bet"]), ("Samrala", ["Khatra", "Machhiwara"])]),
        ("Amritsar", 31.63, 74.87, [("Ajnala", ["Chogawan", "Lopoke"]), ("Majitha", ["Kathunangal", "Tarn Taran Road"])]),
        ("Jalandhar", 31.33, 75.58, [("Nakodar", ["Lohian Khas", "Shankar"]), ("Phillaur", ["Goraya", "Apra"])]),
    ]),
    ("Odisha", "ଓଡ଼ିଶା", [
        ("Bhubaneswar", 20.30, 85.82, [("Balianta", ["Benupur", "Kantilo"]), ("Jatni", ["Kantia", "Retang"])]),
        ("Cuttack", 20.46, 85.88, [("Niali", ["Bodhanga", "Kantapada"]), ("Salepur", ["Chandradeipur", "Madhuban"])]),
        ("Rourkela", 22.26, 84.85, [("Panposh", ["Bondamunda", "Jalda"]), ("Birmitrapur", ["Kuanrmunda", "Raiboga"])]),
    ]),
    ("Jharkhand", "झारखंड", [
        ("Ranchi", 23.34, 85.31, [("Kanke", ["Boreya", "Hesal"]), ("Namkum", ["Dumardaga", "Sithio"])]),
        ("Jamshedpur", 22.80, 86.20, [("Golmuri", ["Birsanagar", "Mango"]), ("Potka", ["Haldipokhar", "Kalika Pur"])]),
        ("Dhanbad", 23.79, 86.43, [("Baghmara", ["Kenduadih", "Mahuda"]), ("Nirsa", ["Chirkunda", "Mugma"])]),
    ]),
    ("Chhattisgarh", "छत्तीसगढ़", [
        ("Raipur", 21.25, 81.63, [("Abhanpur", ["Kharora", "Mana"]), ("Arang", ["Amlidih", "Raveli"])]),
        ("Bilaspur", 22.08, 82.15, [("Takhatpur", ["Bilha", "Kota"]), ("Masturi", ["Jairamnagar", "Sipat"])]),
        ("Durg", 21.19, 81.28, [("Patan", ["Amleshwar", "Jamul"]), ("Bhilai", ["Kumhari", "Utonai"])]),
    ]),
    ("Assam", "অসমীয়া", [
        ("Guwahati", 26.14, 91.74, [("Chandrapur", ["Sonapur", "Panikhaiti"]), ("Rani", ["Azara", "Garbhanga"])]),
        ("Jorhat", 26.75, 94.21, [("Titabor", ["Cinamara", "Meleng"]), ("Teok", ["Kaliapani", "Pulibor"])]),
        ("Dibrugarh", 27.47, 94.91, [("Chabua", ["Bogibeel", "Lahowal"]), ("Naharkatia", ["Namrup", "Tingrai"])]),
    ]),
    ("Kerala", "കേരളം", [
        ("Thiruvananthapuram", 8.52, 76.94, [("Nedumangad", ["Aryanad", "Vithura"]), ("Neyyattinkara", ["Kattakada", "Kollayil"])]),
        ("Kochi", 9.93, 76.27, [("Aluva", ["Choondy", "Kizhakkambalam"]), ("Kunnathunad", ["Perumbavoor", "Puthencruz"])]),
        ("Kozhikode", 11.26, 75.78, [("Koyilandy", ["Atholi", "Moodadi"]), ("Thamarassery", ["Kodenchery", "Omassery"])]),
    ]),
]


def seed():
    if State.query.first():
        print("Locations already seeded")
        return

    village_count = 0
    for state_name, state_name_hi, districts in LOCATION_DATA:
        state = State(name=state_name, name_hi=state_name_hi)
        db.session.add(state)
        for district_name, lat, lng, blocks in districts:
            district = District(name=district_name, lat=lat, lng=lng, state=state)
            db.session.add(district)
            for block_name, village_names in blocks:
                block = Block(name=block_name, district=district)
                db.session.add(block)
                for index, village_name in enumerate(village_names):
                    village = Village(
                        name=village_name,
                        block=block,
                        population=2400 + ((village_count * 137) % 7200),
                        literacy_rate=42.0 + ((village_count * 7) % 390) / 10,
                        primary_occupation=["Agriculture", "Labor", "Mixed", "Fishing"][village_count % 4],
                        nearest_city_km=3.0 + ((village_count * 11) % 43),
                        lat=lat + (index + 1) * 0.012,
                        lng=lng + (index + 1) * 0.012,
                    )
                    db.session.add(village)
                    village_count += 1

    db.session.commit()
    print(f"Seeded {len(LOCATION_DATA)} states, {len(LOCATION_DATA) * 3} districts, {village_count // 2} blocks, {village_count} villages")


if __name__ == "__main__":
    from app import create_app

    app = create_app()
    with app.app_context():
        seed()