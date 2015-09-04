"""
graph_objs
==========

A module that understands plotly language and can manage the json
structures. This module defines two base classes: PlotlyList and PlotlyDict.
The former inherits from `list` and the latter inherits from `dict`. and is
A third structure, PlotlyTrace, is also considered a base class for all
subclassing 'trace' objects like Scatter, Box, Bar, etc. It is also not meant
to instantiated by users.

Goals of this module:
---------------------

* A dict/list with the same entries as a PlotlyDict/PlotlyList should look
exactly the same once a call is made to plot.

* Only mutate object structure when users ASK for it. (some magic now...)

* It should always be possible to get a dict/list JSON representation from a
graph_objs object and it should always be possible to make a graph_objs object
from a dict/list JSON representation.

"""
from __future__ import absolute_import

import copy

import re
import six

from plotly import exceptions, graph_reference
from plotly.graph_objs import graph_objs_tools


class PlotlyBase(object):

    def to_graph_objs(self, **kwargs):
        # everything is cast into graph_objs now. keep for backwards compat.
        pass

    def validate(self):
        # everything is *always* validated now. keep for backwards compat.
        pass

    def get_ordered(self, **kwargs):
        # we have no way to order things anymore. keep for backwards compat.
        return self


class PlotlyList(list, PlotlyBase):

    _name = None
    _items = set()
    _parent = None

    def __init__(self, *args, **kwargs):
        if self._name is None:
            raise exceptions.PlotlyError(
                "PlotlyList is a base class. It's shouldn't be instantiated."
            )

        _raise = kwargs.get('_raise', True)

        if args and isinstance(args[0], dict):
            raise exceptions.PlotlyListEntryError(
                obj=self,
                index=0,
                notes="Just like a `list`, `{name}` must be instantiated with "
                      "a *single* collection.\n"
                      "In other words these are OK:\n"
                      ">>> {name}()\n"
                      ">>> {name}([])\n"
                      ">>> {name}([dict()])\n"
                      ">>> {name}([dict(), dict()])\n"
                      "However, these don't make sense:\n"
                      ">>> {name}(dict())\n"
                      ">>> {name}(dict(), dict())"
                      "".format(name=self.__class__.__name__)
            )

        super(PlotlyList, self).__init__()

        for index, value in enumerate(list(*args)):
            try:
                value = self.value_to_graph_object(index, value, _raise=_raise)
            except exceptions.PlotlyGraphObjectError as err:
                err.prepare()
                raise

            if isinstance(value, PlotlyBase):
                self.append(value)

    def value_to_graph_object(self, index, value, _raise=True):
        """
        Attempt to change the given value into a graph object.

        If _raise is False, this won't raise. If the entry can't be converted,
        `None` is returned, meaning the caller should ignore the value or
        discard it as a failed conversion.

        :param (dict) value: A dict to be converted into a graph object.
        :param (bool) _raise: If False, ignore bad values instead of raising.
        :return: (PlotlyBase|None) The graph object or possibly `None`.

        """
        if not isinstance(value, dict):
            if _raise:
                raise exceptions.PlotlyListEntryError(self, index, value)
            else:
                return

        for i, item in enumerate(self._items, 1):
            try:
                return GraphObjectFactory.create(item, _raise=_raise, **value)
            except exceptions.PlotlyGraphObjectError as e:
                if i == len(self._items) and _raise:
                    e.add_to_error_path(index)
                    e.prepare()
                    raise

    def __setitem__(self, index, value, _raise=True):
        """Override to enforce validation."""
        if not isinstance(index, int):
            if _raise:
                index_type = type(index)
                raise TypeError('Index must be int, not {}'.format(index_type))
            return

        if index >= len(self):
            raise IndexError(index)

        value = self.value_to_graph_object(index, value, _raise=_raise)
        if isinstance(value, (PlotlyDict, PlotlyList)):
            value.__dict__['_parent'] = self
            super(PlotlyList, self).__setitem__(index, value)

    def __setattr__(self, key, value):
        raise exceptions.PlotlyError('Setting attributes on a PlotlyList is '
                                     'not allowed')

    def __copy__(self):
        return GraphObjectFactory.create(self._name, *self)

    def __deepcopy__(self, memodict={}):
        # TODO: this is *wrong*, deepcopy takes a bit more work!
        return self.__copy__()

    def append(self, value):
        """Override to enforce validation."""
        index = len(self)  # used for error messages
        value = self.value_to_graph_object(index, value)
        value.__dict__['_parent'] = self
        super(PlotlyList, self).append(value)

    def extend(self, iterable):
        """Override to enforce validation."""
        for value in iterable:
            index = len(self)
            value = self.value_to_graph_object(index, value)
            super(PlotlyList, self).append(value)

    def insert(self, index, value):
        """Override to enforce validation."""
        value = self.value_to_graph_object(index, value)
        value.__dict__['_parent'] = self
        super(PlotlyList, self).insert(index, value)

    def update(self, changes, make_copies=False):
        """Update current list with changed_list, which must be iterable.
        The 'changes' should be a list of dictionaries, however,
        it is permitted to be a single dict object.

        Because mutable objects contain references to their values, updating
        multiple items in a list will cause the items to all reference the same
        original set of objects. To change this behavior add
        `make_copies=True` which makes deep copies of the update items and
        therefore break references.

        """
        if isinstance(changes, dict):
            changes = [changes]
        for index in range(len(self)):
            try:
                update = changes[index % len(changes)]
            except ZeroDivisionError:
                pass
            else:
                if make_copies:
                    self[index].update(copy.deepcopy(update))
                else:
                    self[index].update(update)

    def strip_style(self):
        """Strip style from the current representation.

        All PlotlyDicts and PlotlyLists are guaranteed to survive the
        stripping process, though they made be left empty. This is allowable.

        Keys that will be stripped in this process are tagged with
        `'type': 'style'` in graph_objs_meta.json.

        This process first attempts to convert nested collections from dicts
        or lists to subclasses of PlotlyList/PlotlyDict. This process forces
        a validation, which may throw exceptions.

        Then, each of these objects call `strip_style` on themselves and so
        on, recursively until the entire structure has been validated and
        stripped.

        """
        for plotly_dict in self:
            plotly_dict.strip_style()

    def get_data(self, flatten=False):
        """
        Returns the JSON for the plot with non-data elements stripped.

        Flattening may increase the utility of the result.

        :param (bool) flatten: {'a': {'b': ''}} --> {'a.b': ''}
        :returns: (dict|list) Depending on (flat|unflat)

        """
        l = list()
        for plotly_dict in self:
            l += [plotly_dict.get_data(flatten=flatten)]
        del_indicies = [index for index, item in enumerate(self)
                        if len(item) == 0]
        del_ct = 0
        for index in del_indicies:
            del self[index - del_ct]
            del_ct += 1

        if flatten:
            d = {}
            for i, e in enumerate(l):
                for k, v in e.items():
                    key = "{0}.{1}".format(i, k)
                    d[key] = v
            return d
        else:
            return l

    def to_string(self, level=0, indent=4, eol='\n',
                  pretty=True, max_chars=80):
        """Returns a formatted string showing graph_obj constructors.

        Example:

            print(obj.to_string())

        Keyword arguments:
        level (default = 0) -- set number of indentations to start with
        indent (default = 4) -- set indentation amount
        eol (default = '\\n') -- set end of line character(s)
        pretty (default = True) -- curtail long list output with a '...'
        max_chars (default = 80) -- set max characters per line

        """
        if not len(self):
            return "{name}()".format(name=self.__class__.__name__)
        string = "{name}([{eol}{indent}".format(
            name=self.__class__.__name__,
            eol=eol,
            indent=' ' * indent * (level + 1))
        for index, entry in enumerate(self):
            string += entry.to_string(level=level+1,
                                      indent=indent,
                                      eol=eol,
                                      pretty=pretty,
                                      max_chars=max_chars)
            if index < len(self) - 1:
                string += ",{eol}{indent}".format(
                    eol=eol,
                    indent=' ' * indent * (level + 1))
        string += (
            "{eol}{indent}])").format(eol=eol, indent=' ' * indent * level)
        return string

    def force_clean(self, **kwargs):
        """Attempts to convert to graph_objs and calls force_clean() on entries.
        Calling force_clean() on a PlotlyList will ensure that the object is
        valid and may be sent to plotly. This process will remove any entries
        that end up with a length == 0. It will also remove itself from
        enclosing trivial structures if it is enclosed by a collection with
        length 1, meaning the data is the ONLY object in the collection.
        Careful! This will delete any invalid entries *silently*.
        """
        for entry in self:
            entry.force_clean()
        del_indicies = [index for index, item in enumerate(self)
                        if len(item) == 0]
        del_ct = 0
        for index in del_indicies:
            del self[index - del_ct]
            del_ct += 1


