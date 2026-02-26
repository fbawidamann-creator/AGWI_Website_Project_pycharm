from geschaeftsobjekte import Adresse, Halle, Trainer, Bewertung
from datetime import datetime



halle_hashmap = {
    1: Halle(
        halleId=1,
        name="Halle 1",
        opening_time=datetime(2024, 12, 14, 8, 0),
        address=Adresse(adresseId=1, name="Hauptstraße 123"),
        image_url="https://www.merkur.de/assets/images/32/878/32878782-mit-blauem-teppichbelag-sind-die-plaetze-in-der-neuen-tennishalle-versehen-Q8BG.jpg",
        bewertung=Bewertung(bewertungId=1, name="Paul Anders", points=5, text="Great hall!"),


    )
}

trainer_hashmap = {
    1: Trainer(
        trainerId=1,
        name="Gabriel Clemens",
        email="gabrielclemens@web.de",
        image_url="https://www.gabriel-clemens.de/wp-content/uploads/2022/10/ursd_gabriel_clemens_unterseite_531x567px_saardartsgala117_rgb_72dpi_frei_ret.png",
        birthday="13.04.1988"

    )
}

def add_trainer_to_hashmap(trainerId, name, email, image_url, birthday):
    trainer_hashmap[trainerId] = Trainer(
        trainerId=trainerId,
        name=name,
        email=email,
        image_url=image_url,
        birthday=birthday
    )

def add_halle_to_hashmap(halleId, name, opening_time, address,  image_url, bewertung):
    halle_hashmap[halleId] = Halle(
        halleId=halleId,
        name=name,
        opening_time=opening_time,
        address=address,
        image_url=image_url,
        bewertung=bewertung


    )