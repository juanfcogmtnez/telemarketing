import pandas as pd

df = pd.read_csv('rel.csv',encoding='utf-8-sig')

#print(df)

filtro = df['item'] == 'MMHA-023'
filtrado = df[filtro]
print("filtrado",filtrado)
filtrado['coste'] = df['coste'].astype(float)
result = filtrado.sort_values(by=['coste'])
print(result)