import pandas as pd
import glob
import matplotlib.pyplot as plt
#devuelve un Dataframe de pandas con todos los datasets del directorio que se le indique por argumentos "path"
def obtain_all_datasets(path):
    all_files = glob.glob(path + "/*.csv")

    li = []

    for filename in all_files:
        df = pd.read_csv(filename, sep=';', encoding='cp1252')

        df.rename(columns={'Importe': 'IMPORTE', '      Importe': 'IMPORTE', '       Importe':'IMPORTE',
                           'SECCION ':'SECCION', 'Descripción':'SECCION', 'N.I.F': 'NIF', 'Tercero': 'CONTRATISTA', 'Contratista': 'CONTRATISTA'}, inplace=True)
        if '2015' in filename:
            df['ANNO']='2015'
        elif '2016' in filename:
            df['ANNO']='2016'
        elif '2017' in filename:
            df['ANNO']='2017'
        elif '2018' in filename:
            df['ANNO']='2018'
        elif '2019' in filename:
            df['ANNO']='2019'
        #quitamos los puntos de los miles y las comas de los decimales (cambio a puntos). tambien se quitan espacios y euros
        df['IMPORTE']=df['IMPORTE'].str.replace('.','')
        df['IMPORTE'] = df['IMPORTE'].str.replace(' ', '')
        df['IMPORTE'] = df['IMPORTE'].str.replace('€', '')
        df['IMPORTE'] = df['IMPORTE'].str.replace(',', '.')
        df['IMPORTE'] = df['IMPORTE'].astype('float')
        df = df[['CONTRATISTA', 'IMPORTE', 'SECCION', 'ANNO']]
        li.append(df)

    datasets = pd.concat(li, axis=0, ignore_index=True)

    return datasets


#funcion que reciba empresa y lista de anos y devuelva un diccionario con el numero de contratos y lo facturado por la empresa dichos anos

def func3(empresa, year_list):
    #En principio los ficheros estan en la misma carpeta que el fichero de python
    dataset = obtain_all_datasets(".")
    dataset = dataset[(dataset['CONTRATISTA'] == empresa)]
    mydict = dict()
    for year in year_list:
        suma =  dataset[dataset['ANNO']==year]['IMPORTE'].sum()
        total = len(dataset[dataset['ANNO']==year].index)
        mydict[year]=[suma, total]
    #dataset.to_csv('./out/isa.csv', sep=";", encoding='utf-8')
    #print(mydict)
    return mydict

#func3('PROSELEC SEGURIDAD S.A.U.',['2015','2016'])

def func4(top, year_list):
    #En principio los ficheros estan en la misma carpeta que el fichero de python
    dataset = obtain_all_datasets(".")
    ax = plt.gca()
    data=dataset[dataset['ANNO'].isin(year_list)].groupby(['CONTRATISTA'], as_index=False).sum().sort_values(by=['IMPORTE'], ascending=False).head(top)
    mytop=data['CONTRATISTA'].tolist()
    data.plot(x='CONTRATISTA', kind='bar', color="r",ax=ax)
    plt.show()
    return mytop
#func4(3,['2015','2016'])


def func5(top, year_list):
    #En principio los ficheros estan en la misma carpeta que el fichero de python
    dataset = obtain_all_datasets(".")
    ax = plt.gca()
    #entendemos que se refiere a las que mas facturan entre todos los annos, ya que de lo contrario puede haber empresas que salgan en
    #unos annos y en otros no (o que no esten en el top de ese anno)
    #Por ello guardamos en el primer dataset aquellas que son el top del acumulado en todos los annos, para luego filtrar en el bucle solo por ellas
    top_years=dataset[dataset['ANNO'].isin(year_list)].groupby(['CONTRATISTA'], as_index=False).sum().sort_values(by=['IMPORTE'], ascending=False).head(top)
    li=[]
    for year in year_list:
        # Consideramos que se quiere ver solo lo que se gana cada anno para los que quedaron en el top final.
        # En caso de querer ver la suma de annos para hacer la evolucion de lo que van acumulando,
        # cambiar dataset['ANNO']==year por dataset['ANNO']<=year en la siguiente linea
        data = dataset[(dataset['ANNO']==year) & (dataset['CONTRATISTA'].isin(top_years['CONTRATISTA'].tolist()))].groupby(['CONTRATISTA'], as_index=False).sum().sort_values(
            by=['IMPORTE'], ascending=False).head(top)
        data['ANNO']=year
        li.append(data)
    dataset = pd.concat(li, axis=0, ignore_index=True)

    #print(dataset)
    dataset.groupby(['CONTRATISTA'], as_index=False).plot(x='ANNO',ax=ax)
    plt.legend(dataset['CONTRATISTA'].tolist())
    plt.show()
    return
#func5(3,['2015','2016','2017'])


# Entendemos que el total facturado a las secciones es realmente el total facturado en el anno (todas las secciones)
def func6(year_list):
    dataset = obtain_all_datasets(".")
    ax = plt.gca()

    dataset=dataset.groupby('ANNO', as_index=False).sum()
    dataset=dataset[dataset['ANNO'].isin(year_list)]
    print(dataset)
    dataset.plot(x='ANNO', ax=ax)
    plt.show()
    return

#func6(['2015','2016','2019'])

# Otra forma de ver el ejercicio 6 es agrupando por secciones aunque la leyenda del grafico es muy grande en funcion de los annos de la lista
def func6_2(year_list):
    dataset = obtain_all_datasets(".")
    ax = plt.gca()

    li = []
    for year in year_list:
        data = dataset[dataset['ANNO']==year].groupby(['SECCION'], as_index=False).sum()
        data['ANNO'] = year
        li.append(data)
    dataset = pd.concat(li, axis=0, ignore_index=True)
    dataset=dataset[dataset['ANNO'].isin(year_list)]
    print(dataset)
    dataset.groupby(['SECCION'], as_index=False).plot(x='ANNO', ax=ax)
    plt.legend(dataset['SECCION'].tolist(), fontsize='xx-small', loc='best')
    plt.show()
    return

#func6_2(['2015','2016','2019'])