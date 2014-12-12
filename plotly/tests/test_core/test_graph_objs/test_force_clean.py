from __future__ import absolute_import

from plotly.graph_objs import *

def createTraceByType(type):
    test_trace = dict(
        x=[1,2,3,4],
        y=[5,6,7,8],
        type=type)
    return test_trace

def test_force_clean_figure_valid_type():
    data = [createTraceByType('bar')]
    fig = Figure()
    fig['data'] = data
    fig.force_clean()
    assert fig['data'][0]['type'] == 'bar'

def test_force_clean_figure_deprecated_type():
    data = [createTraceByType('histogramx'),
            createTraceByType('histogramy')]
    fig = Figure()
    fig['data'] = data
    fig.force_clean()
    assert fig['data'][0]['type'] == 'histogram'
    assert fig['data'][1]['type'] == 'histogram'

def test_force_clean_figure_invalid_type():
    data = [createTraceByType('line')]
    fig = Figure()
    fig['data'] = data
    fig.force_clean()
    assert fig['data'][0]['type'] == 'scatter'
