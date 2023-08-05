from datetime import datetime

import numpy as np


# Modules et métriques

# Liste des 12 modules disponibles
LIST_MODULES = [
    "clientSource", "GpsRawModule", "GpsBaseModule", "CartoModule",
    "GeoSpatialModule", "VehicleModule", "TripModule", "AccelerationModule",
    "WeatherModule", "LanduseModule", "ElevationModule", "communautoSource"
]

# Dictionnaire des différentes métriques avec les modules auxquels elles appartiennent
METRICS_MODULES = {
    "sumTime": "GpsRawModule",
    "sumMetre": "GpsRawModule",

    "deltaTime": "GeoSpatialModule",
    "deltaDistance": "GeoSpatialModule",

    "accumulatedDuration": "GpsBaseModule",
    "accumulatedGpsDistance": "GpsBaseModule",
    "gpsAccX": "GpsBaseModule",
    "gpsSpeed": "GpsBaseModule",
    "sunAzimuth": "GpsBaseModule",
    "sunAltitude": "GpsBaseModule",
    "sunStatus": "GpsBaseModule",
    "moving": "GpsBaseModule",
    "deltaDuration": "GpsBaseModule",
    "deltaGpsDistance": "GpsBaseModule",
    "curveRadiusCategory": "GpsBaseModule",
    "raw.gps.lat": "GpsBaseModule",
    "raw.gps.lng": "GpsBaseModule",
    # "azimuth": "GpsBaseModule",
    "gpsAccY": "GpsBaseModule",

    "accumulatedMapMatchDistance": "CartoModule",
    "accumulatedMapMatchDuration": "CartoModule",
    "matchType": "CartoModule",
    "deltaMapMatchDistance": "CartoModule",
    "deltaMapMatchDuration": "CartoModule",
    "map.gps.lat": "CartoModule",
    "map.gps.lng": "CartoModule",
    "map.route.curve.status": "CartoModule",
    "mapMatchAzimuth": "CartoModule",
    "mapMatchCurveRadius": "CartoModule",

    "vehicleId": "VehicleModule",

    "tripId": "TripModule",
    "tripDistance": "TripModule",
    "tripDuration": "TripModule",
    "tripCount": "TripModule",
    "tripEvent": "TripModule",

    "gpsAccx": "AccelerationModule",
    "gps_speed": "AccelerationModule",
    "gpsAccy": "AccelerationModule",
    "azimuth": "AccelerationModule",

    "temperature": "WeatherModule",
    "condition": "WeatherModule",

    "landuseOsmId": "LanduseModule",
    "landuseOsmType": "LanduseModule",
    "landuseType": "LanduseModule",

    "altitude": "ElevationModule",

    "gpsValid": "communautoSource",
    "odometer": "communautoSource",
    "heading": "communautoSource",
    "address": "communautoSource",
    # "gpsSpeed": "communautoSource",
    # "moving": "communautoSource"
}

