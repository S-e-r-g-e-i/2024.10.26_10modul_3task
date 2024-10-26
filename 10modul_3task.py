""" Домашнее задание по теме "Блокировки и обработка ошибок" """

import threading
# from threading import Thread, Lock
from time import sleep
from random import randint


class Bank:
    def __init__(self, balance=0, lock=threading.Lock()):
        self.balance = balance
        self.lock = lock

    def deposit(self):
        for i in range(100):
            self.lock.acquire()
            if self.balance >= 500:
                print(f'Полон кошель i = {i}')
                self.lock.release()
            else:
                dep = randint(50, 500)
                self.balance += dep
                print(f'Пополнение: {dep}. Баланс: {self.balance} i = {i}.')
                self.lock.release()
            sleep(0.001)

    def take(self):
        for i in range(100):
            self.lock.acquire()
            tak = randint(50, 500)
            print(f'Запрос на {tak} i = {i}')
            if tak > self.balance:
                print(f'Запрос отклонён, недостаточно средств i = {i}')
                self.lock.release()
            else:
                self.balance -= tak
                print(f'Снятие: {tak}. Баланс: {self.balance} i = {i}')
                self.lock.release()
            sleep(0.001)


bk = Bank()

# Т.к. методы принимают self, в потоки нужно передать сам объект класса Bank
th1 = threading.Thread(target=Bank.deposit, args=(bk,))
th2 = threading.Thread(target=Bank.take, args=(bk,))

th1.start()
th2.start()
th1.join()
th2.join()

print(f'Итоговый баланс: {bk.balance}')