import requests
import pandas as pd
import time
import os
import random


def loading_bar(
    total_time: int,
    interval: float,
    current_time: int,
    clear: bool
):
    """
    Funcion encargada de generar barra de carga en la interfaz
    """
    total_time = total_time  # Tiempo total en segundos
    interval = interval  # Intervalo de actualización de la barra en segundos
    current_time = current_time

    while current_time < total_time:
        current_time += interval
        percentage = int(current_time / total_time * 100)
        bar = '[' + '=' * (percentage // 5) + '>' + '.' * (20 - (percentage // 5)) + ']'
        print(f"Cargando: {percentage}% {bar}", end='\r')
        time.sleep(interval)

    if clear:
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
    

def charge_discount_code(
    product_name: str,
    quantity: int
) -> bool:
    """
    Funcion encargada de recibir el discount_code para poder validarlo
    """
    discount_code = input('\nIngrese el código de descuento: ')

    print(f'\nValidando código: {discount_code} ingresado')

    loading_bar(
        total_time=2,
        interval=0.1,
        current_time=0,
        clear=True
    )

    validate_discount = validate_discount_code(
        discount_code=discount_code
    )
    
    if validate_discount:
        print(f'\nConfirmando el pedido del producto: {product_name} cantidad: {quantity}\n')

        loading_bar(
            total_time=3,
            interval=0.1,
            current_time=0,
            clear=False
        )

        print(f'Pedido numero: {random.randint(0, 10000)} confirmado con exito!')
     
    else:
        print(f"Codigo de descuento: {discount_code} no es valido\n")

        charge_discount_code(
            product_name=product_name,
            quantity=quantity
        )
  

def charge_product_name_and_quantity():
    """
    Funcion encargada de pedir el nombre y la cantidad del producto
    asi como pasarle los parametro product_name y quantity a la funcion
    is_product_available()
    """
    product_name = input('\nIngrese el nombre del producto: ')

    quantity = int(input("Ingrese cantidad: "))

    print(f"\nBuscando producto: {product_name} cantidad: {quantity}")

    loading_bar(
        total_time=2,
        interval=0.1,
        current_time=0,
        clear=True
    )

    time.sleep(1)

    get_product_name_and_quantity_from_df()

    results = is_product_available(
        product_name=product_name,
        quantity=quantity
    )

    if results:
        print("\nSe encontro Stock del producto:",  product_name)

        charge_discount_code(
            product_name=product_name,
            quantity=quantity
        ) 

    else:
        print("\nNo se encontro stock del producto:",  product_name)

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


def is_product_available(
    product_name: str, 
    quantity: int
) -> bool:
    """
    Funcion encargada de: Buscar en un pandas DataFrame y devolver True si existe stock, False caso
    contrario.

    :return False `bool`si quantity es menos o igual a 0 o mayor al stock disponible o el stock es 0 o menor:
    :return True `bool`si queantity es mayor a cero, menor o igual al stock disponible y el stock disponible es mayor a cero:
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
_AVAILABLE_DISCOUNT_CODES = ["Primavera2021", "Verano2021", "Navidad2x1", "heladoFrozen"]


def validate_discount_code(
    discount_code: str
) -> bool:
    """
    Dada la lista de códigos de descuento vigentes y un código de descuento
    mencionado por el cliente, devuelve True si la diferencia entre el código
    mencionado y los códigos vigentes es menor a tres caracteres, en al menos
    uno de los casos.

    :param discount_code: Código de descuento mencionado por el cliente
    :return: True si hay una diferencia de menos de tres caracteres con al menos uno de los códigos vigentes, False de lo contrario

    Ejemplo:
    "primavera2021" deberia devolver True, ya que al compararlo:
    vs "Primavera2021" = 2 caracteres de diferencia ("p" y "P")
    vs "Verano2021" = 7 caracteres de diferencia ('i', 'n', 'o',
    'm', 'V', 'p', 'v')
    vs "Navidad2x1" = 8 caracteres de diferencia ('N', 'm', '0',
    'x', 'e', 'd', 'p', 'r')
    vs "heladoFrozen" = 14 caracteres de diferencia ('z', 'i',
    'v', 'n',
    'o', 'm', '2', '0', 'd', 'p', '1', 'F', 'h', 'l')
    """
    for code in _AVAILABLE_DISCOUNT_CODES:
        differences = sum(c1 != c2 for c1, c2 in zip(discount_code, code))
        if differences < 3:
            return True
    
    return False

def start():
    """
    Funcion encargada de iniciar el bot
    """
    os.system('clear')

    print("Iniciando Bot.......\n")
    time.sleep(3.5)
    
    print("Buscando temperatura en: pehuajo")
    time.sleep(2)

    loading_bar(
        total_time=2,
        interval=0.1,
        current_time=0,
        clear=True
    )

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