import random, datetime
from faker import Faker
from utility_func import cur, insert_returning, table_exists, SEED

fake = Faker("ru_RU")

CNT_BOOKINGS = SEED
CNT_PAYMENT_LINKS = SEED
CNT_ADD_SERVICES  = max(1, SEED // 10)
CNT_LINK_BOOK_SVC = CNT_BOOKINGS
TX_PER_ACCOUNT    = max(1, SEED // 20)

def get_ids(table, col):
    cur.execute(f"SELECT {col} FROM {table}")
    return [r[0] for r in cur.fetchall()]

def seed_bonus(users):
    if not (users and table_exists("bonus_account") and table_exists("bonus_transaction")):
        return []
    acc_ids = insert_returning(
        "INSERT INTO bonus_account(user_id) VALUES %s RETURNING bonus_account_id",
        [(u,) for u in users], "bonus_account_id", "bonus_account"
    )
    tx_rows = [
        (random.choice(acc_ids), datetime.date.today(),
         round(random.uniform(-1000, 1000), 2),
         random.choice(["earn","spend"]))
        for _ in range(len(acc_ids) * TX_PER_ACCOUNT)
    ]
    cur.executemany(
        "INSERT INTO bonus_transaction(bonus_account_id,transaction_date,amount,transaction_type) "
        "VALUES (%s,%s,%s,%s)", tx_rows
    )
    print(f"bonus_account: {len(acc_ids)}, tx: {len(tx_rows)}")
    return acc_ids

def seed_payment_methods(users):
    if not table_exists("paymentmethod"):
        return []
    base = [("Card",),("Cash",),("SBP",)]
    m_ids = insert_returning(
        "INSERT INTO paymentmethod(method_name) VALUES %s "
        "ON CONFLICT DO NOTHING RETURNING payment_method_id",
        base, "payment_method_id", "paymentmethod"
    )
    if users and table_exists("userpaymentmethod"):
        rows = [(random.choice(users), random.choice(m_ids),
                 fake.credit_card_number()) for _ in range(CNT_PAYMENT_LINKS)]
        cur.executemany(
            "INSERT INTO userpaymentmethod(user_id,payment_method_id,details) "
            "VALUES (%s,%s,%s)", rows
        )
    print(f"paymentmethod: {len(m_ids)}")
    return m_ids

def seed_bookings(users, rooms):
    if not (users and rooms and table_exists("booking")):
        return []
    status = ["new","in_process","done","canceled"]
    today  = datetime.date.today()
    rows = []
    for _ in range(CNT_BOOKINGS):
        ci = today + datetime.timedelta(days=random.randint(1,30))
        co = ci + datetime.timedelta(days=random.randint(1,14))
        rows.append((random.choice(users), random.choice(rooms), None,
                     ci, co, random.randint(1,4), random.choice(status),
                     round(random.uniform(3000,15000),2), today,
                     random.choice(["yes","no"])))
    ids = insert_returning(
        "INSERT INTO booking(user_id,room_id,payment_id,check_in_date,check_out_date,"
        "guests_number,status,price,date_creation,paid) "
        "VALUES %s RETURNING booking_id",
        rows, "booking_id", "booking"
    )
    print(f"booking: {len(ids)}")
    return ids

def seed_booking_status(b_ids):
    if not (b_ids and table_exists("bookingstatushistory")):
        return
    status = ["new","in_process","done","canceled"]
    rows = [(bid, random.choice(status), random.choice(status),
             datetime.date.today()) for bid in b_ids]
    cur.executemany(
        "INSERT INTO bookingstatushistory(booking_id,old_status,new_status,changed_at) "
        "VALUES (%s,%s,%s,%s)", rows
    )

def seed_payments(b_ids, m_ids):
    if not (b_ids and m_ids and table_exists("payment")):
        return
    pay_rows = [(bid, datetime.date.today(),
                 random.choice(m_ids),
                 random.choice(["pending","completed","failed"]))
                for bid in b_ids]
    pay_ids = insert_returning(
        "INSERT INTO payment(booking_id,payment_date,payment_method_id,payment_status) "
        "VALUES %s RETURNING payment_id",
        pay_rows, "payment_id", "payment"
    )
    cur.executemany(
        "UPDATE booking SET payment_id=%s WHERE booking_id=%s",
        list(zip(pay_ids, b_ids))
    )
    print(f"payment: {len(pay_ids)}")

def seed_services(b_ids):
    if not (b_ids and table_exists("additional_service") and
            table_exists("booking_additional_service")):
        return
    rows = [(round(random.uniform(500,3000),2), fake.word(), fake.sentence())
            for _ in range(CNT_ADD_SERVICES)]
    s_ids = insert_returning(
        "INSERT INTO additional_service(price,service_name,service_description) "
        "VALUES %s RETURNING service_id",
        rows, "service_id", "additional_service"
    )
    bridge = [(random.choice(b_ids), random.choice(s_ids))
              for _ in range(CNT_LINK_BOOK_SVC)]
    cur.executemany(
        "INSERT INTO booking_additional_service(booking_id,service_id) "
        "VALUES (%s,%s) ON CONFLICT DO NOTHING", bridge
    )
    print(f"additional_service: {len(s_ids)}, links: {len(bridge)}")

def seed_reviews(users, hotel_ids):
    if not (users and hotel_ids and table_exists("review")):
        return
    rows = [(random.choice(users), random.choice(hotel_ids),
             fake.paragraph(nb_sentences=2), datetime.date.today())
            for _ in range(CNT_BOOKINGS)]
    cur.executemany(
        "INSERT INTO review(user_id,hotel_id,comment_text,date_creation) "
        "VALUES (%s,%s,%s,%s)", rows
    )
    print(f"review: {len(rows)}")

def run():
    users  = get_ids("users", "user_id")
    rooms  = get_ids("room",  "room_id")
    hotels = get_ids("hotel", "hotel_id")

    seed_bonus(users)
    m_ids  = seed_payment_methods(users)
    b_ids  = seed_bookings(users, rooms)
    seed_booking_status(b_ids)
    seed_payments(b_ids, m_ids)
    seed_services(b_ids)
    seed_reviews(users, hotels)