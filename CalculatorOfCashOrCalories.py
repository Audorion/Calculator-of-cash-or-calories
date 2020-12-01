# -*- coding: cp1251 -*-

import datetime
from datetime import timedelta


class Calculator:

    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append((record.amount, record.comment, record.date))

    def get_today_stats(self):
        summa_stats_of_day = 0
        for i in self.records:
            if datetime.datetime.now().date() == i[2]:
                summa_stats_of_day += i[0]
        return summa_stats_of_day

    def get_week_stats(self):
        summa_stats_of_week = 0
        now = datetime.datetime.now().date()
        week_ago = datetime.datetime.now().date() - timedelta(7)
        for i in self.records:
            if week_ago <= i[2] <= now:
                summa_stats_of_week += i[0]
        return summa_stats_of_week


class CaloriesCalculator(Calculator):

    def get_calories_remained(self):
        if self.limit > (CaloriesCalculator.get_today_stats(self)):
            return (
                f"Сегодня можно съесть что-нибудь ещё,"
                f" но с общей калорийностью не более {self.limit - (CaloriesCalculator.get_today_stats(self))} кКал")
        else:
            return "Хватит есть!"


class CashCalculator(Calculator):
    USD_RATE = "73.223"
    EUR_RATE = "89.322"
    RUS_RATE = "1.001"

    def get_today_cash_remained(self, currency):
        crn = {"rub": self.RUS_RATE,
               "usd": self.USD_RATE,
               "eur": self.EUR_RATE
               }
        current_currency_value = float(crn[currency])
        current_currency_name = currency
        result = abs(
            self.limit / current_currency_value - CashCalculator.get_today_stats(self) / current_currency_value)
        if self.limit > (CashCalculator.get_today_stats(self)):
            return (f"На сегодня осталось "
                    f"{result:.2f} "
                    f"{current_currency_name}")
        elif self.limit == CashCalculator.get_today_stats(self):
            return "Денег нет, держись!"
        else:
            return (f"Денег нет, держись! Твой долг "
                    f"- {result:.2f} "
                    f" {current_currency_name}")


class Record:

    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment
        if date is not None:
            date_format = '%d.%m.%Y'
            moment = datetime.datetime.strptime(date, date_format).date()
            self.date = moment
        else:
            self.date = datetime.datetime.now().date()


cash_calculator = CashCalculator(1000)
calories_calculator = CaloriesCalculator(3000)


cash_calculator.add_record(Record(amount=101, comment="Серёге за обед", date="01.12.2020"))

cash_calculator.add_record(Record(amount=3000, comment="бар в Танин др", date="08.11.2019"))


calories_calculator.add_record(Record(amount=42, comment="похавала пельмеши", date="01.12.2020"))
print(calories_calculator.get_calories_remained())
