import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DB_PATH = "sqlite:///sochi_athletes.sqlite3"
Base = declarative_base()

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

def valid_date(date):
    if len(date.split("-")) != 3:
        return False
    Y, M, D = date.split("-")
    if len(Y) == 4 and len(M) == 2 and len(D) == 2:
        return True
    else:
        return False

def valid_gender(gender):
    if gender == "Male" or gender == "Female":
        return True
    else:
        return False

def request_data():
    print("Здравствуйте! Сейчас произойдёт запись ваших данных!")
    first_name = input("Введите своё имя: ")
    last_name = input("Введите свою фамилию: ")
    gender = input("Укажите свой пол (Male/Female): ")
    email = input("Введите свой адрес электронной почты: ")
    birthdate = input("Введите свою дату рождения (YYYY-MM-DD): ")
    height = float(input("Укажите свой рост (образец: 1.75): "))
    if valid_date(birthdate) and valid_gender(gender):
        obj = User(
            first_name=first_name,
            last_name=last_name,
            gender=gender,
            email=email,
            birthdate=birthdate,
            height=height
        )
        return obj
    else:
        return None

def main():
    """
    Осуществляет взаимодействие с пользователем, обрабатывает пользовательский ввод
    """
    session = connect_db()
    mode = input("Выберите - 1 (чтобы ввести новые данные): ")
    if mode == "1":
        user = request_data()
        if user is not None:
            session.add(user)
            session.commit()
            print("Спасибо, данные сохранены!")
        else:
            print("Некорректный ввод данных!")
    else:
        print("Некорректный режим!")

if __name__ == "__main__":
    main()
