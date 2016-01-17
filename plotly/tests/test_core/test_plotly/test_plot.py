"""
test_plot:
==========

A module intended for use with Nose.

"""
from __future__ import absolute_import

import json
import requests
import six

from unittest import TestCase
from nose.plugins.attrib import attr
from nose.tools import raises

import plotly.tools as tls
from plotly.tests.utils import PlotlyTestCase
from plotly.plotly import plotly as py
from plotly.exceptions import PlotlyError, PlotlyEmptyDataError
from plotly.files import CONFIG_FILE

# username for tests: 'PlotlyImageTest'
# api_key for account: '786r5mecv0'


class TestPlot(TestCase):
    def setUp(self):
        py.sign_in('PlotlyImageTest', '786r5mecv0',
                   plotly_domain='https://plot.ly')
        self.simple_figure = {'data': [{'x': [1, 2, 3], 'y': [2, 1, 2]}]}
        super(TestPlot, self).setUp()

    @attr('slow')
    def test_plot_valid(self):
        fig = {
            'data': [
                {
                    'x': [1, 2, 3],
                    'y': [2, 1, 2]
                }
            ]
        }
        py.plot(fig, auto_open=False, filename='plot_valid')

    @raises(PlotlyError)
    def test_plot_invalid(self):
        fig = {
            'data': [
                {
                    'x': [1, 2, 3],
                    'y': [2, 1, 2],
                    'z': [3, 4, 1]
                }
            ]
        }
        py.plot(fig, auto_open=False, filename='plot_invalid')

    @raises(TypeError)
    def test_plot_invalid_args_1(self):
        py.plot(x=[1, 2, 3], y=[2, 1, 2], auto_open=False, filename='plot_invalid')

    @raises(PlotlyError)
    def test_plot_invalid_args_2(self):
        py.plot([1, 2, 3], [2, 1, 2], auto_open=False, filename='plot_invalid')

    @raises(PlotlyError)
    def test_plot_invalid_kwargs(self):
        py.plot([{'x': [1, 2], 'y': [10, 20]}], privacy='private')

    def test_plot_empty_data(self):
        self.assertRaises(PlotlyEmptyDataError, py.plot, [],
                          filename='plot_invalid')

    def test_plot_sharing_invalid_argument(self):

        # Raise an error if sharing argument is incorrect
        # correct arguments {'public, 'private', 'secret'}

        kwargs = {'filename': 'invalid-sharing-argument',
                  'sharing': 'privste'}

        with self.assertRaisesRegexp(
                PlotlyError,
                "The 'sharing' argument only accepts"):
            py.plot(self.simple_figure, **kwargs)

    def test_plot_world_readable_sharing_conflict_1(self):

        # Raise an error if world_readable=False but sharing='public'

        kwargs = {'filename': 'invalid-privacy-setting',
                  'world_readable': False,
                  'sharing': 'public'}

        with self.assertRaisesRegexp(
                PlotlyError,
                'setting your plot privacy to both public and private.'):
            py.plot(self.simple_figure, **kwargs)

    def test_plot_world_readable_sharing_conflict_2(self):

        # Raise an error if world_readable=True but sharing='secret'

        kwargs = {'filename': 'invalid-privacy-setting',
                  'world_readable': True,
                  'sharing': 'secret'}

        with self.assertRaisesRegexp(
                PlotlyError,
                'setting your plot privacy to both public and private.'):
            py.plot(self.simple_figure, **kwargs)

    def test_plot_option_logic_only_world_readable_given(self):

        # If sharing is not given and world_readable=False,
        # sharing should be set to private

        kwargs = {'filename': 'test',
                  'auto_open': True,
                  'fileopt': 'overwrite',
                  'validate': True,
                  'world_readable': False}

        plot_option_logic = py._plot_option_logic(kwargs)

        expected_plot_option_logic = {'filename': 'test',
                                      'auto_open': True,
                                      'fileopt': 'overwrite',
                                      'validate': True,
                                      'world_readable': False,
                                      'sharing': 'private'}
        self.assertEqual(plot_option_logic, expected_plot_option_logic)

    def test_plot_option_logic_only_sharing_given(self):

        # If world_readable is not given and sharing ='private',
        # world_readable should be set to False

        kwargs = {'filename': 'test',
                  'auto_open': True,
                  'fileopt': 'overwrite',
                  'validate': True,
                  'sharing': 'private'}

        plot_option_logic = py._plot_option_logic(kwargs)

        expected_plot_option_logic = {'filename': 'test',
                                      'auto_open': True,
                                      'fileopt': 'overwrite',
                                      'validate': True,
                                      'world_readable': False,
                                      'sharing': 'private'}
        self.assertEqual(plot_option_logic, expected_plot_option_logic)

    @attr('slow')
    def test_plot_url_given_sharing_key(self):

        # Give share_key is requested, the retun url should contain
        # the share_key

        validate = True
        fig = tls.return_figure_from_figure_or_data(self.simple_figure,
                                                    validate)
        kwargs = {'filename': 'is_share_key_included',
                  'fileopt': 'overwrite',
                  'world_readable': False,
                  'sharing': 'secret'}
        response = py._send_to_plotly(fig, **kwargs)
        plot_url = response['url']

        self.assertTrue('share_key=' in plot_url)

    @attr('slow')
    def test_plot_url_response_given_sharing_key(self):

        # Given share_key is requested, get request of the url should
        # be 200

        kwargs = {'filename': 'is_share_key_included',
                  'fileopt': 'overwrite',
                  'auto_open': False,
                  'world_readable': False,
                  'sharing': 'secret'}

        plot_url = py.plot(self.simple_figure, **kwargs)
        # shareplot basically always gives a 200 if even if permission denied
        # embedplot returns an actual 404
        embed_url = plot_url.split('?')[0] + '.embed?' + plot_url.split('?')[1]
        response = requests.get(embed_url)

        self.assertEqual(response.status_code, 200)

    @attr('slow')
    def test_private_plot_response_with_and_without_share_key(self):

        # The json file of the private plot should be 404 and once
        # share_key is added it should be 200

        kwargs = {'filename': 'is_share_key_included',
                  'fileopt': 'overwrite',
                  'world_readable': False,
                  'sharing': 'private'}

        private_plot_url = py._send_to_plotly(self.simple_figure,
                                              **kwargs)['url']
        private_plot_response = requests.get(private_plot_url + ".json")

        # The json file of the private plot should be 404
        self.assertEqual(private_plot_response.status_code, 404)

        secret_plot_url = py.add_share_key_to_url(private_plot_url)
        urlsplit = six.moves.urllib.parse.urlparse(secret_plot_url)
        secret_plot_json_file = six.moves.urllib.parse.urljoin(
            urlsplit.geturl(), "?.json" + urlsplit.query)
        secret_plot_response = requests.get(secret_plot_json_file)

        # The json file of the secret plot should be 200
        self.assertTrue(secret_plot_response.status_code, 200)