class PlotlyDict(dict, PlotlyBase):

    _name = None
    _attributes = set()
    _parent = None
    _parent_key = None

    def __init__(self, *args, **kwargs):
        if self._name is None:
            raise exceptions.PlotlyError(
                "PlotlyDict is a base class. It's shouldn't be instantiated."
            )

        _raise = kwargs.pop('_raise', True)

        super(PlotlyDict, self).__init__()

        if self._name in graph_reference.TRACE_NAMES:
            self['type'] = self._name

        # force key-value pairs to go through validation
        d = {key: val for key, val in dict(*args, **kwargs).items()}
        for key, val in d.items():
            try:
                self.__setitem__(key, val, _raise=_raise)
            except exceptions.PlotlyGraphObjectError as err:
                err.prepare()
                raise

    def __dir__(self):
        attrs = self.__dict__.keys()
        attrs += [attr for attr in dir(dict()) if attr not in attrs]
        return sorted(self._attributes) + attrs

    def __getitem__(self, key):
        if key not in self:
            self.__missing__(key)
        return super(PlotlyDict, self).__getitem__(key)

    def __setattr__(self, key, value):
        self.__setitem__(key, value)

    def __setitem__(self, key, value, _raise=True):

        if not isinstance(key, six.string_types):
            if _raise:
                raise TypeError('Key must be string, not {}'.format(type(key)))
            return

        if self.is_src_key(key):
            value = graph_objs_tools.assign_id_to_src(key, value)
            return super(PlotlyDict, self).__setitem__(key, value)

        if key not in self._attributes:
            if _raise:
                raise exceptions.PlotlyDictKeyError(self, key)
            return

        if graph_objs_tools.get_role(self, key) == 'object':
            value = self.value_to_graph_object(key, value, _raise=_raise)
            if isinstance(value, (PlotlyDict, PlotlyList)):
                value.__dict__['_parent'] = self
                value.__dict__['_parent_key'] = key
            else:
                return

        super(PlotlyDict, self).__setitem__(key, value)

    def __getattr__(self, key):
        """Python only calls this when key is missing!"""
        try:
            return self.__getitem__(key)
        except KeyError:
            raise AttributeError(key)

    def __copy__(self):
        return GraphObjectFactory.create(self._name, **self)

    def __deepcopy__(self, memodict={}):
        # TODO: this is *wrong*, deepcopy takes a bit more work!
        return self.__copy__()

    def __missing__(self, key):
        if key in self._attributes:
            if graph_objs_tools.get_role(self, key) == 'object':
                value = GraphObjectFactory.create(key)
                value.__dict__['_parent'] = self
                value.__dict__['_parent_key'] = key
                super(PlotlyDict, self).__setitem__(key, value)

    def is_src_key(self, key):

        if not key.endswith('src'):
            return False

        root_key, _ = key.rsplit('src', 1)

        if root_key not in self._attributes:
            return False

        return True

    def get_path(self):
        path = []
        parents = self.get_parents()
        parents.reverse()
        children = [self] + parents[:-1]
        for parent, child in zip(parents, children):
            if isinstance(parent, PlotlyDict):
                path.append(child._parent_key)
            else:
                path.append(parent.index(child))
        path.reverse()
        return tuple(path)

    def get_parents(self):
        parents = []
        parent = self._parent
        while parent is not None:
            parents.append(parent)
            parent = parent._parent
        parents.reverse()
        return parents

    def value_to_graph_object(self, key, value, _raise=True):

        if graph_reference.attribute_is_array(key, self._name):
            val_types = (list, )
            if not isinstance(value, val_types):
                if _raise:
                    e = exceptions.PlotlyDictValueError(self, key, value,
                                                        val_types)
                    e.add_to_error_path(key)
                    e.prepare()
                    raise e
                else:
                    return
            try:
                graph_object = GraphObjectFactory.create(key, value,
                                                         _raise=_raise)
            except exceptions.PlotlyGraphObjectError as e:
                e.add_to_error_path(key)
                e.prepare()
                raise e
        else:
            val_types = (dict, )
            if not isinstance(value, val_types):
                if _raise:
                    e = exceptions.PlotlyDictValueError(self, key, value,
                                                        val_types)
                    e.add_to_error_path(key)
                    e.prepare()
                    raise e
                else:
                    return
            try:
                graph_object = GraphObjectFactory.create(key, value,
                                                         _raise=_raise)
            except exceptions.PlotlyGraphObjectError as e:
                e.add_to_error_path(key)
                e.prepare()
                raise e

        return graph_object  # this can be `None` when `_raise == False`

    def update(self, dict1=None, **dict2):
        """Update current dict with dict1 and then dict2.

        This recursively updates the structure of the original dictionary-like
        object with the new entries in the second and third objects. This
        allows users to update with large, nested structures.

        Note, because the dict2 packs up all the keyword arguments, you can
        specify the changes as a list of keyword agruments.

        Examples:
        # update with dict
        obj = Layout(title='my title', xaxis=XAxis(range=[0,1], domain=[0,1]))
        update_dict = dict(title='new title', xaxis=dict(domain=[0,.8]))
        obj.update(update_dict)
        obj
        {'title': 'new title', 'xaxis': {'range': [0,1], 'domain': [0,.8]}}

        # update with list of keyword arguments
        obj = Layout(title='my title', xaxis=XAxis(range=[0,1], domain=[0,1]))
        obj.update(title='new title', xaxis=dict(domain=[0,.8]))
        obj
        {'title': 'new title', 'xaxis': {'range': [0,1], 'domain': [0,.8]}}

        This 'fully' supports duck-typing in that the call signature is
        identical, however this differs slightly from the normal update
        method provided by Python's dictionaries.

        """
        if dict1 is not None:
            for key, val in list(dict1.items()):
                if key in self:
                    if isinstance(self[key], (PlotlyDict, PlotlyList)):
                        self[key].update(val)
                    else:
                        self[key] = val
                else:
                    self[key] = val

        if len(dict2):
            for key, val in list(dict2.items()):
                if key in self:
                    if isinstance(self[key], (PlotlyDict, PlotlyList)):
                        self[key].update(val)
                    else:
                        self[key] = val
                else:
                    self[key] = val

    def strip_style(self):
        """Strip style from the current representation.

        All PlotlyDicts and PlotlyLists are guaranteed to survive the
        stripping process, though they made be left empty. This is allowable.

        Keys that will be stripped in this process are tagged with
        `'type': 'style'` in graph_objs_meta.json.

        This process first attempts to convert nested collections from dicts
        or lists to subclasses of PlotlyList/PlotlyDict. This process forces
        a validation, which may throw exceptions.

        Then, each of these objects call `strip_style` on themselves and so
        on, recursively until the entire structure has been validated and
        stripped.

        """
        keys = list(self.keys())
        for key in keys:
            if isinstance(self[key], (PlotlyDict, PlotlyList)):
                self[key].strip_style()
            else:
                role = graph_objs_tools.get_role(self, key, self[key])
                if role == 'style':
                    del self[key]

                # this is for backwards compat when we updated graph reference.
                if self._name == 'layout' and key == 'autosize':
                    del self[key]

    def get_data(self, flatten=False):
        """Returns the JSON for the plot with non-data elements stripped."""
        d = dict()
        for key, val in list(self.items()):
            if isinstance(val, (PlotlyDict, PlotlyList)):
                sub_data = val.get_data(flatten=flatten)
                if flatten:
                    for sub_key, sub_val in sub_data.items():
                        key_string = "{0}.{1}".format(key, sub_key)
                        d[key_string] = sub_val
                else:
                    d[key] = sub_data
            else:
                role = graph_objs_tools.get_role(self, key, val)
                if role == 'data':
                    d[key] = val

                # we use the name to help make data frames
                if self._name in graph_reference.TRACE_NAMES and key == 'name':
                    d[key] = val
        keys = list(d.keys())
        for key in keys:
            if isinstance(d[key], (dict, list)):
                if len(d[key]) == 0:
                    del d[key]
        return d

    def to_string(self, level=0, indent=4, eol='\n',
                  pretty=True, max_chars=80):
        """Returns a formatted string showing graph_obj constructors.

        Example:

            print(obj.to_string())

        Keyword arguments:
        level (default = 0) -- set number of indentations to start with
        indent (default = 4) -- set indentation amount
        eol (default = '\\n') -- set end of line character(s)
        pretty (default = True) -- curtail long list output with a '...'
        max_chars (default = 80) -- set max characters per line

        """
        if not len(self):
            return "{name}()".format(name=self.__class__.__name__)
        string = "{name}(".format(name=self.__class__.__name__)
        if self._name in graph_reference.TRACE_NAMES:
            keys = [key for key in self.keys() if key != 'type']
        else:
            keys = self.keys()

        keys = sorted(keys, key=graph_objs_tools.sort_keys)
        num_keys = len(keys)

        for index, key in enumerate(keys, 1):
            string += "{eol}{indent}{key}=".format(
                eol=eol,
                indent=' ' * indent * (level+1),
                key=key)
            try:
                string += self[key].to_string(level=level+1,
                                              indent=indent,
                                              eol=eol,
                                              pretty=pretty,
                                              max_chars=max_chars)
            except AttributeError:
                if pretty:  # curtail representation if too many chars
                    max_len = (max_chars -
                               indent*(level + 1) -
                               len(key + "=") -
                               len(eol))
                    if index < num_keys:
                        max_len -= len(',')  # remember the comma!
                    if isinstance(self[key], list):
                        s = "[]"
                        for iii, entry in enumerate(self[key], 1):
                            if iii < len(self[key]):
                                s_sub = graph_objs_tools.curtail_val_repr(
                                    entry,
                                    max_chars=max_len - len(s),
                                    add_delim=True
                                )
                            else:
                                s_sub = graph_objs_tools.curtail_val_repr(
                                    entry,
                                    max_chars=max_len - len(s),
                                    add_delim=False
                                )
                            s = s[:-1] + s_sub + s[-1]
                            if len(s) == max_len:
                                break
                        string += s
                    else:
                        string += graph_objs_tools.curtail_val_repr(
                            self[key], max_len)
                else:  # they want it all!
                    string += repr(self[key])
            if index < num_keys:
                string += ","
        string += "{eol}{indent})".format(eol=eol, indent=' ' * indent * level)
        return string

    def force_clean(self, caller=True):
        """Attempts to convert to graph_objs and call force_clean() on values.
        Calling force_clean() on a PlotlyDict will ensure that the object is
        valid and may be sent to plotly. This process will also remove any
        entries that end up with a length == 0.
        Careful! This will delete any invalid entries *silently*.
        """
        keys = list(self.keys())
        for key in keys:
            try:
                self[key].force_clean(caller=False)  # TODO: add error handling
            except AttributeError:
                pass
            if isinstance(self[key], (dict, list)):
                if len(self[key]) == 0:
                    del self[key]  # clears empty collections!
            elif self[key] is None:
                del self[key]


