import pandas as pd
import numpy as np
import ast

df = pd.read_csv('data.csv', encoding='utf-8')

df['text_clean'] = df['text_clean'].apply(lambda x: ast.literal_eval(x))
print(df.text_clean.head())