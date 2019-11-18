config = {
    # https://docs.sqlalchemy.org/en/13/core/engines.html
    #'ConnectionString': 'postgresql+psycopg2://[Username]:[Password]@[Host]:[Port]/[DatabaseName]',
    'ConnectionString': 'mssql+pymssql://[Username]:[Password]@[Host]:[Port]/[DatabaseName]',
    # Pin to indicate if there's a problem (temp/humidity out of range, possibly other problems)
    # The intention is that a user will get more detailed information on a specially designed client (web/mobile app).
    "PinWarningLed": 27,
    # Pin of the data pin on a DHT22 sensor
    'PinHumidityTemperatureSensor': 22,

    # TODO Enhancements
    'PinTemperatureControl': 0,
    'PinHumidityControl': 0,
    'PinLightControl': 0,

    # The hostname or IP of this computer
    'HttpHost': '[IP or hostname]',
    # Port for a client to receive status updates from
    'HttpPort': 8080,
    # If we detect values out of range, show a warning. This will eventually be used to
    # control hardware to correct the problem.
    'SensorWarningLimit': {
        'RelativeHumidity': {   # Percent Relative
            'Min': 90,
            'Max': 100
        }, 
        'Temperature': {        # Degrees Celcius
            'Min': 26.5,
            'Max': 35
        }    
    } 
}