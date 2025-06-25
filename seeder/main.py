import os, importlib, sys
from utility_func import conn

SEEDERS = {
    1: "v1_seed",
    2: "v2_seed",
    3: "v3_seed",
}

def main():
    target = os.getenv("MIGRATION_VERSION", "latest")
    if target == "latest":
        target_version = max(SEEDERS)
    else:
        try:
            target_version = int(target)
        except ValueError:
            print("MIGRATION_VERSION Eror", file=sys.stderr)
            sys.exit(1)

    for v in range(1, target_version + 1):
        module_name = SEEDERS.get(v)
        if not module_name:
            print(f"no seeder for V{v}")
            continue
        module = importlib.import_module(module_name)
        print(f"running {module_name}.run()")
        module.run()

    print("seeding finished, version: ", target_version)

if __name__ == "__main__":
    try:
        main()
    finally:
        conn.close()