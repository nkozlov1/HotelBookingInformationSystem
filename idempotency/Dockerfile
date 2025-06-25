FROM postgres:16-alpine
COPY idempotency/test_idempotency.sh /usr/local/bin/test_idempotency.sh
COPY migrations /migrations
RUN chmod +x /usr/local/bin/test_idempotency.sh