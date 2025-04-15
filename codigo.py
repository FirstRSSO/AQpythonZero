import time
from DFRobot_MultiGasSensor import *
from DFRobot_Ozone import *

# Configuración de direcciones I2C
OZONE_I2C_ADDRESS = 0x73  # Dirección del sensor de ozono
NO2_I2C_ADDRESS = 0x74    # Dirección del sensor NO2

# Número de recogida para el sensor de ozono
COLLECT_NUMBER = 20

# Inicialización de sensores
ozone_sensor = DFRobot_Ozone_IIC(1, OZONE_I2C_ADDRESS)
no2_sensor = DFRobot_MultiGasSensor_I2C(1, NO2_I2C_ADDRESS)

# Variables para los datos de sensores
data_packet = ""

def setup_sensors():
    # Inicializar el sensor de ozono
    while not ozone_sensor:
        print("El sensor de ozono no se encuentra. Reintentando...")
        time.sleep(1)
    print("Sensor de ozono conectado exitosamente.")
    ozone_sensor.set_mode(MEASURE_MODE_PASSIVE)
    time.sleep(2)

    # Inicializar el sensor NO2
    while not no2_sensor:
        print("El sensor NO2 no se encuentra. Reintentando...")
        time.sleep(1)
    print("Sensor NO2 conectado exitosamente.")
    no2_sensor.change_acquire_mode(no2_sensor.PASSIVITY)
    time.sleep(1)
    no2_sensor.set_temp_compensation(no2_sensor.ON)

    # Calentamiento inicial de sensores (3 minutos)
    print("Calentando sensores...")
    start_time = time.time()
    while time.time() - start_time < 180:
        print("*", end="", flush=True)
        time.sleep(1)
    print("\nCalentamiento completado.")

def collect_air_quality_data():
    global data_packet

    # Leer la concentración de NO2 en PPM
    no2_concentration = no2_sensor.read_gas_concentration()
    print(f"Concentración de NO2 (PPM): {no2_concentration}")

    # Leer la concentración de ozono en PPB
    ozone_concentration = ozone_sensor.get_ozone_data(COLLECT_NUMBER)
    print(f"Concentración de Ozono (PPB): {ozone_concentration}")

    # Crear paquete de datos
    data_packet = f"{no2_concentration},{ozone_concentration}"

def main():
    setup_sensors()

    while True:
        collect_air_quality_data()

        # Mostrar los datos en la consola
        print("=== Datos de Calidad del Aire ===")
        print(f"Paquete de Datos: {data_packet}")
        print("===============================")

        # Esperar antes de la siguiente medición
        time.sleep(60)

if __name__ == "__main__":
    main()