import _plotly_utils.basevalidators


class TitleValidator(_plotly_utils.basevalidators.StringValidator):

    def __init__(
        self,
        plotly_name='title',
        parent_name='splom.marker.colorbar',
        **kwargs
    ):
        super(TitleValidator, self).__init__(
            plotly_name=plotly_name,
            parent_name=parent_name,
            edit_type=kwargs.pop('edit_type', 'colorbars'),
            role=kwargs.pop('role', 'info'),
            **kwargs
        )
