from flask import Flask
from flask import request
from collections import defaultdict
import numpy as np
from dateutil import parser
import pandas as pd
import random
from datetime import datetime
from TimeSynth import timesynth as ts

time_sampler = ts.TimeSampler(start_time=1546347600 , stop_time=1577797200)
regular_time_samples = time_sampler.sample_regular_time(num_points=31449600)

random_values_list = [random.randint(1, 101) for _ in regular_time_samples]

time_series_dict = {'time': regular_time_samples, 'values': random_values_list}
df = pd.DataFrame(time_series_dict)

app = Flask(__name__)

@app.route("/filter_by_range")
def filter_by_range():
    start_date = parser.parse(request.args.get('start_date'))
    end_date = parser.parse(request.args.get('end_date'))
    start_date = convertDateTime(start_date)
    end_date = convertDateTime(end_date)
    result = df.query(f'{start_date} <= time < {end_date}')
    return result.to_json()


@app.route("/compare_ranges")
def compare_ranges():
    date1 = parser.parse(request.args.get('date1'))
    date2 = parser.parse(request.args.get('date2'))
    resolver = request.args.get('resolver')
    date1 = get_date(date1, resolver)
    date2 = get_date(date1, resolver)
    result1 = df.query(f'{date1[0]} <= time < {date1[1]}')
    result2 = df.query(f'{date2[0]} <= time < {date2[1]}')
    result = pd.concat([result1,result2], axis=1)
    return result.to_json()


def convertDateTime(dateString):
    return datetime.timestamp(dateString)

def get_date(date, resolver):
    """

    :param date: date to convert into start and end date
    :param resolver: can have values like day, month
    :return: list of start and end timestamp
    """
    if resolver.lower() == 'day':
        date1 = convertDateTime(date)
        pass
    elif resolver.lower == 'month':
        pass
    elif resolver.lower() == 'year':
        pass
    return []


if __name__ == '__main__':
    app.run(debug=True)