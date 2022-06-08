from SMARTS_algorithm import SMARTS
from pandas import read_csv
from functions import mkdir
from os.path import join
from tqdm import tqdm
"""
Parametros para interactuar con el modelo, esto esta modificado para el uso
de las estaciones noroeste y noreste del SIMA en el periodo 2015-2020
"""
params = {
    "file data": "Data_found_pristine.csv",
    "folder results": "Results_SMARTS_DM",
    "path stations": "../Data",
    "igas": 1,
    "stations": ["noreste"],
    "hour initial": 8,
    "hour final": 17,
    "wavelength initial": 285,
    "wavelength final": 2800,
}
for station in params["stations"]:
    # Inicialización del objeto que contiene a la clase SMARTS con sus parametros de entrada
    SMARTS_Model = SMARTS(params,
                          station)
    # Direccion donde se encuentran los datos de cada estacion
    station_path = join(params["path stations"],
                        station)
    # Direccion de los resultados
    # Creacion de la carpeta resultados
    path_results = join(station_path,
                        params["folder results"])
    mkdir(path_results)
    # Lectura de los parametros de entrada de cada dia
    filename = join(station_path,
                    params["file data"])
    data = read_csv(filename)
    # Ciclo para variar los dias
    for index in tqdm(data.index):
        # Ejecucion del modelo SMARTS
        SMARTS_Model.run(data["day"][index],
                         data["month"][index],
                         data["year"][index],
                         data["ozone"][index],
                         data["AOD"][index],
                         data["Date"][index],
                         path=path_results)
