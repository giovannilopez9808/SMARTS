from pandas import DataFrame, read_csv
from scipy.integrate import trapz
from os import system as terminal
from numpy import (loadtxt,
                   where,
                   array,
                   mean,
                   max)
from functions import mkdir
from os.path import join
from tqdm import tqdm


class SMARTS:
    """
    Clase que contiene las funciones que interactuaran con el modelo SMARTS
    """

    def __init__(self, parameters: dict, station: str) -> None:
        """
        Valores con los cuales se inicializa el modelo SMARTS
        ### inputs
        + station      ----> Estacion que se analizara
        + hour_i       ----> Hora inicial para correr el modelo
        + hour_f       ----> Hora final para correr el modelo
        + lon_ i       ----> Longitud de onda inicial para el modelo
        + lon_ f       ----> Longitud de onda final para el modelo
        + igas         ----> Card 6a del Modelo SMARTS
        + delta_lon    ----> Número de longitudes de onda que se saltara el resultado del modelo
        + total_minute ----> Total minutos que correra el modelo
        """
        self.params = parameters
        self.delta_lon = parameters["wavelength initial"]-280+1
        self.total_minute = int(
            (parameters["hour final"]-parameters["hour initial"])*60)
        self.define_location(station)

    def define_location(self, station: str) -> None:
        stations = {
            "centro": {
                "Lat": 25.670,
                "Lon": -100.338,
                "Height": 0.560},
            "noreste": {
                "Lat": 25.750,
                "Lon": -100.255,
                "Height": 0.476},
            "noroeste": {
                "Lat": 25.757,
                "Lon": -100.366,
                "Height": 0.571},
            "sureste2": {
                "Lat": 25.646,
                "Lon": -100.096,
                "Height": 0.387},
            "suroeste": {
                "Lat": 25.676,
                "Lon": -100.464,
                "Height": 0.694}
        }
        self.lat = stations[station]["Lat"]
        self.lon = stations[station]["Lon"]
        self.height = stations[station]["Height"]

    def atmosphere_state(self):
        pass

    def run(self,
            day: int,
            month: int,
            year: int,
            o3: float,
            aod: float,
            name: str,
            path: str) -> array:
        """
        Función que ejecuta el modelo SMARTS
        ### inputs:
        + day   ----> Dia del año
        + month ----> Mes del año númerico
        + year  ----> Año del dia por analizar
        + o3    ----> ozono del dia
        + aod   ----> AOD del dia
        + name  ----> nombre del archivo de resultados
        + path  ----> direccion para guardar los archivos
        """
        filename = f"{name}.txt"
        filename = join(path,
                        filename)
        file_date = open(filename,
                         "w")
        for minute in range(self.total_minute):
            # Hora y minutos a hora con decimal
            minutes = self.hour_and_minute_to_hours(minute)
            # Escribir el archivo de input para el modelo SMARTS
            self.write_data_input(day,
                                  month,
                                  year,
                                  minutes,
                                  o3,
                                  aod)
            terminal("./smarts.out")
            # Resultado de la integral a partir de los resultaos del modelo SMARTS
            integral = self.read_results()
            # Escritura de los resultados
            file_date.write("{} {}\n".format(minutes,
                                             integral))
        file_date.close()

    def hour_and_minute_to_hours(self, minute: int) -> float:
        return round(self.params["hour initial"]+minute/60, 4)

    def read_results(self, name_result: str = "data.ext.txt"):
        """
        Funcion que realiza la lectura de los resultados del SMARTS
        y realiza la integral del especto a cada minuto
        Describción de variables
        + wavelength ----> longitudes de onda de los resultados del modelo SMARTS
        + irra       ----> Valor del especto de los resultados del modelo SMARTS
        + integral   ----> Valor que irradiancia solar
        """
        # Lectura de los resultados del modelo SMARTS
        wavelength, irradiance = loadtxt(name_result,
                                         skiprows=self.delta_lon,
                                         unpack=True)
        # Calculo de la irradiancia solar a partir de los resultados del modelo SMARTS
        integral = trapz(irradiance,
                         wavelength)
        # Eliminación de los archivos
        terminal("rm data*")
        # Formato de la integral
        integral = str(round(integral))
        return integral

    def write_data_input(self, day: int,
                         month: int,
                         year: int,
                         hour: int,
                         ozono: int,
                         aod: int) -> None:
        """
        Formato del input del modelo SMARTS
        ### inputs:
        + day   -> Dia del año
        + month -> Mes del año númerico
        + year  -> Año del dia por analizar
        + hour  -> Hora del calculo de la irradiancia
        + ozono -> ozono del dia
        + aod   -> AOD del dia
        + igas  -> Card 6a
        """
        file = open("data.inp.txt", "w")
        file.write(" 'AOD={} '\n".format(aod))
        # Card 2
        file.write(" 2\n")
        # Card 2a
        # lat,altit,height
        file.write(" {:.3f} {} {}\n".format(self.lat,
                                            self.height,
                                            0))
        # Card 3
        # IATMOS
        file.write(" 1\n")
        # Card 3a
        file.write(" 'USSA'\n")
        # Card 4
        # H2O
        file.write(" 1\n")
        # Card 4a
        file.write(" 0\n")
        # Card 5
        # Ozono
        file.write(" {} {:.4f}\n".format(1,
                                         ozono/1000))
        # Card 6
        file.write(" 0\n")
        # Card 6a
        # Pristine ----> 1
        # Moderate ----> 3
        file.write(" {}\n".format(self.params["igas"]))
        # Card 7
        # Co2
        file.write(" 390\n")
        # Card 7a
        file.write(" 0\n")
        # Card 8
        file.write(" 'S&F_URBAN'\n")
        # Card 9
        file.write(" 5\n")
        # Card 9a
        file.write(" {} {}\n".format(aod,
                                     2))
        # Card 10
        file.write(" 18\n")
        # Card 10b
        file.write(" 1\n")
        # Card 10d
        # IALBDG, TILT,WAZIM
        file.write(" {} {} {}\n".format(51,
                                        37.,
                                        180.))
        # Card 11---
        # Wave min, Wave max, suncor, solar cons
        file.write(" {} {} {} {}\n".format(self.params["wavelength initial"],
                                           self.params["wavelength final"],
                                           1,
                                           1366.1))
        # ------Card 12---
        file.write(" 2\n")
        # Card 12a
        # Wave min, Wave max, inter wave
        file.write(" {} {} {}\n".format(self.params["wavelength initial"],
                                        self.params["wavelength final"],
                                        1))
        # Card 12b
        file.write(" 1\n")
        # Card 12c
        file.write(" 4\n")
        # Card 13
        file.write(" 1\n")
        # Card 13a
        #  slope, apert, limit
        file.write(" 0 2.9 0\n")
        # Card 14
        file.write(" 0\n")
        # Card 15
        file.write(" 0\n")
        # Card 16
        file.write(" 1\n")
        # Card 17
        file.write(" 3\n")
        # Card 17a
        # Year, month, day, hour, latit, longit, zone
        file.write(" {} {} {} {} {} {} {}\n".format(year,
                                                    month,
                                                    day,
                                                    hour,
                                                    self.lat,
                                                    self.lon,
                                                    -6))
        file.close()


