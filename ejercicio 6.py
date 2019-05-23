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
    
def func6(year_list):
    dataset = obtain_all_datasets(".")
    ax = plt.gca()

    dataset=dataset.groupby('ANNO', as_index=False).sum()
    dataset=dataset[dataset['ANNO'].isin(year_list)]
    print(dataset)
    dataset.plot(x='ANNO', ax=ax)
    plt.show()
    return
func6(['2015','2016','2019'])