class TestPlotOptionLogic(PlotlyTestCase):
    conflicting_option_set = (
        {'world_readable': True, 'sharing': 'secret'},
        {'world_readable': True, 'sharing': 'private'},
        {'world_readable': False, 'sharing': 'public'}
    )

    def test_default_options(self):
        options = py._plot_option_logic({})
        config_options = tls.get_config_file()
        for key in options:
            if key != 'fileopt' and key in config_options:
                self.assertEqual(options[key], config_options[key])

    def test_conflicting_plot_options_in_plot_option_logic(self):
        for plot_options in self.conflicting_option_set:
            self.assertRaises(PlotlyError, py._plot_option_logic,
                              plot_options)

    def test_set_config_updates_plot_options(self):
        original_config = tls.get_config_file()
        new_options = {
            'world_readable': not original_config['world_readable'],
            'auto_open': not original_config['auto_open'],
            'sharing': ('public' if original_config['world_readable'] is False
                        else 'secret')
        }
        tls.set_config_file(**new_options)
        options = py._plot_option_logic({})
        for key in new_options:
            self.assertEqual(new_options[key], options[key])


def generate_conflicting_plot_options_in_signin():
    """sign_in overrides the default plot options.
    conflicting options aren't raised until plot or iplot is called,
    through _plot_option_logic
    """
    def gen_test(plot_options):
        def test(self):
            py.sign_in('username', 'key', **plot_options)
            self.assertRaises(PlotlyError, py._plot_option_logic, {})
        return test

    for i, plot_options in enumerate(TestPlotOptionLogic.conflicting_option_set):
        setattr(TestPlotOptionLogic,
                'test_conflicting_plot_options_in_signin_{}'.format(i),
                gen_test(plot_options))