class SMARTS_DR(SMARTS):
    """
    Clase heredada de SMARTS, uso especifico para la versión del modelo
    que calcula el AOD a partir de las mediciones y una RD dada
    """

    def __init__(self, parameters: dict, station: str) -> None:
        """
        Valores con los cuales se inicializa el modelo SMARTS
        ### inputs
        + hour_i       ----> Hora inicial para correr el modelo
        + hour_f       ----> Hora final para correr el modelo
        + lon_ i       ----> Longitud de onda inicial para el modelo
        + lon_ f       ----> Longitud de onda final para el modelo
        + delta_lon    ----> Número de longitudes de onda que se saltara
                           el resultado del modelo
        + total_minute ----> Total minutos que correra el modelo
        + RD_lim       ----> RD al cual se quiere llegar
        + RD_delta     ----> Mas menos del RD
        """
        SMARTS.__init__(self,
                        parameters=parameters,
                        station=station)
        self.params = parameters
        self.station = station
        self.delta_hour = int(
            self.params["hour final"]-self.params["hour initial"])
        self.select_path_name_for_results()

    def select_path_name_for_results(self) -> dict:
        names = {
            1: "pristine",
            3: "moderate"
        }
        name = names[self.params["igas"]]
        self.params["path results"] = self.params["path results"]+name+"/"
        self.params["file results"] = self.params["file results"]+name

    def run_search(self) -> DataFrame:
        # Direccion donde se encuentran los datos de cada estacion
        station_path = join(self.params["path stations"],
                            self.station)
        # Creacion de la carpeta resultados si es que no existe
        path_results = join(station_path,
                            self.params["path results"])
        mkdir(path_results)
        # Archivo de resultados donde se guardara el AOD y la RD de cada dia
        filename = f'{self.params["file results"]}.csv'
        filename_results = join(station_path,
                                filename)
        columns = ["Date",
                   "year",
                   "month",
                   "day",
                   "ozone",
                   "AOD",
                   "RD"]
        AOD_results = DataFrame(columns=columns)
        # Lectura de los parametros de entrada de cada dia
        filename = join(station_path,
                        self.params["file data"])
        data = read_csv(filename)
        with tqdm(data.index, unit="date") as bar:
            for i, index in enumerate(bar):
                self.initialize_aod(self.params["AOD inicial"],
                                    self.params["AOD limite"])
                # Lectura de las mediciones
                filename = f'{data["Date"][index]}.txt'
                filename = join(station_path,
                                self.params["folder measurements"],
                                filename)
                hour, measurements = loadtxt(filename,
                                             skiprows=self.params["hour initial"],
                                             unpack=True)
                # Valor maximo de medicion, esta se usara para el calculo de la RD
                data_max = max(measurements[0:self.delta_hour+1])
                stop = False
                # Primer valor de AOD, se puede cambiar por cualquier otro siempre y cuando este entre aod_i y aod_lim
                aod = self.obtain_aod(self.aod_i,
                                      self.aod_lim)
                # Control de iteracciones
                iter = 0
                while not(stop) and iter < 10:
                    # Ejecucion del modelo SMARTS con los parametros de cada dia
                    self.run(day=data["Day"][index],
                             month=data["Month"][index],
                             year=data["Year"][index],
                             o3=data["Ozone"][index],
                             aod=aod,
                             name=data["Date"][index],
                             path=path_results)
                    # Valor maximo de los resultados del modelo SMARTS
                    data_model = self.obtain_maximum_from_results(data["Date"][index],
                                                                  path=path_results)
                    # Calculo del RD y verificación si se cumple la condicion
                    stop, RD = self.RD_decision(data_model,
                                                data_max)
                    bar.set_postfix(AOD=aod,
                                    RD=RD)
                    if not stop:
                        # Se calculara un nuevo AOD siguiendo el algoritmo de busqueda binaria
                        aod = self.aod_binary_search(aod, RD)
                        # Si se queda en un intervalo muy pequeño se verificara que cumpla la condicion si lo hace entonces escribira en el archivo el resultado, esto llega a pasar  si se pone un delta_RD menor a 1
                        rd_diff = abs(RD-self.params["RD limite"])
                        if self.aod_lim >= aod and rd_diff < self.params["RD delta"]:
                            stop = True
                        iter += 1
                AOD_results.loc[i] = [data["Date"][index],
                                      data["Year"][index],
                                      data["Month"][index],
                                      data["Day"][index],
                                      data["Ozone"][index],
                                      aod,
                                      RD]
            AOD_results.to_csv(filename_results,
                               index=False)

    def initialize_aod(self, aod_i: float, aod_lim: float) -> None:
        """
        Funcion que inicializa el limite inferior y superior del AOD
        """
        self.aod_i = aod_i
        self.aod_lim = aod_lim

    def obtain_aod(self, aod_i: float, aod_f: float) -> float:
        return round((aod_i+aod_f)/2, 3)

    def obtain_maximum_from_results(self, name, path=""):
        filename = f"{name}.txt"
        filename = join(path,
                        filename)
        data_model = loadtxt(filename,
                             usecols=1)
        pos = (where(max(data_model) == data_model)[0])[0]
        data_model = mean(data_model[pos-30:pos+31])
        return data_model

    def RD_decision(self, model: float, measurement: float) -> tuple:
        """
        Funcion que calcula la RD entre el modelo y la medicion
        """
        stop = False
        RD = round(100*(model-measurement)/measurement, 3)
        if self.RD_search(RD):
            stop = True
        return stop, RD

    def aod_binary_search(self, aod: float, RD: float) -> float:
        """
        Función que calcula el AOD que se introducira en el modelo SMARTS
        este emplea una busqueda binaria para que sea más eficiente
        """
        if self.RD_search(RD):
            self.aod_i = aod
        elif RD > self.params["RD limite"]+self.params["RD delta"]:
            self.aod_i = aod
        else:
            self.aod_lim = aod
        aod = self.obtain_aod(self.aod_lim,
                              self.aod_i)
        return aod

    def RD_search(self, RD: float) -> bool:
        lim_i = self.params["RD limite"]-self.params["RD delta"]
        lim_f = self.params["RD limite"]+self.params["RD delta"]
        return lim_i < RD < lim_f