# Dictionnaire des différentes métriques avec leur nom dans la base de données et leur type
METRICS_COLNAMES_TYPE = {
    "sumTime": {"name": "sumTime", "type": np.float64},
    "sumMetre": {"name": "sumMetre", "type": np.float64},

    "deltaTime": {"name": "deltaTime", "type": np.float64},
    "deltaDistance": {"name": "deltaDistance", "type": np.float64},

    "accumulatedDuration": {"name": "accumulatedDuration", "type": np.float64},
    "accumulatedGpsDistance": {"name": "accumulatedGpsDistance", "type": np.float64},
    "gpsAccX": {"name": "gpsAccX", "type": np.float64},
    "gpsSpeed": {"name": "gpsSpeed", "type": np.float64},
    "sunAzimuth": {"name": "sunAzimuth", "type": np.float64},
    "sunAltitude": {"name": "sunAltitude", "type": np.float64},
    "sunStatus": {"name": "sunStatus", "type": str},
    "moving": {"name": "moving", "type": None, 'target_type': 'bool'},
    "deltaDuration": {"name": "deltaDuration", "type": np.float64},
    "deltaGpsDistance": {"name": "deltaGpsDistance", "type": np.float64},
    "curveRadiusCategory": {"name": "curveRadiusCategory", "type": str},
    "raw.gps.lat": {"name": "raw.gps.lat", "type": np.float64, 'target_type': np.float64},
    "raw.gps.lng": {"name": "raw.gps.lng", "type": np.float64, 'target_type': np.float64},
    # "azimuth": "GpsBaseModule",
    "gpsAccY": {"name": "gpsAccY", "type": np.float64},

    "accumulatedMapMatchDistance": {"name": "accumulatedMapMatchDistance", "type": np.float64},
    "accumulatedMapMatchDuration": {"name": "accumulatedMapMatchDuration", "type": np.float64},
    "matchType": {"name": "matchType", "type": str},
    "deltaMapMatchDistance": {"name": "deltaMapMatchDistance", "type": np.float64},
    "deltaMapMatchDuration": {"name": "deltaMapMatchDuration", "type": np.float64},
    "map.gps.lat": {"name": "map.gps.lat", "type": np.float64, 'target_type': np.float64},
    "map.gps.lng": {"name": "map.gps.lng", "type": np.float64, 'target_type': np.float64},
    "map.route.curve.status": {"name": "map.route.curve.status", "type": str},
    "mapMatchAzimuth": {"name": "mapMatchAzimuth", "type": np.float64},
    "mapMatchCurveRadius": {"name": "mapMatchCurveRadius", "type": np.float64},

    "vehicleId": {"name": "vehicleId", "type": str},

    "tripId": {"name": "tripId", "type": str},
    "tripDistance": {"name": "tripDistance", "type": np.float64},
    "tripDuration": {"name": "tripDuration", "type": np.float64},
    "tripCount": {"name": "tripCount", "type": np.float64, 'target_type': np.int64},
    "tripEvent": {"name": "tripEvent", "type": str},

    "gpsAccx": {"name": "gpsAccx", "type": np.float64},
    "gps_speed": {"name": "gps_speed", "type": np.float64},
    "gpsAccy": {"name": "gpsAccy", "type": np.float64},
    "azimuth": {"name": "azimuth", "type": np.float64},

    "temperature": {"name": "temperature", "type": np.int64},
    "condition": {"name": "condition", "type": str},

    "landuseOsmId": {"name": "landuseOsmId", "type": np.int64},
    "landuseOsmType": {"name": "landuseOsmType", "type": str},
    "landuseType": {"name": "landuseType", "type": str},

    "altitude": {"name": "altitude", "type": np.float64},

    "gpsValid": {"name": "gpsValid", "type": None, 'target_type': 'bool'},
    "odometer": {"name": "odometer", "type": np.float64},
    "heading": {"name": "heading", "type": np.int64},
    "address": {"name": "address", "type": str},
    # "gpsSpeed": {"name": "gpsSpeed", "type": np.int64},
    # "moving": {"name": "moving", "type": "bool"}
}

# Liste des différentes métriques
LIST_METRICS = list(METRICS_COLNAMES_TYPE)

# Dictionnaire des informations primaires (id, boîtier, date, coordonnées GPS) et leur type associé
OTHER_METRICS_COLNAMES_TYPE = {
    "id": {"name": "id", "type": str},
    "deviceName": {"name": "deviceName", "type": str},
    "date": {"name": "date", "type": datetime},
    "lat": {"name": "lat", "type": np.float64},
    "lon": {"name": "lon", "type": np.float64}
}

# Liste des informations primaires
LIST_OTHER_METRICS = list(OTHER_METRICS_COLNAMES_TYPE)

# Liste de l'ensemble des métriques
ALL_METRICS = LIST_METRICS + LIST_OTHER_METRICS

# Dictionnaire des différentes métriques associées à leur module et à leur colname
METRICS_MODULES_COLNAMES = {}
for m in LIST_METRICS:
    METRICS_MODULES_COLNAMES[m] = {
        "module": METRICS_MODULES[m],
        "colname": METRICS_COLNAMES_TYPE[m]
    }


# Listes métriques concernant véhicules et trajets

LIST_METRICS_VEHICLE = ["id", "deviceName", "vehicleId", "tripDistance"]
LIST_METRICS_VEHICLE_OUTPUT = ["id", "deviceName", "vehicleId", "distance"]
LIST_METRICS_TRIP = ["tripId", "date", "id", "deviceName", "lat", "lon",
                     "tripDistance", "tripDuration"]
LIST_METRICS_TRIP_OUTPUT = ["tripId", "date", "id", "deviceName", "depart", "arrivee",
                            "tripDistance", "tripDuration"]


# Paramètres datetime

DILIVIA_DATE_TIME_FORMAT = '%Y-%m-%dT%H:%M:%SZ'
DILIVIA_START_DATE_TIME = datetime.strptime("1970-01-01T00:00:00Z", DILIVIA_DATE_TIME_FORMAT)
