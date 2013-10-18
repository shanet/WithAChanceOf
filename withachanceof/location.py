
class Location(object):
    def __init__(self, id, zipcode, city, aliases, areacode, latitude, longitude):
        self.id = id
        self.zipcode = zipcode
        self.city = city
        self.aliases = aliases
        self.areacode = areacode
        self.latitude = latitude
        self.longitude = longitude
