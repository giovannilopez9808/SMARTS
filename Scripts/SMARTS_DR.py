from SMARTS_algorithm import *
# Parametros para interactuar con el modelo, esto esta modificado para el uso de las estaciones SIMA en el periodo 2015-2020
parameters = {
    "path stations": "../Data/",
    "folder measurements": "Mediciones",
    "path results": "Results_SMARTS_DR_",
    "file results": "Data_found_",
    "file data": "datos.txt",
    "stations": ["noreste"],
    "hour initial": 9,
    "hour final": 16,
    "wavelength initial": 285,
    "wavelength final": 2800,
    "AOD inicial": 0.01,
    "AOD limite": 1,
    "RD limite": 10,
    "RD delta": 1,
    "igas": 1,
    #    "igas": 3,
}

for station in parameters["stations"]:
    # Inicialización del objeto que contiene a la clase SMARTS con sus parametros de entrada
    SMARTS_Model = SMARTS_DR(parameters=parameters,
                             station=station)
    print("Calculando estacion "+station)
    SMARTS_Model.run_search()
