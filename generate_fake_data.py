from pathlib import Path

import random
import psycopg2
from faker import Faker
from datetime import datetime, timedelta

faker = Faker()

DB_NAME = "mydatabase"
DB_USER = "myuser"
DB_PASSWORD = "mypassword"
DB_HOST = "localhost"
DB_PORT = "5432"

def connect():
    return psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )

def generate_and_insert():
    conn = connect()
    cur = conn.cursor()

    print("🔄 Truncating tables...")
    cur.execute("""
        TRUNCATE TABLE
            collection_log,
            inventory,
            floor,
            "user"
        RESTART IDENTITY CASCADE;
    """)
    conn.commit()
    print("Tables truncated. ---------------------------------------------")

    num_users = 10000
    num_inventory = 300000
    num_floor = 100000
    num_logs = 1000000 - num_users - num_inventory - num_floor

    item_names = {
        "COBBLESTONE": "cobblestone",
        "DIAMOND": "diamond",
        "DIAMOND_PICK": "diamond_pickaxe",
        "DIRT": "dirt",
        "GOLD": "gold",
        "GOLD_PICK": "gold_pickaxe",
        "IRON": "iron",
        "IRON_PICK": "iron_pickaxe",
        "SEED": "seed",
        "STONE_PICK": "stone_pickaxe",
        "WOOD_PICK": "wooden_pickaxe",
        "WOOD_PLANK": "wooden_plank",
        "WOOD_STICK": "wooden_stick"
    }
    
    item_skus = list(item_names.keys())

    print("Inserting users... ------------------------------------------------------------")
    for i in range(num_users):
        cur.execute('INSERT INTO "user" (name) VALUES (%s)', (faker.user_name(),))
        if i % 1000 == 0:
            print(f"   Inserted {i} users...")
    conn.commit()
    print("------------------------------ Users inserted! ------------------------------")

    print("Inserting inventory... ------------------------------------------------------------")
    for i in range(num_inventory):
        sku = random.choice(item_skus)
        item_name = item_names[sku]
        cur.execute(
            'INSERT INTO inventory (sku, item_name, favorite, amount, user_id) VALUES (%s, %s, %s, %s, %s)',
            (
                sku,
                item_name,
                random.choice([True, False]),
                random.randint(1, 100),
                random.randint(1, num_users)
            )
        )
        if i % 10000 == 0:
            print(f"   Inserted {i} inventory rows...")
    conn.commit()
    print("--------------------------------------------- Inventory inserted! ---------------------------------------------")

    print("Inserting floor items... ------------------------------------------------------------")
    for i in range(num_floor):
        cur.execute(
            "INSERT INTO floor (item_sku, quantity) VALUES (%s, %s)",
            (
                random.choice(item_skus),
                random.randint(1, 10),
            )
        )
        if i % 5000 == 0:
            print(f"   Inserted {i} floor items...")
    conn.commit()
    print("------------------------------ Floor items inserted! ------------------------------")

    print("Inserting collection logs... ---------------------------------------------")
    for i in range(num_logs):
        cur.execute(
            "INSERT INTO collection_log (item_sku, quantity_collected, collected_at, user_id) VALUES (%s, %s, %s, %s)",
            (
                random.choice(item_skus),
                random.randint(1, 5),
                faker.date_time_between(start_date='-14d', end_date='now'),
                random.randint(1, num_users),
            )
        )
        if i % 10000 == 0:
            print(f"   Inserted {i} logs...")
    conn.commit()
    print("------------------------------ Collection logs inserted! ------------------------------")

    cur.close()
    conn.close()
    print("------------------------------ All fake data inserted into PostgreSQL! ------------------------------")


if __name__ == "__main__":
    generate_and_insert()