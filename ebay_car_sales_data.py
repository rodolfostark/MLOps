"""
Autor: Jonatas Rodolfo Pereira dos Santos
Data: Nov. 2021
Descrição: Este projeto tem como principal objetivo exercitar os conceitos
de análise e filtragem de dados de uma loja de carros usados do ebay com base num
projeto guiado do dataquest que pode ser acessado em:
https://app.dataquest.io/c/54/m/294/guided-project%3A-exploring-ebay-car-sales-data/
"""
# Importando os módulos do pandas e do numpy
import pandas as pd

if __name__ == '__main__':
    # Lendo o dataset, convertendo para dataframe e atribuindo para a variavel autos
    autos = pd.read_csv('autos.csv', encoding='Latin-1')
    # Criando um dicionário com as colunas para renomear no dataset
    new_column_names = {
        'vehicleType': 'vehicle_type',
        'dateCrawled': 'date_crawled',
        'offerType': 'offer_type',
        'powerPS': 'power_ps',
        'fuelType': 'fuel_type',
        'yearOfRegistration': 'registration_year',
        'monthOfRegistration': 'registration_month',
        'notRepairedDamage': 'unrepaired_damage',
        'dateCreated': 'ad_created',
        'nrOfPictures': 'nr_of_pictures',
        'postalCode': 'postal_code',
        'lastSeen': 'last_seen'
    }
    # Renomeando as colunas do dataset, usando o dicionario anterior
    autos = autos.rename(columns=new_column_names)
    # Criando uma lista com as colunas que serão removidas do dataset
    columns_to_be_dropped = ['seller', 'offer_type', 'abtest']
    # Removendo as colunas previmente selecionadas do dataset
    autos.drop(columns=columns_to_be_dropped, inplace=True)
    # Covertendo os dados da coluna de preços para um tipo numerico
    autos['price'] = [
        float(value
              .replace('$', '')
              .replace(',', ''))
        for value in autos.price
    ]
    # Convertendo os dados da coluna de kilometragem para um tipo numerico
    autos['odometer'] = [
        float(value
              .replace('km', '')
              .replace(',', ''))
        for value in autos.odometer
    ]
    # Criando o dicionario para renomear a coluna odometer
    new_named_column = {
        'odometer': 'odometer_km'
    }
    # Renomeando a coluna odometer para odometer_km
    autos = autos.rename(columns=new_named_column)
    # Filtrando os carros cujo ano de registro estão entre 1900 e 2016
    autos = autos[autos['registration_year'].between(1900, 2016)]
    # Criando uma lista com as 20 marcas de carro mais frequentes no dataset
    brand_list = autos.brand.value_counts().head(20).index
    # Craindo os dicionarios para agregar os dados de marca e kilometragens médias
    dictionary_cars_brand = {}
    dictinary_odometer_mean = {}
    # Iterando na lista de marcas para extrair a média de cada feature
    for brand in brand_list:
        # Atribuindo para cada marca o seu preço médio
        dictionary_cars_brand[brand] = autos[
            autos['brand'] == brand
            ]['price'].mean()
        # Atribuindo para cada marca sua kilometragem média
        dictinary_odometer_mean[brand] = autos[
            autos['brand'] == brand
            ]['odometer_km'].mean()
    # Criando séries com base nos dicionários das médias
    mean_brand_price = pd.Series(dictionary_cars_brand)
    mean_odometer_km = pd.Series(dictinary_odometer_mean)
    # Criando um dataframe com as séries definidas
    dataframe_brand = pd.DataFrame(mean_brand_price, columns=['mean_price'])
    dataframe_brand['mean_odometer_km'] = mean_odometer_km
