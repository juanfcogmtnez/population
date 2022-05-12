import world_bank_data as wb
import pandas as pd
import json

df = pd.read_csv('static/data/pop.csv', encoding='utf-8-sig')
    
def countries():
    paises = []
    codigos = []
    for i in range(len(df)):
        if df.loc[i][0] not in paises:
            paises.append(df.loc[i][0])
            codigos.append(df.loc[i][1])
    newdf = pd.DataFrame()
    newdf['codigos'] = codigos
    newdf['paises'] = paises
    return json.dumps(newdf.to_dict('records'))

def sel(country,year):
    year = str(year)
    filtro = df['Country Code'] == country
    filtrado = df[filtro]
    campos = ['Population ages 00-04, female','Population ages 00-04, male','Population ages 05-09, female','Population ages 05-09, male','Population ages 10-14, female','Population ages 10-14, male','Population ages 15-19, female','Population ages 15-19, male','Population ages 20-24, female','Population ages 20-24, male','Population ages 25-29, female','Population ages 25-29, male','Population ages 30-34, female','Population ages 30-34, male','Population ages 35-39, female','Population ages 35-39, male','Population ages 40-44, female','Population ages 40-44, male','Population ages 45-49, female','Population ages 45-49, male','Population ages 50-54, female','Population ages 50-54, male','Population ages 55-59, female','Population ages 55-59, male','Population ages 10-14, female','Population ages 10-14, male','Population ages 15-19, female','Population ages 15-19, male','Population ages 20-24, female','Population ages 20-24, male','Population ages 25-29, female','Population ages 25-29, male','Population ages 30-24, female','Population ages 30-34, male','Population ages 35-39, female','Population ages 35-39, male','Population ages 40-44, female','Population ages 40-44, male','Population ages 45-49, female','Population ages 45-49, male','Population ages 50-54, female','Population ages 50-54, male','Population ages 60-64, female','Population ages 60-64, male','Population ages 10-14, female','Population ages 10-14, male','Population ages 15-19, female','Population ages 15-19, male','Population ages 20-24, female','Population ages 20-24, male','Population ages 25-29, female','Population ages 25-29, male','Population ages 30-24, female','Population ages 30-34, male','Population ages 35-39, female','Population ages 35-39, male','Population ages 40-44, female','Population ages 40-44, male','Population ages 45-49, female','Population ages 45-49, male','Population ages 50-54, female','Population ages 50-54, male','Population ages 55-59, female','Population ages 55-59, male','Population ages 10-14, female','Population ages 10-14, male','Population ages 15-19, female','Population ages 15-19, male','Population ages 20-24, female','Population ages 20-24, male','Population ages 25-29, female','Population ages 25-29, male','Population ages 30-24, female','Population ages 30-34, male','Population ages 35-39, female','Population ages 35-39, male','Population ages 40-44, female','Population ages 40-44, male','Population ages 45-49, female','Population ages 45-49, male','Population ages 50-54, female','Population ages 50-54, male','Population ages 55-59, female','Population ages 55-59, male','Population ages 60-64, female','Population ages 60-64, male','Population ages 65-69, female','Population ages 65-69, male','Population ages 70-74, female','Population ages 70-74, male','Population ages 75-79, female','Population ages 75-79, male','Population ages 80 and above, female','Population ages 80 and above, male']
    filtro= filtrado['Indicator Name'].isin(campos)
    filtrado = filtrado[filtro]
    filtrado = filtrado.loc[:,['Indicator Name',year]]
    filtrado = filtrado.reset_index()
    indicadores = ['00-04','05-09','10-14','15-19','20-24','25-29','30-34','35-39','40-44','45-49','50-54','55-59','60-64','65-69','70-74','75-79','> 80']
    mujeres = []
    hombres = []
    for i in range(len(filtrado)):
        if i==0 or i % 2 == 0:
            mujeres.append(filtrado.loc[i][2])
            print(filtrado.loc[i][1])
        else:
            hombres.append(filtrado.loc[i][2])
            print(filtrado.loc[i][1])
    newdf = pd.DataFrame()
    print("indicadoreslen:",len(indicadores))
    print("mujereslen:",len(mujeres))
    print("hombreslen:",len(hombres))
    newdf['age'] = indicadores
    newdf['female'] = mujeres
    newdf['male'] = hombres
    data = newdf.to_dict('records')
    return json.dumps(data)


def sel_pop(country):
    filtro = df['Country Code'] == country
    filtrado = df[filtro]
    campos = ['Population, total']
    filtro= filtrado['Indicator Name'].isin(campos)
    filtrado = filtrado[filtro]
    filtrado = filtrado.reset_index()
    return json.dumps(filtrado.to_dict('records'))

def sel_pop_year(country,year):
    year = str(year)
    filtro = df['Country Code'] == country
    filtrado = df[filtro]
    campos = ['Population, total']
    filtro= filtrado['Indicator Name'].isin(campos)
    filtrado = filtrado[filtro]
    filtrado = filtrado.loc[:,['Indicator Name',year]]
    filtrado = filtrado.reset_index()
    return str(filtrado.loc[0][year])