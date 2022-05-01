import pandas as pd

padre = pd.read_csv('t_unit_rooms2.csv',encoding="utf-8-sig")
print(padre)
df = pd.read_csv('t_room_item.csv',encoding="utf-8-sig")
print(df)

newdf = pd.DataFrame()

asc = []

for z in range(len(padre)):
    asc = padre.loc[z][0]
    hijo = padre.loc[z][1]
    progz = z*100 / len(padre)
    progz = round(progz,2)
    progz = str(progz)+' %'
    for y in range(len(df)):
        if df.loc[y][0] == hijo:
            typeB = df.loc[y][3]
            typeB = typeB[0:2]
            row = {'asc':asc,'from':hijo,'to':df.loc[y][3],'typeA':df.loc[y][2],'typeB':typeB,'item_en':df.loc[y][4],'item_es':df.loc[y][5],'item_fr':df.loc[y][6],'qty':df.loc[y][7]}
            newdf = newdf.append(row, ignore_index = True)
            progy = y*100 / len(df)
            progy = round(progy,2)
            progy = str(progy)+' %'
            print(progz, "/", progy)

newdf.to_csv('t_room_items2.csv')
