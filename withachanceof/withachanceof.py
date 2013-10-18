#! /usr/bin/env python

from flask import Flask
from flask import render_template
from flask import request
from flask import url_for

import constants
import errors
from forecast import Forecast

app = Flask(__name__)


def main():
    app.debug = True
    app.run()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/weather')
def weather():
    location = request.args['location']
    
    if location is not None:
        try:
            forecast = Forecast(location)
            forecast.retrieveForecast()

            return render_template('weather.html', forecast=forecast)
        except errors.GenericError as ge:
            return render_template('index.html', error=ge)
    else:
        return render_template('index.html', error=errors.GenericError(errno=constants.ERROR_NO_INPUT))


if __name__ == '__main__':
    main()
