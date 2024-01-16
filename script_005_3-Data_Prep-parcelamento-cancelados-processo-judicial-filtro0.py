#!/usr/bin/env python
# coding: utf-8

# ## Divída Ativa
# 
# More background on the project
# 
# ### Data Sources
# - file1 : Description of where this file came from
# 
# ### Changes
# - 12-18-2023 : Started project




import pandas as pd
from pathlib import Path
from datetime import datetime
from config import Config


# ### File Locations
today = datetime.today()
nome_arquivo = 'parcelamento-cancelados-processo-judicial-filtro0'
file_directory = Config.DIR_DESTINO / "csv"
summary_file = Path.cwd() / "data" / "processed" / f"summary_{nome_arquivo}.pkl"

in_files = [f for f in file_directory.glob('*.csv') 
            if f.name.startswith(nome_arquivo)]

dtypes = {
    'Inscrição': 'string',
    'Ano': 'int64',
    'Numero': 'int64',
    # 'Pc': 'int64',
    # 'Pcs': 'int64',    
}

dataframe_list = []
for file_ in in_files:
    try:
        dfi = pd.read_csv(file_, skiprows=1, sep=';', encoding='ANSI')
        if dfi.shape[0] > 0:
            contador = 0
            while contador <= 10:
                if 'Proc.Judicial' in dfi.columns:
                    break
                columns = dfi.iloc[0]
                dfi.columns = columns
                dfi = dfi.iloc[1:]
                # print(dfi.columns)
                contador += 1


            dataframe_list.append(dfi)
            # print(dfi.shape, dfi.columns, file_)
        
        if dfi.shape[0] == 3:
            pass

    except Exception  as error:
        print(error)
    

if dataframe_list:
    print('Qtd dataframes:', len(dataframe_list))
    for dfi in dataframe_list:
        print(dfi.shape)
        
    df = pd.concat(dataframe_list, ignore_index=True)
    print(df.shape)
    df.head()

    # https://stackoverflow.com/questions/30763351/removing-space-in-dataframe-python
    df.columns = [x.strip() for x in df.columns]

    cols_to_rename = {'col1': 'New_Name'}
    df.rename(columns=cols_to_rename, inplace=True)

    df.to_pickle(summary_file)

    df.columns = [x.strip() for x in df.columns]
    df.columns

    {col: '' for col in df.columns}

    cols_to_rename = {
        'Inscrição'       : 'Inscricao',
        'Descrição'       : 'Descricao',
        'Vl Parcelamento' : 'ValorParcelado',
        'Valor pago'      : 'ValorPago',
        'Proc.Judicial'   : 'ProcessoJudicial',
    }
    df.rename(columns=cols_to_rename, inplace=True)
    df.columns

    # ### Clean Up Data Types
    df.dtypes

    df['ValorParcelado'] = (df['ValorParcelado'].str.replace('.', '', regex=False)
                                                .str.replace(',', '.', regex=False)
                                                .astype('Float64'))

    df['ValorPago'] = (df['ValorPago'].str.replace('.', '', regex=False)
                                                .str.replace(',', '.', regex=False)
                                                .astype('Float64'))

    df['Saldo'] = (df['Saldo'].str.replace('.', '', regex=False)
                                                .str.replace(',', '.', regex=False)
                                                .astype('Float64'))

    def corrige_data(date_str):
        dia, mes, ano = date_str.split('/')
        if dia == '00':
            dia = '01'
        if mes == '00':
            mes = '01'
        return f'{dia}/{mes}/{ano}'

    df['Pagos'] = df['Pagos'].apply(corrige_data)

    df.dtypes

    # ### Data Manipulation
    print(df.head(3))

    for col in df.columns:
        print(f'{col:.<30}:', max([len(str(v)) for v in df[col]]))

    df['IdAcordo'] = (
        (df['Ano'].astype(str)) + 
        (df['Numero'].astype(str)).apply(lambda x: f'{x:0>5}')
    )

    for col in df.columns:
        print(f'{col:.<30}:', max([len(str(v)) for v in df[col]]))

    for col in df.columns:
        print(f'{col:.<30}:', min([len(str(v)) for v in df[col]]))

    # ### Save output file into processed directory
        summary_file = summary_file.with_suffix('.parquet')
    df.to_parquet(summary_file)

else:
    print(f'Nenhum dado foi encontrado nos arquivos .csv que iniciam com "{nome_arquivo}"')
