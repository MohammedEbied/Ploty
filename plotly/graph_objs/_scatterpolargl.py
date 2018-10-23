from plotly.basedatatypes import BaseTraceType
import copy


class Scatterpolargl(BaseTraceType):

    # connectgaps
    # -----------
    @property
    def connectgaps(self):
        """
        Determines whether or not gaps (i.e. {nan} or missing values)
        in the provided data arrays are connected.
    
        The 'connectgaps' property must be specified as a bool
        (either True, or False)

        Returns
        -------
        bool
        """
        return self['connectgaps']

    @connectgaps.setter
    def connectgaps(self, val):
        self['connectgaps'] = val

    # customdata
    # ----------
    @property
    def customdata(self):
        """
        Assigns extra data each datum. This may be useful when
        listening to hover, click and selection events. Note that,
        "scatter" traces also appends customdata items in the markers
        DOM elements
    
        The 'customdata' property is an array that may be specified as a tuple,
        list, numpy array, or pandas Series

        Returns
        -------
        numpy.ndarray
        """
        return self['customdata']

    @customdata.setter
    def customdata(self, val):
        self['customdata'] = val

    # customdatasrc
    # -------------
    @property
    def customdatasrc(self):
        """
        Sets the source reference on plot.ly for  customdata .
    
        The 'customdatasrc' property must be specified as a string or
        as a plotly.grid_objs.Column object

        Returns
        -------
        str
        """
        return self['customdatasrc']

    @customdatasrc.setter
    def customdatasrc(self, val):
        self['customdatasrc'] = val

    # dr
    # --
    @property
    def dr(self):
        """
        Sets the r coordinate step.
    
        The 'dr' property is a number and may be specified as:
          - An int or float

        Returns
        -------
        int|float
        """
        return self['dr']

    @dr.setter
    def dr(self, val):
        self['dr'] = val

    # dtheta
    # ------
    @property
    def dtheta(self):
        """
        Sets the theta coordinate step. By default, the `dtheta` step
        equals the subplot's period divided by the length of the `r`
        coordinates.
    
        The 'dtheta' property is a number and may be specified as:
          - An int or float

        Returns
        -------
        int|float
        """
        return self['dtheta']

    @dtheta.setter
    def dtheta(self, val):
        self['dtheta'] = val

    # fill
    # ----
    @property
    def fill(self):
        """
        Sets the area to fill with a solid color. Defaults to "none"
        unless this trace is stacked, then it gets "tonexty"
        ("tonextx") if `orientation` is "v" ("h") Use with `fillcolor`
        if not "none". "tozerox" and "tozeroy" fill to x=0 and y=0
        respectively. "tonextx" and "tonexty" fill between the
        endpoints of this trace and the endpoints of the trace before
        it, connecting those endpoints with straight lines (to make a
        stacked area graph); if there is no trace before it, they
        behave like "tozerox" and "tozeroy". "toself" connects the
        endpoints of the trace (or each segment of the trace if it has
        gaps) into a closed shape. "tonext" fills the space between two
        traces if one completely encloses the other (eg consecutive
        contour lines), and behaves like "toself" if there is no trace
        before it. "tonext" should not be used if one trace does not
        enclose the other. Traces in a `stackgroup` will only fill to
        (or be filled to) other traces in the same group. With multiple
        `stackgroup`s or some traces stacked and some not, if fill-
        linked traces are not already consecutive, the later ones will
        be pushed down in the drawing order.
    
        The 'fill' property is an enumeration that may be specified as:
          - One of the following enumeration values:
                ['none', 'tozeroy', 'tozerox', 'tonexty', 'tonextx',
                'toself', 'tonext']

        Returns
        -------
        Any
        """
        return self['fill']

    @fill.setter
    def fill(self, val):
        self['fill'] = val

    # fillcolor
    # ---------
    @property
    def fillcolor(self):
        """
        Sets the fill color. Defaults to a half-transparent variant of
        the line color, marker color, or marker line color, whichever
        is available.
    
        The 'fillcolor' property is a color and may be specified as:
          - A hex string (e.g. '#ff0000')
          - An rgb/rgba string (e.g. 'rgb(255,0,0)')
          - An hsl/hsla string (e.g. 'hsl(0,100%,50%)')
          - An hsv/hsva string (e.g. 'hsv(0,100%,100%)')
          - A named CSS color:
                aliceblue, antiquewhite, aqua, aquamarine, azure,
                beige, bisque, black, blanchedalmond, blue,
                blueviolet, brown, burlywood, cadetblue,
                chartreuse, chocolate, coral, cornflowerblue,
                cornsilk, crimson, cyan, darkblue, darkcyan,
                darkgoldenrod, darkgray, darkgrey, darkgreen,
                darkkhaki, darkmagenta, darkolivegreen, darkorange,
                darkorchid, darkred, darksalmon, darkseagreen,
                darkslateblue, darkslategray, darkslategrey,
                darkturquoise, darkviolet, deeppink, deepskyblue,
                dimgray, dimgrey, dodgerblue, firebrick,
                floralwhite, forestgreen, fuchsia, gainsboro,
                ghostwhite, gold, goldenrod, gray, grey, green,
                greenyellow, honeydew, hotpink, indianred, indigo,
                ivory, khaki, lavender, lavenderblush, lawngreen,
                lemonchiffon, lightblue, lightcoral, lightcyan,
                lightgoldenrodyellow, lightgray, lightgrey,
                lightgreen, lightpink, lightsalmon, lightseagreen,
                lightskyblue, lightslategray, lightslategrey,
                lightsteelblue, lightyellow, lime, limegreen,
                linen, magenta, maroon, mediumaquamarine,
                mediumblue, mediumorchid, mediumpurple,
                mediumseagreen, mediumslateblue, mediumspringgreen,
                mediumturquoise, mediumvioletred, midnightblue,
                mintcream, mistyrose, moccasin, navajowhite, navy,
                oldlace, olive, olivedrab, orange, orangered,
                orchid, palegoldenrod, palegreen, paleturquoise,
                palevioletred, papayawhip, peachpuff, peru, pink,
                plum, powderblue, purple, red, rosybrown,
                royalblue, saddlebrown, salmon, sandybrown,
                seagreen, seashell, sienna, silver, skyblue,
                slateblue, slategray, slategrey, snow, springgreen,
                steelblue, tan, teal, thistle, tomato, turquoise,
                violet, wheat, white, whitesmoke, yellow,
                yellowgreen

        Returns
        -------
        str
        """
        return self['fillcolor']

    @fillcolor.setter
    def fillcolor(self, val):
        self['fillcolor'] = val

    # hoverinfo
    # ---------
    @property
    def hoverinfo(self):
        """
        Determines which trace information appear on hover. If `none`
        or `skip` are set, no information is displayed upon hovering.
        But, if `none` is set, click and hover events are still fired.
    
        The 'hoverinfo' property is a flaglist and may be specified
        as a string containing:
          - Any combination of ['r', 'theta', 'text', 'name', 'name'] joined with '+' characters
            (e.g. 'r+theta')
            OR exactly one of ['all', 'none', 'skip'] (e.g. 'skip')
          - A list or array of the above

        Returns
        -------
        Any|numpy.ndarray
        """
        return self['hoverinfo']

    @hoverinfo.setter
    def hoverinfo(self, val):
        self['hoverinfo'] = val

    # hoverinfosrc
    # ------------
    @property
    def hoverinfosrc(self):
        """
        Sets the source reference on plot.ly for  hoverinfo .
    
        The 'hoverinfosrc' property must be specified as a string or
        as a plotly.grid_objs.Column object

        Returns
        -------
        str
        """
        return self['hoverinfosrc']

    @hoverinfosrc.setter
    def hoverinfosrc(self, val):
        self['hoverinfosrc'] = val

    # hoverlabel
    # ----------
    @property
    def hoverlabel(self):
        """
        The 'hoverlabel' property is an instance of Hoverlabel
        that may be specified as:
          - An instance of plotly.graph_objs.scatterpolargl.Hoverlabel
          - A dict of string/value properties that will be passed
            to the Hoverlabel constructor
    
            Supported dict properties:
                
                bgcolor
                    Sets the background color of the hover labels
                    for this trace
                bgcolorsrc
                    Sets the source reference on plot.ly for
                    bgcolor .
                bordercolor
                    Sets the border color of the hover labels for
                    this trace.
                bordercolorsrc
                    Sets the source reference on plot.ly for
                    bordercolor .
                font
                    Sets the font used in hover labels.
                namelength
                    Sets the length (in number of characters) of
                    the trace name in the hover labels for this
                    trace. -1 shows the whole name regardless of
                    length. 0-3 shows the first 0-3 characters, and
                    an integer >3 will show the whole name if it is
                    less than that many characters, but if it is
                    longer, will truncate to `namelength - 3`
                    characters and add an ellipsis.
                namelengthsrc
                    Sets the source reference on plot.ly for
                    namelength .

        Returns
        -------
        plotly.graph_objs.scatterpolargl.Hoverlabel
        """
        return self['hoverlabel']

    @hoverlabel.setter
    def hoverlabel(self, val):
        self['hoverlabel'] = val

    # hovertext
    # ---------
    @property
    def hovertext(self):
        """
        Sets hover text elements associated with each (x,y) pair. If a
        single string, the same string appears over all the data
        points. If an array of string, the items are mapped in order to
        the this trace's (x,y) coordinates. To be seen, trace
        `hoverinfo` must contain a "text" flag.
    
        The 'hovertext' property is a string and must be specified as:
          - A string
          - A number that will be converted to a string
          - A tuple, list, or one-dimensional numpy array of the above

        Returns
        -------
        str|numpy.ndarray
        """
        return self['hovertext']

    @hovertext.setter
    def hovertext(self, val):
        self['hovertext'] = val

    # hovertextsrc
    # ------------
    @property
    def hovertextsrc(self):
        """
        Sets the source reference on plot.ly for  hovertext .
    
        The 'hovertextsrc' property must be specified as a string or
        as a plotly.grid_objs.Column object

        Returns
        -------
        str
        """
        return self['hovertextsrc']

    @hovertextsrc.setter
    def hovertextsrc(self, val):
        self['hovertextsrc'] = val

    # ids
    # ---
    @property
    def ids(self):
        """
        Assigns id labels to each datum. These ids for object constancy
        of data points during animation. Should be an array of strings,
        not numbers or any other type.
    
        The 'ids' property is an array that may be specified as a tuple,
        list, numpy array, or pandas Series

        Returns
        -------
        numpy.ndarray
        """
        return self['ids']

    @ids.setter
    def ids(self, val):
        self['ids'] = val

    # idssrc
    # ------
    @property
    def idssrc(self):
        """
        Sets the source reference on plot.ly for  ids .
    
        The 'idssrc' property must be specified as a string or
        as a plotly.grid_objs.Column object

        Returns
        -------
        str
        """
        return self['idssrc']

    @idssrc.setter
    def idssrc(self, val):
        self['idssrc'] = val

    # legendgroup
    # -----------
    @property
    def legendgroup(self):
        """
        Sets the legend group for this trace. Traces part of the same
        legend group hide/show at the same time when toggling legend
        items.
    
        The 'legendgroup' property is a string and must be specified as:
          - A string
          - A number that will be converted to a string

        Returns
        -------
        str
        """
        return self['legendgroup']

    @legendgroup.setter
    def legendgroup(self, val):
        self['legendgroup'] = val

    # line
    # ----
    @property
    def line(self):
        """
        The 'line' property is an instance of Line
        that may be specified as:
          - An instance of plotly.graph_objs.scatterpolargl.Line
          - A dict of string/value properties that will be passed
            to the Line constructor
    
            Supported dict properties:
                
                color
                    Sets the line color.
                dash
                    Sets the style of the lines.
                width
                    Sets the line width (in px).

        Returns
        -------
        plotly.graph_objs.scatterpolargl.Line
        """
        return self['line']

    @line.setter
    def line(self, val):
        self['line'] = val

    # marker
    # ------
    @property
    def marker(self):
        """
        The 'marker' property is an instance of Marker
        that may be specified as:
          - An instance of plotly.graph_objs.scatterpolargl.Marker
          - A dict of string/value properties that will be passed
            to the Marker constructor
    
            Supported dict properties:
                
                autocolorscale
                    Determines whether the colorscale is a default
                    palette (`autocolorscale: true`) or the palette
                    determined by `marker.colorscale`. Has an
                    effect only if in `marker.color`is set to a
                    numerical array. In case `colorscale` is
                    unspecified or `autocolorscale` is true, the
                    default  palette will be chosen according to
                    whether numbers in the `color` array are all
                    positive, all negative or mixed.
                cauto
                    Determines whether or not the color domain is
                    computed with respect to the input data (here
                    in `marker.color`) or the bounds set in
                    `marker.cmin` and `marker.cmax`  Has an effect
                    only if in `marker.color`is set to a numerical
                    array. Defaults to `false` when `marker.cmin`
                    and `marker.cmax` are set by the user.
                cmax
                    Sets the upper bound of the color domain. Has
                    an effect only if in `marker.color`is set to a
                    numerical array. Value should have the same
                    units as in `marker.color` and if set,
                    `marker.cmin` must be set as well.
                cmin
                    Sets the lower bound of the color domain. Has
                    an effect only if in `marker.color`is set to a
                    numerical array. Value should have the same
                    units as in `marker.color` and if set,
                    `marker.cmax` must be set as well.
                color
                    Sets themarkercolor. It accepts either a
                    specific color or an array of numbers that are
                    mapped to the colorscale relative to the max
                    and min values of the array or relative to
                    `marker.cmin` and `marker.cmax` if set.
                colorbar
                    plotly.graph_objs.scatterpolargl.marker.ColorBa
                    r instance or dict with compatible properties
                colorscale
                    Sets the colorscale. Has an effect only if in
                    `marker.color`is set to a numerical array. The
                    colorscale must be an array containing arrays
                    mapping a normalized value to an rgb, rgba,
                    hex, hsl, hsv, or named color string. At
                    minimum, a mapping for the lowest (0) and
                    highest (1) values are required. For example,
                    `[[0, 'rgb(0,0,255)', [1, 'rgb(255,0,0)']]`. To
                    control the bounds of the colorscale in color
                    space, use`marker.cmin` and `marker.cmax`.
                    Alternatively, `colorscale` may be a palette
                    name string of the following list: Greys,YlGnBu
                    ,Greens,YlOrRd,Bluered,RdBu,Reds,Blues,Picnic,R
                    ainbow,Portland,Jet,Hot,Blackbody,Earth,Electri
                    c,Viridis,Cividis.
                colorsrc
                    Sets the source reference on plot.ly for  color
                    .
                line
                    plotly.graph_objs.scatterpolargl.marker.Line
                    instance or dict with compatible properties
                opacity
                    Sets the marker opacity.
                opacitysrc
                    Sets the source reference on plot.ly for
                    opacity .
                reversescale
                    Reverses the color mapping if true. Has an
                    effect only if in `marker.color`is set to a
                    numerical array. If true, `marker.cmin` will
                    correspond to the last color in the array and
                    `marker.cmax` will correspond to the first
                    color.
                showscale
                    Determines whether or not a colorbar is
                    displayed for this trace. Has an effect only if
                    in `marker.color`is set to a numerical array.
                size
                    Sets the marker size (in px).
                sizemin
                    Has an effect only if `marker.size` is set to a
                    numerical array. Sets the minimum size (in px)
                    of the rendered marker points.
                sizemode
                    Has an effect only if `marker.size` is set to a
                    numerical array. Sets the rule for which the
                    data in `size` is converted to pixels.
                sizeref
                    Has an effect only if `marker.size` is set to a
                    numerical array. Sets the scale factor used to
                    determine the rendered size of marker points.
                    Use with `sizemin` and `sizemode`.
                sizesrc
                    Sets the source reference on plot.ly for  size
                    .
                symbol
                    Sets the marker symbol type. Adding 100 is
                    equivalent to appending "-open" to a symbol
                    name. Adding 200 is equivalent to appending
                    "-dot" to a symbol name. Adding 300 is
                    equivalent to appending "-open-dot" or "dot-
                    open" to a symbol name.
                symbolsrc
                    Sets the source reference on plot.ly for
                    symbol .

        Returns
        -------
        plotly.graph_objs.scatterpolargl.Marker
        """
        return self['marker']

    @marker.setter
    def marker(self, val):
        self['marker'] = val

    # mode
    # ----
    @property
    def mode(self):
        """
        Determines the drawing mode for this scatter trace. If the
        provided `mode` includes "text" then the `text` elements appear
        at the coordinates. Otherwise, the `text` elements appear on
        hover. If there are less than 20 points and the trace is not
        stacked then the default is "lines+markers". Otherwise,
        "lines".
    
        The 'mode' property is a flaglist and may be specified
        as a string containing:
          - Any combination of ['lines', 'markers', 'text'] joined with '+' characters
            (e.g. 'lines+markers')
            OR exactly one of ['none'] (e.g. 'none')

        Returns
        -------
        Any
        """
        return self['mode']

    @mode.setter
    def mode(self, val):
        self['mode'] = val

    # name
    # ----
    @property
    def name(self):
        """
        Sets the trace name. The trace name appear as the legend item
        and on hover.
    
        The 'name' property is a string and must be specified as:
          - A string
          - A number that will be converted to a string

        Returns
        -------
        str
        """
        return self['name']

    @name.setter
    def name(self, val):
        self['name'] = val

    # opacity
    # -------
    @property
    def opacity(self):
        """
        Sets the opacity of the trace.
    
        The 'opacity' property is a number and may be specified as:
          - An int or float in the interval [0, 1]

        Returns
        -------
        int|float
        """
        return self['opacity']

    @opacity.setter
    def opacity(self, val):
        self['opacity'] = val

    # r
    # -
    @property
    def r(self):
        """
        Sets the radial coordinates
    
        The 'r' property is an array that may be specified as a tuple,
        list, numpy array, or pandas Series

        Returns
        -------
        numpy.ndarray
        """
        return self['r']

    @r.setter
    def r(self, val):
        self['r'] = val

    # r0
    # --
    @property
    def r0(self):
        """
        Alternate to `r`. Builds a linear space of r coordinates. Use
        with `dr` where `r0` is the starting coordinate and `dr` the
        step.
    
        The 'r0' property accepts values of any type

        Returns
        -------
        Any
        """
        return self['r0']

    @r0.setter
    def r0(self, val):
        self['r0'] = val

    # rsrc
    # ----
    @property
    def rsrc(self):
        """
        Sets the source reference on plot.ly for  r .
    
        The 'rsrc' property must be specified as a string or
        as a plotly.grid_objs.Column object

        Returns
        -------
        str
        """
        return self['rsrc']

    @rsrc.setter
    def rsrc(self, val):
        self['rsrc'] = val

    # selected
    # --------
    @property
    def selected(self):
        """
        The 'selected' property is an instance of Selected
        that may be specified as:
          - An instance of plotly.graph_objs.scatterpolargl.Selected
          - A dict of string/value properties that will be passed
            to the Selected constructor
    
            Supported dict properties:
                
                marker
                    plotly.graph_objs.scatterpolargl.selected.Marke
                    r instance or dict with compatible properties
                textfont
                    plotly.graph_objs.scatterpolargl.selected.Textf
                    ont instance or dict with compatible properties

        Returns
        -------
        plotly.graph_objs.scatterpolargl.Selected
        """
        return self['selected']

    @selected.setter
    def selected(self, val):
        self['selected'] = val

    # selectedpoints
    # --------------
    @property
    def selectedpoints(self):
        """
        Array containing integer indices of selected points. Has an
        effect only for traces that support selections. Note that an
        empty array means an empty selection where the `unselected` are
        turned on for all points, whereas, any other non-array values
        means no selection all where the `selected` and `unselected`
        styles have no effect.
    
        The 'selectedpoints' property accepts values of any type

        Returns
        -------
        Any
        """
        return self['selectedpoints']

    @selectedpoints.setter
    def selectedpoints(self, val):
        self['selectedpoints'] = val

    # showlegend
    # ----------
    @property
    def showlegend(self):
        """
        Determines whether or not an item corresponding to this trace
        is shown in the legend.
    
        The 'showlegend' property must be specified as a bool
        (either True, or False)

        Returns
        -------
        bool
        """
        return self['showlegend']

    @showlegend.setter
    def showlegend(self, val):
        self['showlegend'] = val

    # stream
    # ------
    @property
    def stream(self):
        """
        The 'stream' property is an instance of Stream
        that may be specified as:
          - An instance of plotly.graph_objs.scatterpolargl.Stream
          - A dict of string/value properties that will be passed
            to the Stream constructor
    
            Supported dict properties:
                
                maxpoints
                    Sets the maximum number of points to keep on
                    the plots from an incoming stream. If
                    `maxpoints` is set to 50, only the newest 50
                    points will be displayed on the plot.
                token
                    The stream id number links a data trace on a
                    plot with a stream. See
                    https://plot.ly/settings for more details.

        Returns
        -------
        plotly.graph_objs.scatterpolargl.Stream
        """
        return self['stream']

    @stream.setter
    def stream(self, val):
        self['stream'] = val

    # subplot
    # -------
    @property
    def subplot(self):
        """
        Sets a reference between this trace's data coordinates and a
        polar subplot. If "polar" (the default value), the data refer
        to `layout.polar`. If "polar2", the data refer to
        `layout.polar2`, and so on.
    
        The 'subplot' property is an identifier of a particular
        subplot, of type 'polar', that may be specified as the string 'polar'
        optionally followed by an integer >= 1
        (e.g. 'polar', 'polar1', 'polar2', 'polar3', etc.)

        Returns
        -------
        str
        """
        return self['subplot']

    @subplot.setter
    def subplot(self, val):
        self['subplot'] = val

    # text
    # ----
    @property
    def text(self):
        """
        Sets text elements associated with each (x,y) pair. If a single
        string, the same string appears over all the data points. If an
        array of string, the items are mapped in order to the this
        trace's (x,y) coordinates. If trace `hoverinfo` contains a
        "text" flag and "hovertext" is not set, these elements will be
        seen in the hover labels.
    
        The 'text' property is a string and must be specified as:
          - A string
          - A number that will be converted to a string
          - A tuple, list, or one-dimensional numpy array of the above

        Returns
        -------
        str|numpy.ndarray
        """
        return self['text']

    @text.setter
    def text(self, val):
        self['text'] = val

    # textfont
    # --------
    @property
    def textfont(self):
        """
        Sets the text font.
    
        The 'textfont' property is an instance of Textfont
        that may be specified as:
          - An instance of plotly.graph_objs.scatterpolargl.Textfont
          - A dict of string/value properties that will be passed
            to the Textfont constructor
    
            Supported dict properties:
                
                color
    
                colorsrc
                    Sets the source reference on plot.ly for  color
                    .
                family
                    HTML font family - the typeface that will be
                    applied by the web browser. The web browser
                    will only be able to apply a font if it is
                    available on the system which it operates.
                    Provide multiple font families, separated by
                    commas, to indicate the preference in which to
                    apply fonts if they aren't available on the
                    system. The plotly service (at https://plot.ly
                    or on-premise) generates images on a server,
                    where only a select number of fonts are
                    installed and supported. These include "Arial",
                    "Balto", "Courier New", "Droid Sans",, "Droid
                    Serif", "Droid Sans Mono", "Gravitas One", "Old
                    Standard TT", "Open Sans", "Overpass", "PT Sans
                    Narrow", "Raleway", "Times New Roman".
                familysrc
                    Sets the source reference on plot.ly for
                    family .
                size
    
                sizesrc
                    Sets the source reference on plot.ly for  size
                    .

        Returns
        -------
        plotly.graph_objs.scatterpolargl.Textfont
        """
        return self['textfont']

    @textfont.setter
    def textfont(self, val):
        self['textfont'] = val

    # textposition
    # ------------
    @property
    def textposition(self):
        """
        Sets the positions of the `text` elements with respects to the
        (x,y) coordinates.
    
        The 'textposition' property is an enumeration that may be specified as:
          - One of the following enumeration values:
                ['top left', 'top center', 'top right', 'middle left',
                'middle center', 'middle right', 'bottom left', 'bottom
                center', 'bottom right']
          - A tuple, list, or one-dimensional numpy array of the above

        Returns
        -------
        Any|numpy.ndarray
        """
        return self['textposition']

    @textposition.setter
    def textposition(self, val):
        self['textposition'] = val

    # textpositionsrc
    # ---------------
    @property
    def textpositionsrc(self):
        """
        Sets the source reference on plot.ly for  textposition .
    
        The 'textpositionsrc' property must be specified as a string or
        as a plotly.grid_objs.Column object

        Returns
        -------
        str
        """
        return self['textpositionsrc']

    @textpositionsrc.setter
    def textpositionsrc(self, val):
        self['textpositionsrc'] = val

    # textsrc
    # -------
    @property
    def textsrc(self):
        """
        Sets the source reference on plot.ly for  text .
    
        The 'textsrc' property must be specified as a string or
        as a plotly.grid_objs.Column object

        Returns
        -------
        str
        """
        return self['textsrc']

    @textsrc.setter
    def textsrc(self, val):
        self['textsrc'] = val

    # theta
    # -----
    @property
    def theta(self):
        """
        Sets the angular coordinates
    
        The 'theta' property is an array that may be specified as a tuple,
        list, numpy array, or pandas Series

        Returns
        -------
        numpy.ndarray
        """
        return self['theta']

    @theta.setter
    def theta(self, val):
        self['theta'] = val

    # theta0
    # ------
    @property
    def theta0(self):
        """
        Alternate to `theta`. Builds a linear space of theta
        coordinates. Use with `dtheta` where `theta0` is the starting
        coordinate and `dtheta` the step.
    
        The 'theta0' property accepts values of any type

        Returns
        -------
        Any
        """
        return self['theta0']

    @theta0.setter
    def theta0(self, val):
        self['theta0'] = val

    # thetasrc
    # --------
    @property
    def thetasrc(self):
        """
        Sets the source reference on plot.ly for  theta .
    
        The 'thetasrc' property must be specified as a string or
        as a plotly.grid_objs.Column object

        Returns
        -------
        str
        """
        return self['thetasrc']

    @thetasrc.setter
    def thetasrc(self, val):
        self['thetasrc'] = val

    # thetaunit
    # ---------
    @property
    def thetaunit(self):
        """
        Sets the unit of input "theta" values. Has an effect only when
        on "linear" angular axes.
    
        The 'thetaunit' property is an enumeration that may be specified as:
          - One of the following enumeration values:
                ['radians', 'degrees', 'gradians']

        Returns
        -------
        Any
        """
        return self['thetaunit']

    @thetaunit.setter
    def thetaunit(self, val):
        self['thetaunit'] = val

    # uid
    # ---
    @property
    def uid(self):
        """
        The 'uid' property is a string and must be specified as:
          - A string
          - A number that will be converted to a string

        Returns
        -------
        str
        """
        return self['uid']

    @uid.setter
    def uid(self, val):
        self['uid'] = val

    # unselected
    # ----------
    @property
    def unselected(self):
        """
        The 'unselected' property is an instance of Unselected
        that may be specified as:
          - An instance of plotly.graph_objs.scatterpolargl.Unselected
          - A dict of string/value properties that will be passed
            to the Unselected constructor
    
            Supported dict properties:
                
                marker
                    plotly.graph_objs.scatterpolargl.unselected.Mar
                    ker instance or dict with compatible properties
                textfont
                    plotly.graph_objs.scatterpolargl.unselected.Tex
                    tfont instance or dict with compatible
                    properties

        Returns
        -------
        plotly.graph_objs.scatterpolargl.Unselected
        """
        return self['unselected']

    @unselected.setter
    def unselected(self, val):
        self['unselected'] = val

    # visible
    # -------
    @property
    def visible(self):
        """
        Determines whether or not this trace is visible. If
        "legendonly", the trace is not drawn, but can appear as a
        legend item (provided that the legend itself is visible).
    
        The 'visible' property is an enumeration that may be specified as:
          - One of the following enumeration values:
                [True, False, 'legendonly']

        Returns
        -------
        Any
        """
        return self['visible']

    @visible.setter
    def visible(self, val):
        self['visible'] = val

    # type
    # ----
    @property
    def type(self):
        return self._props['type']

    # property parent name
    # --------------------
    @property
    def _parent_path_str(self):
        return ''

    # Self properties description
    # ---------------------------
    @property
    def _prop_descriptions(self):
        return """\
        connectgaps
            Determines whether or not gaps (i.e. {nan} or missing
            values) in the provided data arrays are connected.
        customdata
            Assigns extra data each datum. This may be useful when
            listening to hover, click and selection events. Note
            that, "scatter" traces also appends customdata items in
            the markers DOM elements
        customdatasrc
            Sets the source reference on plot.ly for  customdata .
        dr
            Sets the r coordinate step.
        dtheta
            Sets the theta coordinate step. By default, the
            `dtheta` step equals the subplot's period divided by
            the length of the `r` coordinates.
        fill
            Sets the area to fill with a solid color. Defaults to
            "none" unless this trace is stacked, then it gets
            "tonexty" ("tonextx") if `orientation` is "v" ("h") Use
            with `fillcolor` if not "none". "tozerox" and "tozeroy"
            fill to x=0 and y=0 respectively. "tonextx" and
            "tonexty" fill between the endpoints of this trace and
            the endpoints of the trace before it, connecting those
            endpoints with straight lines (to make a stacked area
            graph); if there is no trace before it, they behave
            like "tozerox" and "tozeroy". "toself" connects the
            endpoints of the trace (or each segment of the trace if
            it has gaps) into a closed shape. "tonext" fills the
            space between two traces if one completely encloses the
            other (eg consecutive contour lines), and behaves like
            "toself" if there is no trace before it. "tonext"
            should not be used if one trace does not enclose the
            other. Traces in a `stackgroup` will only fill to (or
            be filled to) other traces in the same group. With
            multiple `stackgroup`s or some traces stacked and some
            not, if fill-linked traces are not already consecutive,
            the later ones will be pushed down in the drawing
            order.
        fillcolor
            Sets the fill color. Defaults to a half-transparent
            variant of the line color, marker color, or marker line
            color, whichever is available.
        hoverinfo
            Determines which trace information appear on hover. If
            `none` or `skip` are set, no information is displayed
            upon hovering. But, if `none` is set, click and hover
            events are still fired.
        hoverinfosrc
            Sets the source reference on plot.ly for  hoverinfo .
        hoverlabel
            plotly.graph_objs.scatterpolargl.Hoverlabel instance or
            dict with compatible properties
        hovertext
            Sets hover text elements associated with each (x,y)
            pair. If a single string, the same string appears over
            all the data points. If an array of string, the items
            are mapped in order to the this trace's (x,y)
            coordinates. To be seen, trace `hoverinfo` must contain
            a "text" flag.
        hovertextsrc
            Sets the source reference on plot.ly for  hovertext .
        ids
            Assigns id labels to each datum. These ids for object
            constancy of data points during animation. Should be an
            array of strings, not numbers or any other type.
        idssrc
            Sets the source reference on plot.ly for  ids .
        legendgroup
            Sets the legend group for this trace. Traces part of
            the same legend group hide/show at the same time when
            toggling legend items.
        line
            plotly.graph_objs.scatterpolargl.Line instance or dict
            with compatible properties
        marker
            plotly.graph_objs.scatterpolargl.Marker instance or
            dict with compatible properties
        mode
            Determines the drawing mode for this scatter trace. If
            the provided `mode` includes "text" then the `text`
            elements appear at the coordinates. Otherwise, the
            `text` elements appear on hover. If there are less than
            20 points and the trace is not stacked then the default
            is "lines+markers". Otherwise, "lines".
        name
            Sets the trace name. The trace name appear as the
            legend item and on hover.
        opacity
            Sets the opacity of the trace.
        r
            Sets the radial coordinates
        r0
            Alternate to `r`. Builds a linear space of r
            coordinates. Use with `dr` where `r0` is the starting
            coordinate and `dr` the step.
        rsrc
            Sets the source reference on plot.ly for  r .
        selected
            plotly.graph_objs.scatterpolargl.Selected instance or
            dict with compatible properties
        selectedpoints
            Array containing integer indices of selected points.
            Has an effect only for traces that support selections.
            Note that an empty array means an empty selection where
            the `unselected` are turned on for all points, whereas,
            any other non-array values means no selection all where
            the `selected` and `unselected` styles have no effect.
        showlegend
            Determines whether or not an item corresponding to this
            trace is shown in the legend.
        stream
            plotly.graph_objs.scatterpolargl.Stream instance or
            dict with compatible properties
        subplot
            Sets a reference between this trace's data coordinates
            and a polar subplot. If "polar" (the default value),
            the data refer to `layout.polar`. If "polar2", the data
            refer to `layout.polar2`, and so on.
        text
            Sets text elements associated with each (x,y) pair. If
            a single string, the same string appears over all the
            data points. If an array of string, the items are
            mapped in order to the this trace's (x,y) coordinates.
            If trace `hoverinfo` contains a "text" flag and
            "hovertext" is not set, these elements will be seen in
            the hover labels.
        textfont
            Sets the text font.
        textposition
            Sets the positions of the `text` elements with respects
            to the (x,y) coordinates.
        textpositionsrc
            Sets the source reference on plot.ly for  textposition
            .
        textsrc
            Sets the source reference on plot.ly for  text .
        theta
            Sets the angular coordinates
        theta0
            Alternate to `theta`. Builds a linear space of theta
            coordinates. Use with `dtheta` where `theta0` is the
            starting coordinate and `dtheta` the step.
        thetasrc
            Sets the source reference on plot.ly for  theta .
        thetaunit
            Sets the unit of input "theta" values. Has an effect
            only when on "linear" angular axes.
        uid

        unselected
            plotly.graph_objs.scatterpolargl.Unselected instance or
            dict with compatible properties
        visible
            Determines whether or not this trace is visible. If
            "legendonly", the trace is not drawn, but can appear as
            a legend item (provided that the legend itself is
            visible).
        """

    def __init__(
        self,
        arg=None,
        connectgaps=None,
        customdata=None,
        customdatasrc=None,
        dr=None,
        dtheta=None,
        fill=None,
        fillcolor=None,
        hoverinfo=None,
        hoverinfosrc=None,
        hoverlabel=None,
        hovertext=None,
        hovertextsrc=None,
        ids=None,
        idssrc=None,
        legendgroup=None,
        line=None,
        marker=None,
        mode=None,
        name=None,
        opacity=None,
        r=None,
        r0=None,
        rsrc=None,
        selected=None,
        selectedpoints=None,
        showlegend=None,
        stream=None,
        subplot=None,
        text=None,
        textfont=None,
        textposition=None,
        textpositionsrc=None,
        textsrc=None,
        theta=None,
        theta0=None,
        thetasrc=None,
        thetaunit=None,
        uid=None,
        unselected=None,
        visible=None,
        **kwargs
    ):
        """
        Construct a new Scatterpolargl object
        
        The scatterpolargl trace type encompasses line charts, scatter
        charts, and bubble charts in polar coordinates using the WebGL
        plotting engine. The data visualized as scatter point or lines
        is set in `r` (radial) and `theta` (angular) coordinates Bubble
        charts are achieved by setting `marker.size` and/or
        `marker.color` to numerical arrays.

        Parameters
        ----------
        arg
            dict of properties compatible with this constructor or
            an instance of plotly.graph_objs.Scatterpolargl
        connectgaps
            Determines whether or not gaps (i.e. {nan} or missing
            values) in the provided data arrays are connected.
        customdata
            Assigns extra data each datum. This may be useful when
            listening to hover, click and selection events. Note
            that, "scatter" traces also appends customdata items in
            the markers DOM elements
        customdatasrc
            Sets the source reference on plot.ly for  customdata .
        dr
            Sets the r coordinate step.
        dtheta
            Sets the theta coordinate step. By default, the
            `dtheta` step equals the subplot's period divided by
            the length of the `r` coordinates.
        fill
            Sets the area to fill with a solid color. Defaults to
            "none" unless this trace is stacked, then it gets
            "tonexty" ("tonextx") if `orientation` is "v" ("h") Use
            with `fillcolor` if not "none". "tozerox" and "tozeroy"
            fill to x=0 and y=0 respectively. "tonextx" and
            "tonexty" fill between the endpoints of this trace and
            the endpoints of the trace before it, connecting those
            endpoints with straight lines (to make a stacked area
            graph); if there is no trace before it, they behave
            like "tozerox" and "tozeroy". "toself" connects the
            endpoints of the trace (or each segment of the trace if
            it has gaps) into a closed shape. "tonext" fills the
            space between two traces if one completely encloses the
            other (eg consecutive contour lines), and behaves like
            "toself" if there is no trace before it. "tonext"
            should not be used if one trace does not enclose the
            other. Traces in a `stackgroup` will only fill to (or
            be filled to) other traces in the same group. With
            multiple `stackgroup`s or some traces stacked and some
            not, if fill-linked traces are not already consecutive,
            the later ones will be pushed down in the drawing
            order.
        fillcolor
            Sets the fill color. Defaults to a half-transparent
            variant of the line color, marker color, or marker line
            color, whichever is available.
        hoverinfo
            Determines which trace information appear on hover. If
            `none` or `skip` are set, no information is displayed
            upon hovering. But, if `none` is set, click and hover
            events are still fired.
        hoverinfosrc
            Sets the source reference on plot.ly for  hoverinfo .
        hoverlabel
            plotly.graph_objs.scatterpolargl.Hoverlabel instance or
            dict with compatible properties
        hovertext
            Sets hover text elements associated with each (x,y)
            pair. If a single string, the same string appears over
            all the data points. If an array of string, the items
            are mapped in order to the this trace's (x,y)
            coordinates. To be seen, trace `hoverinfo` must contain
            a "text" flag.
        hovertextsrc
            Sets the source reference on plot.ly for  hovertext .
        ids
            Assigns id labels to each datum. These ids for object
            constancy of data points during animation. Should be an
            array of strings, not numbers or any other type.
        idssrc
            Sets the source reference on plot.ly for  ids .
        legendgroup
            Sets the legend group for this trace. Traces part of
            the same legend group hide/show at the same time when
            toggling legend items.
        line
            plotly.graph_objs.scatterpolargl.Line instance or dict
            with compatible properties
        marker
            plotly.graph_objs.scatterpolargl.Marker instance or
            dict with compatible properties
        mode
            Determines the drawing mode for this scatter trace. If
            the provided `mode` includes "text" then the `text`
            elements appear at the coordinates. Otherwise, the
            `text` elements appear on hover. If there are less than
            20 points and the trace is not stacked then the default
            is "lines+markers". Otherwise, "lines".
        name
            Sets the trace name. The trace name appear as the
            legend item and on hover.
        opacity
            Sets the opacity of the trace.
        r
            Sets the radial coordinates
        r0
            Alternate to `r`. Builds a linear space of r
            coordinates. Use with `dr` where `r0` is the starting
            coordinate and `dr` the step.
        rsrc
            Sets the source reference on plot.ly for  r .
        selected
            plotly.graph_objs.scatterpolargl.Selected instance or
            dict with compatible properties
        selectedpoints
            Array containing integer indices of selected points.
            Has an effect only for traces that support selections.
            Note that an empty array means an empty selection where
            the `unselected` are turned on for all points, whereas,
            any other non-array values means no selection all where
            the `selected` and `unselected` styles have no effect.
        showlegend
            Determines whether or not an item corresponding to this
            trace is shown in the legend.
        stream
            plotly.graph_objs.scatterpolargl.Stream instance or
            dict with compatible properties
        subplot
            Sets a reference between this trace's data coordinates
            and a polar subplot. If "polar" (the default value),
            the data refer to `layout.polar`. If "polar2", the data
            refer to `layout.polar2`, and so on.
        text
            Sets text elements associated with each (x,y) pair. If
            a single string, the same string appears over all the
            data points. If an array of string, the items are
            mapped in order to the this trace's (x,y) coordinates.
            If trace `hoverinfo` contains a "text" flag and
            "hovertext" is not set, these elements will be seen in
            the hover labels.
        textfont
            Sets the text font.
        textposition
            Sets the positions of the `text` elements with respects
            to the (x,y) coordinates.
        textpositionsrc
            Sets the source reference on plot.ly for  textposition
            .
        textsrc
            Sets the source reference on plot.ly for  text .
        theta
            Sets the angular coordinates
        theta0
            Alternate to `theta`. Builds a linear space of theta
            coordinates. Use with `dtheta` where `theta0` is the
            starting coordinate and `dtheta` the step.
        thetasrc
            Sets the source reference on plot.ly for  theta .
        thetaunit
            Sets the unit of input "theta" values. Has an effect
            only when on "linear" angular axes.
        uid

        unselected
            plotly.graph_objs.scatterpolargl.Unselected instance or
            dict with compatible properties
        visible
            Determines whether or not this trace is visible. If
            "legendonly", the trace is not drawn, but can appear as
            a legend item (provided that the legend itself is
            visible).

        Returns
        -------
        Scatterpolargl
        """
        super(Scatterpolargl, self).__init__('scatterpolargl')

        # Validate arg
        # ------------
        if arg is None:
            arg = {}
        elif isinstance(arg, self.__class__):
            arg = arg.to_plotly_json()
        elif isinstance(arg, dict):
            arg = copy.copy(arg)
        else:
            raise ValueError(
                """\
The first argument to the plotly.graph_objs.Scatterpolargl 
constructor must be a dict or 
an instance of plotly.graph_objs.Scatterpolargl"""
            )

        # Handle skip_invalid
        # -------------------
        self._skip_invalid = kwargs.pop('skip_invalid', False)

        # Import validators
        # -----------------
        from plotly.validators import (scatterpolargl as v_scatterpolargl)

        # Initialize validators
        # ---------------------
        self._validators['connectgaps'
                        ] = v_scatterpolargl.ConnectgapsValidator()
        self._validators['customdata'] = v_scatterpolargl.CustomdataValidator()
        self._validators['customdatasrc'
                        ] = v_scatterpolargl.CustomdatasrcValidator()
        self._validators['dr'] = v_scatterpolargl.DrValidator()
        self._validators['dtheta'] = v_scatterpolargl.DthetaValidator()
        self._validators['fill'] = v_scatterpolargl.FillValidator()
        self._validators['fillcolor'] = v_scatterpolargl.FillcolorValidator()
        self._validators['hoverinfo'] = v_scatterpolargl.HoverinfoValidator()
        self._validators['hoverinfosrc'
                        ] = v_scatterpolargl.HoverinfosrcValidator()
        self._validators['hoverlabel'] = v_scatterpolargl.HoverlabelValidator()
        self._validators['hovertext'] = v_scatterpolargl.HovertextValidator()
        self._validators['hovertextsrc'
                        ] = v_scatterpolargl.HovertextsrcValidator()
        self._validators['ids'] = v_scatterpolargl.IdsValidator()
        self._validators['idssrc'] = v_scatterpolargl.IdssrcValidator()
        self._validators['legendgroup'
                        ] = v_scatterpolargl.LegendgroupValidator()
        self._validators['line'] = v_scatterpolargl.LineValidator()
        self._validators['marker'] = v_scatterpolargl.MarkerValidator()
        self._validators['mode'] = v_scatterpolargl.ModeValidator()
        self._validators['name'] = v_scatterpolargl.NameValidator()
        self._validators['opacity'] = v_scatterpolargl.OpacityValidator()
        self._validators['r'] = v_scatterpolargl.RValidator()
        self._validators['r0'] = v_scatterpolargl.R0Validator()
        self._validators['rsrc'] = v_scatterpolargl.RsrcValidator()
        self._validators['selected'] = v_scatterpolargl.SelectedValidator()
        self._validators['selectedpoints'
                        ] = v_scatterpolargl.SelectedpointsValidator()
        self._validators['showlegend'] = v_scatterpolargl.ShowlegendValidator()
        self._validators['stream'] = v_scatterpolargl.StreamValidator()
        self._validators['subplot'] = v_scatterpolargl.SubplotValidator()
        self._validators['text'] = v_scatterpolargl.TextValidator()
        self._validators['textfont'] = v_scatterpolargl.TextfontValidator()
        self._validators['textposition'
                        ] = v_scatterpolargl.TextpositionValidator()
        self._validators['textpositionsrc'
                        ] = v_scatterpolargl.TextpositionsrcValidator()
        self._validators['textsrc'] = v_scatterpolargl.TextsrcValidator()
        self._validators['theta'] = v_scatterpolargl.ThetaValidator()
        self._validators['theta0'] = v_scatterpolargl.Theta0Validator()
        self._validators['thetasrc'] = v_scatterpolargl.ThetasrcValidator()
        self._validators['thetaunit'] = v_scatterpolargl.ThetaunitValidator()
        self._validators['uid'] = v_scatterpolargl.UidValidator()
        self._validators['unselected'] = v_scatterpolargl.UnselectedValidator()
        self._validators['visible'] = v_scatterpolargl.VisibleValidator()

        # Populate data dict with properties
        # ----------------------------------
        _v = arg.pop('connectgaps', None)
        self['connectgaps'] = connectgaps if connectgaps is not None else _v
        _v = arg.pop('customdata', None)
        self['customdata'] = customdata if customdata is not None else _v
        _v = arg.pop('customdatasrc', None)
        self['customdatasrc'
            ] = customdatasrc if customdatasrc is not None else _v
        _v = arg.pop('dr', None)
        self['dr'] = dr if dr is not None else _v
        _v = arg.pop('dtheta', None)
        self['dtheta'] = dtheta if dtheta is not None else _v
        _v = arg.pop('fill', None)
        self['fill'] = fill if fill is not None else _v
        _v = arg.pop('fillcolor', None)
        self['fillcolor'] = fillcolor if fillcolor is not None else _v
        _v = arg.pop('hoverinfo', None)
        self['hoverinfo'] = hoverinfo if hoverinfo is not None else _v
        _v = arg.pop('hoverinfosrc', None)
        self['hoverinfosrc'] = hoverinfosrc if hoverinfosrc is not None else _v
        _v = arg.pop('hoverlabel', None)
        self['hoverlabel'] = hoverlabel if hoverlabel is not None else _v
        _v = arg.pop('hovertext', None)
        self['hovertext'] = hovertext if hovertext is not None else _v
        _v = arg.pop('hovertextsrc', None)
        self['hovertextsrc'] = hovertextsrc if hovertextsrc is not None else _v
        _v = arg.pop('ids', None)
        self['ids'] = ids if ids is not None else _v
        _v = arg.pop('idssrc', None)
        self['idssrc'] = idssrc if idssrc is not None else _v
        _v = arg.pop('legendgroup', None)
        self['legendgroup'] = legendgroup if legendgroup is not None else _v
        _v = arg.pop('line', None)
        self['line'] = line if line is not None else _v
        _v = arg.pop('marker', None)
        self['marker'] = marker if marker is not None else _v
        _v = arg.pop('mode', None)
        self['mode'] = mode if mode is not None else _v
        _v = arg.pop('name', None)
        self['name'] = name if name is not None else _v
        _v = arg.pop('opacity', None)
        self['opacity'] = opacity if opacity is not None else _v
        _v = arg.pop('r', None)
        self['r'] = r if r is not None else _v
        _v = arg.pop('r0', None)
        self['r0'] = r0 if r0 is not None else _v
        _v = arg.pop('rsrc', None)
        self['rsrc'] = rsrc if rsrc is not None else _v
        _v = arg.pop('selected', None)
        self['selected'] = selected if selected is not None else _v
        _v = arg.pop('selectedpoints', None)
        self['selectedpoints'
            ] = selectedpoints if selectedpoints is not None else _v
        _v = arg.pop('showlegend', None)
        self['showlegend'] = showlegend if showlegend is not None else _v
        _v = arg.pop('stream', None)
        self['stream'] = stream if stream is not None else _v
        _v = arg.pop('subplot', None)
        self['subplot'] = subplot if subplot is not None else _v
        _v = arg.pop('text', None)
        self['text'] = text if text is not None else _v
        _v = arg.pop('textfont', None)
        self['textfont'] = textfont if textfont is not None else _v
        _v = arg.pop('textposition', None)
        self['textposition'] = textposition if textposition is not None else _v
        _v = arg.pop('textpositionsrc', None)
        self['textpositionsrc'
            ] = textpositionsrc if textpositionsrc is not None else _v
        _v = arg.pop('textsrc', None)
        self['textsrc'] = textsrc if textsrc is not None else _v
        _v = arg.pop('theta', None)
        self['theta'] = theta if theta is not None else _v
        _v = arg.pop('theta0', None)
        self['theta0'] = theta0 if theta0 is not None else _v
        _v = arg.pop('thetasrc', None)
        self['thetasrc'] = thetasrc if thetasrc is not None else _v
        _v = arg.pop('thetaunit', None)
        self['thetaunit'] = thetaunit if thetaunit is not None else _v
        _v = arg.pop('uid', None)
        self['uid'] = uid if uid is not None else _v
        _v = arg.pop('unselected', None)
        self['unselected'] = unselected if unselected is not None else _v
        _v = arg.pop('visible', None)
        self['visible'] = visible if visible is not None else _v

        # Read-only literals
        # ------------------
        from _plotly_utils.basevalidators import LiteralValidator
        self._props['type'] = 'scatterpolargl'
        self._validators['type'] = LiteralValidator(
            plotly_name='type',
            parent_name='scatterpolargl',
            val='scatterpolargl'
        )
        arg.pop('type', None)

        # Process unknown kwargs
        # ----------------------
        self._process_kwargs(**dict(arg, **kwargs))

        # Reset skip_invalid
        # ------------------
        self._skip_invalid = False
