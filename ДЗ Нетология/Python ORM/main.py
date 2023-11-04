import json
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from models import create_tables, Publisher, Book, Shop, Stock, Sale
from config import DSN, database_url

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
def print_publisher_sales(publisher_name_or_id):
    session = get_session(database_url)

    # определяем, осуществляется запрос по ИД или же по имени автора
    if publisher_name_or_id.isdigit():
        publisher_query = session.query(Publisher).filter(Publisher.id == int(publisher_name_or_id))
    else:
        publisher_query = session.query(Publisher).filter(Publisher.name == publisher_name_or_id)

        publisher = publisher_query.first()
        if not publisher:
            print('No publisher')

    # делем запрос для получения фактов покупки книг издателя
    sales_query = session.query(Book.title, Shop.name, Sale.price, Sale.date_sale)\
    .join(Publisher)\
    .join(Stock, Book.id == Stock.id_book)\
    .join(Shop, Stock.id_shop == Shop.id)\
    .join(Sale, Stock.id == Sale.id_stock)\
    .filter(Publisher.id == Book.id_publisher)\
    .order_by(Sale.date_sale.desc())

    # выводим результаты
    for title, shop_name, price, date_sale in sales_query:
        print(f"{title} | {shop_name} | {price} | {date_sale.strftime('%d-%d-%y')}")


if __name__ == "__main__":
    publisher_input = input("Введите имя или идентификатор издателя: ")
    print_publisher_sales(publisher_input)
    get_session(database_url).close()