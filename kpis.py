import pandas as pd

valid_brands = [
    "Audi","BMW","Mercedes-Benz","Volkswagen","VW","Porsche","Opel","Smart","Maybach",
    "Renault","Peugeot","Citroen","DS Automobiles","Dacia","Bugatti",
    "Fiat","Alfa Romeo","Lancia","Ferrari","Lamborghini","Maserati","Abarth","Pagani",
    "SEAT","Cupra","Skoda",
    "Volvo","Saab","Koenigsegg","Polestar",
    "Mini","Jaguar","Land Rover","Range Rover","Aston Martin","Bentley","Rolls-Royce","McLaren","Lotus",
    "Ford","Chevrolet","GMC","Cadillac","Buick","Chrysler","Dodge","Jeep","Ram","Lincoln",
    "Tesla","Rivian","Lucid","Hummer",
    "Toyota","Lexus","Honda","Acura","Nissan","Infiniti","Mazda","Mitsubishi","Subaru","Suzuki","Daihatsu","Isuzu",
    "Hyundai","Kia","Genesis",
    "BYD","Geely","Great Wall","Chery","MG","NIO","Xpeng","Lynk & Co","Ora","Zeekr",
    "Tata","Mahindra",
    "Iveco","MAN","Scania","DAF","Renault Trucks","Volvo Trucks","Mercedes-Benz Vans","Ford Trucks"
]

df = pd.read_excel('stock_list.xlsx')
df = df[df['Hersteller'].isin(valid_brands)]
df_sales = pd.read_excel('sales_list.xlsx')

#------------STOCK LIST-------------------------------
def n_of_cars():
    cars = int(df['FIN'].count())
    cars = int(cars)
    return cars

def brands_available():
    brands_list = df['Hersteller'].unique()
    brands_list.tolist()
    return brands_list

def count_p_brand(brand):
    brand_count = df['Hersteller'].value_counts()
    brand_count = brand_count.to_dict()
    return brand_count.get(brand, 0)

#------------SALES LIST-------------------------------

def units_sold(brand):
    units_sales = df_sales['Hersteller'].value_counts()
    units_sales = units_sales.to_dict()
    return units_sales.get(brand, 0)



