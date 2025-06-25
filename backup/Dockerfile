FROM postgres:15-alpine

ENV BACKUP_DIR=/backups

COPY backup.sh /usr/local/bin/backup.sh
RUN chmod +x /usr/local/bin/backup.sh

ENTRYPOINT ["/bin/sh", "-c", "\
  echo \"${BACKUP_INTERVAL_CRON:-0 * * * *} /usr/local/bin/backup.sh >> /var/log/pg_backup.log 2>&1\" | crontab - && \
  crond -f -L /var/log/cron.log"]