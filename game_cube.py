from sklearn.datasets import load_iris
from sklearn.linear_model import LinearRegression, Ridge, Lasso
import matplotlib.pyplot as plt
from sklearn import random_projection
from sklearn.manifold import TSNE
import numpy as np
import pandas as pd
import random

df = pd.read_csv('characters.csv')

char_bonus = [None, -5, -4, -4, -3, -3, -2, -2, -1, -1, 0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9, 10]

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