class Figure(PlotlyDict):

    _name = 'figure'
    _attributes = set(graph_reference.get_object_info(
        object_name='figure'
    )['attributes'])

    def __init__(self, *args, **kwargs):
        super(Figure, self).__init__(*args, **kwargs)
        if 'data' not in self:
            self.data = []

    def get_data(self, flatten=False):
        """
        Returns the JSON for the plot with non-data elements stripped.

        Flattening may increase the utility of the result.

        :param (bool) flatten: {'a': {'b': ''}} --> {'a.b': ''}
        :returns: (dict|list) Depending on (flat|unflat)

        """
        return self.data.get_data(flatten=flatten)

    def to_dataframe(self):
        data = self.get_data(flatten=True)
        from pandas import DataFrame, Series
        return DataFrame(dict([(k, Series(v)) for k, v in data.items()]))

    def print_grid(self):
        """Print a visual layout of the figure's axes arrangement.

        This is only valid for figures that are created
        with plotly.tools.make_subplots.
        """
        try:
            grid_str = self.__dict__['_grid_str']
        except AttributeError:
            raise Exception("Use plotly.tools.make_subplots "
                            "to create a subplot grid.")
        print(grid_str)

    def append_trace(self, trace, row, col):
        """ Helper function to add a data traces to your figure
        that is bound to axes at the row, col index.

        The row, col index is generated from figures created with
        plotly.tools.make_subplots and can be viewed with Figure.print_grid.

        Example:
        # stack two subplots vertically
        fig = tools.make_subplots(rows=2)

        This is the format of your plot grid:
        [ (1,1) x1,y1 ]
        [ (2,1) x2,y2 ]

        fig.append_trace(Scatter(x=[1,2,3], y=[2,1,2]), 1, 1)
        fig.append_trace(Scatter(x=[1,2,3], y=[2,1,2]), 2, 1)

        Arguments:

        trace (plotly trace object):
            The data trace to be bound.

        row (int):
            Subplot row index on the subplot grid (see Figure.print_grid)

        col (int):
            Subplot column index on the subplot grid (see Figure.print_grid)

        """
        try:
            grid_ref = self._grid_ref
        except AttributeError:
            raise Exception("In order to use Figure.append_trace, "
                            "you must first use plotly.tools.make_subplots "
                            "to create a subplot grid.")
        if row <= 0:
            raise Exception("Row value is out of range. "
                            "Note: the starting cell is (1, 1)")
        if col <= 0:
            raise Exception("Col value is out of range. "
                            "Note: the starting cell is (1, 1)")
        try:
            ref = grid_ref[row-1][col-1]
        except IndexError:
            raise Exception("The (row, col) pair sent is out of range. "
                            "Use Figure.print_grid to view the subplot grid. ")
        if 'scene' in ref[0]:
            trace['scene'] = ref[0]
            if ref[0] not in self['layout']:
                raise Exception("Something went wrong. "
                                "The scene object for ({r},{c}) subplot cell "
                                "got deleted.".format(r=row, c=col))
        else:
            xaxis_key = "xaxis{ref}".format(ref=ref[0][1:])
            yaxis_key = "yaxis{ref}".format(ref=ref[1][1:])
            if (xaxis_key not in self['layout']
                    or yaxis_key not in self['layout']):
                raise Exception("Something went wrong. "
                                "An axis object for ({r},{c}) subplot cell "
                                "got deleted.".format(r=row, c=col))
            trace['xaxis'] = ref[0]
            trace['yaxis'] = ref[1]
        self['data'] += [trace]


