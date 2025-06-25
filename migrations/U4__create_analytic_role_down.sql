DO
$$
BEGIN
    IF EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'analytic') THEN

        REVOKE USAGE  ON SCHEMA  public FROM analytic;
        REVOKE SELECT ON ALL TABLES IN SCHEMA public FROM analytic;

        ALTER DEFAULT PRIVILEGES IN SCHEMA public
            REVOKE SELECT ON TABLES FROM analytic;

        DROP ROLE analytic;
    END IF;
END
$$;