import httplib
import json

import constants
import database
import errors
from location import Location

class Forecast(object):

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