class Data(PlotlyList):

    _name = 'data'
    _items = set(graph_reference.TRACE_NAMES)

    def value_to_graph_object(self, index, value, _raise=True):

        if not isinstance(value, dict):
            if _raise:
                e = exceptions.PlotlyListEntryError(self, index, value)
                e.add_note('Entry should subclass dict.')
                raise e
            else:
                return

        item = value.get('type', 'scatter')
        if item not in self._items:
            if _raise:
                err = exceptions.PlotlyListEntryError(self, index, value)
                err.add_note("Entry does not have a valid 'type' key")
                err.add_to_error_path(index)
                raise err

        try:
            return GraphObjectFactory.create(item, _raise=_raise, **value)
        except exceptions.PlotlyGraphObjectError as e:
            e.add_to_error_path(index)
            raise

    def get_data(self, flatten=False):
        """
        :param flatten:
        :return:
        """
        if flatten:
            data = [v.get_data(flatten=flatten) for v in self]
            d = {}
            taken_names = []
            for i, trace in enumerate(data):

                # we want to give the traces helpful names
                # however, we need to be sure they're unique too...
                trace_name = trace.pop('name', 'trace_{0}'.format(i))
                if trace_name in taken_names:
                    j = 1
                    new_trace_name = "{0}_{1}".format(trace_name, j)
                    while new_trace_name in taken_names:
                        new_trace_name = "{0}_{1}".format(trace_name, j)
                        j += 1
                    trace_name = new_trace_name
                taken_names.append(trace_name)

                # finish up the dot-concatenation
                for k, v in trace.items():
                    key = "{0}.{1}".format(trace_name, k)
                    d[key] = v
            return d
        else:
            return super(Data, self).get_data(flatten=flatten)

