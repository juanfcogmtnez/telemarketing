import pandas as pd
import os
import requests

df = pd.read_csv('t_rooms1.csv',encoding='utf-8-sig')

print(df)


for i in range(len(df)):
    carpeta = df.loc[i][0]
    try:
        os.mkdir(carpeta)
    except:
        print("ya existe la carpeta")
    url2 = 'https://aushfg-prod-com-au.s3.amazonaws.com/download/RLS_'+carpeta+'_1.pdf'

    for x in range(10):
        url1 = 'https://aushfg-prod-com-au.s3.amazonaws.com/download/RDS_'+carpeta+'_'+str(x)+'.pdf'
        myfile = requests.get(url1)
        text = myfile.text
        if '<Error>' in text:
            print ("Error")
        else:
            print ("correcto")
            open(carpeta+'/RDS_'+carpeta+'_1.pdf', 'wb').write(myfile.content)
            break

    for x in range(10):
        url1 = 'https://aushfg-prod-com-au.s3.amazonaws.com/download/RLS_'+carpeta+'_'+str(x)+'.pdf'
        myfile = requests.get(url1)
        text = myfile.text
        if '<Error>' in text:
            print ("Error")
        else:
            print ("correcto")
            open(carpeta+'/RLS_'+carpeta+'_1.pdf', 'wb').write(myfile.content)
            break
