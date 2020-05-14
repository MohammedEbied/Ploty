import _plotly_utils.basevalidators


class BValidator(_plotly_utils.basevalidators.NumberValidator):
    def __init__(self, plotly_name="b", parent_name="treemap.marker.pad", **kwargs):
        super(BValidator, self).__init__(
            plotly_name=plotly_name,
            parent_name=parent_name,
            edit_type=kwargs.pop("edit_type", "plot"),
            min=kwargs.pop("min", 0),
            role=kwargs.pop("role", "style"),
            **kwargs
        )
