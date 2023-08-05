from datetime import datetime

import logging
from typing import List

import requests
import pandas as pd

from dateutil.relativedelta import relativedelta
from dilivia_data_client import query
from dilivia_data_client.mapping_dilivia import METRICS_MODULES, LIST_METRICS, \
    LIST_METRICS_TRIP, LIST_METRICS_VEHICLE, LIST_METRICS_TRIP_OUTPUT, np, DILIVIA_DATE_TIME_FORMAT,\
    DILIVIA_START_DATE_TIME

pd.options.mode.chained_assignment = None


URL = "https://enovea.dilivia.net/"
ENDPOINT = "db/fetch"  # endpoint nécessaire pour la connexion


class Connexion:
    """
    Cette classe va permettre d'établir la connexion vers les données Fetch\n
        - "url" + "endpoint" : permettent d'établir la connexion
        - "token" : permet d'authentifier l'utilisateur et de pouvoir effectuer une requete
    """

    url = ""
    endpoint = ""
    token = ""

    df = pd.DataFrame()
    param_request = {}
    mapping = {}

    def __init__(self, url: str = "", endpoint: str = ENDPOINT):
        """
        Cette méthode initialise les paramètres de connexion
        """
        self.url = url
        self.endpoint = endpoint

    def auth(self, token: str = ""):
        """
        Cette méthode authentifie l'utilisateur à l'aide du "token"
        """
        self.token = token
        return self

    def get_list_devices(self) -> List[str]:
        df = self.select() \
                 .date() \
                 .vehicle() \
                 .metrics(["id", "vehicleId"]) \
                 .dataframe()
        return sorted(set(df["id"]))

    def get_list_vehicles(self) -> List[str]:
        df = self.select() \
                 .date() \
                 .vehicle() \
                 .metrics(["id", "vehicleId"]) \
                 .dataframe()
        return sorted(set(df["vehicleId"]))

    def select(self) -> 'Connexion':
        """
        Cette méthode va réinitialiser la requête afin d'en effectuer une nouvelle
        """
        self.param_request = {}
        self.mapping = {}
        self.df = pd.DataFrame()
        return self

    def vehicle_devices(self) -> dict:
        list_vehicles = self.get_list_vehicles()
        df_vehicles = self.select().date().vehicle().metrics(["id", "vehicleId"]).dataframe()
        dict_v2ds = {}
        for vehicle in list_vehicles:
            dict_v2ds[vehicle] = []
            for i in range(len(df_vehicles)):
                if df_vehicles['vehicleId'].iloc[i] == vehicle:
                    dict_v2ds[vehicle].append(df_vehicles['id'].iloc[i])
        return dict_v2ds

    def device_vehicles(self) -> dict:
        list_devices = self.get_list_devices()
        df_devices = self.select().date().vehicle().metrics(["id", "vehicleId"]).dataframe()
        dict_d2vs = {}
        for device in list_devices:
            dict_d2vs[device] = []
            for i in range(len(df_devices)):
                if df_devices['vehicleId'].iloc[i] == device:
                    dict_d2vs[device].append(df_devices['id'].iloc[i])
        return dict_d2vs

    def vehicle(self, vid: str = '') -> 'Connexion':
        # TODO : Remplacer boitier par vehicule id
        """
        Cette méthode va alimenter le param_request en remplissant le champ "vid"
        """
        self.param_request['vid'] = vid
        return self

    def vehicles(self, vid_s: List[str] = None):
        if vid_s is None:
            vid_s = []
        self.param_request['vid'] = vid_s
        return self

    def date(self,
             start: datetime = DILIVIA_START_DATE_TIME,
             end: datetime = datetime.now()) -> 'Connexion':
        """
        Cette méthode va alimenter le param_request en remplissant les champs "start" et "end"
        """
        self.param_request['date'] = {'start': datetime.strftime(start, DILIVIA_DATE_TIME_FORMAT),
                                      'end': datetime.strftime(end, DILIVIA_DATE_TIME_FORMAT)}
        return self

    def metrics(self, list_metrics: List[str] = LIST_METRICS) -> 'Connexion':
        """
        Cette méthode va alimenter le champ "metrics" de "param_request" à partir de la
        "list_metrics" entrée
        """
        self.param_request['metrics'] = list_metrics
        return self

    def __filter(self, dataframe_: pd.DataFrame) -> 'Connexion':
        """
        Cette méthode va filtrer, parmi toutes les variables des différents modules générés,
        les colonnes intéressantes (metrics) pour l'utilisateur #
        """
        for metric in self.param_request['metrics']:
            self.df[metric] = dataframe_[metric]
        return self

    def select_vehicle(self, vid: str,
                       start: datetime = DILIVIA_START_DATE_TIME,
                       end: datetime = datetime.now())\
            -> pd.Series:
        """
        Selection des données intéressantes relatives à un véhicule
        """
        dataframe_ = self.select() \
            .vehicle(vid) \
            .date(start, end) \
            .metrics(LIST_METRICS_VEHICLE) \
            .dataframe()
        somme = dataframe_['tripDistance'].sum()
        dataframe_ = dataframe_.iloc[0]
        del dataframe_['tripDistance']
        dataframe_.loc['distance'] = somme
        return dataframe_

    def select_trips(self,
                     vid: str,
                     start=datetime.now() - relativedelta(years=1),
                     end=datetime.now()) \
            -> pd.DataFrame:
        """
        Selection de certaines données pour des trajets
        """
        dataframe_ = self.select() \
            .vehicle(vid) \
            .date(start, end) \
            .metrics(LIST_METRICS_TRIP) \
            .dataframe()
        arr = np.array(dataframe_)
        l_depart = arr.tolist()[::2]
        l_arrivee = arr.tolist()[1::2]
        nb_trips = len(l_arrivee)
        for i in range(nb_trips):
            l_arrivee[i][5] = '(' + str(l_arrivee[i][4]) + ' , ' + str(l_arrivee[i][5]) + ')'
            l_arrivee[i][4] = '(' + str(l_depart[i][4]) + ' , ' + str(l_depart[i][5]) + ')'
        dataframe_2 = pd.DataFrame(l_arrivee, columns=LIST_METRICS_TRIP_OUTPUT)
        return dataframe_2

    def select_metrics(self, vid: str,
                       list_metrics: List[str] = LIST_METRICS,
                       start: datetime = datetime.now() - relativedelta(years=1),
                       end: datetime = datetime.now()) \
            -> pd.DataFrame:
        """
        Selection de certaines "metrics"
        """
        return self.select() \
            .vehicle(vid) \
            .date(start, end) \
            .metrics(list_metrics) \
            .dataframe()

    def __to_query(self) -> dict:
        """
        Cette méthode convertit les query params en query (JSON)
        """
        param_request_ = self.param_request
        list_metrics = param_request_['metrics']
        list_modules = []
        for metric in list_metrics:
            if metric in LIST_METRICS and not METRICS_MODULES[metric] in list_modules:
                list_modules.append(METRICS_MODULES[metric])
        return query.query(param_request_['vid'],
                           datetime.strptime(param_request_['date']['start'],
                                             DILIVIA_DATE_TIME_FORMAT),
                           datetime.strptime(param_request_['date']['end'],
                                             DILIVIA_DATE_TIME_FORMAT),
                           list_modules)

    def dataframe(self) -> pd.DataFrame:
        try:
            response = requests.post(self.url + self.endpoint, json=self.__to_query(),
                                     headers=query.headers(self.token))
            if not query.error_status_code(response):
                try:
                    dataframe_ = query.dataframe_read_csv(response.text)
                    self.__filter(dataframe_)
                    return self.df
                except TypeError:
                    logging.error(response.text)
                    logging.error('No data for vid:' + self.param_request['vid'])
            else:
                logging.error("%s %s" % (response, response.reason))
                logging.error(response.text)
        except (requests.exceptions.InvalidSchema,
                requests.exceptions.MissingSchema,
                KeyError):
            pass
        return pd.DataFrame()
