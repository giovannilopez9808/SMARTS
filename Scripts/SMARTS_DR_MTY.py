from SMARTS_algorithm import SMARTS_DR_SSAAER_CUSTOM
# Parametros para interactuar con el modelo, esto esta modificado para el uso de las estaciones noroeste y noreste del SIMA en el periodo 2015-2020
parameters = {
    "path stations": "../Data",
    "folder measurements": "Mediciones",
    "path results": "Results_SMARTS_DR_SSAAER_",
    "file results": "Data_found_SSAAER_",
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
    #   "Igas": 3,
}

for station in parameters["stations"]:
    # Inicialización del objeto que contiene a la clase SMARTS con sus parametros de entrada
    SMARTS_Model = SMARTS_DR_SSAAER_CUSTOM(parameters=parameters,
                                           station=station)
    print("Calculando estacion "+station)
    SMARTS_Model.run_search()
