from unittest import TestCase
from plotly.graph_objs import graph_objs, Scatter, Data, Marker, Line, Trace
from plotly.exceptions import PlotlyError

import plotly.plotly as py
import plotly.tools as tls
import math
from nose.tools import raises


@raises(PlotlyError)
def test_unequal_xy_length():
    data = tls.TraceFactory.create_quiver(x=[1, 2], y=[1], u=[1, 2], v=[1, 2])


@raises(ValueError)
def test_wrong_scale():
    data = tls.TraceFactory.create_quiver(x=[1], y=[1], u=[1], v=[1],
                                          scale=0)


@raises(ValueError)
def test_wrong_arrow_scale():
    data = tls.TraceFactory.create_quiver(x=[1], y=[1], u=[1], v=[1],
                                          arrow_scale=-1)


class TestQuiver(TestCase):

    def test_one_arrow(self):
        self.assertAlmostEqual(tls.TraceFactory.create_quiver(x=[1], y=[1],
                                                              u=[1], v=[1],
                                                              scale=1),
                               {'y': [1, 2, None, 1.615486170766527, 2,
                                1.820698256761928, None], 'x': [1, 2, None,
                                1.820698256761928, 2, 1.615486170766527, None],
                                'type': 'scatter', 'mode': 'lines'})

    def test_more_kwargs(self):
        self.assertAlmostEqual(tls.TraceFactory.create_quiver(x=[1, 2],
                                                              y=[1, 2],
                                                              u=[math.cos(1),
                                                                 math.cos(2)],
                                                              v=[math.sin(1),
                                                                 math.sin(2)],
                                                              arrow_scale=.4,
                                                              angle=math.pi/6,
                                                              line=Line(
                                                                color='purple',
                                                                width=3)),
                               {'y': [1, 1.0841470984807897, None, 2,
                                      2.0909297426825684, None,
                                      1.044191642387781, 1.0841470984807897,
                                      1.0658037346225067, None,
                                      2.0677536925644366, 2.0909297426825684,
                                      2.051107819102551, None],
                                'x': [1, 1.0540302305868139, None, 2,
                                      1.9583853163452858, None,
                                      1.052143029378767, 1.0540302305868139,
                                      1.0184841899864512, None,
                                      1.9909870141679737, 1.9583853163452858,
                                      1.9546151170949464, None],
                                'line': {'color': 'purple', 'width': 3},
                                'type': 'scatter', 'mode': 'lines', })


@raises(ValueError)
def test_wrong_arrow_scale():
    stream = tls.TraceFactory.create_streamline(x=[0, 2], y=[0, 2],
                                                u=[[-1, -5], [-1, -5]],
                                                v=[[1, 1], [-3, -3]],
                                                arrow_scale=0)


@raises(ValueError)
def test_wrong_density():
    stream = tls.TraceFactory.create_streamline(x=[0, 2], y=[0, 2],
                                                u=[[-1, -5], [-1, -5]],
                                                v=[[1, 1], [-3, -3]],
                                                density=-1)


@raises(PlotlyError)
def test_uneven_x():
    stream = tls.TraceFactory.create_streamline(x=[0, 2, 7, 9], y=[0, 2, 4, 6],
                                                u=[[-1, -5], [-1, -5]],
                                                v=[[1, 1], [-3, -3]])


@raises(PlotlyError)
def test_uneven_y():
    stream = tls.TraceFactory.create_streamline(x=[0, 2, 4], y=[0, 2, 6],
                                                u=[[-1, -5], [-1, -5]],
                                                v=[[1, 1], [-3, -3]])


class TestStreamline(TestCase):

    def test_simple(self):
        self.assertEqual((tls.TraceFactory.create_streamline(x=[0, 2],
                                                             y=[0, 2],
                                                             u=[[-1, -5],
                                                                [-1, -5]],
                                                             v=[[1, 1],
                                                                [-3, -3]],
                                                             density=2,
                                                             arrow_scale=.4,
                                                             angle=math.pi/6,
                                                             line=Line(
                                                              color='purple',
                                                              width=3))).keys(),
                         (['y', 'x', 'line', 'type', 'mode']))