class Layout(PlotlyDict):

    _name = 'layout'
    _attributes = set(graph_reference.get_object_info(
        object_name='layout'
    )['attributes'])

    def _get_subplot_key(self, key):

        # TODO: this can use _isSubplotObj instead and won't require subclass!
        subplot_key_strings = ('xaxis', 'yaxis', 'zaxis', 'lataxis', 'lonaxis',
                               'radialaxis', 'angularaxis', 'geo', 'scene')
        match = re.search(r'(?P<digits>\d+$)', key)
        if match:
            root_key = key[:match.start()]
            digits = match.group('digits')

            if root_key in self._attributes:
                role = graph_objs_tools.get_role(self, root_key)
                if (role == 'object' and not digits.startswith('0')
                        and root_key in subplot_key_strings):
                    return root_key

    def __missing__(self, key):

        if not isinstance(key, six.string_types):
            raise TypeError('Key must be string, not {}'.format(type(key)))

        subplot_key = self._get_subplot_key(key)
        if subplot_key is None:
            return super(Layout, self).__missing__(key)

        value = GraphObjectFactory.create(subplot_key)
        value.__dict__['_parent'] = self
        value.__dict__['_parent_key'] = key
        super(PlotlyDict, self).__setitem__(key, value)

    def __setitem__(self, key, value, _raise=True):

        if not isinstance(key, six.string_types):
            if _raise:
                raise TypeError('Key must be string, not {}'.format(type(key)))
            return

        subplot_key = self._get_subplot_key(key)
        if subplot_key is None:
            return super(Layout, self).__setitem__(key, value, _raise=_raise)

        value = self.value_to_graph_object(subplot_key, value,  _raise=_raise)
        if isinstance(value, (PlotlyDict, PlotlyList)):
            value.__dict__['_parent'] = self
            value.__dict__['_parent_key'] = key
            return super(PlotlyDict, self).__setitem__(key, value)


