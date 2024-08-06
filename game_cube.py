from sklearn.datasets import load_iris
from sklearn.linear_model import LinearRegression, Ridge, Lasso
import matplotlib.pyplot as plt
from sklearn import random_projection
from sklearn.manifold import TSNE
import numpy as np
import pandas as pd
import random

df = pd.read_csv('characters.csv')

char_bonus = {
    1: -5,
    2: -4,
    3: -4,
    4: -3,
    5: -3,
    6: -2,
    7: -2,
    8: -1,
    9: -1,
    10: 0,
    11: 0,
    12: 1,
    13: 1,
    14: 2,
    15: 2,
    16: 3,
    17: 3,
    18: 4,
    19: 4,
    20: 5,
    21: 5,
    22: 6,
    23: 6,
    24: 7,
    25: 7,
    26: 8,
    27: 8,
    28: 9,
    29: 9,
    30: 10
}

difficult = {
    'Очень лёгкая':	5,
    'Лёгкая':	10,
    'Средняя':	15,
    'Сложная':	20,
    'Очень сложная':	25,
    'Практически невозможная':	30
}

def roll_bonus(characteristic: int, diff: int):
    roll =random.randint(1, 20)
    if roll ==1:
        print('Критический провал')
        return roll
    elif roll ==20:
        print('Критический успех')
        return roll
    roll = roll + char_bonus[characteristic]
    print(f'бонус = {char_bonus[characteristic]}')
    if roll < diff:
        print('не успех')
    elif roll >= diff:
        print('успех')
    return roll

strght = df.loc[0, 'strength']
diff = difficult['Лёгкая']

roll_bonus(strght, diff)