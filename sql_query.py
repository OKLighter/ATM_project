import sqlite3


class Text:
    text_get_money = "Введите пожалуйста сумму которую желаете снять: \n"
    text_transfer_money = "Введите пожалуйста сумму которую желаете перевести: \n"
    text_deposition_money = "Введите пожалуйста сумму которую желаете внести: \n"


class Sql_Atm:

    @staticmethod
    def create_table():
        """Создание таблицы Users_data"""
        with sqlite3.connect("atm.db") as db:
            cur = db.cursor()
            cur.execute("""CREATE TABLE IF NOT EXISTS Users_data(
            UserID INTEGER PRIMARY KEY AUTOINCREMENT,
            Number_card INTEGER NOT NULL,
            Pin_code INTEGER NOT NULL,
            Balance INTEGER NOT NULL);""")
            print("""Создание таблицы Users_data""")

    @staticmethod
    def insert_users(data_users):
        """Создание нового пользователя"""
        with sqlite3.connect("atm.db") as db:
            cur = db.cursor()
            cur.execute("""INSERT INTO Users_data(
            Number_card, Pin_code, Balance)
            VALUES(?, ?, ?); """, data_users)
            print("Создание нового пользователя")

    @staticmethod
    def input_card(number_card):
        """Ввод и проверка карты"""
        try:
            with sqlite3.connect("atm.db") as db:
                cur = db.cursor()
                cur.execute(f"""SELECT Number_card FROM Users_data WHERE Number_card = {number_card}""")
                result_card = cur.fetchone()
                if result_card is None:
                    print("Введен неизвестный номер карты")
                    return False
                else:
                    print(f"Введен номер карты {number_card}")
                    return True
        except:
            print("Введен неизвестный номер карты")

    @staticmethod
    def input_code(number_card):
        """Ввод и проверка пин-кода"""
        pin_code = input("Введите пожалуйста пин-код карты: ")
        with sqlite3.connect('atm.db') as db:
            cur = db.cursor()
            cur.execute(f"""SELECT Pin_code FROM Users_data WHERE Number_card = {number_card}""")
            result_code = cur.fetchone()
            input_pin = result_code[0]
            try:
                if input_pin == int(pin_code):
                    print("Введен верный пин-код")
                    return True
                else:
                    print("Введен некорректный пин-код")
                    return False
            except:
                print("Введен некорректный пин-код")
                return False

    @staticmethod
    def info_balance(number_card):
        """Информация о балансе"""

        with sqlite3.connect('atm.db') as db:
            cur = db.cursor()
            cur.execute(f"""SELECT Balance FROM Users_data WHERE Number_card = {number_card}""")
            result_info_balance = cur.fetchone()
            balance_card = result_info_balance[0]
            print(f"Баланс вашей карты: {balance_card}")

    @staticmethod
    def withdraw_money(number_card, text_input):
        """Снятие денежных средств с карты"""

        amount = input(text_input)
        with sqlite3.connect('atm.db') as db:
            cur = db.cursor()
            cur.execute(f"""SELECT Balance FROM Users_data WHERE Number_card = {number_card}""")
            result_info_balance = cur.fetchone()
            balance_card = result_info_balance[0]
            try:
                if int(amount) > balance_card:
                    print("На вашей карте недостаточно денежных средств")
                    return False
                else:
                    cur.execute(
                        f"""UPDATE Users_data SET Balance = Balance - {amount} WHERE Number_card = {number_card};""")
                    db.commit()
                    Sql_Atm.info_balance(number_card)
                    return True
            except:
                print("Попытка выполнить некорректное действие")
                return False

    @staticmethod
    def deposition_money(number_card, text_input):
        """Внести денежные средства на баланс"""

        amount = input(text_input)
        with sqlite3.connect('atm.db') as db:
            try:
                cur = db.cursor()
                cur.execute(
                    f"""UPDATE Users_data SET Balance = Balance + {amount} WHERE Number_card = {number_card};""")
                db.commit()
                Sql_Atm.info_balance(number_card)
            except:
                print("Попытка выполнить некорректное действие")
                return False

    @staticmethod
    def transfer_money(number_card):
        """Перевести денежные средства"""

        amount = input(Text.text_transfer_money)
        with sqlite3.connect('atm.db') as db:
            cur = db.cursor()
            cur.execute(f"""SELECT Balance FROM Users_data WHERE Number_card = {number_card}""")
            result_info_balance = cur.fetchone()
            balance_card = result_info_balance[0]
            try:
                if int(amount) > balance_card:
                    print("На вашей карте недостаточно денежных средств")
                    return False
                else:
                    cur.execute(
                        f"""UPDATE Users_data SET Balance =
                         Balance - {amount} WHERE Number_card = {number_card};""")
                    db.commit()
                    card_recipient = input(f"Введите номер карты получателя \n")
                    confirm = input("Для подтверждения операции введите - yes \n")
                    if confirm == 'yes':
                        try:
                            with sqlite3.connect("atm.db") as db:
                                cur = db.cursor()
                                cur.execute(f"""SELECT Number_card
                                 FROM Users_data WHERE Number_card = {card_recipient}""")
                                result_card = cur.fetchone()
                                if result_card is None:
                                    print("Введен неизвестный номер карты")
                                    return False
                                else:
                                    db = sqlite3.connect("atm.db")
                                    cur = db.cursor()
                                    cur.execute(
                                        f"""UPDATE Users_data SET Balance = Balance + {amount}
                                         WHERE Number_card = {card_recipient};""")
                                    db.commit()
                                    print(f"Перевод денежных средств в размере:"
                                          f" {amount} тубриков на карту №{card_recipient} успешно выполнен")
                                    Sql_Atm.info_balance(number_card)
                                    return True
                        except:
                            print("Попытка выполнить некорректное действие")
                            return False
                    else:
                        print("Вы не подтвердили операцию, возвращаемся в главное меню")
                        return False

            except:
                print("Попытка выполнить некорректное действие")
                return False

    @staticmethod
    def input_operation(number_card):
        """Выбор операции"""

        while True:
            operation = input("Введите пожалуйста операцию, которую хотите совершить: \n"
                              "1. Узнать баланс \n"
                              "2. Снять денежные средства \n"
                              "3. Внести денежные средства \n"
                              "4. Завершить работу \n"
                              "5. Перевести денежные средства \n")

            match operation:
                case "1":
                    Sql_Atm.info_balance(number_card)

                case "2":
                    Sql_Atm.withdraw_money(number_card, Text.text_get_money)

                case "3":
                    Sql_Atm.deposition_money(number_card, Text.text_deposition_money)

                case "4":
                    print("Спасибо за ваш визит, всего доброго")
                    return False

                case "5":
                    Sql_Atm.transfer_money(number_card)

                case _:
                    print("Данная операция недоступна, попробуйте другую операцию")
