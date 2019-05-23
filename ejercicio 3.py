import pandas as pd
import glob
import matplotlib.pyplot as plt

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
        
        df['IMPORTE']=df['IMPORTE'].str.replace('.','')
        df['IMPORTE'] = df['IMPORTE'].str.replace(' ', '')
        df['IMPORTE'] = df['IMPORTE'].str.replace('€', '')
        df['IMPORTE'] = df['IMPORTE'].str.replace(',', '.')
        df['IMPORTE'] = df['IMPORTE'].astype('float')
        df = df[['CONTRATISTA', 'IMPORTE', 'SECCION', 'ANNO']]
        li.append(df)

    datasets = pd.concat(li, axis=0, ignore_index=True)

    return datasets




def func3(empresa, year_list):
    
    dataset = obtain_all_datasets(".")
    dataset = dataset[(dataset['CONTRATISTA'] == empresa)]
    mydict = dict()
    for year in year_list:
        suma =  dataset[dataset['ANNO']==year]['IMPORTE'].sum()
        total = len(dataset[dataset['ANNO']==year].index)
        mydict[year]=[suma, total]
    print(mydict)
    return(mydict)
func3('PROSELEC SEGURIDAD S.A.U.', ['2015','2016'])  
