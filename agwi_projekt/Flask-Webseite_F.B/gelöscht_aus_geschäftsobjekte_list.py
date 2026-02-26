# Initialize data
halle_hashmap = {}
user_hashmap = {}
trainer_hashmap = {}
bewertung_hashmap = {}

adresse1 = Adresse(adresseId=1, name="Hauptstraße 123")
bewertung1 = Bewertung(bewertungId=1, name="Bewertung1", points=5, text="Toll")
halle1 = Halle(halleId=1, name="Fitness Zentrum A", opening_time=datetime(2024, 12, 14, 8, 0), address=adresse1, bewertung=bewertung1)
user1 = User(userid=1, name="Max Mustermann", email="max@example.com", password="securepassword")
trainer1 = Trainer(trainerId=1, name="John Doe", email="john.doe@example.com", image_url="https://www.gabriel-clemens.de/wp-content/uploads/2022/10/ursd_gabriel_clemens_unterseite_531x567px_saardartsgala117_rgb_72dpi_frei_ret.png"  , birthday=datetime(1990, 5, 15), bewertung=bewertung1)

# Populate hashmaps
halle_hashmap[halle1.halleId] = halle1
user_hashmap[user1.userid] = user1
trainer_hashmap[trainer1.trainerId] = trainer1
bewertung_hashmap[bewertung1.bewertungId] = bewertung1

# Print and iterate over hashmaps
print(halle_hashmap[1])
print(user_hashmap[1])
print(trainer_hashmap[1])
print(bewertung_hashmap[1])

if 1 in halle_hashmap:
    print("Halle mit ID 1 gefunden")

for halle_id, halle_obj in halle_hashmap.items():
    print(f"Halle ID: {halle_id}, Name: {halle_obj.name}")

for user_id, user_obj in user_hashmap.items():
    print(f"User ID: {user_id}, Name: {user_obj.name}")

for trainer_id, trainer_obj in trainer_hashmap.items():
    print(f"Trainer ID: {trainer_id}, Name: {trainer_obj.name}")

for bewertung_id, bewertung_obj in bewertung_hashmap.items():
    print(f"Bewertung ID: {bewertung_id}, Name: {bewertung_obj.name}")