"""
This module handles accessing, storing, and managing the graph reference.

"""
from __future__ import absolute_import

import json
import re
import requests

from plotly import exceptions, files, utils

GRAPH_REFERENCE_PATH = '/plot-schema.json'
META_KEYS = ['_isLinkedToArray', 'description', 'role']

# for backwards compat, we need to add a few class names
_BACKWARDS_COMPAT_CLASS_NAME_TO_OBJECT_NAME = {
    'AngularAxis': 'angularaxis',
    'ColorBar': 'colorbar',
    'Area': 'scatter',
    'Font': 'textfont',
    'Histogram2dContour': 'histogram2dcontour',
    'RadialAxis': 'radialaxis',
    'XAxis': 'xaxis',
    'XBins': 'xbins',
    'YAxis': 'yaxis',
    'YBins': 'ybins',
    'ZAxis': 'zaxis'
}


def get_graph_reference():
    """
    Attempts to load local copy of graph reference or makes GET request if DNE.

    :return: (dict) The graph reference.
    :raises: (PlotlyError) When graph reference DNE and GET request fails.

    """
    if files.check_file_permissions():
        graph_reference = utils.load_json_dict(files.GRAPH_REFERENCE_FILE)
        config = utils.load_json_dict(files.CONFIG_FILE)
        plotly_domain = config['plotly_domain']
    else:
        graph_reference = {}
        plotly_domain = files.FILE_CONTENT[files.CONFIG_FILE]['plotly_domain']

    if not graph_reference:

        graph_reference_url = plotly_domain + GRAPH_REFERENCE_PATH

        try:
            response = requests.get(graph_reference_url)
            response.raise_for_status()
        except requests.exceptions.RequestException:
            raise exceptions.PlotlyError(
                "The schema used to validate Plotly figures has never been "
                "downloaded to your computer. You'll need to connect to a "
                "Plotly server at least once to do this.\n"
                "You're seeing this error because the attempt to download "
                "the schema from '{}' failed.".format(graph_reference_url)
            )

        # TODO: Hash this so we don't have to load it every time. The server
        #       will need to accept a hash query param as well.
        graph_reference = json.loads(response.content)

    return utils.decode_unicode(graph_reference)


def get_object_info(path=None, object_name=None):
    """
    Can be used outside this module to get meta info about a graph object.

    :param (tuple) path: A path inside GRAPH_REFERENCE to an object.
    :param (str|unicode) object_name: The name of an object in GRAPH_REFERENCE.
    :return: (dict)

    """
    if path:
        return _get_object_info_from_path(path)
    else:
        return _get_object_info_from_name(object_name)


def string_to_class_name(string):
    """
    Single function to handle turning object names into class names.

    GRAPH_REFERENCE has names like `error_y`, which we'll turn into `ErrorY`.

    :param (str) string: Presumably an object_name from GRAPH_REFERENCE.
    :return: (str)

    """

    # capitalize first letter
    string = re.sub(r'[A-Za-z]', lambda m: m.group().title(), string, count=1)

    # replace `*_<c>` with `*<C>` E.g., `Error_x` --> `ErrorX`
    string = re.sub(r'_[A-Za-z]+', lambda m: m.group()[1:].title(), string)

    return string


def attribute_is_array(attribute, parent_name):
    """
    Returns True if attribute should be an special *array* object.

    :param (str) attribute: Possibly the name of an object.
    :param (str) parent_name: We need the parent object name as context.
    :return: (bool)

    """
    if attribute not in OBJECTS:
        return False

    if OBJECTS[attribute]:
        object_infos = [get_object_info(path=path)
                        for path in OBJECTS[attribute]]
    else:
        object_info = get_object_info(object_name=attribute)
        object_infos = [object_info]

    for object_info in object_infos:

        if object_info['parent'] == parent_name and object_info['is_array']:
            return True

    return False


def _get_objects():
    """
    Return the main dict that we'll work with for graph objects.

    This maps object names to paths inside GRAPH_REFERENCE. If the object
    doesn't have a path, no path is associated and methods are provided to look
    the object up *by name*.

    :return: (dict)

    """
    objects = {}
    for object_path in OBJECT_PATHS:

        if object_path[-1] == '_isLinkedToArray':
            name = object_path[-2][:-1]
        else:
            name = object_path[-1]

        if name not in objects:
            objects[name] = []
        objects[name].append(object_path)

    objects.update({trace_name: [] for trace_name in TRACE_NAMES})
    objects.update(figure=[], data=[], layout=[])

    return objects


