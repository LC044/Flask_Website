#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time : 2020/8/26 14:48
# @Author : way
# @Site :
# @Describe:

from flask import Flask, render_template
from data import SourceData
from data_corp import CorpData
from data_job import JobData
import numpy as np
import random
import json


def gen_data():
    data = np.random.randint(0, 1500, size=[1, 7])
    # return list(data[0])
    a = [random.randint(0, 50) for i in range(7)]
    # return [12, 16, 18, 20, 52, 32, 12]
    return a


app = Flask(__name__)

app = Flask(__name__, static_url_path='')


@app.route('/get_data1')
def get_data1():
    # data = SourceData()
    data = {
        'series': gen_data()
    }
    return data


@app.route('/get_data2')
def get_data2():
    # data = SourceData()
    data = {
        'series': gen_data()
    }
    return data


@app.route('/')
def index():
    data = SourceData()
    # return render_template('index.html')
    return render_template('visualizedCharts.html', form=data, title=data.title)


@app.route('/corp')
def corp():
    data = CorpData()
    return render_template('visualizedCharts.html', form=data, title=data.title)


@app.route('/job')
def job():
    data = JobData()
    return render_template('visualizedCharts.html', form=data, title=data.title)


@app.route('/123.zip')
def job1():
    f = open('123.zip', 'rb')
    return f.read()


if __name__ == "__main__":
    # app.run()
    app.run(host='127.0.0.1', port=7789, debug=False)
    # app.run(host='192.168.1.100', debug=False)
