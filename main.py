from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://Sivka:v7ddG9W62P23Oc5L@cluster0.zpagku6.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

client = MongoClient(uri, server_api=ServerApi('1'))

db = client.db_cats

cats_collection = db["cats"]

# Додавання кота в БД
def add_cat(name: str, age: int, features: list):
    cats_collection.insert_one({"name": name, "age": age, "features": features})
    print(f"Додано кота: {name}")

# Пошук кота за ім'ям в БД
def cat_name(name: str):
    cat = cats_collection.find_one({"name": name})
    if cat:
        print(f"Кота знайдено: {cat}")
    else:
        print(f"Кота {name} не знайдено")

# Всі коти в БД
def all_cats():
    for cat in cats_collection.find():
        print(cat)

# Додавання характеристики коту
def add_feature_cat(name: str, feature: str):
    result = cats_collection.update_one({"name": name}, {"$push": {"features": feature}})
    if result.modified_count:
        print(f"Додано характеристику '{feature}' коту {name}")
    else:
        print(f"Кота {name} не знайдено")

# Оновлення віку кота
def update_cat_age(name: str, new_age: int):
    result = cats_collection.update_one({"name": name}, {"$set": {"age": new_age}})
    if result.modified_count:
        print(f"Вік кота {name} оновлено до {new_age}")
    else:
        print(f"Кота {name} не знайдено")

# Видалення кота за ім'ям в БД
def delete_cat_by_name(name: str):
    result = cats_collection.delete_one({"name": name})
    if result.deleted_count:
        print(f"Кота {name} видалено")
    else:
        print(f"Кота {name} не знайдено")

# Видалення всі котів з БД
def delete_all_cats():
    cats_collection.delete_many({})
    print("Всіх котів видалено")

# Виконання завдань
def main():
    add_cat("barsik", 3, ["ходить в капці", "дає себе гладити", "рудий"])
    add_cat("boris", 7, ["ходить в капці", "дає себе гладити", "рудий"])
    cat_name("boris")
    all_cats()
    update_cat_age("barsik", 4)
    add_feature_cat("barsik", "лизькати лапу")
    delete_cat_by_name("barsik")
    delete_all_cats()


if __name__ == "__main__":
    main()
    


