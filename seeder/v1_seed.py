from faker import Faker
import random
from utility_func import cur, insert_returning, table_exists, SEED

fake = Faker("ru_RU")
ROOMS_PER_HOTEL = 3
CNT_HOTELS = SEED
CNT_PARTNERS = SEED
CNT_ROOMS = CNT_HOTELS * ROOMS_PER_HOTEL

CNT_AMENITIES = max(1, SEED // 10)
CNT_FACILITIES = max(1, SEED // 10)

CNT_USERS = SEED

CNT_LINK_HOTEL_AM = CNT_HOTELS
CNT_LINK_ROOM_FAC = CNT_ROOMS
def seed_partnertypes():
    if not table_exists("partnertype"):
        return []
    rows = [("HotelOwner","Владелец"), ("Agency","Агентство"), ("Corp","Корп-клиент")]
    return insert_returning(
        """INSERT INTO partnertype(type_name,description)
           VALUES %s ON CONFLICT DO NOTHING RETURNING partner_type_id""",
        rows, "partner_type_id", "partnertype")

def seed_partners(ptype_ids):
    if not ptype_ids or not table_exists("partner"):
        return []
    rows = [(fake.first_name(), fake.last_name(), fake.email(),
             fake.phone_number(), fake.user_name(), random.choice(ptype_ids))
            for _ in range(CNT_PARTNERS)]
    return insert_returning(
        """INSERT INTO partner(name,second_name,email,phone,login,partner_type_id)
           VALUES %s RETURNING partner_id""",
        rows, "partner_id", "partner")

def seed_hotels(partner_ids):
    if not partner_ids or not table_exists("hotel"):
        return []
    rows = [(random.choice(partner_ids), fake.company(),
             fake.address().replace("\n",", "), fake.city(),
             fake.phone_number(), fake.company_email(),
             fake.catch_phrase(), random.randint(1,5))
            for _ in range(CNT_HOTELS)]
    return insert_returning(
        """INSERT INTO hotel(partner_id,hotel_name,address,city,
                              phone,email,description,rating)
           VALUES %s RETURNING hotel_id""",
        rows, "hotel_id", "hotel")

def run():
    pt_ids = seed_partnertypes()
    p_ids  = seed_partners(pt_ids)
    h_ids  = seed_hotels(p_ids)
    return dict(partner_types=pt_ids, partners=p_ids, hotels=h_ids)