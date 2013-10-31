import httplib
import json

import constants
import database
import errors
from location import Location

class Forecast(object):
    skyconsConstantsMap = {"clear-day": "Skycons.CLEAR_DAY",
        "clear-night": "Skycons.CLEAR_NIGHT",
        "partly-cloudy-day": "Skycons.PARTLY_CLOUDY_DAY",
        "partly-cloudy-night": "Skycons.PARTLY_CLOUDY_NIGHT",
        "cloudy": "Skycons.CLOUDY",
        "rain": "Skycons.RAIN",
        "sleet": "Skycons.SLEET",
        "snow": "Skycons.SNOW",
        "wind": "Skycons.WIND",
        "fog": "Skycons.FOG",
    }

    def __init__(self, location):
        db = database.ZipcodeDb()
        
        # Try to get the location by zipcode
        # If no results are returned, try to get the location by city
        searchResults = db.getRecordByZipcode(location)
        if searchResults is None:
            searchResults = db.getRecordByCity(location)

            if len(searchResults) > 1:
                print "Warning: Multiple locations found. Defaulting to first one. TODO: Handle this."
                searchResults = searchResults[0]

            if not searchResults:
                raise errors.LocationNotFoundError(errno=constants.ERROR_NO_LOCATION_FOUND)

        self.location = Location(*searchResults)
        self.forecast = None


    def retrieveForecast(self):
        try:
            httpConnection = httplib.HTTPSConnection('api.forecast.io')
            httpConnection.request('GET', '/forecast/%s/%f,%f' % (constants.APIKEY, self.location.latitude, self.location.longitude))
            response = httpConnection.getresponse()
            if response.status != 200:
                raise errors.GetForecastError(str(response.status), constants.ERROR_GET_FORECAST_NON_200)

            response = response.read()
            httpConnection.close()
            self.forecast = json.loads(response)
        except Exception as e:
            raise errors.GetForecastError(str(e), constants.ERROR_GET_FORECAST_NETWORK_ERROR)


    def getCurrentWeatherSkyconsConstant(self):
        return self.skyconsConstantsMap[self.forecast['currently']['icon']]

    def getSkyconsConstantForDay(self, dayNumber):
        return self.skyconsConstantsMap[self.forecast['daily']['data'][dayNumber]['icon']]
