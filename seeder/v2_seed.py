import random, datetime
from faker import Faker
from utility_func import cur, insert_returning, table_exists, SEED

fake = Faker("ru_RU")

ROOMS_PER_HOTEL = 3
CNT_HOTELS = SEED
CNT_ROOMS = CNT_HOTELS * ROOMS_PER_HOTEL

CNT_AMENITIES = max(1, SEED // 10)
CNT_FACILITIES = max(1, SEED // 10)

CNT_USERS = SEED

CNT_LINK_HOTEL_AM = CNT_HOTELS
CNT_LINK_ROOM_FAC = CNT_ROOMS

def get_ids(table: str, column: str):
    cur.execute(f"SELECT {column} FROM {table}")
    return [r[0] for r in cur.fetchall()]

def seed_users():
    if not table_exists("users"):
        return []
    rows = [(fake.first_name(), fake.last_name(), fake.email(),
             fake.phone_number(), fake.user_name())
            for _ in range(CNT_USERS)]
    ids = insert_returning(
        "INSERT INTO users (name,second_name,email,phone,login) "
        "VALUES %s RETURNING user_id",
        rows, "user_id", "users"
    )
    print(f"users: {len(ids)}")
    return ids

def seed_rooms(hotel_ids):
    if not (hotel_ids and table_exists("room")):
        return []
    room_rows = []
    for hid in hotel_ids:
        for _ in range(ROOMS_PER_HOTEL):
            room_rows.append(
                (hid, random.randint(1, 4),
                 round(random.uniform(2000, 8000), 2),
                 fake.sentence(),
                 random.choice(["single", "double", "suite"]))
            )
    ids = insert_returning(
        "INSERT INTO room (hotel_id,capacity,price,description,room_type) "
        "VALUES %s RETURNING room_id",
        room_rows, "room_id", "room"
    )
    print(f"room: {len(ids)}")
    return ids

def seed_amenities(hotel_ids):
    if not (hotel_ids and table_exists("amenity") and table_exists("hotelamenity")):
        return
    amen_rows = [(fake.word(), fake.sentence()) for _ in range(CNT_AMENITIES)]
    amen_ids = insert_returning(
        "INSERT INTO amenity (amenity_name,amenity_description) "
        "VALUES %s RETURNING amenity_id",
        amen_rows, "amenity_id", "amenity"
    )
    bridge = [(random.choice(hotel_ids), random.choice(amen_ids))
              for _ in range(CNT_LINK_HOTEL_AM)]
    cur.execute("SET client_min_messages = warning")
    insert_returning(
        "INSERT INTO hotelamenity (hotel_id,amenity_id) VALUES %s "
        "ON CONFLICT DO NOTHING RETURNING hotel_id",
        bridge, "hotel_id", "hotelamenity"
    )
    print(f"amenity: {len(amen_ids)}, links: {len(bridge)}")

def seed_facilities(room_ids):
    if not (room_ids and table_exists("roomfacility") and table_exists("roomhasfacility")):
        return
    fac_rows = [(fake.word(), fake.sentence()) for _ in range(CNT_FACILITIES)]
    fac_ids = insert_returning(
        "INSERT INTO roomfacility (facility_name,facility_description) "
        "VALUES %s RETURNING facility_id",
        fac_rows, "facility_id", "roomfacility"
    )
    bridge = [(random.choice(room_ids), random.choice(fac_ids))
              for _ in range(CNT_LINK_ROOM_FAC)]
    insert_returning(
        "INSERT INTO roomhasfacility (room_id,facility_id) VALUES %s "
        "ON CONFLICT DO NOTHING RETURNING room_id",
        bridge, "room_id", "roomhasfacility"
    )
    print(f"roomfacility: {len(fac_ids)}, links: {len(bridge)}")

def run():
    hotel_ids = get_ids("hotel", "hotel_id")
    room_ids  = seed_rooms(hotel_ids)
    seed_amenities(hotel_ids)
    seed_facilities(room_ids)
    user_ids  = seed_users()
    return dict(users=user_ids, rooms=room_ids, hotels=hotel_ids)