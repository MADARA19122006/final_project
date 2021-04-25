from requests import post
from random import randint
import datetime

"""Заполняем таблицу Availability рандомными данными через API"""

av = {'availability': []}
cdate = datetime.date(2021, 4, 13)
for i in range(390):
    av['availability'].append({'date': cdate.strftime('%Y%m%d'), 'room': 1, 'qty': randint(3, 7), 'price': randint(20, 30) * 100})
    av['availability'].append({'date': cdate.strftime('%Y%m%d'), 'room': 2, 'qty': randint(3, 7), 'price': randint(40, 60) * 100})
    cdate = cdate + datetime.timedelta(days=1)
print(av)

print(post('http://localhost:5000/api/availability',
           json=av).json())