from faker import Faker
import pandas as pd
from pymongo import MongoClient
import random
from sqlalchemy import create_engine
from uuid import uuid4


fake = Faker()

df_users = list()
df_user_info = list()
df_user_roles = pd.DataFrame(
    [
        {"id": 1, "name": "admin"},
        {"id": 2, "name": "manager"},
        {"id": 3, "name": "user"},
    ]
)
df_transactions = list()

for i in range(100):
    id = i + 1
    email = fake.free_email()
    name = fake.name()
    address = fake.address()

    df_users.append({
        "id": id,
        "email": email,
        "role_id": random.randint(1, 5),
    })

    df_user_info.append({
        "user_id": id,
        "name": name,
        "address": address,
    })
df_users = pd.DataFrame(df_users)
df_user_info = pd.DataFrame(df_user_info)


for _ in range(1_000_000):
    df_transactions.append(
        {
            "_id": str(uuid4()),
            "amount": 100.0 * random.random(),
            "user_id": random.randint(1, len(df_users)),
        }
    )

engine = create_engine("mysql+pymysql://dbt:dbt@mysql:3306/dbt")
df_users.to_sql("users", engine, index=False, if_exists="replace")
df_user_info.to_sql("user_info", engine, index=False, if_exists="replace")
df_user_roles.to_sql("roles", engine, index=False, if_exists="replace")
engine.dispose()

client = MongoClient("mongodb://dbt:dbt@mongo:27017")
collection = client["dbt"]["transactions"]
collection.insert_many(df_transactions)
client.close()
