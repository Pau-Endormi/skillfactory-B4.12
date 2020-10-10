import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import datetime

DB_PATH = "sqlite:///sochi_athletes.sqlite3"
Base = declarative_base()

class Athelete(Base):
    """
    Описывает структуру таблицы athelete, содержащую данные об атлетах
    """
    __tablename__ = 'athelete'
    id = sa.Column(sa.Integer, primary_key=True)
    age = sa.Column(sa.Integer)
    birthdate = sa.Column(sa.Text)
    gender = sa.Column(sa.Text)
    height = sa.Column(sa.Float)
    name = sa.Column(sa.Text)
    weight = sa.Column(sa.Integer)
    gold_medals = sa.Column(sa.Integer)
    silver_medals = sa.Column(sa.Integer)
    bronze_medals = sa.Column(sa.Integer)
    total_medals = sa.Column(sa.Integer)
    sport = sa.Column(sa.Text)
    country = sa.Column(sa.Text)

class User(Base):
    __tablename__ = 'user'
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    first_name = sa.Column(sa.Text)
    last_name = sa.Column(sa.Text)
    gender = sa.Column(sa.Text)
    email = sa.Column(sa.Text)
    birthdate = sa.Column(sa.Text)
    height = sa.Column(sa.Float)

#=================function

def connect_db():
    """
    Соединяется с БД, создает таблицы, если их нет и возвращает объект сессии
    """
    engine = sa.create_engine(DB_PATH)
    Base.metadata.create_all(engine)
    session = sessionmaker(engine)
    return session()

def convert_str_to_date(date_str):
    """
    Конвертирует строку 'YYYY-MM-DD' в объект  datetime.date
    """
    parts = date_str.split("-")
    date_parts = map(int, parts)
    date = datetime.date(*date_parts)
    return date

def nearest_athletes_by_birthdate(user, session):
    """
    Находит по дате рождения ближайшего к пользователю атлета
    """
    list_athletes = session.query(Athelete).all()
    athlete_id_birthdate = {}
    for athlete in list_athletes:
        birthdate = convert_str_to_date(athlete.birthdate)
        athlete_id_birthdate[athlete.id] = birthdate
    user_birthdate = convert_str_to_date(user.birthdate)
    min_dist = None
    athlete_id = None
    athlete_birthdate = None
    for id_, birthdate in athlete_id_birthdate.items():
        dist = abs(user_birthdate - birthdate)
        if not min_dist or dist < min_dist:
            min_dist = dist
            athlete_id = id_
            athlete_birthdate = birthdate
    return athlete_id, athlete_birthdate

def nearest_athletes_by_height(user, session):
    """
    Находит по росту ближайшего к пользователю атлета
    """
    list_athletes = session.query(Athelete).filter(Athelete.height != None).all()
    atlhete_id_height = {athlete.id: athlete.height for athlete in list_athletes}
    user_height = user.height
    min_dist = None
    athlete_id = None
    athlete_height = None
    for id_, height in atlhete_id_height.items():
        if height is None:
            continue
        dist = abs(user_height - height)
        if not min_dist or dist < min_dist:
            min_dist = dist
            athlete_id = id_
            athlete_height = height
    return athlete_id, athlete_height

def main():
    """
    Осуществляет взаимодействие с пользователем, обрабатывает пользовательский ввод
    """
    session = connect_db()
    mode = input("Выберите - 1 (чтобы показать двух атлетов ближайших к вам по росту и дате рождения): ")
    if mode == "1":
        user_id = int(input("Укажите свой id: "))
        user = session.query(User).filter(User.id == user_id).first()
        if not user:
            print("Данного пользователя не существует!")
        else:
            birthdate_athlete, birthdate = nearest_athletes_by_birthdate(user, session)
            height_athlete, height = nearest_athletes_by_height(user, session)
            print(f'Два ближайших к вам по параметрам атлета: \nАтлет: {birthdate_athlete}, c годом рождения: {birthdate} \nАтлет: {height_athlete}, с ростом: {height}')
    else:
        print("Некорректный режим!")

if __name__ == "__main__":
    main()
