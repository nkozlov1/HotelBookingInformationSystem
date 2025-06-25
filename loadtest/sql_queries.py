STATEMENTS = {
    "top_rooms":
        """
        SELECT h.hotel_name, r.room_id, r.price
        FROM   hotel h
        JOIN   room r ON r.hotel_id = h.hotel_id
        ORDER  BY h.hotel_id, r.price DESC
        LIMIT  10;
        """,
    "bookings_by_status":
        """
        SELECT   status,
                 COUNT(*) AS cnt,
                 SUM(price)::numeric(12,2) AS total_amount
        FROM     booking
        GROUP BY status;
        """,
    "top_spenders":
        """
        SELECT u.user_id,
               u.name,
               SUM( (p.payment_status = 'completed')::int ) AS payments_done,
               SUM(b.price) AS total_spent
        FROM   users    u
        JOIN   booking  b ON b.user_id = u.user_id
        JOIN   payment  p ON p.booking_id = b.booking_id
        WHERE  p.payment_status = 'completed'
        GROUP  BY u.user_id, u.name
        ORDER  BY total_spent DESC
        LIMIT  20;
        """,
    "amenities_of_top_hotels":
        """
        SELECT h.hotel_id,
               h.hotel_name,
               array_agg(a.amenity_name ORDER BY a.amenity_name) AS amenities
        FROM   (
                 SELECT *
                 FROM   hotel
                 ORDER  BY rating DESC
                 LIMIT  50
               ) h
        JOIN   hotelamenity ha ON ha.hotel_id = h.hotel_id
        JOIN   amenity      a  ON a.amenity_id = ha.amenity_id
        GROUP  BY h.hotel_id, h.hotel_name;
        """,
    "available_rooms_filtered":
        """
        SELECT r.room_id,
               h.hotel_name,
               r.price,
               r.capacity
        FROM   room   r
        JOIN   hotel  h ON h.hotel_id = r.hotel_id
        WHERE  r.price BETWEEN 3000 AND 8000
          AND  r.capacity >= 2
          AND  NOT EXISTS (
                SELECT 1 FROM booking b
                WHERE  b.room_id = r.room_id
                  AND  b.check_in_date <= now() + INTERVAL '7 day'
                  AND  b.check_out_date >= now()
          )
        ORDER  BY r.price DESC
        LIMIT  100;
        """,
    "price_histogram_by_city":
        """
        SELECT city,
               width_bucket(price, 0, 10000, 10) AS bucket,
               COUNT(*) AS bucket_count
        FROM   room r
        JOIN   hotel h ON h.hotel_id = r.hotel_id
        GROUP  BY city, bucket
        ORDER  BY city, bucket;
        """,
}