#! /usr/bin/env python

import csv
import memcache
import sqlite3


class ZipcodeDb(object):
    DB_PATH = 'db/zipcodes.db'
    TABLE_NAME = 'zipcodes'


    def __init__(self):
        self.db = sqlite3.connect(self.DB_PATH)
        self.memcache = memcache.Client(['127.0.0.1:11211'])
        self.cursor = self.db.cursor()
        self.createTable()


    def createTable(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS " + self.TABLE_NAME + "("
                                "id INTEGER PRIMARY KEY AUTOINCREMENT,"
                                "zipcode INTEGER,"
                                "city TEXT,"
                                "aliases TEXT,"
                                "areacode TEXT,"
                                "latitude REAL,"
                                "longitude REAL"
                            ")")


    def insertRecord(self, zipcode, city, aliases, areacode, latitude, longitude):
        self.cursor.execute('INSERT INTO %s VALUES (NULL, ?, ?, ?, ?, ?, ?)' % self.TABLE_NAME, (zipcode, city, aliases, areacode, latitude, longitude))


    def updateRecord(self, id, zipcode, city, aliases, areacode, latitude, longitude):
        self.cursor.execute('UPDATE %s SET zipcode=%d, city=\'%s\', aliases=\'%s\', areacode=\'%s\', latitude=%f, longitude=%f WHERE id=%d' % \
                        (self.TABLE_NAME, zipcode, city, aliases, areacode, latitude, longitude, id))


    def getRecordByZipcode(self, zipcode):
        record = self.memcache.get(str(zipcode))

        if not record:
            self.cursor.execute('SELECT * FROM %s WHERE zipcode = ?' % self.TABLE_NAME, (zipcode,))
            record = self.cursor.fetchone()
            self.memcache.set(str(zipcode), record)

        return record


    def getRecordByCity(self, city):
        self.cursor.execute('SELECT * FROM %s WHERE UPPER(city) LIKE UPPER(?)' % self.TABLE_NAME, (city,))
        return self.cursor.fetchall()


    def updateDb(self, filename):
        with open(filename, 'r') as csvFile:
            csvReader = csv.DictReader(csvFile)
            for fields in csvReader:
                # Escape single quotes
                fields['primary_city'] = fields['primary_city'].replace('\'', '\'\'')
                fields['acceptable_cities'] = fields['acceptable_cities'].replace('\'', '\'\'')

                # If the field is already in the database, update it. Otherwise, insert it
                record = self.getRecordByZipcode(fields['zip'])
                if record is None:
                    print 'Inserting ' + fields['zip']
                    self.insertRecord(int(fields['zip']), fields['primary_city'], fields['acceptable_cities'], fields['area_codes'], float(fields['latitude']), float(fields['longitude']))
                else:
                    print 'Updating ' + fields['zip']
                    self.updateRecord(record[0], int(fields['zip']), fields['primary_city'], fields['acceptable_cities'], fields['area_codes'], float(fields['latitude']), float(fields['longitude']))

        self.db.commit()



if __name__ == '__main__':
    print "Updating database"

    db = ZipcodeDb()
    db.updateDb('db/zipcodes.csv')

    print "Database updated"