class SMARTS_DR_SSAAER_CUSTOM(SMARTS_DR):
    def __init__(self, parameters: dict, station: str) -> None:
        SMARTS_DR.__init__(self,
                           parameters=parameters,
                           station=station)
        self.params = parameters

    def write_data_input(self, day: int,
                         month: int,
                         year: int,
                         hour: int,
                         ozono: float,
                         aod: float) -> None:
        """
        Formato del input del modelo SMARTS
        day   ----> Dia del año
        month ----> Mes del año númerico
        year  ----> Año del dia por analizar
        hour  ----> Hora del calculo de la irradiancia
        ozono ----> ozono del dia
        aod   ----> AOD del dia
        igas  ----> Card 6a
        """
        file = open("data.inp.txt", "w")
        file.write(" 'AOD={} '\n".format(aod))
        # Card 2
        file.write(" 2\n")
        # Card 2a
        # lat,altit,height
        file.write(" {:.3f} {} {}\n".format(self.lat,
                                            self.height,
                                            0))
        # Card 3
        # IATMOS
        file.write(" 1\n")
        # Card 3a
        file.write(" 'USSA'\n")
        # Card 4
        # H2O
        file.write(" 1\n")
        # Card 4a
        file.write(" 0\n")
        # Card 5
        # Ozono
        file.write(" {} {:.4f}\n".format(1,
                                         ozono/1000))
        # Card 6
        file.write(" 0\n")
        # Card 6a
        # Pristine ----> 1
        # Moderate ----> 3
        file.write(" {}\n".format(self.params["igas"]))
        # Card 7
        # Co2
        file.write(" 390\n")
        # Card 7a
        file.write(" 0\n")
        # Card 8
        file.write(" 'USER'\n")
        # Card 8a
        # SSAAER Palancar
        # Asymmetry Promedio de 550 nm y humedad ente 50-70%
        file.write(" {} {} {} {}\n".format(1, 1, 0.8, 0.68))
        # Card 9
        file.write(" 5\n")
        # Card 9a
        file.write(" {} {}\n".format(aod,
                                     2))
        # Card 10
        file.write(" 18\n")
        # Card 10b
        file.write(" 1\n")
        # Card 10d
        # IALBDG, TILT,WAZIM
        file.write(" {} {} {}\n".format(51,
                                        37.,
                                        180.))
        # Card 11---
        # Wave min, Wave max, suncor, solar cons
        file.write(" {} {} {} {}\n".format(self.params["wavelength initial"],
                                           self.params["wavelength final"],
                                           1,
                                           1366.1))
        # ------Card 12---
        file.write(" 2\n")
        # Card 12a
        # Wave min, Wave max, inter wave
        file.write(" {} {} {}\n".format(self.params["wavelength initial"],
                                        self.params["wavelength final"],
                                        1))
        # Card 12b
        file.write(" 1\n")
        # Card 12c
        file.write(" 4\n")
        # Card 13
        file.write(" 1\n")
        # Card 13a
        #  slope, apert, limit
        file.write(" 0 2.9 0\n")
        # Card 14
        file.write(" 0\n")
        # Card 15
        file.write(" 0\n")
        # Card 16
        file.write(" 1\n")
        # Card 17
        file.write(" 3\n")
        # Card 17a
        # Year, month, day, hour, latit, longit, zone
        file.write(" {} {} {} {} {} {} {}\n".format(year,
                                                    month,
                                                    day,
                                                    hour,
                                                    self.lat,
                                                    self.lon,
                                                    -6))
        file.close()
