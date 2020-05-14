import _plotly_utils.basevalidators


class ShapeValidator(_plotly_utils.basevalidators.EnumeratedValidator):
    def __init__(
        self, plotly_name="shape", parent_name="scatterpolargl.line", **kwargs
    ):
        super(ShapeValidator, self).__init__(
            plotly_name=plotly_name,
            parent_name=parent_name,
            edit_type=kwargs.pop("edit_type", "calc"),
            role=kwargs.pop("role", "style"),
            values=kwargs.pop("values", ["linear", "hv", "vh", "hvh", "vhv"]),
            **kwargs
        )
