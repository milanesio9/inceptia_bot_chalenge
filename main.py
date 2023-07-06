import requests
import pandas as pd
import time
import os


def barra_de_carga():
    """
    Funcion encargada de generar barra de carga en la interfaz
    """
    total_time = 2  # Tiempo total en segundos
    interval = 0.1  # Intervalo de actualización de la barra en segundos
    current_time = 0

    while current_time < total_time:
        current_time += interval
        percentage = int(current_time / total_time * 100)
        bar = '[' + '=' * (percentage // 5) + '>' + '.' * (20 - (percentage // 5)) + ']'
        print(f"Cargando: {percentage}% {bar}", end='\r')
        time.sleep(interval)

    os.system('clear')


def is_temperature_greater_than_twenty_eight(
    *,
    temperature: float
) -> bool:
    '''
    Funcion encargada de verificar si la temperatura pasado por parametro es mayor
    a 28°C

    :param temperature `float`: Temperatura en grados Celcius.

    :return False `bool`si la temperatura es menor:
    :return True `bool`si la temperatura es mayor:
    '''
    if temperature > 28:
        return True
    else:
        return False
    

def charge_product_name_and_quantity():
    """
    Funcion encargada de pedir el nombre y la cantidad del producto
    asi como pasarle los parametro product_name y quantity a la funcion
    is_product_available()

    :return False `bool`si is_product_available retorna False:
    :return True `bool`si is_product_available retorna True:
    """
    product_name = input('\nIngrese el nombre del producto: ')

    quantity = int(input("Ingrese cantidad: "))

    get_product_name_and_quantity_from_df()

    results = is_product_available(
        product_name=product_name,
        quantity=quantity
    )

    if results:
        print("\nSe encontro Stock del producto: ", product_name)
    else:
        charge_product_name_and_quantity()
    

# Ejercicio 1:
class GeoAPI:
    API_KEY = "d81015613923e3e435231f2740d5610b"
    LAT = "-35.836948753554054"
    LON = "-61.870523905384076"


    @classmethod
    def is_hot_in_pehuajo(cls):
        """
        Funcion encargada de consultar el clima en pehuajo y determinar
        si la temperatura actual es mayor a 28°C (Method: GET)

        Returns:
            bool: True si la temperatura es mayor a 28°C,
            bool: False si la temperatura es menor
        """
        
        url = f'https://api.openweathermap.org/data/2.5/weather?lat={cls.LAT}&lon={cls.LON}&appid={cls.API_KEY}&units=metric'
        
        try:
            req = requests.get(url=url)
            
            if req.status_code >= 400:
                return False
            
            data = req.json()

            temperature = data['main']['temp']

            result = is_temperature_greater_than_twenty_eight(
                temperature=temperature
            )
            
            return result
            
        except requests.exceptions.RequestException:
            return False
        

# Ejercicio 2.1:
PRODUCT_DF = pd.DataFrame(
    {
        "product_name": ["Chocolate", "Granizado", "Limon", "Dulce de Leche"], "quantity":[3,10,0,5]
    }
)


def get_product_name_and_quantity_from_df():
    """
    Funcion encargada de mostrar el nombre del producto y su cantidad
    """
    board = PRODUCT_DF[["product_name", "quantity"]]
    return print("\n", board)


def is_product_available(product_name, quantity):
    """
    Funcion encargada de: Buscar en un pandas DataFrame y devolver True si existe stock, False caso
    contrario.
    """
    search = PRODUCT_DF.loc[PRODUCT_DF["product_name"] == product_name, "quantity"]

    if not search.empty:
        real_quantity = search.iloc[0]
        if real_quantity >= 0 and quantity <= real_quantity and quantity > 0 and not quantity > real_quantity:
            return True
        else:
            return False
    else:
        print(f"No se encontró el producto {product_name} en el DataFrame.")


# Ejercicio 3:


def start():
    """
    Funcion encargada de iniciar el bot
    """
    print("Iniciando Bot.......")
    time.sleep(5.5)
    
    print("Buscando temperatura en: pehuajo")
    barra_de_carga()

    if GeoAPI.is_hot_in_pehuajo():
        print("#" * 18)
        print("# Bienvenido!! #")
        print("#" * 18)

        charge_product_name_and_quantity()
    
    else:
        print("#" * 18)
        print("# Bienvenido!! 2 #")
        print("#" * 18)

        charge_product_name_and_quantity()


if __name__ == "__main__":
    start()