from __future__ import absolute_import

from plotly import exceptions, optional_imports
import plotly.graph_objects as go
import plotly.express as px

pd = optional_imports.get_module("pandas")
np = optional_imports.get_module("numpy")


CHART_TYPES = ['bar', 'box', 'violin']


def create_upset(data_frame, x=None, color=None, title=None, sort_by='Counts', asc=False, mode='Counts',
                 max_subsets=50, subset_bgcolor='#C9C9C9', subset_fgcolor='#000000', category_orders=None,
                 color_discrete_sequence=None, color_discrete_map=None, log_y=False, barmode='group', textangle=0):
    plot_obj = _Upset(**locals())
    upset_plot = plot_obj.make_upset_plot()
    return upset_plot, plot_obj


def _expand_subset_column(df):
    # TODO: Fill in this method for alternate data representation
    # TODO: Add input for subset_column
    pass


def _make_binary(t):
    """
    Converts tuple of 0,1s to binary number. Used in _transform_upset_data for sort order.
    """
    return sum([t[i] * 2**i for i in range(len(t))])


def _transform_upset_data(df):
    """
    Takes raw data of binary vectors for set inclusion and produces counts over each.
    """
    intersect_counts = pd.DataFrame({'Intersections': list(df.value_counts().to_dict().keys()),
                                     'Counts': list(df.value_counts().to_dict().values())})
    return intersect_counts


def _sort_intersect_counts(df, sort_by='Counts', asc=True):
    """
    Takes output from _transform_upset_data and sorts by method requested.
    """
    key = None if (sort_by == 'Counts') else lambda x: x.apply(lambda y: (sum(y), _make_binary(y)))
    df = df.sort_values(by=sort_by, key=key, ascending=asc)
    return df


