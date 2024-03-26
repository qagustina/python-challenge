import pandas as pd
import os

def open():
    dir = '../challengue-python'
    excel_file = 'Datos.xlsx' 
    csv_file = 'lut_paises.csv'
    datos = os.path.join(dir, excel_file) 
    lut_paises = os.path.join(dir, csv_file) 
    return datos, lut_paises


def read():
    datos, lut_paises = open()
    excel_df = pd.read_excel(datos)
    csv_df = pd.read_csv(lut_paises, encoding="latin1", delimiter=";")
    return excel_df, csv_df


def merge_files():
    excel_df, csv_df = read()
    merged_df = pd.merge(excel_df, csv_df, how='left', left_on='País', right_on='DescENG')
    merged_df.rename(columns={'DescESP': 'pais_esp'}, inplace=True)
    merged_df.drop(columns=['DescENG'], inplace=True)
    return merged_df


def cod_pais(row):
    '''
    Receives a row as a parameter, for each row convert to expected format.
    '''
    pais_esp = row['pais_esp']
    if pais_esp == "ESTADOS UNIDOS":
        pais_esp = "USA"
    else:
        pais_esp = row['pais_esp'].capitalize()
    return f"{pais_esp} (+{row['Código país']})"


def names_clean():
    '''
    Defines dictionary and lists to later use as filters.
    '''
    country_names = {
    'BRAZIL': 'BRASIL',
    'UNITED STATES': 'USA',
    'SPAIN': 'ESPAÑA',
    'SWEDEN': 'SUECIA',
    'TRINIDAD AND TOBAGO': 'TRINIDAD Y TOBAGO',
    'GERMANY': 'ALEMANIA',
    'BELIZE': 'BELICE',
    'KOREA (SOUTH)': 'COREA DEL SUR',
    'DOMINICAN REPUBLIC': 'REPUBLICA DOMINICANA',
    'DEMOCRATIC REPUBLIC OF THE CONGO(KINSHASA)': 'REPÚBLICA DEMOCRÁTICA DEL CONGO',
    'SOUTH AFRICA': 'SUDAFRICA',
    'KYRGYZSTAN': 'KIRGIZSTAN',
    'LATVIA': 'LETONIA',
    'RUSSIA': 'RUSIA',
    'KENYA': 'KENIA',
    'EQUATORIAL GUINEA': 'GUINEA',
    'BELARUS': 'BIELORRUSIA',
    'TURKEY' : 'TURQUIA',
    'UNITED KINGDOM (GREAT BRITAIN)': 'REINO UNIDO',
    'UNITED ARAB EMIRATES': 'EMIRATOS ARABES UNIDOS',
    'FRANCE': 'FRANCIA'
    }
    relevants_positions = ["ANALISTA", "ASISTENTE", "AUDITOR", "CEO", "DIRECTOR",
                        "ESPECIALISTA", "GERENTE", "INGENIERO", "JEFE", "LIDER",
                        "PRESIDENTE", "REPRESENTANTE", "RESPONSABLE", "SECRETARIO", 
                        "SECRETARIA", "SUBDIRECTOR", "SUBGERENTE", "SUPERVISOR",
                        "VICEPRESIDENTE"]
    return country_names, relevants_positions


def get_area(text):
    '''
    Receives a text as a parameter. Defines dictionary containing each word in the string.
    Make an iterable to search each word in a text string.
    '''
    areas_f = {
    'CADENA DE SUMINISTROS': ['cadena de suministros'],
    'LOGISTICA': ['logística'],
    'OPERACIONES': ['operaciones'],
    'PLANEACION': ['planeación'],
    'PREVENCION DE PERDIDAS': ['prevención de pérdidas'],
    'PRODUCCION': ['producción'],
    'CARGA / EMBARQUES / DESPACHO': ['carga', 'embarques', 'despacho'],
    'COMERCIO EXTERIOR / IMPORTACION / EXPORTACION': ['comercio exterior', 'importación', 'exportación'],
    'COMPRAS': ['compras'],
    'INVENTARIOS': ['inventarios'],
    'LEAN SIX SIGMA / BLACK BELT': ['lean six sigma', 'black belt'],
    'PROCESOS / MEJORA CONTINUA / DESARROLLO ESTRATEGICO': ['procesos', 'mejora continua', 'desarrollo estratégico'],
    'TRAFICO / EXPEDICION': ['tráfico', 'expedición'],
    'TRANSPORTE': ['transporte']
    }
    for area, keywords in areas_f.items():
        if any(keyword in text.lower() for keyword in keywords):
            return area
    return 


def homologate():
    '''
    Assigns country codes to each row in the df using cod_pais function,
    assigns normalized country names using the country_names dictionary.
    Filters Area column by relevants_positions list and creates a new column by using get_area function.
    Exclude null values to create new dataframe later.
    Returns new df
    '''
    country_names, relevants_positions = names_clean()
    merged_df = merge_files()
    merged_df['Codigo pais'] = merged_df.apply(lambda row: cod_pais(row), axis=1)
    merged_df['Pais'] = merged_df['País'].replace(country_names)
    merged_df['Cargo'] = merged_df['Puesto de trabajo'].str.split().str[0].str.upper()
    merged_df_new = merged_df[merged_df.Cargo.isin(relevants_positions)] # filter
    merged_df_new['Area'] = merged_df_new['Puesto de trabajo'].apply(get_area)
    merged_df_new = merged_df_new[merged_df_new["Area"].notna()] # exclude nan values
    return merged_df_new


def create_df():
    '''
    Defines the columns for new df and returns new df.
    '''
    merged_df_new = homologate()
    cols = ['Nombre', 'Correo', 'Pais', 'Codigo pais', 'Teléfono', 'Cargo', 'Area']
    new_df = merged_df_new[cols]
    return new_df


def export_file(df):
    df.to_excel('Datos - homologados.xlsx', index=False)


def main():
    new_df = create_df()
    export_file(new_df)


if __name__ == '__main__': 
    main()