generate_conflicting_plot_options_in_signin()


def generate_conflicting_plot_options_in_tools_dot_set_config():
    """tls.set_config overrides the default plot options.
    conflicting options are actually raised when the options are saved,
    because we push out default arguments for folks, and we don't want to
    require users to specify both world_readable and secret *and* we don't
    want to raise an error if they specified only one of these options
    and didn't know that a default option was being saved for them.
    """
    def gen_test(plot_options):
        def test(self):
            self.assertRaises(PlotlyError, tls.set_config_file,
                              **plot_options)
        return test

    for i, plot_options in enumerate(TestPlotOptionLogic.conflicting_option_set):
        setattr(TestPlotOptionLogic,
                'test_conflicting_plot_options_in_'
                'tools_dot_set_config{}'.format(i),
                gen_test(plot_options))
generate_conflicting_plot_options_in_tools_dot_set_config()


def generate_conflicting_plot_options_with_json_writes_of_config():
    """ if the user wrote their own options in the config file,
    then we'll raise the error when the call plot or iplot through
    _plot_option_logic
    """
    def gen_test(plot_options):
        def test(self):
            config = json.load(open(CONFIG_FILE))
            with open(CONFIG_FILE, 'w') as f:
                config.update(plot_options)
                f.write(json.dumps(config))
            self.assertRaises(PlotlyError, py._plot_option_logic, {})
        return test

    for i, plot_options in enumerate(TestPlotOptionLogic.conflicting_option_set):
        setattr(TestPlotOptionLogic,
                'test_conflicting_plot_options_with_'
                'json_writes_of_config{}'.format(i),
                gen_test(plot_options))
generate_conflicting_plot_options_with_json_writes_of_config()


def generate_private_sharing_and_public_world_readable_precedence():
    """ Test that call signature arguments applied through _plot_option_logic
    overwrite options supplied through py.sign_in which overwrite options
    set through tls.set_config
    """
    plot_option_sets = (
        {
            'parent': {'world_readable': True, 'auto_open': False},
            'child': {'sharing': 'secret', 'auto_open': True},
            'expected_output': {'world_readable': False,
                                'sharing': 'secret',
                                'auto_open': True}
        },
        {
            'parent': {'world_readable': True, 'auto_open': True},
            'child': {'sharing': 'private', 'auto_open': False},
            'expected_output': {'world_readable': False,
                                'sharing': 'private',
                                'auto_open': False}
        },
        {
            'parent': {'world_readable': False, 'auto_open': False},
            'child': {'sharing': 'public', 'auto_open': True},
            'expected_output': {'world_readable': True,
                                'sharing': 'public',
                                'auto_open': True}
        }
    )

    def gen_test_signin(plot_options):
        def test(self):
            py.sign_in('username', 'key', **plot_options['parent'])
            options = py._plot_option_logic(plot_options['child'])
            for option, value in plot_options['expected_output'].items():
                self.assertEqual(options[option], value)
        return test

    def gen_test_config(plot_options):
        def test(self):
            tls.set_config(**plot_options['parent'])
            options = py._plot_option_logic(plot_options['child'])
            for option, value in plot_options['expected_output'].items():
                self.assertEqual(options[option], value)

    for i, plot_options in enumerate(plot_option_sets):
        setattr(TestPlotOptionLogic,
                'test_private_sharing_and_public_'
                'world_readable_precedence_signin{}'.format(i),
                gen_test_signin(plot_options))

        setattr(TestPlotOptionLogic,
                'test_private_sharing_and_public_'
                'world_readable_precedence_config{}'.format(i),
                gen_test_config(plot_options))

generate_private_sharing_and_public_world_readable_precedence()
