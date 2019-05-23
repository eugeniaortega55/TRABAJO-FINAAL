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




def func5(top, year_list):
    
    dataset = obtain_all_datasets(".")
    ax = plt.gca()
    
    top_years=dataset[dataset['ANNO'].isin(year_list)].groupby(['CONTRATISTA'], as_index=False).sum().sort_values(by=['IMPORTE'], ascending=False).head(top)
    li=[]
    for year in year_list:
        
        data = dataset[(dataset['ANNO']==year) & (dataset['CONTRATISTA'].isin(top_years['CONTRATISTA'].tolist()))].groupby(['CONTRATISTA'], as_index=False).sum().sort_values(
            by=['IMPORTE'], ascending=False).head(top)
        data['ANNO']=year
        li.append(data)
    dataset = pd.concat(li, axis=0, ignore_index=True)

    print(dataset)
    dataset.groupby(['CONTRATISTA'], as_index=False).plot(x='ANNO',ax=ax)
    plt.legend(dataset['CONTRATISTA'].tolist())
    plt.show()
    return
func5(3,['2015','2016','2017'])
