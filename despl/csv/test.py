import pandas as pd

df = pd.read_csv('reltotal.csv',encoding='utf-8-sig')

print (df)

items_presentes = []
no_copy = []

for x in range(len(df)):
    if df.loc[x][14] not in no_copy:
        items_presentes.append(df.loc[x][14])
        no_copy.append(df.loc[x][14])

print (items_presentes)
