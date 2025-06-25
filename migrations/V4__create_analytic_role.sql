DO
$$
BEGIN
   IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'analytic') THEN
      CREATE ROLE analytic NOLOGIN;
   END IF;
END
$$;

GRANT USAGE ON SCHEMA public TO analytic;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO analytic;

ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO analytic;

DO
$$
DECLARE
    n text;
BEGIN
    FOREACH n IN ARRAY string_to_array('${analyst_names}', ',') LOOP
        n := trim(n);
        CONTINUE WHEN n = '';
        BEGIN
            EXECUTE format(
                'CREATE ROLE %I LOGIN PASSWORD %L IN ROLE analytic',
                n, n || '_123'
            );
        EXCEPTION WHEN duplicate_object THEN NULL;
        END;
    END LOOP;
END
$$;