def _get_class_names_to_object_names():
    """
    We eventually make classes out of the objects in GRAPH_REFERENCE.

    :return: (dict) A mapping of class names to object names.

    """
    class_names_to_object_names = {}
    for object_name in OBJECTS:
        class_name = string_to_class_name(object_name)
        class_names_to_object_names[class_name] = object_name

    for class_name in _BACKWARDS_COMPAT_CLASS_NAME_TO_OBJECT_NAME:
        object_name = _BACKWARDS_COMPAT_CLASS_NAME_TO_OBJECT_NAME[class_name]
        class_names_to_object_names[class_name] = object_name

    return class_names_to_object_names


def _get_object_info_from_path(path):
    """
    Get object info given a path in GRAPH_REFERENCE.

    :param (tuple) path: A valid path in GRAPH_REFERENCE.

    :return: (dict)

    """
    if path[-1] == '_isLinkedToArray':

        attribute_container = utils.get_by_path(GRAPH_REFERENCE, path[:-1])

        is_array = False
        parent = path[-2]
        name = parent[:-1]
        description = attribute_container.get('description', '')
        attributes = {k: v for k, v in attribute_container.items()
                      if k not in META_KEYS}
        items = None

    else:

        name = path[-1]

        if path[-2] == 'attributes':
            parent = path[-3]  # a trace
        elif path[-2] == 'layoutAttributes':
            parent = 'layout'
        else:
            parent = path[-2]

        path_value = utils.get_by_path(GRAPH_REFERENCE, path)

        if '_isLinkedToArray' in path_value:

            is_array = True
            description = ''
            attributes = None
            items = [name[:-1]]

        else:

            is_array = False
            description = path_value.get('description', '')
            attributes = {k: v for k, v in path_value.items()
                          if k not in META_KEYS}
            items = None

    return {
        'role': 'object',
        'is_array': is_array,
        'parent': parent,
        'name': name,
        'description': description,
        'attributes': attributes,
        'items': items
    }


def _get_object_info_from_name(object_name):
    """
    Get object info given an object name in OBJECTS.

    If a valid path *could* have been used, this will fail. This is meant to be
    a last resort to get the object info dict.

    :param (str) object_name: The name of an object in OBJECTS.

    :return: (dict)

    """
    if object_name not in ['figure', 'data', 'layout'] + TRACE_NAMES:
        raise Exception('TBD')

    if object_name in TRACE_NAMES:

        trace = utils.get_by_path(GRAPH_REFERENCE, ('traces', object_name))
        description = 'A {} trace'.format(object_name)
        attributes = {k: v for k, v in trace['attributes'].items()}
        attributes['type'] = {'role': 'info'}

        return {'role': 'object', 'name': object_name, 'is_array': False,
                'parent': 'data', 'description': description,
                'attributes': attributes, 'items': None}

    elif object_name == 'data':

        return {'role': 'object', 'name': 'data', 'is_array': True,
                'parent': 'figure', 'attributes': None, 'items': TRACE_NAMES,
                'description': 'Array container for trace objects.'}

    elif object_name == 'layout':

        # find and add layout keys from traces
        attributes = {}
        for trace_name in TRACE_NAMES:
            try:
                path = ('traces', trace_name, 'layoutAttributes')
                layout_attributes = utils.get_by_path(GRAPH_REFERENCE, path)
            except KeyError:
                pass
            else:
                for key, val in layout_attributes.items():
                    if key not in META_KEYS:
                        attributes[key] = val

        # find and add layout keys from layout
        layout_attributes = GRAPH_REFERENCE['layout']['layoutAttributes']
        for key, val in layout_attributes.items():
            if key not in META_KEYS:
                attributes[key] = val

        return {'role': 'object', 'name': 'layout', 'is_array': False,
                'parent': 'figure', 'attributes': attributes, 'items': None,
                'description': 'Plot layout object container.'}

    else:  # assume it's 'figure'

        attributes = {'data': _get_object_info_from_name('data'),
                      'layout': _get_object_info_from_name('layout')}

        return {'role': 'object', 'name': 'figure', 'is_array': False,
                'parent': '', 'description': 'Top level of figure object.',
                'attributes': attributes, 'items': None}


# The ordering here is important.
GRAPH_REFERENCE = get_graph_reference()
TRACE_NAMES = GRAPH_REFERENCE['traces'].keys()
OBJECT_PATHS = [path for node, path in utils.node_generator(GRAPH_REFERENCE)
                if node.get('role') == 'object']
OBJECTS = _get_objects()
CLASS_NAMES_TO_OBJECT_NAMES = _get_class_names_to_object_names()
