import random
import datetime as dt

import numpy as np
import pandas as pd
from faker import Faker
from numpy.random import choice
from randomtimestamp import randomtimestamp

if __name__ == '__main__':
    fake = Faker(locale='ru_RU')
    regions = ['Москва', 'Свердловская обл', 'Свердловская обл', 'Пензенская обл', 'Татарстан']
    cities = ['Москва', 'Екатеринбург', 'Тюмень', 'Пенза', 'Казань']
    users = []
    for i in range(11000):
        first_name = fake.first_name_male()
        second_name = fake.last_name_male()
        c = random.randint(0, len(cities) - 1)
        users.append({
            'first_name': first_name,
            'second_name': second_name,
            'city': cities[c],
            'region': regions[c],
            'id': i,
            'email': 'mr.applexz@gmail.com'
        })
    users = pd.DataFrame(users)
    users.to_csv('users.csv', index=False)
    errors = []
    error_types = [f'Ошибка {i}' for i in range(20)]
    error_weights = [0.2, 0.1, 0.1, 0.1, 0.05, 0.05, 0.02, 0.03, 0.01, 0.01, 0.01, 0.01, 0.01, 0.005, 0.005, 0.005,
                     0.005, 0.15, 0.1, 0.03]
    for i in range(80000):
        errors.append({
            'id': i,
            'user_id': random.randint(0, 1000),
            'timestamp': randomtimestamp(start=dt.datetime.now() - dt.timedelta(days=365)),
            'error_type': choice(error_types, 1, p=error_weights)[0],
            'severity': random.choice(['low', 'high']),
            'logs': random.choice([
                'У вас тупа браузер пажилой, сайт лагает и оффни адблокер',
                'Нашу систему атаковал хакер, система упала, самоуничтожение через 3, 2, 1'
            ])
        })
    errors = pd.DataFrame(errors)
    errors.to_csv('errors.csv', index=False)
    fake.name()
    print(123)
