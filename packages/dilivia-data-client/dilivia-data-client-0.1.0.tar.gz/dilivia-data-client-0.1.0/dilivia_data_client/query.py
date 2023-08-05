from datetime import datetime

import io
from typing import List

import logging
import pandas as pd
import requests
import numpy as np

from dilivia_data_client.mapping_dilivia import \
    LIST_METRICS, LIST_OTHER_METRICS, \
    METRICS_COLNAMES_TYPE, OTHER_METRICS_COLNAMES_TYPE, \
    LIST_MODULES, DILIVIA_START_DATE_TIME, DILIVIA_DATE_TIME_FORMAT


def query(vid: str or List[str],
          start: datetime = DILIVIA_START_DATE_TIME,
          end: datetime = datetime.now(),
          list_modules: List[str] = LIST_MODULES) -> dict:
    """
    Cette fonction va créer un objet JSON "query" à partir des attributs suivants :\n
        - "vid" : l'identifiant d'un véhicule donné
        - "start" : début de la période considérée
        - "end" : fin de la période considérée
        - "list_module" : liste des différents modules considérés
    """
    gts_ids = []
    if isinstance(vid, List):
        gts_ids = vid
    elif isinstance(vid, str) and not(vid == ''):
        gts_ids = [vid]
    return {
        "modulesName": list_modules,
        "start": datetime.strftime(start, DILIVIA_DATE_TIME_FORMAT),
        "end": datetime.strftime(end, DILIVIA_DATE_TIME_FORMAT),
        "gtsIds": gts_ids
    }


def headers(auth_token: str) -> dict:
    """
    Cette fonction va créer l'en tête d'un fichier -
    accessible à partir d'un token "auth_token" donné
    """
    return {'Accept': 'text/plain',
            "Accept-Encoding": "identity",
            'Content-Type': 'application/json',
            'X-Warp10-Token': auth_token}


def error_status_code(request_post: requests.models.Response) -> bool:
    """
    Cette fonction renvoie :\n
        - "False" lorsque la connexion du request_post ne présente aucun défaut (status_code = 200)
        - "True" lorsque la connexion du request_post présente un défaut
    """
    return request_post.status_code != 200


def dataframe_read_csv(csv: str) -> pd.DataFrame:
    """
    A partir de la dataframe au format csv,
    cette fonction va générer les données correspondantes sous forme de dataframe
    """
    metrics = csv.split('\n')[0].split(',')
    list_types = {}
    for met in metrics:
        if met != 'date':
            if met in LIST_METRICS:
                list_types[met] = METRICS_COLNAMES_TYPE[met]["type"]
            elif met in LIST_OTHER_METRICS:
                list_types[met] = OTHER_METRICS_COLNAMES_TYPE[met]["type"]
    try:
        dataframe_ = pd.read_csv(io.StringIO(csv), sep=",", parse_dates=['date'], dtype=list_types)
        for met in metrics:
            if met in LIST_METRICS \
                    and 'target_type' in list(METRICS_COLNAMES_TYPE[met].keys()):
                dataframe_[met].fillna(0.0, inplace=True)
                dataframe_ = dataframe_.astype({met: METRICS_COLNAMES_TYPE[met]['target_type']})
        return dataframe_
    except pd.errors.EmptyDataError:
        return pd.DataFrame()
