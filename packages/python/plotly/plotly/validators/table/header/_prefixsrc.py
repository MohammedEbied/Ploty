import _plotly_utils.basevalidators


class PrefixsrcValidator(_plotly_utils.basevalidators.SrcValidator):
    def __init__(self, plotly_name="prefixsrc", parent_name="table.header", **kwargs):
        super(PrefixsrcValidator, self).__init__(
            plotly_name=plotly_name,
            parent_name=parent_name,
            edit_type=kwargs.pop("edit_type", "none"),
            **kwargs
        )