Font = Trace = dict  # for backwards compat.


class GraphObjectFactory(object):
    """GraphObject creation in this module should run through this factory."""

    @staticmethod
    def create(object_name, *args, **kwargs):
        """
        Create a graph object from the OBJECTS dict by name, args, and kwargs.

        :param (str) object_name: A valid object name from OBJECTS.
        :param args: Arguments to pass to class constructor.
        :param kwargs: Keyword arguments to pass to class constructor.

        :return: (PlotlyList|PlotlyDict) The instantiated graph object.

        """
        if object_name not in graph_reference.OBJECTS:
            raise Exception('tbd')  # TODO
        class_name = graph_reference.string_to_class_name(object_name)
        graph_object_class = globals()[class_name]

        return graph_object_class(*args, **kwargs)


def _add_classes_to_globals(globals):
    """
    Create and add all the Graph Objects to this module for export.

    :param (dict) globals: The globals() dict from this module.

    """
    for object_name in graph_reference.OBJECTS:

        if object_name in ['figure', 'data', 'layout']:
            continue  # we manually define these

        class_name, class_bases, class_dict = \
            graph_objs_tools.get_class_create_args(object_name,
                                                   list_class=PlotlyList,
                                                   dict_class=PlotlyDict)
        doc = graph_objs_tools.make_doc(object_name)
        class_dict.update(__doc__=doc, __name__=class_name)
        cls = type(class_name, class_bases, class_dict)

        globals[class_name] = cls

        for key, val in graph_reference.CLASS_NAMES_TO_OBJECT_NAMES.items():
            if val == object_name:
                class_dict.update(__name__=key)
                cls = type(key, class_bases, class_dict)
                globals[key] = cls

_add_classes_to_globals(globals())

# We don't want to expose this module to users, just the classes.
_globals_keys = globals().keys()  # TODO: all class names should work
__all__ = [k for k in graph_reference.CLASS_NAMES_TO_OBJECT_NAMES.keys()
           if k in _globals_keys]
