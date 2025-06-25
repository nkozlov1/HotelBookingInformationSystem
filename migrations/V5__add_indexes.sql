CREATE INDEX IF NOT EXISTS ix_room_hotel_price_desc
       ON room (hotel_id, price DESC)
       INCLUDE (room_id);

CREATE INDEX IF NOT EXISTS ix_payment_completed
       ON payment (booking_id)
       WHERE payment_status = 'completed';

CREATE INDEX IF NOT EXISTS ix_booking_user
       ON booking (user_id, booking_id);

CREATE INDEX IF NOT EXISTS ix_hotel_rating_desc
       ON hotel (rating DESC);

CREATE INDEX IF NOT EXISTS ix_hotelamenity_hotel
       ON hotelamenity (hotel_id, amenity_id);

CREATE INDEX IF NOT EXISTS ix_room_price_capacity
       ON room (price, capacity DESC)
       INCLUDE (hotel_id);

CREATE INDEX IF NOT EXISTS ix_hotel_city
       ON hotel (city);