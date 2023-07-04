import requests

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
                raise Exception(req.text)
            
            data = req.json()

            temperature = data['main']['temp']

            result = is_temperature_greater_than_twenty_eight(
                temperature=temperature
            )
            print(data)
            print(result)
        except requests.exceptions.RequestException:
            return False
GeoAPI.is_hot_in_pehuajo()