class _Upset:
    """
    Represents builder object for UpSet plot. Refer to figure_factory.create_upset() for full docstring.
    """

    def __init__(self, data_frame, x=None, color=None, title=None, sort_by='Counts', asc=False, mode='Counts',
                 max_subsets=50, subset_bgcolor='#C9C9C9', subset_fgcolor='#000000', category_orders=None,
                 color_discrete_sequence=None, color_discrete_map=None, log_y=False, barmode='group', textangle=0):

        # Plot inputs and settings
        self.df = data_frame
        self.x = x
        self.color = color
        self.title = title
        self.sort_by = sort_by
        self.asc = asc
        self.mode = mode
        self.max_subsets = max_subsets,
        self.subset_bgcolor = subset_bgcolor
        self.subset_fgcolor = subset_fgcolor
        self.category_orders = category_orders
        self.color_discrete_sequence = color_discrete_sequence
        self.color_discrete_map = color_discrete_map
        self.log_y = log_y
        self.barmode = barmode
        self.textangle = textangle

        # TODO: Refactor code for "common plot args" that can be reused for eventual box/violin plots

        # Figure-building specific attributes
        self.fig = go.Figure()
        self.intersect_counts = pd.DataFrame()
        self.subset_col_names = [c for c in data_frame.columns if c != x and c != color]
        self.switchboard_heights = []

        # Validate inputs
        self.validate_upset_inputs()

        # DEBUG
        self.test = None

    def make_upset_plot(self):
        # Create intersect_counts df depending on if color provided
        color = self.color
        df = self.df
        if color is not None:
            # TODO: Consider refactor using groupby instead of looping over colors
            for c in df[color].unique():
                sub_df = df[df[color] == c].drop(columns=[color])
                if self.x is not None:
                    # TODO: Check counting code for clustering by x value for distribution plots
                    new_df = sub_df.groupby(self.x).apply(lambda x: _transform_upset_data(x.drop(columns=['self.x'])))
                    new_df = new_df.reset_index()[[self.x, 'Intersections', 'Counts']]
                else:
                    new_df = _transform_upset_data(sub_df)
                # Sort subgroup in requested order
                new_df = _sort_intersect_counts(new_df, sort_by=self.sort_by, asc=self.asc).reset_index(drop=True).reset_index()
                new_df[color] = c
                self.intersect_counts = pd.concat([self.intersect_counts, new_df])
            # TODO: Need to saturate each cluster with 0 value for subsets in one but not other...
        else:
            self.intersect_counts = _transform_upset_data(df)
            self.intersect_counts = _sort_intersect_counts(self.intersect_counts, sort_by=self.sort_by, asc=self.asc)
            self.intersect_counts = self.intersect_counts.reset_index(drop=True).reset_index()

        # Rescale for percents if requested
        mode = self.mode
        if mode == 'Percent':
            if color is not None:
                denom = self.intersect_counts.groupby(color).sum().reset_index()
                denom_dict = dict(zip(denom[color], denom['Counts']))
                self.intersect_counts['Counts'] = round(self.intersect_counts['Counts'] / self.intersect_counts[color].map(denom_dict), 2)
            else:
                self.intersect_counts['Counts'] = round(self.intersect_counts['Counts'] / self.intersect_counts['Counts'].sum(), 2)

        # Create 3 main components for figure
        self.make_primary_plot()
        self.make_switchboard()
        self.make_margin_plot()

        # Add title
        self.fig.update_layout(title=self.title, title_x=0.5)

        return self.fig

    def validate_upset_inputs(self):
        # Check sorting inputs are valid
        sort_by = self.sort_by
        try:
            assert (sort_by == 'Counts') or (sort_by == 'Intersections')
        except AssertionError:
            raise ValueError(f'Invalid input for "sort_by". Must be either "Counts" or "Intersections" but you provided {sort_by}')

        # Check mode is either Counts or Percent
        mode = self.mode
        try:
            assert (mode == 'Counts') or (mode == 'Percent')
        except AssertionError:
            raise ValueError(f'Invalid input for "mode". Must be either "Counts" or "Percent" but you provided {mode}')

    def make_primary_plot(self):
        bar_args = {
            'color': self.color,
            'category_orders': self.category_orders,
            'color_discrete_sequence': self.color_discrete_sequence,
            'color_discrete_map': self.color_discrete_map,
            'barmode': self.barmode,
            'log_y': self.log_y
        }

        # TODO: Override default hover info for something more useful
        self.fig = px.bar(self.intersect_counts, x='index', y='Counts', text='Counts', **bar_args)
        self.fig.update_traces(textposition='outside', cliponaxis=False, textangle=self.textangle)
        self.fig.update_layout(plot_bgcolor='#FFFFFF', xaxis_visible=False, xaxis_showticklabels=False,
                               yaxis_visible=False, yaxis_showticklabels=False)

    def make_switchboard(self):
        """
        Method to add subset points to input fig px.bar chart in the style of UpSet plot.
        Returns updated figure, and list of heights of dots for downstream convenience.
        """
        # Compute coordinates for bg subset scatter points
        d = len(self.subset_col_names)
        num_bars = len(self.fig.data[0]['x'])
        x_bg_scatter = np.repeat(self.fig.data[0]['x'], d)
        y_scatter_offset = 0.2  # Offsetting ensures bars will hover just above the subset scatterplot
        y_max = (1 + y_scatter_offset) * max([max(bar['y']) for bar in self.fig.data])
        self.switchboard_heights = [-y_max / d * i - y_scatter_offset * y_max for i in list(range(d))]
        y_bg_scatter = num_bars * self.switchboard_heights

        # Add bg subset scatter points to figure below bar chart
        self.fig.add_trace(go.Scatter(x=x_bg_scatter, y=y_bg_scatter, mode='markers', showlegend=False,
                                      marker=dict(size=16, color=self.subset_bgcolor)))
        self.fig.update_layout(xaxis=dict(showgrid=False, zeroline=False), yaxis=dict(showgrid=True, zeroline=False),
                               margin=dict(t=40, l=150))

        # Compute list of intersections
        intersections = None
        if self.color is not None:
            # Pull out full list of possible intersection combinations from first color grouping
            query = self.intersect_counts[self.color] == self.intersect_counts[self.color].iloc[0]
            intersections = list(self.intersect_counts[query]['Intersections'])
        else:
            intersections = list(self.intersect_counts['Intersections'])

        # Then fill in subset markers with fg color
        x = 0
        for s in intersections:
            x_subsets = []
            y_subsets = []
            y = 0
            for e in s:
                if e:
                    x_subsets += [x]
                    y_subsets += [-y_max / d * y - y_scatter_offset * y_max]
                y += 1
            x += 1
            # TODO: Add hover information for subset/intersection description
            self.fig.add_trace(go.Scatter(x=x_subsets, y=y_subsets, mode='markers+lines', showlegend=False,
                                          marker=dict(size=16, color=self.subset_fgcolor, showscale=False)))

    def make_margin_plot(self):
        """
        Method to add left margin count px.bar chart in style of UpSet plot.
        """
        # Group and count according to color input
        color = self.color
        counts_df = self.df.groupby(color).sum().reset_index() if color is not None else self.df.sum().reset_index().rename(
            columns={'index': 'variable', 0: 'value'})

        bar_args = {
            'color': self.color,
            'category_orders': self.category_orders,
            'color_discrete_sequence': self.color_discrete_sequence,
            'color_discrete_map': self.color_discrete_map,
            'barmode': self.barmode,
            'log_y': self.log_y
        }

        # Create counts px.bar chart
        plot_df = counts_df.melt(id_vars=color) if color is not None else counts_df
        if self.mode == 'Percent':
            if color is not None:
                denom = plot_df.groupby(color).sum().reset_index()
                denom_dict = dict(zip(denom[color], denom['value']))
                plot_df['value'] = round(plot_df['value'] / plot_df[color].map(denom_dict), 2)
            else:
                plot_df['value'] = round(plot_df['value'] / plot_df['value'].sum(), 2)
        counts_bar = px.bar(plot_df, x='value', y='variable', orientation='h', text='value', **bar_args)
        counts_bar.update_traces(textposition='outside', cliponaxis=False)
        # TODO: Change hover info to be more useful

        # Add subset names as text into plot
        subset_names = self.subset_col_names
        # subset_names = counts_bar.data[0]['y']
        max_name_len = max([len(s) for s in subset_names])
        annotation_center = -1 + -0.01 * max_name_len
        for i, s in enumerate(subset_names):
            self.fig.add_annotation(x=annotation_center, y=self.switchboard_heights[i], text=s, showarrow=False,
                                    font=dict(size=12, color='#000000'), align='left')

        # Reflect horizontally the bars while preserving labels; Shift heights to match input subset scatter heights
        for trace in counts_bar.data:
            trace['x'] = -trace['x'] / max(trace['x'])
            trace['y'] = self.switchboard_heights
        counts_bar.update_traces(base=annotation_center - 1, showlegend=False)

        # Add counts chart traces to main fig
        for trace in counts_bar.data:
            self.fig.add_trace(trace)
