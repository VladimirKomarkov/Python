import json
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from models import create_tables, Publisher, Book, Shop, Stock, Sale

DSN = "postgresql://postgres:35255@localhost:5432/netology_db"
database_url = "jdbc:postgresql://localhost:5432/postgres"

# функция для создания сессии
def get_session(database_URL):
    engine = sqlalchemy.create_engine(DSN)

    create_tables(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    return session

# работаем с предоставленным JSON-файлом, заполняем наши таблицы его содержимым
with open('C:/Python/tests_data.json', 'r') as fd:
    data = json.load(fd)

for record in data:
    model = {
        'publisher': Publisher,
        'shop': Shop,
        'book': Book,
        'stock': Stock,
        'sale': Sale,
    }[record.get('model')]
    get_session(database_url).add(model(id=record.get('pk'), **record.get('fields')))
get_session(database_url).commit()


# функция для вывода фактов покупки книг издателя
def get_shops(publisher_name_or_id):
    sales_query = get_session(database_url).query(Book.title, Shop.name, Sale.price, Sale.date_sale) \
        .select_from(Shop). \
        join(Stock, Shop.id == Stock.id_shop). \
        join(Book, Stock.id_book == Book.id). \
        join(Publisher, Book.id_publisher == Publisher.id). \
        join(Sale, Stock.id == Sale.id_stock)
    if publisher_name_or_id.isdigit():
        publisher_query = sales_query.filter(Publisher.id == publisher_name_or_id).all()
    else:
        publisher_query = sales_query.filter(Publisher.name == publisher_name_or_id).all()
    if not publisher_query:
        print("Издатель с таким именем или ID не найден.")
    else:
        for title, shop_name, price, date_sale in publisher_query:
                print(f"{title: <40} | {shop_name: <10} | {price: <8} | {date_sale.strftime('%d-%m-%y')}")

if __name__ == "__main__":
    publisher_input = input("Введите имя или идентификатор издателя: ")
    get_shops(publisher_input)
    get_session(database_url).close()