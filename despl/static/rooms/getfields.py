import pandas as pd
import os
import requests
import PyPDF2
import re

# Read each line of the PDF


df = pd.read_csv('t_rooms1.csv',encoding='utf-8-sig')

print(df)

for i in range(1):
    # Importing required modules
    # Creating a pdf file object
    carpeta = df.loc[i][0]
    pdfFileObj = open(carpeta+'/RDS_'+carpeta+'_1.pdf','rb')

    # Creating a pdf reader object
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

    # Getting number of pages in pdf file
    pages = pdfReader.numPages

    body_protected = []
    cardiac_protected = []
    airconditioning = []
    hepa = []
    positive = []
    negative = []
    exhaust = []
    ventilation = []
    colour_corrected = []
    dimmable = []
    downs = []
    downs_dimmable = []
    fluo_downs = []
    proof = []
    fluo = []
    indirect = []
    nurse = []

    for i in range(len(df)):

            # Creating a page object
            pageObj = pdfReader.getPage(0)

            # Printing Page Number
            print("Page No: ",i)

            # Extracting text from page
            # And splitting it into chunks of lines
            text = pageObj.extractText().split("  ")
            #print('text:',text)
            # Finally the lines are stored into list
            # For iterating over list a loop is used
            for x in range(len(text)):
                if text[x].startswith(' \n \nAustralasian'):
                    n = x
                    print( text[n])
                    lista = text[n].split("\n")
                    print(lista)
                    campos = ['BODY PROTECTED','CARDIAC PROTECTED ','AIRCONDITIONING','AIRCONDITIONING: hepa filtered','AIRCONDITIONING: positive pressure','AIRCONDITIONING: negative pressure','EXHAUST: room exhaust','VENTILATION','LIGHTING: colour corrected','LIGHTING: dimmable','LIGHTING: downlights','LIGHTING: downlights, dimmable','LIGHTING: fluorescent/LED, downlights','proof','LIGHTING: fluorescent/LED, general','LIGHTING: indirect','NURSE CALL SYSTEM']
                    #llaves = [body_protected,cardiac_protected,airconditioning,hepa,positive,negative,exhaust,ventilation,color_corrected,dimmable,downs,downs_dimmable,fluorescent_downs,proof,fluorescent,indirect,nurse]
                    campo = 'BODY PROTECTED'
                    for y in range(len(lista)):
                            #print ('lenlista:',len(lista))
                        if lista[y] == campo:
                            body_protected.append(lista[y+2])
                    campo = 'CARDIAC PROTECTED '
                    for y in range(len(lista)):
                        if lista[y] == campo:
                            cardiac_protected.append(lista[y+2])
                    campo = 'AIRCONDITIONING'
                    for y in range(len(lista)):
                        if lista[y] == campo:
                            airconditioning.append(lista[y+2])
                    campo = 'AIRCONDITIONING: hepa filtered'
                    for y in range(len(lista)):
                        if lista[y] == campo:
                            hepa.append(lista[y+2])
                    campo = 'AIRCONDITIONING: positive pressure'
                    for y in range(len(lista)):
                        if lista[y] == campo:
                            positive.append(lista[y+2])
                    campo = 'AIRCONDITIONING: negative pressure'
                    for y in range(len(lista)):
                        if lista[y] == campo:
                            negative.append(lista[y+2])
                    campo = 'EXHAUST: room exhaust'
                    for y in range(len(lista)):
                        if lista[y] == campo:
                            exhaust.append(lista[y+2])
                    campo = 'VENTILATION'

                    for y in range(len(lista)):
                        if lista[y] == campo:
                            ventilation.append(lista[y+2])
                    campo = 'LIGHTING: colour corrected'

                    for y in range(len(lista)):
                        if lista[y] == campo:
                            colour_corrected.append(lista[y+2])
                    campo = 'LIGHTING: dimmable'

                    for y in range(len(lista)):
                        if lista[y] == campo:
                            dimmable.append(lista[y+2])
                    campo = 'LIGHTING: downlights'

                    for y in range(len(lista)):
                        if lista[y] == campo:
                            downs.append(lista[y+2])
                    campo = 'LIGHTING: downlights, dimmable'

                    for y in range(len(lista)):
                        if lista[y] == campo:
                            downs_dimmable.append(lista[y+2])
                    campo = 'LIGHTING: fluorescent/LED, downlights'

                    for y in range(len(lista)):
                        if lista[y] == campo:
                            fluo_downs.append(lista[y+2])
                    campo = 'proof'

                    for y in range(len(lista)):
                        if lista[y] == campo:
                            proof.append(lista[y+2])
                    campo = 'LIGHTING: fluorescent/LED, general'

                    for y in range(len(lista)):
                        if lista[y] == campo:
                            fluo.append(lista[y+2])
                    campo = 'LIGHTING: indirect'

                    for y in range(len(lista)):
                        if lista[y] == campo:
                            indirect.append(lista[y+2])
                    campo = 'NURSE CALL SYSTEM'

                    for y in range(len(lista)):
                        if lista[y] == campo:
                            nurse.append(lista[y+2])

    # closing the pdf file object
    pdfFileObj.close()

try:
    df['body_protected'] = body_protected
except:
    print(len(body_protected))
try:
    df['cardiac_protected'] = cardiac_protected
except:
    len(cardiac_protected)
    print('cardiac_protected:',cardiac_protected)
df['airconditioning'] = airconditioning
df['hepa'] = hepa
df['positive'] = positive
df['negative'] = negative
df['exhaust'] = exhaust
df['ventilation'] = ventilation
df['colour_corrected'] = colour_corrected
df['dimmable'] = dimmable
df['downs'] = downs
df['downs_dimmable'] = downs_dimmable
df['fluo_downs'] = fluo_downs
df['proof'] = proof
df['fluo'] = fluo
df['indirect'] = indirect
df['nurse'] = nurse


df.to_csv('t_rooms2.csv',index=False)
